import os
import logging
from params               import config, configSankhya
from src.sankhya.dbConfig import dbConfig

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

class Item:
    def __init__(self,
                nunota:int=None,
                sequencia:int=None,
                codemp:int=None,
                codprod:int=None,
                codlocalorig:int=None,
                usoprod:str=None,    
                qtdneg:int=None,
                vlrunit:float=None,
                vlrtot:float=None,    
                codvol:int=None,
                atualestoque:int=None,
                reserva:str=None,
                statusnota:str=None,
                codvend:int=None
                 ):
        
        self.nunota       = nunota
        self.sequencia    = sequencia
        self.codemp       = codemp
        self.codprod      = codprod
        self.codlocalorig = codlocalorig
        self.usoprod      = usoprod
        self.qtdneg       = qtdneg
        self.vlrunit      = vlrunit
        self.vlrtot       = vlrtot   
        self.codvol       = codvol
        self.atualestoque = atualestoque
        self.reserva      = reserva
        self.statusnota   = statusnota
        self.codvend      = codvend  
        pass


    def decodificar(self,data:dict=None) -> bool:
        if data:
            try:
                self.nunota       = data["nunota"]
                self.sequencia    = data["sequencia"]
                self.codemp       = data["codemp"]
                self.codprod      = data["codprod"]
                self.codlocalorig = data["codlocalorig"]
                self.usoprod      = data["usoprod"]  
                self.qtdneg       = data["qtdneg"]
                self.vlrunit      = data["vlrunit"]
                self.vlrtot       = data["vlrtot"]
                self.codvol       = data["codvol"]
                self.atualestoque = data["atualestoque"]
                self.reserva      = data["reserva"]
                self.statusnota   = data["statusnota"]
                self.codvend      = data["codvend"]
                return True

            except Exception as e:
                logger.error("Erro ao extrair dados dos itens do pedido. Cód. %s. %s",data["nunota"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    async def buscar(self, nunota:int=None, sequencia:int=None) -> bool:
        file_path = configSankhya.PATH_SCRIPT_PEDIDO_ITE

        if not os.path.exists(file_path):
            logger.error("Script da TGFITE não encontrado em %s",file_path)
            return False
        else:    
            db = dbConfig()
            with open(file_path, "r", encoding="utf-8") as f:
                query = f.read()
                
                try:
                    params = {
                        "NUNOTA": nunota or self.nunota,
                        "SEQUENCIA": sequencia or self.sequencia
                    }
                    rows = await db.select(query=query,params=params)
                                        
                    if rows:
                        self.decodificar(rows[0])
                        return True
                    else:
                        return False
                except:
                    logger.error("Nº único do pedido %s",self.nunota)
                    return False
                
