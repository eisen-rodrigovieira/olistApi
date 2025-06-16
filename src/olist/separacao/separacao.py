import os
import time
import json
import logging
import requests
from src.olist.connect import Connect
from src.olist.separacao import item
from params            import config, configOlist
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Separacao:

    def __init__(
        self,
        id:int = None,
        situacao:int = None,
        situacaoCheckout:int = None,
        dataCriacao:str = None,
        dataSeparacao:str = None,
        dataCheckout:str = None,
        cliente_nome:str = None,
        cliente_codigo:str = None,
        cliente_fantasia:str = None,
        cliente_tipoPessoa:str = None,
        cliente_cpfCnpj:str = None,
        cliente_inscricaoEstadual:str = None,
        cliente_rg:str = None,
        cliente_telefone:str = None,
        cliente_celular:str = None,
        cliente_email:str = None,
        cliente_endereco_endereco:str = None,
        cliente_endereco_numero:str = None,
        cliente_endereco_complemento:str = None,
        cliente_endereco_bairro:str = None,
        cliente_endereco_municipio:str = None,
        cliente_endereco_cep:str = None,
        cliente_endereco_uf:str = None,
        cliente_endereco_pais:str = None,
        cliente_id:int = None,
        venda_id:int = None,
        venda_numero:int = None,
        venda_data:str = None,
        venda_situacao:int = None,
        notaFiscal_id:int = None,
        notaFiscal_numero:int = None,
        notaFiscal_dataEmissao:str = None,
        notaFiscal_situacao:int = None,
        ecommerce_id:int = None,
        ecommerce_nome:str = None,
        ecommerce_numeroPedidoEcommerce:str = None,
        ecommerce_numeroPedidoCanalVenda:str = None,
        ecommerce_canalVenda:str = None,
        formaEnvio_id:int = None,
        formaEnvio_nome:str = None,
        volumes:str = None
    ):
        self.con                              = Connect()  
        self.req_sleep                        = config.REQ_TIME_SLEEP  
        self.endpoint                         = config.API_URL+config.ENDPOINT_SEPARACAO
        self.situacao_separacao               = configOlist.SITUACAO_SEPARACAO
        self.id                               = id
        self.situacao                         = situacao
        self.situacaoCheckout                 = situacaoCheckout
        self.dataCriacao                      = dataCriacao
        self.dataSeparacao                    = dataSeparacao
        self.dataCheckout                     = dataCheckout
        self.cliente_nome                     = cliente_nome
        self.cliente_codigo                   = cliente_codigo
        self.cliente_fantasia                 = cliente_fantasia
        self.cliente_tipoPessoa               = cliente_tipoPessoa
        self.cliente_cpfCnpj                  = cliente_cpfCnpj
        self.cliente_inscricaoEstadual        = cliente_inscricaoEstadual
        self.cliente_rg                       = cliente_rg
        self.cliente_telefone                 = cliente_telefone
        self.cliente_celular                  = cliente_celular
        self.cliente_email                    = cliente_email
        self.cliente_endereco_endereco        = cliente_endereco_endereco
        self.cliente_endereco_numero          = cliente_endereco_numero
        self.cliente_endereco_complemento     = cliente_endereco_complemento
        self.cliente_endereco_bairro          = cliente_endereco_bairro
        self.cliente_endereco_municipio       = cliente_endereco_municipio
        self.cliente_endereco_cep             = cliente_endereco_cep
        self.cliente_endereco_uf              = cliente_endereco_uf
        self.cliente_endereco_pais            = cliente_endereco_pais
        self.cliente_id                       = cliente_id
        self.venda_id                         = venda_id
        self.venda_numero                     = venda_numero
        self.venda_data                       = venda_data
        self.venda_situacao                   = venda_situacao
        self.notaFiscal_id                    = notaFiscal_id
        self.notaFiscal_numero                = notaFiscal_numero
        self.notaFiscal_dataEmissao           = notaFiscal_dataEmissao
        self.notaFiscal_situacao              = notaFiscal_situacao
        self.ecommerce_id                     = ecommerce_id
        self.ecommerce_nome                   = ecommerce_nome
        self.ecommerce_numeroPedidoEcommerce  = ecommerce_numeroPedidoEcommerce
        self.ecommerce_numeroPedidoCanalVenda = ecommerce_numeroPedidoCanalVenda
        self.ecommerce_canalVenda             = ecommerce_canalVenda
        self.formaEnvio_id                    = formaEnvio_id
        self.formaEnvio_nome                  = formaEnvio_nome
        self.volumes                          = volumes
        self.itens                            = []
        self.acao                             = None
        
    def decodificar(self,payload:dict=None) -> bool:
        
        if payload:
            try:
                self.id                               = payload["id"]
                self.situacao                         = payload["situacao"]
                self.situacaoCheckout                 = payload["situacaoCheckout"]
                self.dataCriacao                      = payload["dataCriacao"]
                self.dataSeparacao                    = payload["dataSeparacao"]
                self.dataCheckout                     = payload["dataCheckout"]
                if payload.get("cliente"):
                    self.cliente_nome                   = payload["cliente"]["nome"]
                    self.cliente_codigo                 = payload["cliente"]["codigo"]
                    self.cliente_fantasia               = payload["cliente"]["fantasia"]
                    self.cliente_tipoPessoa             = payload["cliente"]["tipoPessoa"]
                    self.cliente_cpfCnpj                = payload["cliente"]["cpfCnpj"]
                    self.cliente_inscricaoEstadual      = payload["cliente"]["inscricaoEstadual"]
                    self.cliente_rg                     = payload["cliente"]["rg"]
                    self.cliente_telefone               = payload["cliente"]["telefone"]
                    self.cliente_celular                = payload["cliente"]["celular"]
                    self.cliente_email                  = payload["cliente"]["email"]
                    self.cliente_id                     = payload["cliente"]["id"]
                    if payload["cliente"].get("endereco"):
                        self.cliente_endereco_endereco      = payload["cliente"]["endereco"]["endereco"]
                        self.cliente_endereco_numero        = payload["cliente"]["endereco"]["numero"]
                        self.cliente_endereco_complemento   = payload["cliente"]["endereco"]["complemento"]
                        self.cliente_endereco_bairro        = payload["cliente"]["endereco"]["bairro"]
                        self.cliente_endereco_municipio     = payload["cliente"]["endereco"]["municipio"]
                        self.cliente_endereco_cep           = payload["cliente"]["endereco"]["cep"]
                        self.cliente_endereco_uf            = payload["cliente"]["endereco"]["uf"]
                        self.cliente_endereco_pais          = payload["cliente"]["endereco"]["pais"]
                if payload.get("venda"):
                    self.venda_id                         = payload["venda"]["id"]
                    self.venda_numero                     = payload["venda"]["numero"]
                    self.venda_data                       = payload["venda"]["data"]
                    self.venda_situacao                   = payload["venda"]["situacao"]
                else:
                    self.venda_id = self.venda_numero = self.venda_data = self.venda_situacao = None
                if payload.get("notaFiscal"):
                    self.notaFiscal_id                    = payload["notaFiscal"]["id"]
                    self.notaFiscal_numero                = payload["notaFiscal"]["numero"]
                    self.notaFiscal_dataEmissao           = payload["notaFiscal"]["dataEmissao"]
                    self.notaFiscal_situacao              = payload["notaFiscal"]["situacao"]
                else:
                    self.notaFiscal_id = self.notaFiscal_numero = self.notaFiscal_dataEmissao = self.notaFiscal_situacao = None
                if payload.get("ecommerce"):
                    self.ecommerce_id                       = payload["ecommerce"]["id"]
                    self.ecommerce_nome                     = payload["ecommerce"]["nome"]
                    self.ecommerce_numeroPedidoEcommerce    = payload["ecommerce"]["numeroPedidoEcommerce"]
                    self.ecommerce_numeroPedidoCanalVenda   = payload["ecommerce"]["numeroPedidoCanalVenda"]
                    self.ecommerce_canalVenda               = payload["ecommerce"]["canalVenda"]
                else:
                    self.ecommerce_id = self.ecommerce_nome = self.ecommerce_numeroPedidoEcommerce = self.ecommerce_numeroPedidoCanalVenda = self.ecommerce_canalVenda = None
                self.formaEnvio_id                    = payload["formaEnvio"]["id"]
                self.formaEnvio_nome                  = payload["formaEnvio"]["nome"]
                self.volumes                          = payload["volumes"]                
                for i in payload["itens"]:
                    it = item.Item()
                    it.decodificar(i)
                    self.itens.append(it)
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
        file_path = configOlist.PATH_OBJECT_SEPARACAO
        if not os.path.exists(file_path):
            logger.error("Objeto da separacao não encontrado em %s",file_path)
            return {"status":"Erro"}
        else:    
            with open(file_path, "r", encoding="utf-8") as f:
                obj = json.load(f)        

        if self.acao == 'get':
            try:
                data = obj[self.acao]

                data["id"]                                  = self.id
                data["situacao"]                            = self.situacao
                data["situacaoCheckout"]                    = self.situacaoCheckout
                data["dataCriacao"]                         = self.dataCriacao
                data["dataSeparacao"]                       = self.dataSeparacao
                data["dataCheckout"]                        = self.dataCheckout
                data["cliente"]["nome"]                     = self.cliente_nome
                data["cliente"]["codigo"]                   = self.cliente_codigo
                data["cliente"]["fantasia"]                 = self.cliente_fantasia
                data["cliente"]["tipoPessoa"]               = self.cliente_tipoPessoa
                data["cliente"]["cpfCnpj"]                  = self.cliente_cpfCnpj
                data["cliente"]["inscricaoEstadual"]        = self.cliente_inscricaoEstadual
                data["cliente"]["rg"]                       = self.cliente_rg
                data["cliente"]["telefone"]                 = self.cliente_telefone
                data["cliente"]["celular"]                  = self.cliente_celular
                data["cliente"]["email"]                    = self.cliente_email
                data["cliente"]["endereco"]["endereco"]     = self.cliente_endereco_endereco
                data["cliente"]["endereco"]["numero"]       = self.cliente_endereco_numero
                data["cliente"]["endereco"]["complemento"]  = self.cliente_endereco_complemento
                data["cliente"]["endereco"]["bairro"]       = self.cliente_endereco_bairro
                data["cliente"]["endereco"]["municipio"]    = self.cliente_endereco_municipio
                data["cliente"]["endereco"]["cep"]          = self.cliente_endereco_cep
                data["cliente"]["endereco"]["uf"]           = self.cliente_endereco_uf
                data["cliente"]["endereco"]["pais"]         = self.cliente_endereco_pais
                data["cliente"]["id"]                       = self.cliente_id                
                data["venda"]["id"]                         = self.venda_id
                data["venda"]["numero"]                     = self.venda_numero
                data["venda"]["data"]                       = self.venda_data
                data["venda"]["situacao"]                   = self.venda_situacao
                data["notaFiscal"]["id"]                    = self.notaFiscal_id
                data["notaFiscal"]["numero"]                = self.notaFiscal_numero
                data["notaFiscal"]["dataEmissao"]           = self.notaFiscal_dataEmissao
                data["notaFiscal"]["situacao"]              = self.notaFiscal_situacao
                data["ecommerce"]["id"]                     = self.ecommerce_id
                data["ecommerce"]["nome"]                   = self.ecommerce_nome
                data["ecommerce"]["numeroPedidoEcommerce"]  = self.ecommerce_numeroPedidoEcommerce
                data["ecommerce"]["numeroPedidoCanalVenda"] = self.ecommerce_numeroPedidoCanalVenda
                data["ecommerce"]["canalVenda"]             = self.ecommerce_canalVenda
                data["formaEnvio_id"]                       = self.formaEnvio_id
                data["formaEnvio_nome"]                     = self.formaEnvio_nome
                data["volumes"]                             = self.volumes
                
                itens_list = list()
                for it in self.itens:
                    itens_list.append(it.encodificar(self.acao))
                data["itens"] = itens_list
                
                return data               
            except Exception as e:
                logger.error("Erro ao formatar dict separacao: %s",e)
                return {"status":"Erro"} 
        else:
            return {"status":"Ação não configurada"} 

    async def buscar(self, id:int=None) -> bool:
        
        url = self.endpoint+f"/{id or self.id}"
        try:
            token = self.con.get_latest_valid_token_or_refresh()
            if url and token:                
                get_separacao = requests.get(
                    url=url,
                    headers={
                        "Authorization":f"Bearer {token}",
                        "Content-Type":"application/json",
                        "Accept":"application/json"
                    }
                )
                if get_separacao.status_code == 200:
                        if self.decodificar(get_separacao.json()):
                            self.acao = 'get'
                            return True
                        else:
                            logger.error("Erro ao decodificar separação %s", self.id)
                            return False
                else:                      
                    logger.error("Erro %s: %s cod %s", get_separacao.status_code, get_separacao.json().get("mensagem","Erro desconhecido"), self.id)
                    return False                    
            else:
                logger.warning("Endpoint da API ou token de acesso faltantes")
                return False                    
        except Exception as e:
            logger.error("Erro relacionado ao token de acesso. %s",e)
            return False  

    async def buscar_todas(self) -> bool:

        dataInicial = None
        wkday = datetime.today().weekday()
        if wkday in [5,6]:
            pass
        elif wkday == 1:
            dataInicial = datetime.strftime(datetime.today()-timedelta(days=3),'%Y-%m-%d')
        else:
            dataInicial = datetime.strftime(datetime.today()-timedelta(days=1),'%Y-%m-%d')
        
        dataInicial = '2025-06-01'

        if dataInicial:
            token = self.con.get_latest_valid_token_or_refresh()
            lista_pedidos_separacao = []
            url = self.endpoint+f"/?dataInicial={dataInicial}"
            try:                    
                if url and token:
                    get_separacao = requests.get(
                        url=url,
                        headers={
                            "Authorization":f"Bearer {token}",
                            "Content-Type":"application/json",
                            "Accept":"application/json"
                        }
                    )
                    if get_separacao.status_code == 200:
                        pedidos_separacao = get_separacao.json().get('itens')
                        for ps in pedidos_separacao:
                            if await self.buscar(ps.get('id')):                            
                                reg_separacao = {
                                    "id_separacao":self.id,
                                    "id_pedido":self.venda_id,
                                    "id_nf":self.notaFiscal_id
                                }
                                lista_pedidos_separacao.append(reg_separacao)
                        return True, lista_pedidos_separacao
                    else:
                        logger.error("Erro %s: %s cod %s", get_separacao.status_code, get_separacao.json().get("mensagem","Erro desconhecido"), self.id)
                        return False, []
                else:
                    logger.warning("Endpoint da API ou token de acesso faltantes")
                    return False, []
            except Exception as e:
                logger.error("Erro relacionado ao token de acesso. %s",e)
                return False, []
            finally:
                pass
        else:
            pass