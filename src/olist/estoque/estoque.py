import json
import logging
import requests
from src.olist.connect          import Connect
from params                     import config, configOlist
from src.olist.estoque.deposito import Deposito
from src.utils.validaPath       import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Estoque:

    def __init__(self,
                 id:int=None,
                 nome:int=None,
                 codigo:int=None,
                 unidade:int=None,
                 saldo:int=None,
                 reservado:int=None,
                 disponivel:int=None,
                 deposito:list=None,
                 tipo:int=None,
                 data:int=None,
                 quantidade:int=None,
                 precoUnitario:int=None,
                 observacoes:int=None,):
        self.con                           = Connect()  
        self.valida_path                   = validaPath()
        self.req_sleep                     = config.REQ_TIME_SLEEP  
        self.endpoint                      = config.API_URL+config.ENDPOINT_ESTOQUES        
        self.id                            = id
        self.nome                          = nome
        self.codigo                        = codigo
        self.unidade                       = unidade
        self.saldo                         = saldo
        self.reservado                     = reservado
        self.disponivel                    = disponivel
        self.tipo                          = tipo
        self.data                          = data
        self.quantidade                    = quantidade
        self.precoUnitario                 = precoUnitario
        self.observacoes                   = observacoes
        self.deposito                      = deposito
        self.acao                          = None
        
    def decodificar(self,payload:dict=None) -> bool:
        
        if payload:
            #print(payload)
            try:
                self.id            = payload["id"]
                self.nome          = payload["nome"]
                self.codigo        = payload["codigo"]
                self.unidade       = payload["unidade"]
                self.saldo         = payload["saldo"]
                self.reservado     = payload["reservado"]
                self.disponivel    = payload["disponivel"]

                self.deposito = []
                for d in payload["depositos"]:
                    dep = Deposito()
                    dep.decodificar(d)
                    self.deposito.append(dep)

                return True

            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    async def encodificar(self) -> dict:
        obj = {}
        data = {}
        file_path = configOlist.PATH_OBJECT_ESTOQUE

        obj = await self.valida_path.validar(path=file_path,mode='r',method='json')

        if self.acao == 'get':
            try:
                data = obj[self.acao]
                data["id"]                            = self.id
                data["nome"]                          = self.nome
                data["codigo"]                        = self.codigo
                data["unidade"]                       = self.unidade
                data["saldo"]                         = self.saldo
                data["reservado"]                     = self.reservado
                data["disponivel"]                    = self.disponivel
                depositos_list = list()
                for dep in self.deposito:
                    depositos_list.append(await dep.encodificar(self.acao))
                data["depositos"] = depositos_list

                return data
            except Exception as e:
                logger.error("Erro ao formatar dict estoque: %s", e)
                return {"status": "Erro"}

        elif self.acao == 'post':
            try:
                data = obj[self.acao]
                data["deposito"]                      = await self.deposito[0].encodificar(self.acao)
                data["tipo"]                          = self.tipo
                data["data"]                          = self.data
                data["quantidade"]                    = self.quantidade
                data["precoUnitario"]                 = self.precoUnitario or 0
                data["observacoes"]                   = self.observacoes or configOlist.OBS_MVTO_ESTOQUE
                return data
            except Exception as e:
                logger.error("Erro ao formatar dict estoque: %s", e)
                return {"status": "Erro"}
        else:
            return {"status": "Ação não configurada"}

    async def buscar(self, id:int=None) -> bool:

        url = config.API_URL+config.ENDPOINT_ESTOQUES+f"/{id or self.id}"
        try:
            token = self.con.get_latest_valid_token_or_refresh()
            if url and token:                
                get_estoque = requests.get(
                    url=url,
                    headers={
                        "Authorization":f"Bearer {token}",
                        "Content-Type":"application/json",
                        "Accept":"application/json"
                    }
                )
                if get_estoque.status_code == 200:
                    if self.decodificar(get_estoque.json()):
                        self.acao = 'get'
                        return True
                    else:
                        logger.error("Erro ao decodificar estoque %s", self.id)
                        return False
                else:
                    logger.error("Erro %s: %s cod %s", get_estoque.status_code, get_estoque.json().get("mensagem","Erro desconhecido"), self.id)
                    return False   
            else:
                logger.warning("Endpoint da API ou token de acesso faltantes")
                return False         
        except Exception as e:
            logger.error("Erro relacionado ao token de acesso. %s",e)
            return False
        
    async def enviar_saldo(self,id:int=None) -> bool:

        url = config.API_URL+config.ENDPOINT_ESTOQUES+f"/{id or self.id}"
        try:
            token = self.con.get_latest_valid_token_or_refresh()
            payload = await self.encodificar()
            # print(payload)
            if url and token:                
                post_estoque = requests.post(
                    url=url,
                    headers={
                        "Authorization":f"Bearer {token}",
                        "Content-Type":"application/json",
                        "Accept":"application/json"
                    },
                    data=json.dumps(payload)
                )
                if post_estoque.status_code == 200:
                    return True
                else:
                    logger.error("Erro %s: %s cod %s", post_estoque.status_code, post_estoque.json().get("mensagem","Erro desconhecido"), self.id)
                    return False   
            else:
                logger.warning("Endpoint da API ou token de acesso faltantes")
                return False         
        except Exception as e:
            logger.error("Erro relacionado ao token de acesso. %s",e)
            return False
