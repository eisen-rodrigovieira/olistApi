import os
import logging
from params               import config, configSankhya
from src.sankhya.pedido import item, parcela
from src.sankhya.dbConfig import dbConfig

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

class Pedido:

    def __init__(self,
                nunota:int=None,
                numnota:int=None,
                ad_mkp_id:int=None,
                ad_mkp_numped:int=None,
                ad_mkp_codped:str=None,
                ad_mkp_origem:str=None,
                codemp:int=None,
                codcencus:int=None,
                dtneg:str=None,
                dtmov:str=None,
                dtalter:str=None,
                codempnegoc:int=None,
                codparc:int=None,
                codtipoper:int=None,
                dhtipoper:str=None,
                tipmov:str=None,
                codtipvenda:int=None,
                dhtipvenda:str=None,
                codvend:int=None,
                observacao:str=None,
                vlrdesctot:float=None,
                vlrdesctotitem:float=None,
                vlrfrete:float=None,
                cif_fob:str=None,
                vlrnota:float=None,
                qtdvol:int=None,
                baseicms:float=None,
                vlricms:float=None,
                baseipi:float=None,
                vlripi:float=None,
                issretido:str=None,
                baseiss:float=None,
                vlriss:float=None,
                aprovado:str=None,
                codusu:int=None,
                irfretido:str=None,
                vlrirf:float=None,
                volume:str=None,
                vlrsubst:float=None,
                basesubstit:float=None,
                peso:float=None,
                codnat:int=None,
                vlrfretecpl:float=None,
                codusuinc:int=None,
                baseirf:float=None,
                aliqirf:float=None,
                pesobruto:float=None,
                hrentsai:str=None,
                libconf:str=None,
                vlricmsdifaldest:float=None,
                vlricmsdifalrem:float=None,
                vlricmsfcp:float=None,
                codcidorigem:int=None,
                codciddestino:int=None,
                codcidentrega:int=None,
                coduforigem:int=None,
                codufdestino:int=None,
                codufentrega:int=None,
                classificms:str=None,
                vlricmsfcpint:float=None,
                vlrstfcpintant:float=None,
                statuscfe:str=None,
                histconfig:str=None,
                ad_idshopee:str=None,
                ad_taxashopee:float=None,
                qtdite:int=None,
                qtdfin:int=None
                 ):
        self.nunota           =  nunota
        self.numnota          =  numnota
        self.ad_mkp_id        =  ad_mkp_id
        self.ad_mkp_numped    =  ad_mkp_numped
        self.ad_mkp_codped    =  ad_mkp_codped
        self.ad_mkp_origem    =  ad_mkp_origem
        self.codemp           =  codemp
        self.codcencus        =  codcencus
        self.dtneg            =  dtneg
        self.dtmov            =  dtmov
        self.dtalter          =  dtalter
        self.codempnegoc      =  codempnegoc
        self.codparc          =  codparc
        self.codtipoper       =  codtipoper
        self.dhtipoper        =  dhtipoper
        self.tipmov           =  tipmov
        self.codtipvenda      =  codtipvenda
        self.dhtipvenda       =  dhtipvenda
        self.codvend          =  codvend
        self.observacao       =  observacao
        self.vlrdesctot       =  vlrdesctot
        self.vlrdesctotitem   =  vlrdesctotitem
        self.vlrfrete         =  vlrfrete
        self.cif_fob          =  cif_fob
        self.vlrnota          =  vlrnota
        self.qtdvol           =  qtdvol
        self.baseicms         =  baseicms
        self.vlricms          =  vlricms
        self.baseipi          =  baseipi
        self.vlripi           =  vlripi
        self.issretido        =  issretido
        self.baseiss          =  baseiss
        self.vlriss           =  vlriss
        self.aprovado         =  aprovado
        self.codusu           =  codusu
        self.irfretido        =  irfretido
        self.vlrirf           =  vlrirf
        self.volume           =  volume
        self.vlrsubst         =  vlrsubst
        self.basesubstit      =  basesubstit
        self.peso             =  peso
        self.codnat           =  codnat
        self.vlrfretecpl      =  vlrfretecpl
        self.codusuinc        =  codusuinc
        self.baseirf          =  baseirf
        self.aliqirf          =  aliqirf
        self.pesobruto        =  pesobruto
        self.hrentsai         =  hrentsai
        self.libconf          =  libconf
        self.vlricmsdifaldest =  vlricmsdifaldest
        self.vlricmsdifalrem  =  vlricmsdifalrem
        self.vlricmsfcp       =  vlricmsfcp
        self.codcidorigem     =  codcidorigem
        self.codciddestino    =  codciddestino
        self.codcidentrega    =  codcidentrega
        self.coduforigem      =  coduforigem
        self.codufdestino     =  codufdestino
        self.codufentrega     =  codufentrega
        self.classificms      =  classificms
        self.vlricmsfcpint    =  vlricmsfcpint
        self.vlrstfcpintant   =  vlrstfcpintant
        self.statuscfe        =  statuscfe
        self.histconfig       =  histconfig
        self.ad_idshopee      =  ad_idshopee
        self.ad_taxashopee    =  ad_taxashopee
        self.qtdite           =  qtdite
        self.qtdfin           =  qtdfin
        self.itens            =  []
        self.parcelas         =  []
  
        pass


    async def decodificar(self,data:dict=None) -> bool:
        if data:
            try:
                self.nunota           =  data["nunota"]
                self.numnota          =  data["numnota"]
                self.ad_mkp_id        =  data["ad_mkp_id"]
                self.ad_mkp_numped    =  data["ad_mkp_numped"]
                self.ad_mkp_codped    =  data["ad_mkp_codped"]
                self.ad_mkp_origem    =  data["ad_mkp_origem"]
                self.codemp           =  data["codemp"]
                self.codcencus        =  data["codcencus"]
                self.dtneg            =  data["dtneg"]
                self.dtmov            =  data["dtmov"]
                self.dtalter          =  data["dtalter"]
                self.codempnegoc      =  data["codempnegoc"]
                self.codparc          =  data["codparc"]
                self.codtipoper       =  data["codtipoper"]
                self.dhtipoper        =  data["dhtipoper"]
                self.tipmov           =  data["tipmov"]
                self.codtipvenda      =  data["codtipvenda"]
                self.dhtipvenda       =  data["dhtipvenda"]
                self.codvend          =  data["codvend"]
                self.observacao       =  data["observacao"]
                self.vlrdesctot       =  data["vlrdesctot"]
                self.vlrdesctotitem   =  data["vlrdesctotitem"]
                self.vlrfrete         =  data["vlrfrete"]
                self.cif_fob          =  data["cif_fob"]
                self.vlrnota          =  data["vlrnota"]
                self.qtdvol           =  data["qtdvol"]
                self.baseicms         =  data["baseicms"]
                self.vlricms          =  data["vlricms"]
                self.baseipi          =  data["baseipi"]
                self.vlripi           =  data["vlripi"]
                self.issretido        =  data["issretido"]
                self.baseiss          =  data["baseiss"]
                self.vlriss           =  data["vlriss"]
                self.aprovado         =  data["aprovado"]
                self.codusu           =  data["codusu"]
                self.irfretido        =  data["irfretido"]
                self.vlrirf           =  data["vlrirf"]
                self.volume           =  data["volume"]
                self.vlrsubst         =  data["vlrsubst"]
                self.basesubstit      =  data["basesubstit"]
                self.peso             =  data["peso"]
                self.codnat           =  data["codnat"]
                self.vlrfretecpl      =  data["vlrfretecpl"]
                self.codusuinc        =  data["codusuinc"]
                self.baseirf          =  data["baseirf"]
                self.aliqirf          =  data["aliqirf"]
                self.pesobruto        =  data["pesobruto"]
                self.hrentsai         =  data["hrentsai"]
                self.libconf          =  data["libconf"]
                self.vlricmsdifaldest =  data["vlricmsdifaldest"]
                self.vlricmsdifalrem  =  data["vlricmsdifalrem"]
                self.vlricmsfcp       =  data["vlricmsfcp"]
                self.codcidorigem     =  data["codcidorigem"]
                self.codciddestino    =  data["codciddestino"]
                self.codcidentrega    =  data["codcidentrega"]
                self.coduforigem      =  data["coduforigem"]
                self.codufdestino     =  data["codufdestino"]
                self.codufentrega     =  data["codufentrega"]
                self.classificms      =  data["classificms"]
                self.vlricmsfcpint    =  data["vlricmsfcpint"]
                self.vlrstfcpintant   =  data["vlrstfcpintant"]
                self.statuscfe        =  data["statuscfe"]
                self.histconfig       =  data["histconfig"]
                self.ad_idshopee      =  data["ad_idshopee"]
                self.ad_taxashopee    =  data["ad_taxashopee"]
                self.qtdite           =  data["qtdite"]
                self.qtdfin           =  data["qtdfin"]

                for i in range(self.qtdite):
                    it = item.Item()
                    await it.buscar(nunota=data["nunota"],sequencia=i+1)
                    self.itens.append(it)

                #for p in range(self.qtdfin):
                pr = parcela.Parcela()
                await pr.buscar(nunota=data["nunota"])
                self.parcelas.append(pr)

                return True

            except Exception as e:
                logger.error("Erro ao extrair dados do pedido. Cód. %s. %s",data["nunota"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    async def buscar(self,nunota:int=None) -> bool:
        file_path = configSankhya.PATH_SCRIPT_PEDIDO_CAB

        if not os.path.exists(file_path):
            logger.error("Script da TGFCAB não encontrado em %s",file_path)
            return False
        else:    
            db = dbConfig()
            with open(file_path, "r", encoding="utf-8") as f:
                query = f.read()
                
                try:
                    params = {"NUNOTA": nunota or self.nunota}
                    rows = await db.select(query=query,params=params)
                                        
                    if rows:
                        return await self.decodificar(rows[0])
                    else:
                        return False
                except:
                    logger.error("Nº único do pedido %s",self.nunota)
                    return False
                


    async def atualizar(self, params: dict=None) -> tuple[bool,int]:
        """
        Atualiza os dados do produto no banco de dados com os parâmetros informados.

        Args:
            params (dict): Dicionário com os parâmetros para a atualização.

        Returns:
            tuple: Tupla contendo um booleano indicando sucesso e o número de linhas afetadas (ou None).
        """

        if not os.path.exists(configSankhya.PATH_UPDATE_PRODUTO):
            logger.error("Script de update da TGFPRO não encontrado em %s",configSankhya.PATH_UPDATE_PRODUTO)
            return False, None
        else: 
            db = dbConfig()   
            with open(configSankhya.PATH_UPDATE_PRODUTO, "r", encoding="utf-8") as f:
                query = f.read()
                ack, rows = await db.dml(query=query,params=params)
                if ack:
                   return ack, rows
                else:
                    return ack, None
        
            