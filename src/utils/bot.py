import time
import logging
from datetime import datetime
from keys                              import keys
from selenium.webdriver.common.by      import By
from selenium.webdriver.support.ui     import WebDriverWait
from selenium.webdriver.support        import expected_conditions as EC
from selenium.webdriver.support.select import Select
from params                            import config, configUtils

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Bot:
    def __init__(self):
        self.link_erp     = configUtils.LINK_ERP_OLIST
        self.link_estoque = configUtils.LINK_ERP_ESTOQUE
        self.link_logout  = configUtils.LINK_ERP_LOGOUT
        self.time_sleep   = configUtils.REQ_TIME_SLEEP
        self.username     = keys.BOT_USERNAME
        self.password     = keys.BOT_PASSWORD
        

    def buscar_e_remover(self, lista, chave, valor):
        for i, item in enumerate(lista):
            if item.get(chave) == valor:
                return lista.pop(i)
        return None

    async def login(self, driver): 
        try:   
            driver.get(self.link_erp)
            login_input = driver.find_element(By.ID, "username")
            next_button = driver.find_element(By.XPATH, "//button[@class='sc-dAlyuH biayZs sc-dAbbOL ddEnAE']")
            login_input.clear()
            login_input.send_keys(self.username)
            next_button.click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
            pass_input = driver.find_element(By.ID, "password")
            submit_button = driver.find_element(By.XPATH, "//button[@class='sc-dAlyuH biayZs sc-dAbbOL ddEnAE']")
            pass_input.clear()
            pass_input.send_keys(self.password)
            submit_button.click()

            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//h3[@class='modal-title']")))
                elemento = driver.find_element(By.XPATH, "//h3[@class='modal-title']")
                if elemento.text == 'Este usuário já está logado em outro dispositivo':
                    btn_confirma_login = driver.find_element(By.XPATH, "//button[@class='btn btn-primary']")
                    btn_confirma_login.click()
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sidebar-menu-logo-usuario']")))
                    time.sleep(self.time_sleep)
            except:
                pass
            return True, driver
        except Exception as e:
            logger.error(e)
            return False, None 

    async def logout(self,driver):
        driver.get(self.link_logout)
        driver.quit()        

    async def lanca_estoque(self,driver,dados_produto):

        try:
            driver.get(self.link_estoque.format(dados_produto.get('idproduto')))
            # clica em incluir e aguarda carregar o modal
            btn_incluir = driver.find_element(By.ID, "botaoIncluir")
            btn_incluir.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//form[@name='formEstoquePopup']")))
            time.sleep(self.time_sleep)

            # informa o tipo
            tipo = driver.find_element(By.XPATH, "//select[@name='tipoPopup']")
            tipo = Select(tipo)
            tipo.select_by_value("B")

            # informa a quantidade
            qtd = driver.find_element(By.XPATH, "//input[@name='quantidadePopup']")
            qtd.send_keys(dados_produto.get('qtd'))

            # clica em salvar
            self.time_sleep
            btn_salvar = driver.find_element(By.XPATH, "//button[@name='btn_salvar_popup']")
            btn_salvar.click()

            # aguarda carregar o modal dos lotes e verifica se o produto está configurado para isso
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//form[@name='formLancarLotesEntrada']")))
            time.sleep(self.time_sleep)       

            return True, driver
        except Exception as e:
            logger.error(e)
            return False, driver

    async def valida_configuracao_lote(self,driver,codigo):
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//form[@name='formLancarLotesEntrada']")))
            return True
        except:
            original_window = driver.current_window_handle
            driver.switch_to.new_window('tab')
            driver.get(f"https://erp.tiny.com.br/produtos#edit/{codigo}")
            try:
                time.sleep(self.time_sleep)
                btn_editar = driver.find_element(By.XPATH, "//button[@class='btn btn-primary btn-edicao-item']")
                btn_editar.click()
                time.sleep(self.time_sleep)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "controlarLotes")))    
                controle_lote = driver.find_element(By.ID, "controlarLotes")        
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                controle_lote = Select(controle_lote)
                controle_lote.select_by_value('1')
                btn_salvar = driver.find_element(By.ID, "botaoSalvar")
                btn_salvar.click()        
                time.sleep(self.time_sleep)
                driver.close()
                driver.switch_to.window(original_window)
                return True
            except Exception as e:
                print(f"ERRO AO ATUALIZAR CADASTRO DO PRODUTO {codigo}: {e}")                
                return False

    async def lanca_lotes(self,driver,dados_lote):

        try:
            table_lotes      = driver.find_element(By.XPATH,"//tbody[@id='listaLancarLotesEntrada']")    
            table_lotes_rows = table_lotes.find_elements(By.XPATH,"//tr[@class='linha-lote-estoque']")
            idestoque        = table_lotes_rows[0].get_attribute('idestoque')
            idproduto        = table_lotes_rows[0].get_attribute('idproduto')
            tem_lote         = True if table_lotes_rows[0].find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][0][numeroLote]']") != '' else False
        except Exception as e:
            logger.error(e)
            return False, driver

        # verifica se o produto está sem nenhum lote
        if len(table_lotes_rows) == 1 and not tem_lote:
            # adiciona linhas para lançar os lotes
            try:                
                for i in range(len(dados_lote)-1):                
                    btn_add = driver.find_element(By.XPATH, "//button[@class='btn btn-default btn-sm dropdown-toggle']")
                    btn_add.click()    
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-right']")))
                    time.sleep(self.time_sleep)            
                    lista_opcoes_lote = driver.find_element(By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-right']")
                    add_lote = lista_opcoes_lote.find_elements(By.TAG_NAME, "a")
                    add_lote[0].click()     
                    time.sleep(self.time_sleep)
            except Exception as e:
                logger.error("Erro ao adicionar linhas de lote: %s",e)
                return False, driver
            
            # informa os lotes
            try:
                lotes_rows = table_lotes.find_elements(By.XPATH,"//tr[@class='linha-lote-estoque']")
                for i, row in enumerate(lotes_rows):
                    lote_codigo = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][numeroLote]']")
                    lote_fabric = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][dataFabricacao]']")
                    lote_valid  = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][dataValidade]']")
                    lote_qtd    = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][quantidade]']")

                    lote_codigo.clear()
                    lote_fabric.clear()
                    lote_valid .clear()
                    lote_qtd   .clear()

                    lote_codigo.send_keys(dados_lote[i].get('numeroLote'))
                    lote_fabric.send_keys(dados_lote[i].get('dataFabricacao'))
                    lote_valid .send_keys(dados_lote[i].get('dataValidade'))
                    lote_qtd   .send_keys(int(dados_lote[i].get('quantidade')))
                    
                    time.sleep(self.time_sleep)                
            except Exception as e:
                logger.error("Erro ao informar os lotes: %s",e)
                return False, driver  

        elif tem_lote:
            # verifica se no Olist tem menos lote do que no Sankhya
            if len(table_lotes_rows) < len(dados_lote):
                # adiciona linhas para lançar os lotes
                try:                    
                    for i in range(len(dados_lote)-1):                
                        btn_add = driver.find_element(By.XPATH, "//button[@class='btn btn-default btn-sm dropdown-toggle']")
                        btn_add.click()
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-right']")))
                        time.sleep(self.time_sleep)
                        lista_opcoes_lote = driver.find_element(By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-right']")
                        add_lote = lista_opcoes_lote.find_elements(By.TAG_NAME, "a")
                        add_lote[0].click()     
                        time.sleep(self.time_sleep)
                except Exception as e:
                    logger.error("Erro ao adicionar linhas de lote: %s",e)
                    return False, driver

                # informa os lotes
                try:                    
                    lotes_rows = table_lotes.find_elements(By.XPATH,"//tr[@class='linha-lote-estoque']")
                    for i, row in enumerate(lotes_rows):
                        lote_codigo = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][numeroLote]']")
                        lote_fabric = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][dataFabricacao]']")
                        lote_valid  = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][dataValidade]']")
                        lote_qtd    = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][quantidade]']")
                        
                        lote_olist = {
                            "numeroLote"     : lote_codigo.get_property('value'),
                            "dataFabricacao" : lote_fabric.get_property('value'),
                            "dataValidade"   : lote_valid .get_property('value'),
                            "quantidade"     : lote_qtd   .get_property('value')
                        }

                        lote_sankhya = self.buscar_e_remover(dados_lote, 'numeroLote', lote_olist.get('numeroLote'))

                        if lote_sankhya:
                            lote_qtd.clear()
                            lote_qtd.send_keys(int(lote_sankhya.get('quantidade')))
                        else:
                            lote_codigo.clear()
                            lote_fabric.clear()
                            lote_valid .clear()
                            lote_qtd   .clear()

                            lote_sankhya = dados_lote.pop(0)

                            lote_codigo.send_keys(lote_sankhya.get('numeroLote'))
                            lote_fabric.send_keys(lote_sankhya.get('dataFabricacao'))
                            lote_valid .send_keys(lote_sankhya.get('dataValidade'))
                            lote_qtd   .send_keys(int(lote_sankhya.get('quantidade')))
                        
                        time.sleep(self.time_sleep)
                except Exception as e:
                    logger.error("Erro ao informar os lotes: %s",e)
                    return False, driver
                
            elif len(table_lotes_rows) > len(dados_lote):                    
                for i, row in enumerate(table_lotes_rows):
                    # coleta os lotes
                    try:
                        lote_codigo = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][numeroLote]']")
                        lote_fabric = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][dataFabricacao]']")
                        lote_valid  = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][dataValidade]']")
                        lote_qtd    = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][quantidade]']")
                        
                        lote_olist = {
                            "numeroLote"     : lote_codigo.get_property('value'),
                            "dataFabricacao" : lote_fabric.get_property('value'),
                            "dataValidade"   : lote_valid .get_property('value'),
                            "quantidade"     : lote_qtd   .get_property('value')
                        }
                    except Exception as e:
                        logger.error("Erro ao coletar os lotes: %s",e)
                        return False, driver
                    
                    lote_sankhya = self.buscar_e_remover(dados_lote, 'numeroLote', lote_olist.get('numeroLote'))

                    if lote_sankhya:
                        lote_qtd.clear()
                        lote_qtd.send_keys(int(lote_sankhya.get('quantidade')))
                    else:
                        # remove se o lote do olist não está na lista do sankhya                        
                        # Olist não deixa exluir o lote se for a primeira linha
                        if i == 0:
                            try:
                                # separa os dados do lote a ser excluido
                                line0_codigo = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][numeroLote]']")
                                line0_fabric = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][dataFabricacao]']")
                                line0_valid  = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][dataValidade]']")
                                line0_qtd    = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][quantidade]']")                                
                                line_0 = {
                                    "numeroLote"     : line0_codigo.get_property('value'),
                                    "dataFabricacao" : line0_fabric.get_property('value'),
                                    "dataValidade"   : line0_valid .get_property('value'),
                                    "quantidade"     : line0_qtd   .get_property('value')
                                }

                                # separa os dados da linha sequente
                                line_nxt_codigo = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i+1}][numeroLote]']")
                                line_nxt_fabric = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i+1}][dataFabricacao]']")
                                line_nxt_valid  = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i+1}][dataValidade]']")
                                line_nxt_qtd    = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i+1}][quantidade]']")                                
                                line_nxt = {
                                    "numeroLote"     : line_nxt_codigo.get_property('value'),
                                    "dataFabricacao" : line_nxt_fabric.get_property('value'),
                                    "dataValidade"   : line_nxt_valid .get_property('value'),
                                    "quantidade"     : line_nxt_qtd   .get_property('value')
                                }
                                
                                # troca os dados de lote entre as linhas
                                line_nxt_codigo.clear()
                                line_nxt_fabric.clear()
                                line_nxt_valid .clear()
                                line_nxt_qtd   .clear()
                                line_nxt_codigo.send_keys(line_0.get('numeroLote'))
                                line_nxt_fabric.send_keys(line_0.get('dataFabricacao'))
                                line_nxt_valid .send_keys(line_0.get('dataValidade'))
                                line_nxt_qtd   .send_keys(int(line_0.get('quantidade')))
                                line0_codigo.clear()
                                line0_fabric.clear()
                                line0_valid .clear()
                                line0_qtd   .clear()
                                line0_codigo.send_keys(line_nxt.get('numeroLote'))
                                line0_fabric.send_keys(line_nxt.get('dataFabricacao'))
                                line0_valid .send_keys(line_nxt.get('dataValidade'))
                                line0_qtd   .send_keys(int(line_nxt.get('quantidade')))
                            except Exception as e:
                                logger.error("Erro trocar os lotes de linha: %s",e)
                                return False, driver  

                            try:
                                # remove a linha que recebeu os dados do lote esgotado
                                btn_remove = driver.find_elements(By.XPATH, "//button[@class='btn btn-default btn-sm dropdown-toggle']")
                                btn_remove[i+1].click()    
                                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-right']")))
                                time.sleep(self.time_sleep)
                                lista_opcoes_lote = driver.find_elements(By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-right']")
                                del_lote = lista_opcoes_lote[i+1].find_elements(By.TAG_NAME, "a")
                                time.sleep(self.time_sleep)                            
                                driver.execute_script(del_lote[i+1].get_attribute('onclick'))
                                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@popup-action-id='0']")))
                                time.sleep(self.time_sleep)
                                btn_confirma = driver.find_elements(By.XPATH, "//button[@popup-action-id='0']")
                                btn_confirma[0].click()
                            except Exception as e:
                                logger.error("Erro ao remover linha de lote: %s",e)
                                return False, driver                                  
                        else:
                            try:
                                btn_remove = driver.find_elements(By.XPATH, "//button[@class='btn btn-default btn-sm dropdown-toggle']")
                                btn_remove[i].click()    
                                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-right']")))
                                time.sleep(self.time_sleep)
                                lista_opcoes_lote = driver.find_elements(By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-right']")
                                del_lote = lista_opcoes_lote[i].find_elements(By.TAG_NAME, "a")
                                time.sleep(self.time_sleep)                            
                                driver.execute_script(del_lote[1].get_attribute('onclick'))
                                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@popup-action-id='0']")))
                                time.sleep(self.time_sleep)
                                btn_confirma = driver.find_elements(By.XPATH, "//button[@popup-action-id='0']")
                                btn_confirma[0].click()
                            except Exception as e:
                                logger.error("Erro ao remover linhas de lotes: %s",e)
                                return False, driver                        
                        time.sleep(self.time_sleep)

            elif len(table_lotes_rows) == len(dados_lote):
                for i, row in enumerate(table_lotes_rows):
                    try:
                        lote_codigo = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][numeroLote]']")
                        lote_fabric = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][dataFabricacao]']")
                        lote_valid  = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][dataValidade]']")
                        lote_qtd    = row.find_element(By.XPATH, f"//input[@name='lotes[{idproduto}][{idestoque}][{i}][quantidade]']")
                        
                        lote_olist = {
                            "numeroLote"     : lote_codigo.get_property('value'),
                            "dataFabricacao" : lote_fabric.get_property('value'),
                            "dataValidade"   : lote_valid .get_property('value'),
                            "quantidade"     : lote_qtd   .get_property('value')
                        }
                    except Exception as e:
                        logger.error("Erro ao coletar os lotes: %s",e)
                        return False, driver


                    lote_sankhya = self.buscar_e_remover(dados_lote, 'numeroLote', lote_olist.get('numeroLote'))

                    if lote_sankhya:
                        lote_qtd.clear()
                        lote_qtd.send_keys(int(lote_sankhya.get('quantidade')))
                    else:
                        # lança o lote do sankhya
                        try:
                            lote_codigo.clear()
                            lote_fabric.clear()
                            lote_valid .clear()
                            lote_qtd   .clear()

                            lote_sankhya = dados_lote.pop(0)

                            lote_codigo.send_keys(lote_sankhya.get('numeroLote'))
                            lote_fabric.send_keys(lote_sankhya.get('dataFabricacao'))
                            lote_valid .send_keys(lote_sankhya.get('dataValidade'))
                            lote_qtd   .send_keys(int(lote_sankhya.get('quantidade')))
                        except Exception as e:
                            logger.error("Erro ao informar os lotes: %s",e)
                            return False, driver                         
                        time.sleep(self.time_sleep)
            
            try:
                driver.execute_script("estoqueEntrada.lancarLotesPopup();")
            except Exception as e:
                logger.error("Erro ao confirmar lançamento dos lotes: %s",e)
                return False, driver

            try:
                start_time = datetime.now()
                if WebDriverWait(driver, configUtils.TIMEOUT_LANCA_LOTES).until(EC.staleness_of(driver.find_element(By.XPATH, "//div[@id='waitLancarLotesEntradaModal']"))):
                    return True, driver
            except Exception as e:
                end_time = datetime.now()
                tempo = int((end_time - start_time).total_seconds())
                logger.error("A finalização do lançamento dos lotes demorou %s segundos para concluir. Limite %ss: %s", tempo, configUtils.TIMEOUT_LANCA_LOTES, e)
                return False, driver
                