import logging
from params               import config, configOlist
from src.utils.validaPath import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Deposito:  
    def __init__(self,):
        self.file_path     = configOlist.PATH_OBJECT_ESTOQUE_DEPOSITO
        self.valida_path   = validaPath()
        self.id            = None
        self.nome          = None
        self.desconsiderar = None
        self.saldo         = None
        self.reservado     = None
        self.disponivel    = None
        self.acao          = None      

    def decodificar(self,payload:dict=None) -> bool:     
        if payload:
            try:
                self.id            = payload['id']
                self.nome          = payload['nome']
                self.desconsiderar = payload['desconsiderar']
                self.saldo         = payload['saldo']
                self.reservado     = payload['reservado']
                self.disponivel    = payload['disponivel']
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
                    data['id']            = self.id           
                    data['nome']          = self.nome         
                    data['desconsiderar'] = self.desconsiderar
                    data['saldo']         = self.saldo        
                    data['reservado']     = self.reservado    
                    data['disponivel']    = self.disponivel
                except Exception as e:
                    logger.error("Erro ao formatar dicionário deposito estoque: %s",e)                    
            elif acao == 'post':
                try:
                    data = obj[acao]                                 
                    data['id'] = self.id   
                except Exception as e:
                    logger.error("Erro ao formatar dicionário deposito estoque: %s",e)            
        except Exception as e:
            logger.error("Erro ao formatar dicionário deposito estoque: %s",e)
        finally:
            return data            