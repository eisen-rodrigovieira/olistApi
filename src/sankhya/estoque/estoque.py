import os
import json
import datetime
import logging
from params                    import config, configSankhya
from src.sankhya.dbConfig      import dbConfig
from src.utils.validaPath      import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

class Estoque:

    def __init__(self,
                 codprod:int=None,
                 idprod:int=None,
                 dhevento:datetime=None):
        self.db               = dbConfig()
        self.valida_path      = validaPath() 
        self.codprod          = codprod
        self.idprod           = idprod
        self.dhevento         = dhevento

    async def decodificar(self,data:dict=None) -> bool:
        if data:
            try:
                self.codprod  = data["codprod"]
                self.idprod   = data["idprod"]
                self.dhevento = data["dhevento"]
                return True
            except Exception as e:
                logger.error("Erro ao extrair dados do estoque. Cód. %s. %s",data["codprod"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    async def encodificar(self) -> dict:
        data = {}
        try:
            data["codprod"]  = self.codprod
            data["idprod"]   = self.idprod
            data["dhevento"] = self.dhevento            
        except Exception as e:
            logger.error("Erro ao montar dados do estoque. Cód. %s. %s",self.codprod,e)
        finally:
            return data

    async def buscar_movimentacoes(self) -> list:
        file_path = configSankhya.PATH_SCRIPT_SYNCESTOQUE
        query = await self.valida_path.validar(path=file_path,mode='r',method='full')

        if query:                
            try:
                rows = await self.db.select(query=query)                                    
                if rows:
                    res = []
                    for r in rows:
                        await self.decodificar(data=r)
                        res.append(await self.encodificar())
                    return res
                else:
                    return []
            except:
                logger.error("Erro ao buscar dados de movimentação do estoque")
                return []

    async def buscar_disponivel(self,codprod:int=None) -> bool:

        disp = None
        file_path = configSankhya.PATH_SCRIPT_ESTOQUE_DISP
        query = await self.valida_path.validar(path=file_path,mode='r',method='full')
                        
        try:
            params = {"P_CODPROD": codprod or self.codprod}
            rows = await self.db.select(query=query,params=params)                                    
            if rows:
                disp = rows[0].get('qtd')
            else:
                pass
        except:
            logger.error("Erro ao buscar estoque disponível do produto %s",codprod or self.codprod)
        finally:
            return disp
                
