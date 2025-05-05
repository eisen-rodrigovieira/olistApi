import os
import json
import asyncio
import logging
import requests
from datetime                      import datetime,timedelta
from selenium                      import webdriver
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support    import expected_conditions as EC
from urllib.parse                  import urlparse, parse_qs
from cryptography.fernet           import Fernet
from keys                          import keys
from params                        import config, configOlist

logger = logging.getLogger(__name__)
logging.basicConfig(filename=configOlist.PATH_LOGS, encoding='utf-8', format=config.LOGGER_FORMAT, datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

class Connect(object):
    """
    Classe responsável por realizar o fluxo de autenticação com uma API,
    e armazenar os tokens de forma segura (criptografada).
    """

    def __init__(self):
        """
        Inicializa a classe codificando credenciais e configurando criptografia.
        """
        self.fernet = Fernet(keys.FERNET_KEY.encode())     
        self.access_token = ''   
        self.refresh_token = ''   

    async def get_auth_code(self) -> str:
        """
        Realiza login automatizado e extrai código de autorização da URL.
        """

        url = config.AUTH_URL+f'/auth?scope=openid&response_type=code&client_id={keys.CLIENT_ID}&redirect_uri={config.REDIRECT_URI}'

        try:
            driver = webdriver.Firefox()
            driver.get(url)

            login_input = driver.find_element(By.ID, "username")
            next_button = driver.find_element(By.XPATH, "//button[@class='sc-dAlyuH biayZs sc-dAbbOL ddEnAE']")
            login_input.clear()
            login_input.send_keys(keys.USERNAME)
            next_button.click()
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
            pass_input = driver.find_element(By.ID, "password")
            submit_button = driver.find_element(By.XPATH, "//button[@class='sc-dAlyuH biayZs sc-dAbbOL ddEnAE']")
            pass_input.clear()
            pass_input.send_keys(keys.PASSWORD)
            submit_button.click()
            
            res_url = driver.current_url
            parsed_url = urlparse(res_url)
            auth_code = parse_qs(parsed_url.query).get('code', [''])[0]
            return auth_code
        except Exception as e:
            logger.error("Erro durante a autenticação via navegador: %s", e)
        finally:
            driver.quit()

    async def get_token(self, authorization_code: str = None, refresh_token: str = None) -> dict:
        """
        Obtém um novo token usando authorization_code ou refresh_token.
        """
        if not authorization_code and not refresh_token:
            logger.error("authorization_code ou refresh_token não informado")
            return {"erro":"authorization_code ou refresh_token não informado"}

        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            "grant_type": "authorization_code",
            "client_id": keys.CLIENT_ID,
            "client_secret":keys.CLIENT_SECRET,
            "redirect_uri":config.REDIRECT_URI,
            "code": authorization_code
        } if authorization_code else {
            "grant_type": "refresh_token",
            "client_id": keys.CLIENT_ID,
            "client_secret":keys.CLIENT_SECRET,            
            "refresh_token": refresh_token
        }

        try:
            res = requests.post(
                url=config.AUTH_URL + config.ENDPOINT_TOKEN,
                headers=header,
                data=payload
            )
            if res.status_code == 200:
                return res.json()
            else:
                error = res.json().get("error_description", "Erro desconhecido")
                logger.error("Erro ao obter token: %s",error)
                return {"erro":error}
        except requests.exceptions.RequestException as e:
            logger.error("Erro de conexão: %s",e)
            return {"erro":e}

    def save_token_to_file(self, token_data: dict, filename: str = config.PATH_TOKENS) -> bool:
        """
        Salva o token criptografado com timestamp.
        """
        try:
            # Converte o token em string JSON e criptografa
            access_token = json.dumps(token_data['access_token']).encode("utf-8")
            refresh_token = json.dumps(token_data['refresh_token']).encode("utf-8")
            id_token = json.dumps(token_data['id_token']).encode("utf-8")
            encrypted_access_token = self.fernet.encrypt(access_token).decode()
            encrypted_refresh_token = self.fernet.encrypt(refresh_token).decode()
            encrypted_id_token = self.fernet.encrypt(id_token).decode()

            # Carrega histórico se existir
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    history = json.load(f)
            else:
                history = []

            # Adiciona nova entrada
            history.append({
                "timestamp": datetime.now().isoformat(),
                "access_token_encrypted": encrypted_access_token,
                "access_token_expires_at": (datetime.now()+timedelta(0,token_data['expires_in'])).isoformat(),
                "refresh_token_encrypted": encrypted_refresh_token,
                "refresh_token_expires_at": (datetime.now()+timedelta(0,token_data['refresh_expires_in'])).isoformat(),
                "id_token_encrypted": encrypted_id_token,
            })

            # Salva novamente
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=4, ensure_ascii=False)
            logger.info("Token criptografado salvo em %s",filename)
            return True
        except Exception as e:
            logger.error("Erro ao salvar token criptografado: %s",e)
            return False
        
    def decrypt_last(self, filename: str = config.PATH_TOKENS):
            
        if not os.path.exists(filename):
            logger.error("Histórico de tokens não encontrado")
            return ''

        with open(filename, "r", encoding="utf-8") as f:
            history = json.load(f)                       

        latest = history[-1]

        latest["access_token_raw"] = self.fernet.decrypt(latest["access_token_encrypted"].encode()).decode()
        latest["refresh_token_raw"] = self.fernet.decrypt(latest["refresh_token_encrypted"].encode()).decode()

        return latest
                

    def get_latest_valid_token_or_refresh(self, filename: str = config.PATH_TOKENS) -> str:
        """
        Verifica o token mais recente. Se expirado, usa o refresh_token criptografado para renovar.
        """
        logger.debug("Iniciando")
        try:
            if not os.path.exists(filename):
                logger.error("Histórico de tokens não encontrado")
                return ''

            with open(filename, "r", encoding="utf-8") as f:
                history = json.load(f)

            #logger.debug("Json carregado")

            latest = history[-1]
            access_token_expires = datetime.fromisoformat(latest["access_token_expires_at"])
            refresh_token_expires = datetime.fromisoformat(latest["refresh_token_expires_at"])
            now = datetime.now()

            #logger.debug("Dados de expiracao carregados")

            if now < access_token_expires:   
                
                #logger.debug("Access token valido")

                decrypted_access_token = self.fernet.decrypt(latest["access_token_encrypted"].encode()).decode()
                return json.loads(decrypted_access_token)
            
            elif now < refresh_token_expires:

                #logger.debug("Access token vencido")

                decrypted_refresh_token = self.fernet.decrypt(latest["refresh_token_encrypted"].encode()).decode()                
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    coro = self.get_token(refresh_token=json.loads(decrypted_refresh_token))
                    new_token = asyncio.ensure_future(coro)
                    # Use nest_asyncio para rodar em notebooks (opcional)
                    import nest_asyncio
                    nest_asyncio.apply()
                    #logger.debug("Rodando busca 2 com refresh token 1")
                    new_token = loop.run_until_complete(new_token)     
                    #logger.debug("Retorno da busca com refresh token 1")               
                else:
                    #logger.debug("Buscando com refresh token 2")
                    new_token = loop.run_until_complete(self.get_token(refresh_token=decrypted_refresh_token))                
                
                #logger.debug("Solicitado com refresh_token")

                if new_token.get("erro"):
                    logger.error("Retorno do token de acesso invalido. Tentando no")

                    return ''               
                else:
                    self.save_token_to_file(new_token)                
                    logger.warning("Token de acesso atualizado.")
                    return new_token["access_token"]
            else:
                logger.debug("Refresh token vencido")

                loop = asyncio.get_event_loop()
                if loop.is_running():
                    coro = self.login()
                    new_token = asyncio.ensure_future(coro)
                    #logger.debug("Rodando busca com novo login")
                    # Use nest_asyncio para rodar em notebooks (opcional)
                    import nest_asyncio
                    nest_asyncio.apply()
                    #logger.debug("Rodando busca com novo loginn")
                    new_token = loop.run_until_complete(new_token)     
                    logger.debug("Retorno da busca com novo login")               
                else:
                    #logger.debug("Rodando busca com novo login 2")
                    new_token = loop.run_until_complete(self.login())
        except Exception as e:
            logger.error("Erro ao recuperar ou renovar token: %s",e)
            return ''

    async def login(self) -> str:
        """
        Executa o fluxo completo de autenticação inicial.
        """
        try:
            authcode = await self.get_auth_code()
            token = await self.get_token(authorization_code=authcode)
            self.save_token_to_file(token)
            logger.warning("Token de acesso recuperado via login.")
            return token["access_token"]
        except Exception as e:
            logger.error("Erro no login: %s",e)            
            return ''

