import logging
from params               import config, configOlist
from src.utils.validaPath import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig( filename=config.PATH_LOGS,
                     encoding='utf-8',
                     format=config.LOGGER_FORMAT,
                     datefmt='%Y-%m-%d %H:%M:%S',
                     level=logging.INFO )

class Parcela:
      
    def __init__(self):    
        self.file_path        = configOlist.PATH_OBJECT_NOTA_PARCELA
        self.endpoint         = config.API_URL+config.ENDPOINT_NOTAS
        self.valida_path      = validaPath()        
        self.dias             = None
        self.data             = None
        self.valor            = None
        self.observacoes      = None
        self.idFormaPagamento = None
        self.idMeioPagamento  = None
        self.acao             = None        

    def decodificar(self,payload:dict=None) -> bool:     
        if payload:
            try:
                self.dias             = payload['dias']
                self.data             = payload['data']
                self.valor            = payload['valor']
                self.observacoes      = payload['observacoes']
                self.idFormaPagamento = payload['idFormaPagamento']
                self.idMeioPagamento  = payload['idMeioPagamento']
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
                    data['dias']             = self.dias
                    data['data']             = self.data
                    data['valor']            = self.valor
                    data['observacoes']      = self.observacoes
                    data['idFormaPagamento'] = self.idFormaPagamento
                    data['idMeioPagamento']  = self.idMeioPagamento
                except Exception as e:
                    logger.error("Erro ao formatar dict parcela nota: %s",e)
                    return {"status":"Erro"} 
            else:
                pass
            return data            
        except Exception as e:
            logger.error("Erro ao formatar dicionario parcela de nota: %s",e)
            return {"erro":True}