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

class Producao:
    def __init__(self
                ,produto_id        :int  = None
                ,produto_sku       :str  = None
                ,produto_descricao :str  = None
                ,quantidade        :int  = None
                ,etapas            :list = None
                ):
        self.produto_id        = produto_id
        self.produto_sku       = produto_sku
        self.produto_descricao = produto_descricao
        self.quantidade        = quantidade
        self.etapas            = etapas

    def decodificar(self,payload:dict=None) -> bool:
        if payload:
            try:
                self.produto_id        = payload["produto_id"]
                self.produto_sku       = payload["produto_sku"]
                self.produto_descricao = payload["produto_descricao"]
                self.quantidade        = payload["quantidade"]
                self.etapas            = payload["etapas"]
                return True
            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    def encodificar(self) -> dict:
        data = {}
        try:
            if not os.path.exists(configOlist.PATH_OBJECT_PRODUTO_PRODUCAO):
                logger.error("Objeto do kit de produto não encontrado em %s",configOlist.PATH_OBJECT_PRODUTO_PRODUCAO)
                return {"erro":True}
            else:    
                with open(configOlist.PATH_OBJECT_PRODUTO_PRODUCAO, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["produto_id"]        = self.produto_id
                data["produto_sku"]       = self.produto_sku
                data["produto_descricao"] = self.produto_descricao
                data["quantidade"]        = self.quantidade
                data["etapas"]            = self.etapas
                return data               
        except Exception as e:
            logger.error("Erro ao formatar dicionario producao de produto: %s",e)
            return {"erro":True} 
