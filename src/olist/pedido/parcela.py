import logging
from params               import config, configOlist
from src.utils.validaPath import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Parcela:
  
    def __init__(self):
        self.file_path           = configOlist.PATH_OBJECT_PEDIDO_PARCELA
        self.valida_path         = validaPath()         
        self.dias                = None
        self.data                = None
        self.valor               = None
        self.observacoes         = None
        self.formaPagamento_id   = None
        self.formaPagamento_nome = None
        self.meioPagamento_id    = None
        self.meioPagamento_nome  = None

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

    async def encodificar(self,acao:str=None) -> dict:
        data = {}
        try:
            obj = await self.valida_path.validar(path=self.file_path,mode='r',method='json')        
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