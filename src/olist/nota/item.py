import logging
from params               import config, configOlist
from src.utils.validaPath import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig( filename=config.PATH_LOGS,
                     encoding='utf-8',
                     format=config.LOGGER_FORMAT,
                     datefmt='%Y-%m-%d %H:%M:%S',
                     level=logging.INFO )

class Item:
      
    def __init__(self):    
        self.file_path     = configOlist.PATH_OBJECT_NOTA_ITEM
        self.endpoint      = config.API_URL+config.ENDPOINT_NOTAS
        self.valida_path   = validaPath()        
        self.idProduto     = None
        self.codigo        = None
        self.descricao     = None
        self.unidade       = None
        self.quantidade    = None
        self.valorUnitario = None
        self.valorTotal    = None
        self.cfop          = None
        self.acao          = None        

    def decodificar(self,payload:dict=None) -> bool:     
        if payload:
            try:
                self.idProduto     = payload['idProduto']
                self.codigo        = int(payload['codigo'])
                self.descricao     = payload['descricao']
                self.unidade       = payload['unidade']
                self.quantidade    = payload['quantidade']
                self.valorUnitario = payload['valorUnitario']
                self.valorTotal    = payload['valorTotal']
                self.cfop          = int(payload['cfop'])
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
                    data['idProduto']     = self.idProduto     
                    data['codigo']        = self.codigo        
                    data['descricao']     = self.descricao     
                    data['unidade']       = self.unidade       
                    data['quantidade']    = self.quantidade    
                    data['valorUnitario'] = self.valorUnitario 
                    data['valorTotal']    = self.valorTotal    
                    data['cfop']          = self.cfop          
                    data['acao']          = self.acao
                except Exception as e:
                    logger.error("Erro ao formatar dict item nota: %s",e)
                    return {"status":"Erro"} 
            else:
                pass
            return data            
        except Exception as e:
            logger.error("Erro ao formatar dicionario item de nota: %s",e)
            return {"erro":True}