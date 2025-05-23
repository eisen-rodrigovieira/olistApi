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

class Parcela:
  
    def __init__(self
                 ,dias:int=None
                 ,data:str=None
                 ,valor:float=None
                 ,observacoes:str=None
                 ,formaPagamento_id:int=None
                 ,formaPagamento_nome:str=None
                 ,meioPagamento_id:int=None
                 ,meioPagamento_nome:str=None
                ):
        self.file_path           = configOlist.PATH_OBJECT_PEDIDO_PARCELA
        self.dias                = dias
        self.data                = data
        self.valor               = valor
        self.observacoes         = observacoes
        self.formaPagamento_id   = formaPagamento_id
        self.formaPagamento_nome = formaPagamento_nome
        self.meioPagamento_id    = meioPagamento_id
        self.meioPagamento_nome  = meioPagamento_nome

    def decodificar(self,payload:dict=None) -> bool:
     
        if payload:
            try:
                self.dias                = payload["dias"]
                self.data                = payload["data"]
                self.valor               = payload["valor"]
                self.observacoes         = payload["observacoes"]
                if payload.get("formaPagamento"):
                    self.formaPagamento_id   = payload["formaPagamento"]["id"]
                    self.formaPagamento_nome = payload["formaPagamento"]["nome"]
                else:
                    self.formaPagamento_id = self.formaPagamento_nome = None
                if payload.get("meioPagamento"):
                    self.meioPagamento_id    = payload["meioPagamento"]["id"]
                    self.meioPagamento_nome  = payload["meioPagamento"]["nome"]
                else:
                    self.meioPagamento_id = self.meioPagamento_nome = None 
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
                logger.error("Objeto da parcela de pedido não encontrado em %s",self.file_path)
                return {"erro":True}
            else:    
                with open(self.file_path, "r", encoding="utf-8") as f:
                    obj = json.load(f)   
                if acao == 'get':
                    try:
                        data = obj[acao]  
                        data["dias"]                   = self.dias
                        data["data"]                   = self.data
                        data["valor"]                  = self.valor
                        data["observacoes"]            = self.observacoes
                        data["formaPagamento"]["id"]   = self.formaPagamento_id
                        data["formaPagamento"]["nome"] = self.formaPagamento_nome
                        data["meioPagamento"]["id"]    = self.meioPagamento_id
                        data["meioPagamento"]["nome"]  = self.meioPagamento_nome
                    except Exception as e:
                        logger.error("Erro ao formatar dict parcela pedido: %s",e)
                        return {"status":"Erro"}                         
                return data               
        except Exception as e:
            logger.error("Erro ao formatar dicionario parcela de pedido: %s",e)
            return {"erro":True}