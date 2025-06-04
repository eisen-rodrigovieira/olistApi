import os
import json
import logging
from params               import config, configSankhya
from src.sankhya.dbConfig import dbConfig
from src.sankhya.produto.produto  import Produto

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
        self.db           = dbConfig()
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
            with open(file_path, "r", encoding="utf-8") as f:
                query = f.read()
                
                try:
                    params = {
                        "NUNOTA": nunota or self.nunota,
                        "SEQUENCIA": sequencia or self.sequencia
                    }
                    rows = await self.db.select(query=query,params=params)
                                        
                    if rows:
                        self.decodificar(rows[0])
                        return True
                    else:
                        return False
                except:
                    logger.error("Nº único do pedido %s",self.nunota)
                    return False

    async def buscar_parametros(self,**kwargs) -> dict:    
         
        try:
            uf_destino = await self.db.select(query='''
                                                    SELECT CODUF
                                                    FROM TSIUFS
                                                    WHERE UF = :UF
                                                ''',
                                                params={"UF":kwargs['ufdestino']})
            
            icms = await self.db.select(query='''
                                                SELECT IDALIQ, ALIQUOTA, CODTRIB, CODANTECIPST
                                                FROM TGFICM 
                                                WHERE 1=1
                                                    AND UFORIG = 15
                                                    AND UFDEST = :UFDEST
                                                    AND ( CODRESTRICAO = :NCM OR CODRESTRICAO2 = :NCM)
                                                    AND ( CODRESTRICAO2 = 31 OR TIPRESTRICAO2 = 'S')
                                            ''',
                                            params={"UFDEST":uf_destino[0]['coduf'],"NCM":kwargs['ncm']})
            
            if icms:
                res = {
                    "cod_icms":icms[0]['idaliq'],
                    "aliq_icms":icms[0]['aliquota'],
                    "cod_trib":icms[0]['codtrib'],
                    "cod_antst":icms[0]['codantecipst'],
                }
            else:
                res = {
                    "cod_icms":None,
                    "aliq_icms":None,
                    "cod_trib":None,
                    "cod_antst":None
                }

        except Exception as e:
            logger.error("Erro ao buscar parametros: %s",e)
            res = {}            
        finally:
            return res

    async def preparacao(self,payload_olist:dict=None,uf:str=None,nunota:int=None,sequencia:int=None) -> tuple[bool,dict]:
        file_path = configSankhya.PATH_PARAMS_INS_PEDIDO_ITE

        if payload_olist and nunota and sequencia:
            try:
                if not os.path.exists(file_path):
                    raise FileNotFoundError("Parametros de inserção de item de pedido não encontrados.")
                with open(file_path, "r", encoding="utf-8") as f:
                    ins_tgfite = json.load(f)
            except Exception as e:
                print(f"Erro: {e}") 

            produto = Produto()
            if await produto.buscar(codprod=int(payload_olist["produto"]["sku"])):    

                parametros = await self.buscar_parametros( ufdestino = uf,
                                                           ncm       = produto.ncm )

                if parametros:
                    valores_insert = {
                        "NUNOTA"        : nunota,
                        "SEQUENCIA"     : sequencia,
                        "CODEMP"        : ins_tgfite["CODEMP"],
                        "CODPROD"       : int(payload_olist["produto"]["sku"]),
                        "CODLOCALORIG"  : ins_tgfite["CODLOCALORIG"],
                        "USOPROD"       : ins_tgfite["USOPROD"],
                        "QTDNEG"        : payload_olist["quantidade"],
                        "VLRUNIT"       : payload_olist["valorUnitario"],
                        "VLRTOT"        : payload_olist["quantidade"] * payload_olist["valorUnitario"],
                        "CODVOL"        : 'UN',
                        "CODTRIB"       : parametros["cod_trib"],
                        "ALIQICMS"      : parametros["aliq_icms"],
                        "IDALIQICMS"    : parametros["cod_icms"],
                        "BASEICMS"      : payload_olist["quantidade"] * payload_olist["valorUnitario"],
                        "VLRICMS"       : round(payload_olist["quantidade"] * payload_olist["valorUnitario"] * parametros["aliq_icms"] / 100, 3) if parametros["aliq_icms"] else 0,
                        "ALIQIPI"       : 0,
                        "CSTIPI"        : ins_tgfite["CSTIPI"],
                        "CODANTECIPST"  : parametros["cod_antst"],
                        "ATUALESTOQUE"  : ins_tgfite["ATUALESTOQUE"],
                        "RESERVA"       : ins_tgfite["RESERVA"],
                        "STATUSNOTA"    : ins_tgfite["STATUSNOTA"],
                        "CODVEND"       : ins_tgfite["CODVEND"]
                    }
                    return True, valores_insert
                else:
                    return False, {}
        else:
            print("Dados faltantes")
            return False, {}            

    async def atualiza_seqs(self,kwargs):

        pass

    async def registrar(self, payload:dict=None, uf:str=None,nunota:int=None, sequencia:int=None) -> tuple[bool,int]:
        file_path = configSankhya.PATH_INSERT_PEDIDO_ITE

        if not os.path.exists(file_path):
            logger.error("Script de insert da TGFITE não encontrado em %s",file_path)
            return False, None
        else: 
            ack, data = await self.preparacao(payload_olist=payload,
                                              uf=uf,
                                              nunota=nunota,
                                              sequencia=sequencia)
            if ack:
                with open(file_path, "r", encoding="utf-8") as f:
                    query = f.read()                    
                ack2, rows = await self.db.dml(query=query,params=data)
                if ack2:
                    logger.info("Item %s inserido no pedido %s com sucesso",payload["produto"]["sku"],nunota)
                    return ack2, rows
                else:
                    logger.info("Erro ao inserir item %s inserido no pedido %s",payload["produto"]["sku"],nunota)
                    return ack2, None                
                
