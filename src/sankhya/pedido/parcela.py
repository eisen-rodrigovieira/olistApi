import os
import json
import logging
from params               import config, configSankhya
from src.sankhya.dbConfig import dbConfig

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

## OBS.: ASSUME-SE 1 PARCELA/DESDOBRAMENTO POR PEDIDO

class Parcela:
    def __init__(self,
                nufin:int=None,
                codemp:int=None,
                numnota:int=None,
                dtneg:str=None,
                desdobramento:int=None,
                dhmov:str=None,
                dtvencinic:str=None,
                dtvenc:str=None,
                codparc:int=None,
                codtipoper:int=None,
                dhtipoper:str=None,
                codbco:int=None,
                codctabcoint:int=None,
                codnat:int=None,
                codvend:int=None,
                codtiptit:int=None,
                vlrdesdob:int=None,
                recdesp:int=None,
                provisao:str=None,
                origem:str=None,
                tipmarccheq:str=None,
                nunota:int=None,
                dtentsai:str=None,
                dtalter:str=None,
                codusu:int=None,
                sequencia:int=None,
                tpagnfce:str=None,
                dtprazo:str=None,
                ad_taxashopee:int=None
            ):
        self.db              = dbConfig()
        self.nufin           = nufin
        self.codemp          = codemp
        self.numnota         = numnota
        self.dtneg           = dtneg
        self.desdobramento   = desdobramento
        self.dhmov           = dhmov
        self.dtvencinic      = dtvencinic
        self.dtvenc          = dtvenc
        self.codparc         = codparc
        self.codtipoper      = codtipoper
        self.dhtipoper       = dhtipoper
        self.codbco          = codbco
        self.codctabcoint    = codctabcoint
        self.codnat          = codnat
        self.codvend         = codvend
        self.codtiptit       = codtiptit
        self.vlrdesdob       = vlrdesdob
        self.recdesp         = recdesp
        self.provisao        = provisao
        self.origem          = origem
        self.tipmarccheq     = tipmarccheq
        self.nunota          = nunota
        self.dtentsai        = dtentsai
        self.dtalter         = dtalter
        self.codusu          = codusu
        self.sequencia       = sequencia
        self.tpagnfce        = tpagnfce
        self.dtprazo         = dtprazo
        self.ad_taxashopee   = ad_taxashopee
        pass

    def decodificar(self,data:dict=None) -> bool:
        if data:
            try:

                self.nufin           = data["nufin"]
                self.codemp          = data["codemp"]
                self.numnota         = data["numnota"]
                self.dtneg           = data["dtneg"]
                self.desdobramento   = data["desdobramento"]
                self.dhmov           = data["dhmov"]
                self.dtvencinic      = data["dtvencinic"]
                self.dtvenc          = data["dtvenc"]
                self.codparc         = data["codparc"]
                self.codtipoper      = data["codtipoper"]
                self.dhtipoper       = data["dhtipoper"]
                self.codbco          = data["codbco"]
                self.codctabcoint    = data["codctabcoint"]
                self.codnat          = data["codnat"]
                self.codvend         = data["codvend"]
                self.codtiptit       = data["codtiptit"]
                self.vlrdesdob       = data["vlrdesdob"]
                self.recdesp         = data["recdesp"]
                self.provisao        = data["provisao"]
                self.origem          = data["origem"]
                self.tipmarccheq     = data["tipmarccheq"]
                self.nunota          = data["nunota"]
                self.dtentsai        = data["dtentsai"]
                self.dtalter         = data["dtalter"]
                self.codusu          = data["codusu"]
                self.sequencia       = data["sequencia"]
                self.tpagnfce        = data["tpagnfce"]
                self.dtprazo         = data["dtprazo"]
                self.ad_taxashopee   = data["ad_taxashopee"]

                return True

            except Exception as e:
                logger.error("Erro ao extrair dados das parcelas do pedido. Cód. %s. %s",data["nunota"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    async def buscar(self, nunota:int=None, sequencia:int=None) -> bool:
        file_path = configSankhya.PATH_SCRIPT_PEDIDO_FIN

        if not os.path.exists(file_path):
            logger.error("Script da TGFFIN não encontrado em %s",file_path)
            return False
        else:    
            with open(file_path, "r", encoding="utf-8") as f:
                query = f.read()
                
                try:
                    params = {"NUNOTA": nunota or self.nunota}
                    rows = await self.db.select(query=query,params=params)
                                        
                    if rows:
                        self.decodificar(rows[0])
                        return True
                    else:
                        return False
                except:
                    logger.error("Nº único do pedido %s",self.nunota)
                    return False
                
    async def buscar_parametros(self,**kwargs) -> tuple:   
        try:
            dhalter_top = await self.db.select(query='''
                                                    SELECT MAX(DHALTER) DHALTER
                                                    FROM TGFTOP
                                                    WHERE CODTIPOPER = :CODTIPOPER
                                                ''',
                                                params={"CODTIPOPER":kwargs['codtipoper']})
            return { "dhalter_top":dhalter_top[0]['dhalter'].strftime('%Y-%m-%d %H:%M:%S') }
        except:
            print("erro ao buscar parametros")

    async def preparacao(self,payload_olist:dict=None,nunota:int=None,numnota:int=None) -> tuple[bool,dict]:
        file_path = configSankhya.PATH_PARAMS_INS_PEDIDO_FIN

        if payload_olist and nunota and numnota:
            try:
                if not os.path.exists(file_path):
                    raise FileNotFoundError("Parametros de inserção de movimentação financeira não encontrados.")
                with open(file_path, "r", encoding="utf-8") as f:
                    ins_tgffin = json.load(f)
            except Exception as e:
                print(f"Erro: {e}")

            parametros = await self.buscar_parametros( codtipoper  = ins_tgffin['CODTIPOPER'] )                
            
            valores_insert = {
                "CODEMP"        : ins_tgffin["CODEMP"],
                "NUMNOTA"       : int(numnota),
                "DTNEG"         : payload_olist["data"],
                "DESDOBRAMENTO" : ins_tgffin["DESDOBRAMENTO"],
                "DTVENCINIC"    : payload_olist["data"],
                "DTVENC"        : payload_olist["data"],
                "CODPARC"       : ins_tgffin["CODPARC"],
                "CODTIPOPER"    : ins_tgffin["CODTIPOPER"],
                "DHTIPOPER"     : parametros["dhalter_top"],
                "CODBCO"        : ins_tgffin["CODBCO"],
                "CODCTABCOINT"  : ins_tgffin["CODCTABCOINT"],
                "CODNAT"        : ins_tgffin["CODNAT"],
                "CODVEND"       : ins_tgffin["CODVEND"],
                "CODTIPTIT"     : ins_tgffin["CODTIPTIT"],
                "VLRDESDOB"     : float(payload_olist["valor"]),
                "RECDESP"       : ins_tgffin["RECDESP"],
                "PROVISAO"      : ins_tgffin["PROVISAO"],
                "ORIGEM"        : ins_tgffin["ORIGEM"],
                "TIPMARCCHEQ"   : ins_tgffin["TIPMARCCHEQ"],
                "NUNOTA"        : int(nunota),
                "CODUSU"        : ins_tgffin["CODUSU"],
                "SEQUENCIA"     : 1,
                "TPAGNFCE"      : ins_tgffin["TPAGNFCE"],
                "DTPRAZO"       : payload_olist["data"],
                "AD_TAXASHOPEE" : 0
            }

            return True, valores_insert
        else:
            print("Dados faltantes")

    async def atualiza_seqs(self,kwargs):

        pass

    async def registrar(self, payload:dict=None, nunota:int=None, numnota:int=None) -> tuple[bool,int]:
        file_path = configSankhya.PATH_INSERT_PEDIDO_FIN

        if not os.path.exists(file_path):
            logger.error("Script de insert da TGFFIN não encontrado em %s",file_path)
            return False, None
        else: 
            ack, data = await self.preparacao(payload_olist=payload,
                                              nunota=nunota,
                                              numnota=numnota)
            if ack:
                with open(file_path, "r", encoding="utf-8") as f:
                    query = f.read()
                ack2, rows = await self.db.dml(query=query,params=data)
                if ack2:
                    logger.info("Financeiro inserido no pedido %s com sucesso",nunota)
                    return ack2, rows
                else:
                    return ack2, None     