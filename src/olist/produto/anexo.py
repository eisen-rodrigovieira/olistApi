import os
import json
import logging
from params import config, configOlist

logger = logging.getLogger(__name__)
logging.basicConfig(filename=configOlist.PATH_LOGS, encoding='utf-8', format=config.LOGGER_FORMAT, datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

class Anexo:
    def __init__(self
                ,url:str=None
                ,externo:bool=None
                ):
        self.url     = url
        self.externo = externo

    def decodificar(self,payload:dict=None):
        if payload:
            try:
                self.url     = payload["url"]
                self.externo = payload["externo"]
            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    def encodificar(self) -> dict:
        data = {}
        try:
            if not os.path.exists(configOlist.PATH_OBJECT_PRODUTO_ANEXO):
                logger.error("Objeto do anexo de produto não encontrado em %s",configOlist.PATH_OBJECT_PRODUTO_ANEXO)
                return {"erro":True}
            else:    
                with open(configOlist.PATH_OBJECT_PRODUTO_ANEXO, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["url"]     = self.url
                data["externo"] = self.externo
                return data               
        except Exception as e:
            logger.error("Erro ao formatar dicionario anexo de produto: %s",e)
            return {"erro":True} 