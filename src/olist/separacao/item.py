import os
import json
import logging
from params               import config, configOlist
from src.utils.validaPath import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Item:
      
    def __init__(self):    
        self.file_path     = configOlist.PATH_OBJECT_SEPARACAO_ITEM
        self.endpoint      = config.API_URL+config.ENDPOINT_SEPARACAO
        self.valida_path   = validaPath()        
        self.id            = None
        self.sku           = None
        self.descricao     = None
        self.quantidade    = None
        self.unidade       = None
        self.localizacao   = None
        self.infoAdicional = None
        self.acao          = None        

    def decodificar(self,payload:dict=None) -> bool:     
        if payload:
            try:
                self.id            = payload['produto']['id']
                self.sku           = payload['produto']['sku']
                self.descricao     = payload['produto']['descricao']
                self.quantidade    = payload['quantidade']
                self.unidade       = payload['unidade']
                self.localizacao   = payload['localizacao']
                self.infoAdicional = payload['infoAdicional']
            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    async def encodificar(self,acao:str=None) -> dict:
        data = {}
        try:
            obj = await self.valida_path.validar(path=self.file_path,mode='r',method='json')
            if acao == 'get':
                try:
                    data = obj[acao]                                 
                    data['produto']['id']        = self.id
                    data['produto']['sku']       = self.sku
                    data['produto']['descricao'] = self.descricao
                    data['quantidade']           = self.quantidade
                    data['unidade']              = self.unidade
                    data['localizacao']          = self.localizacao
                    data['infoAdicional']        = self.infoAdicional
                except Exception as e:
                    logger.error("Erro ao formatar dict item separacao: %s",e)
                    return {"status":"Erro"} 
            else:
                pass
            return data            
        except Exception as e:
            logger.error("Erro ao formatar dicionario item de separacao: %s",e)
            return {"erro":True}