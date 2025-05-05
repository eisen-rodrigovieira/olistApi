import os
import json
import logging
from params import config, configOlist

logger = logging.getLogger(__name__)
logging.basicConfig(filename=configOlist.PATH_LOGS, encoding='utf-8', format=config.LOGGER_FORMAT, datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

class Fornecedor:
    def __init__(self
                ,id:int=None
                ,nome:str=None
                ,codigoProdutoNoFornecedor:str=None
                ,padrao:bool=None
                ):
        self.id                        = id
        self.nome                      = nome
        self.codigoProdutoNoFornecedor = codigoProdutoNoFornecedor
        self.padrao                    = padrao

    def decodificar(self,payload:dict=None):
        if payload:
            try:
                self.id                        = payload["id"]
                self.nome                      = payload["nome"]
                self.codigoProdutoNoFornecedor = payload["codigoProdutoNoFornecedor"]
                self.padrao                    = payload["padrao"]
            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    def encodificar(self) -> dict:
        data = {}
        try:
            if not os.path.exists(configOlist.PATH_OBJECT_PRODUTO_FORNECEDOR):
                logger.error("Objeto do fornecedor de produto não encontrado em %s",configOlist.PATH_OBJECT_PRODUTO_FORNECEDOR)
                return {"erro":True}
            else:    
                with open(configOlist.PATH_OBJECT_PRODUTO_FORNECEDOR, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["id"]                        = self.id
                data["nome"]                      = self.nome
                data["codigoProdutoNoFornecedor"] = self.codigoProdutoNoFornecedor           
                data["padrao"]                    = self.padrao           
                return data               
        except Exception as e:
            logger.error("Erro ao formatar dicionario fornecedor de produto: %s",e)
            return {"erro":True}