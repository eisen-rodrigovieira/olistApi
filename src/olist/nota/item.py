import logging
from params               import config, configOlist
from src.utils.validaPath import validaPath
from src.olist.nota       import rastro
from lxml                 import etree

logger = logging.getLogger(__name__)
logging.basicConfig( filename=config.PATH_LOGS,
                     encoding='utf-8',
                     format=config.LOGGER_FORMAT,
                     datefmt='%Y-%m-%d %H:%M:%S',
                     level=logging.INFO )

class Item:
      
    def __init__(self):    
        self.file_path     = configOlist.PATH_OBJECT_NOTA_ITEM
        self.valida_path   = validaPath()
        self.ns            = configOlist.NAMESPACE_XML        
        self.idProduto     = None
        self.codigo        = None
        self.descricao     = None
        self.unidade       = None
        self.quantidade    = None
        self.valorUnitario = None
        self.valorTotal    = None
        self.cfop          = None
        self.rastro        = []
        self.acao          = None        

    def decodificar(self,payload:dict=None,rastros=None) -> bool:     
        if payload:
            try:
                self.idProduto     = payload['idProduto']
                self.codigo        = payload['codigo']
                self.descricao     = payload['descricao']
                self.unidade       = payload['unidade']
                self.quantidade    = payload['quantidade']
                self.valorUnitario = payload['valorUnitario']
                self.valorTotal    = payload['valorTotal']
                self.cfop          = payload['cfop']
                try:
                    controles = []
                    for r in rastros:
                        controles.append({
                            "quantidade": int(float(r.findtext('nfe:qLote', namespaces=self.ns))),
                            "lote": r.findtext('nfe:nLote', namespaces=self.ns),
                            "dtFab": r.findtext('nfe:dFab', namespaces=self.ns),
                            "dtVal": r.findtext('nfe:dVal', namespaces=self.ns)
                        })
                except Exception as e:
                    logger.error("Erro ao extrair dados de controle. ID %s. %s",payload["idProduto"],e)
                for controle in controles:
                    rs = rastro.Rastro()
                    rs.decodificar(controle)
                    self.rastro.append(rs)

            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["idProduto"],e)
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
                    rastros_list = list()
                    for rs in self.rastro:
                        rastros_list.append(await rs.encodificar(acao))
                    data["rastro"] = rastros_list
                except Exception as e:
                    logger.error("Erro ao formatar dict item nota: %s",e)
                    return {"status":"Erro"} 
            else:
                pass
            return data            
        except Exception as e:
            logger.error("Erro ao formatar dicionario item de nota: %s",e)
            return {"erro":True}