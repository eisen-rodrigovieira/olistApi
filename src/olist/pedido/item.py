import os
import json
import logging
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
        self.id            = id
        self.sku           = sku
        self.descricao     = descricao
        self.quantidade    = quantidade
        self.valorUnitario = valorUnitario
        self.infoAdicional = infoAdicional
        self.acao          = None        

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