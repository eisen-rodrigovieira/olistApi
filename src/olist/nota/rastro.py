import logging
from params               import config, configOlist
from src.utils.validaPath import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig( filename=config.PATH_LOGS,
                     encoding='utf-8',
                     format=config.LOGGER_FORMAT,
                     datefmt='%Y-%m-%d %H:%M:%S',
                     level=logging.INFO )

class Rastro:
      
    def __init__(self):
        self.file_path   = configOlist.PATH_OBJECT_NOTA_ITEM_RASTRO
        self.valida_path = validaPath()         
        self.quantidade  = None  
        self.lote        = None
        self.dtVal       = None
        self.dtFab       = None

    def decodificar(self,payload:dict=None) -> bool:     
        if payload:
            try:
                self.quantidade = payload['quantidade']
                self.lote       = payload['lote']
                self.dtVal      = payload['dtVal']
                self.dtFab      = payload['dtFab']
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
                    data['quantidade'] = self.quantidade
                    data['lote']       = self.lote
                    data['dtVal']      = self.dtVal
                    data['dtFab']      = self.dtFab
                except Exception as e:
                    logger.error("Erro ao formatar dict rastro item nota: %s",e)
                    return {"status":"Erro"} 
            else:
                pass
            return data            
        except Exception as e:
            logger.error("Erro ao formatar dicionario rastro do item de nota: %s",e)
            return {"erro":True}