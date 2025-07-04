import logging
from src.utils.validaPath import validaPath
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
    def __init__(self):
        self.db              = dbConfig()
        self.valida_path     = validaPath()   
        self.nufin           = None
        self.codemp          = None
        self.numnota         = None
        self.dtneg           = None
        self.desdobramento   = None
        self.dhmov           = None
        self.dtvencinic      = None
        self.dtvenc          = None
        self.codparc         = None
        self.codtipoper      = None
        self.dhtipoper       = None
        self.codbco          = None
        self.codctabcoint    = None
        self.codnat          = None
        self.codvend         = None
        self.codtiptit       = None
        self.vlrdesdob       = None
        self.recdesp         = None
        self.provisao        = None
        self.origem          = None
        self.tipmarccheq     = None
        self.nunota          = None
        self.dtentsai        = None
        self.dtalter         = None
        self.codusu          = None
        self.sequencia       = None
        self.tpagnfce        = None
        self.dtprazo         = None
        self.ad_taxashopee   = None

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
        query = await self.valida_path.validar(path=file_path,mode='r',method='full')
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
                
    async def buscar_parametros(self,**kwargs) -> tuple[bool,dict]:   
        try:
            dhalter_top = await self.db.select(query='''
                                                    SELECT MAX(DHALTER) DHALTER
                                                    FROM TGFTOP
                                                    WHERE CODTIPOPER = :CODTIPOPER
                                                ''',
                                                params={"CODTIPOPER":kwargs['codtipoper']})
            return True, { "dhalter_top":dhalter_top[0]['dhalter'].strftime('%Y-%m-%d %H:%M:%S') }
        except:
            logger.error("Erro ao buscar parametros")
            return False, {}

    async def preparacao(self,payload_olist:dict=None,nunota:int=None,numnota:int=None) -> tuple[bool,dict]:
        file_path = configSankhya.PATH_PARAMS_INS_PEDIDO_FIN

        if payload_olist and nunota and numnota:
            ins_tgffin = await self.valida_path.validar(path=file_path,mode='r',method='json')
            ack, parametros = await self.buscar_parametros(codtipoper=ins_tgffin['CODTIPOPER'])
            if ack:
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
                logger.error("Erro ao buscar parametros.")
                return False, {}
        else:
            logger.error("Erro. Dados faltantes.")
            return False, {}

    async def registrar(self, payload:dict=None, nunota:int=None, numnota:int=None) -> tuple[bool,int]:
        file_path = configSankhya.PATH_INSERT_PEDIDO_FIN
        ack, data = await self.preparacao(payload_olist=payload,nunota=nunota,numnota=numnota)
        if ack:
            query = await self.valida_path.validar(path=file_path,mode='r',method='full')
            ack2, rows = await self.db.dml(query=query,params=data)
            if ack2:
                return ack2, rows
            else:
                logger.error("Falha ao inserir financeiro no pedido %s",nunota)
                return ack2, 0
        else:
            logger.error("Falha ao preparar os dados")
            return ack, 0    