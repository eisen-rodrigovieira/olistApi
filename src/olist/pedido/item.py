import os
import json
import logging
import requests
from src.olist.connect import Connect
from src.olist.produto.produto import Produto
from params import config, configOlist

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Item:
  
    def __init__(self
                 ,id:int=None
                 ,sku:str=None
                 ,descricao:str=None
                 ,quantidade:int=None
                 ,valorUnitario:float=None
                 ,infoAdicional:str=None
                ):    
        self.file_path     = configOlist.PATH_OBJECT_PEDIDO_ITEM
        self.endpoint      = config.API_URL+config.ENDPOINT_PRODUTOS             
        self.id            = id
        self.sku           = sku
        self.descricao     = descricao
        self.quantidade    = quantidade
        self.valorUnitario = valorUnitario
        self.infoAdicional = infoAdicional
        self.acao          = None        

    def valida_kit(self,id:int=None,lcto_item:dict=None) -> tuple[bool,dict]:
        # print("KIT: iniciando validacao")
        # print(f"KIT: dados recebidos {lcto_item}")
        self.con = Connect() 

        url = self.endpoint+f"/{id or self.id}"
        # print(f"KIT: url {url}")
        prod = Produto()      
        #print(url)
        try:
            token = self.con.get_latest_valid_token_or_refresh()
            if url and token:                
                get_produto = requests.get(
                    url=url,
                    headers={
                        "Authorization":f"Bearer {token}",
                        "Content-Type":"application/json",
                        "Accept":"application/json"
                    }
                )
                if get_produto.status_code == 200:
                    # print("KIT: buscado dados do produto")
                    if prod.decodificar(get_produto.json()):
                        self.acao = 'get'
                        if prod.tipo == 'K':
                            # print(f"KIT: é kit de {len(prod.kit)} produtos")
                            qtd_kit = lcto_item["quantidade"]
                            vlt_kit = lcto_item["valorUnitario"]
                            res_item = []
                            # print(f"KIT: {(prod.kit)} produtos")
                            for k in prod.kit:
                                kit_item = {
                                    "produto": {
                                        "id": k.produto_id,
                                        "sku": k.produto_sku,
                                        "descricao": k.produto_descricao
                                    },
                                    "quantidade": k.quantidade * qtd_kit,
                                    "valorUnitario": vlt_kit / len(prod.kit),
                                    "infoAdicional": ""                                    
                                }
                                # print(f"KIT: item {kit_item}")
                                res_item.append(kit_item)                            
                            return True, res_item
                        else:
                            return False, {}
                    else:
                        logger.error("Erro ao decodificar pedido %s", self.id)
                        return False, {}
                else:                      
                    logger.error("Erro %s: %s cod %s", get_produto.status_code, get_produto.json().get("mensagem","Erro desconhecido"), self.id)
                    return False, {}                   
            else:
                logger.warning("Endpoint da API ou token de acesso faltantes")
                return False, {}                    
        except Exception as e:
            logger.error("Erro relacionado ao token de acesso. %s",e)
            return False, {}
        

    def decodificar(self,payload:dict=None) -> bool:     
        if payload:
            try:
                self.id            = payload['produto']['id']
                self.sku           = payload['produto']['sku']
                self.descricao     = payload['produto']['descricao']
                self.quantidade    = payload['quantidade']
                self.valorUnitario = payload['valorUnitario']
                self.infoAdicional = payload['infoAdicional']
            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    def encodificar(self,acao:str=None) -> dict:
        data = {}
        try:
            if not os.path.exists(self.file_path):
                logger.error("Objeto do item de pedido não encontrado em %s",self.file_path)
                return {"erro":True}
            else:    
                with open(self.file_path, "r", encoding="utf-8") as f:
                    obj = json.load(f)   
                if acao == 'get':
                    try:
                        data = obj[acao]                                 
                        data['produto']['id']        = self.id
                        data['produto']['sku']       = self.sku
                        data['produto']['descricao'] = self.descricao
                        data['quantidade']           = self.quantidade
                        data['valorUnitario']        = self.valorUnitario
                        data['infoAdicional']        = self.infoAdicional
                    except Exception as e:
                        logger.error("Erro ao formatar dict item pedido: %s",e)
                        return {"status":"Erro"} 
                else:
                    pass
                return data
            
        except Exception as e:
            logger.error("Erro ao formatar dicionario item de pedido: %s",e)
            return {"erro":True}