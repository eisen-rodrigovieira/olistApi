import logging
from datetime              import datetime
from params                import config, configSankhya
from src.olist.pedido.item import Item
from src.sankhya.pedido    import item, parcela
from src.sankhya.dbConfigTEST  import dbConfig
from src.utils.validaPath  import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

class Pedido:

    def __init__(self):
        self.db                 = dbConfig()
        self.valida_path        = validaPath()
        self.nunota             = None
        self.numnota            = None
        self.ad_mkp_codped      = None
        self.ad_mkp_destino     = None
        self.ad_mkp_dhcheckout  = None
        self.ad_mkp_dhseparacao = None
        self.ad_mkp_id          = None
        self.ad_mkp_idnfe       = None
        self.ad_mkp_idseparacao = None
        self.ad_mkp_numped      = None        
        self.ad_mkp_origem      = None
        self.codemp             = None
        self.codcencus          = None
        self.dtneg              = None
        self.dtmov              = None
        self.dtalter            = None
        self.confirmada         = None
        self.pendente           = None
        self.codempnegoc        = None
        self.codparc            = None
        self.codtipoper         = None
        self.dhtipoper          = None
        self.tipmov             = None
        self.codtipvenda        = None
        self.dhtipvenda         = None
        self.codvend            = None
        self.observacao         = None
        self.vlrdesctot         = None
        self.vlrdesctotitem     = None
        self.vlrfrete           = None
        self.cif_fob            = None
        self.vlrnota            = None
        self.qtdvol             = None
        self.aliqicms           = None
        self.baseicms           = None
        self.vlricms            = None
        self.baseipi            = None
        self.vlripi             = None
        self.issretido          = None
        self.baseiss            = None
        self.vlriss             = None
        self.aprovado           = None
        self.codusu             = None
        self.irfretido          = None
        self.vlrirf             = None
        self.volume             = None
        self.vlrsubst           = None
        self.basesubstit        = None
        self.peso               = None
        self.codnat             = None
        self.vlrfretecpl        = None
        self.codusuinc          = None
        self.baseirf            = None
        self.aliqirf            = None
        self.pesobruto          = None
        self.hrentsai           = None
        self.libconf            = None
        self.vlricmsdifaldest   = None
        self.vlricmsdifalrem    = None
        self.vlricmsfcp         = None
        self.codcidorigem       = None
        self.codciddestino      = None
        self.codcidentrega      = None
        self.coduforigem        = None
        self.codufdestino       = None
        self.codufentrega       = None
        self.classificms        = None
        self.vlricmsfcpint      = None
        self.vlrstfcpintant     = None
        self.statuscfe          = None
        self.histconfig         = None
        self.ad_idshopee        = None
        self.ad_taxashopee      = None
        self.qtdite             = None
        self.qtdfin             = None
        self.itens              = []
        self.parcelas           = []

    async def decodificar(self,data:dict=None) -> bool:
        if data:
            try:
                self.nunota             = data["nunota"]
                self.numnota            = data["numnota"]
                self.ad_mkp_codped      = data["ad_mkp_codped"]
                self.ad_mkp_destino     = data["ad_mkp_destino"]
                self.ad_mkp_dhcheckout  = data["ad_mkp_dhcheckout"]
                self.ad_mkp_dhseparacao = data["ad_mkp_dhseparacao"]
                self.ad_mkp_id          = data["ad_mkp_id"]
                self.ad_mkp_idnfe       = data["ad_mkp_idnfe"]
                self.ad_mkp_idseparacao = data["ad_mkp_idseparacao"]
                self.ad_mkp_numped      = data["ad_mkp_numped"]
                self.ad_mkp_origem      = data["ad_mkp_origem"]                
                self.codemp             = data["codemp"]
                self.codcencus          = data["codcencus"]
                self.dtneg              = data["dtneg"]
                self.dtmov              = data["dtmov"]
                self.dtalter            = data["dtalter"]
                self.confirmada         = data["confirmada"]
                self.pendente           = data["pendente"]
                self.codempnegoc        = data["codempnegoc"]
                self.codparc            = data["codparc"]
                self.codtipoper         = data["codtipoper"]
                self.dhtipoper          = data["dhtipoper"]
                self.tipmov             = data["tipmov"]
                self.codtipvenda        = data["codtipvenda"]
                self.dhtipvenda         = data["dhtipvenda"]
                self.codvend            = data["codvend"]
                self.observacao         = data["observacao"]
                self.vlrdesctot         = data["vlrdesctot"]
                self.vlrdesctotitem     = data["vlrdesctotitem"]
                self.vlrfrete           = data["vlrfrete"]
                self.cif_fob            = data["cif_fob"]
                self.vlrnota            = data["vlrnota"]
                self.qtdvol             = data["qtdvol"]
                self.baseicms           = data["baseicms"]
                self.vlricms            = data["vlricms"]
                self.baseipi            = data["baseipi"]
                self.vlripi             = data["vlripi"]
                self.issretido          = data["issretido"]
                self.baseiss            = data["baseiss"]
                self.vlriss             = data["vlriss"]
                self.aprovado           = data["aprovado"]
                self.codusu             = data["codusu"]
                self.irfretido          = data["irfretido"]
                self.vlrirf             = data["vlrirf"]
                self.volume             = data["volume"]
                self.vlrsubst           = data["vlrsubst"]
                self.basesubstit        = data["basesubstit"]
                self.peso               = data["peso"]
                self.codnat             = data["codnat"]
                self.vlrfretecpl        = data["vlrfretecpl"]
                self.codusuinc          = data["codusuinc"]
                self.baseirf            = data["baseirf"]
                self.aliqirf            = data["aliqirf"]
                self.pesobruto          = data["pesobruto"]
                self.hrentsai           = data["hrentsai"]
                self.libconf            = data["libconf"]
                self.vlricmsdifaldest   = data["vlricmsdifaldest"]
                self.vlricmsdifalrem    = data["vlricmsdifalrem"]
                self.vlricmsfcp         = data["vlricmsfcp"]
                self.codcidorigem       = data["codcidorigem"]
                self.codciddestino      = data["codciddestino"]
                self.codcidentrega      = data["codcidentrega"]
                self.coduforigem        = data["coduforigem"]
                self.codufdestino       = data["codufdestino"]
                self.codufentrega       = data["codufentrega"]
                self.classificms        = data["classificms"]
                self.vlricmsfcpint      = data["vlricmsfcpint"]
                self.vlrstfcpintant     = data["vlrstfcpintant"]
                self.statuscfe          = data["statuscfe"]
                self.histconfig         = data["histconfig"]
                self.ad_idshopee        = data["ad_idshopee"]
                self.ad_taxashopee      = data["ad_taxashopee"]
                self.qtdite             = data["qtdite"]
                self.qtdfin             = data["qtdfin"]

                for i in range(self.qtdite):
                    it = item.Item()
                    await it.buscar(nunota=data["nunota"],sequencia=i+1)
                    self.itens.append(it)

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

    async def buscar(self,nunota:int=None,id:int=None,ecommerce:str=None) -> bool:
        file_path = configSankhya.PATH_SCRIPT_PEDIDO_CAB
        query = await self.valida_path.validar(path=file_path,mode='r',method='full')

        if query:                
            try:
                params = {
                    "NUNOTA": nunota or self.nunota,
                    "ID": id or self.ad_mkp_id,
                    "ECOMMERCE": ecommerce or self.ad_mkp_codped
                }
                rows = await self.db.select(query=query,params=params)
                                    
                if rows:
                    return await self.decodificar(rows[0])
                else:
                    return False
            except:
                logger.error("Erro ao buscar dados do pedido Nº único %s",self.nunota)
                return False

    async def buscar_parametros(self,**kwargs) -> dict: 
        proc = configSankhya.PROC_PARAMS_PEDIDO
        empresa_padrao = configSankhya.CODEMP
        res = {}
        try:
            ack, params = await self.db.callproc(procedure=proc,
                                                params_in=[kwargs['codtipoper'],
                                                           kwargs['codtipvenda'],
                                                           empresa_padrao,
                                                           kwargs['ciddestino'],
                                                           kwargs['ufdestino']],
                                                params_out_type=[datetime,datetime,int,int,int])
            res = {
                "dhalter_top"     : params[0],
                "dhalter_tpv"     : params[1],
                "nunota_nextval"  : params[2],
                "numnota_nextval" : params[3],
                "cid_destino"     : params[4]
            }
        except Exception as e:
            logger.error("Erro ao buscar parametros: %s",e)
        finally:
            return res

    async def preparacao(self,payload_olist:dict=None) -> tuple[bool,dict]:
        file_path = configSankhya.PATH_PARAMS_INS_PEDIDO_CAB

        if payload_olist:
            ins_tgfcab = await self.valida_path.validar(path=file_path,mode='r',method='json')
            parametros = await self.buscar_parametros( codtipoper  = ins_tgfcab['CODTIPOPER'],
                                                       codtipvenda = ins_tgfcab['CODTIPVENDA'],
                                                       ciddestino  = payload_olist["cliente"]["endereco"]["municipio"],
                                                       ufdestino   = payload_olist["cliente"]["endereco"]["uf"] )
            if parametros:
                valores_insert = {
                    "NUNOTA"           : parametros["nunota_nextval"],
                    "NUMNOTA"          : parametros["numnota_nextval"],
                    "AD_MKP_CODPED"    : payload_olist["ecommerce"]["numeroPedidoEcommerce"],
                    "AD_MKP_DESTINO"   : parametros["cid_destino"],
                    "AD_MKP_ID"        : int(payload_olist["id"]),
                    "AD_MKP_NUMPED"    : int(payload_olist["numeroPedido"]),
                    "AD_MKP_ORIGEM"    : int(payload_olist["ecommerce"]["id"]),
                    "CODEMP"           : ins_tgfcab["CODEMP"],
                    "CODCENCUS"        : ins_tgfcab["CODCENCUS"],
                    "DTNEG"            : payload_olist["data"],
                    "DTMOV"            : payload_olist["data"],
                    "DTALTER"          : payload_olist["data"],
                    "CODEMPNEGOC"      : ins_tgfcab["CODEMP"],
                    "CODPARC"          : ins_tgfcab["CODPARC"],
                    "CODTIPOPER"       : ins_tgfcab["CODTIPOPER"],
                    "DHTIPOPER"        : parametros["dhalter_top"],
                    "TIPMOV"           : ins_tgfcab["TIPMOV"],
                    "CODTIPVENDA"      : ins_tgfcab["CODTIPVENDA"],
                    "DHTIPVENDA"       : parametros["dhalter_tpv"],
                    "CODVEND"          : ins_tgfcab["CODVEND"],
                    "OBSERVACAO"       : f"#{int(payload_olist["numeroPedido"])} - TESTE IMPORTAÇÃO API OLIST",
                    "VLRDESCTOT"       : float(payload_olist["valorDesconto"]),
                    "VLRDESCTOTITEM"   : float(payload_olist["valorDesconto"]),
                    "VLRFRETE"         : float(payload_olist["valorFrete"]),
                    "CIF_FOB"          : "C" if payload_olist["transportador"]["fretePorConta"] == "R" else "F" if payload_olist["transportador"]["fretePorConta"] == "D" else "",
                    "VLRNOTA"          : float(payload_olist["valorTotalPedido"]),
                    "QTDVOL"           : 0,
                    "BASEICMS"         : float(payload_olist["valorTotalPedido"]),
                    "VLRICMS"          : 0,
                    "BASEIPI"          : float(0),
                    "VLRIPI"           : float(0),
                    "ISSRETIDO"        : "N",
                    "BASEISS"          : float(0),
                    "VLRISS"           : float(0),
                    "APROVADO"         : ins_tgfcab["APROVADO"],
                    "CODUSU"           : ins_tgfcab["CODUSU"],
                    "IRFRETIDO"        : "N",
                    "VLRIRF"           : float(0),
                    "VOLUME"           : ins_tgfcab["VOLUME"],
                    "VLRSUBST"         : float(0),
                    "BASESUBSTIT"      : float(0),
                    "PESO"             : 0,
                    "CODNAT"           : ins_tgfcab["CODNAT"],
                    "VLRFRETECPL"      : float(0),
                    "CODUSUINC"        : ins_tgfcab["CODUSU"],
                    "BASEIRF"          : float(0),
                    "ALIQIRF"          : float(0),
                    "PESOBRUTO"        : 0,
                    "HRENTSAI"         : payload_olist["data"],
                    "LIBCONF"          : "N",
                    "VLRICMSDIFALDEST" : float(0),
                    "VLRICMSDIFALREM"  : float(0),
                    "VLRICMSFCP"       : float(0),
                    "VLRICMSFCPINT"    : float(0),
                    "VLRSTFCPINTANT"   : float(0),
                    "STATUSCFE"        : "N",
                    "HISTCONFIG"       : "S",
                    "AD_IDSHOPEE"      : payload_olist["ecommerce"]["numeroPedidoEcommerce"],
                    "AD_TAXASHOPEE"    : float(0) 
                }
                return True, valores_insert
            else:
                return False, {}
        else:
            logger.error("Erro. Dados olist faltantes.")
            return False, {}

    async def atualiza_seqs(self,**kwargs):
        file_path = configSankhya.PATH_UPDATE_TGFNUM
        query = await self.valida_path.validar(path=file_path,mode='r',method='full')
        ack_seq_nunota, res_seq_nunota = await self.db.dml(query=query,
                                                           params= {"P_PROXCOD":int(kwargs["nunota_nextval"]),
                                                                    "P_TABELA":"TGFCAB",
                                                                    "P_CODEMP":None})
        ack_seq_numnota, res_seq_numnota = await self.db.dml(query=query,
                                                             params={"P_PROXCOD":int(kwargs["numnota_nextval"]),
                                                                     "P_TABELA":"PEDVEN",
                                                                     "P_CODEMP":31})        
        
        return True if ack_seq_nunota and ack_seq_numnota else False
    
    async def atualiza_impostos(self,nunota:int=None):
        file_path = configSankhya.PATH_UPDATE_PEDIDO_IMP
        query = await self.valida_path.validar(path=file_path,mode='r',method='full')
        ack_upd_impostos, res_upd_impostos = await self.db.dml(query=query,
                                                               params={"P_NUNOTA":nunota})

        return ack_upd_impostos
    
    async def registrar(self, payload:dict=None) -> tuple[bool,int]:
        file_path = configSankhya.PATH_INSERT_PEDIDO_CAB
        it = item.Item()
        pr = parcela.Parcela()

        ack, data = await self.preparacao(payload_olist=payload)
        if ack:
            query = await self.valida_path.validar(path=file_path,mode='r',method='full')
            nunota = data["NUNOTA"]
            numnota = data["NUMNOTA"]
            ack_cab, rows_cab = await self.db.dml(query=query,params=data)
            if ack_cab:                
                if payload.get("itens"):
                    rows_itens = 0
                    seq_pedido = 0
                    uf_destino = payload["cliente"]["endereco"]["uf"]                        
                    for i, it_dict in enumerate(payload["itens"]): 
                        olItm = Item()
                        ack_kit, kit_dict = await olItm.valida_kit(id=int(it_dict["produto"]["id"]),lcto_item=it_dict)
                        if ack_kit:
                            for kd in kit_dict:
                                seq_pedido+=1
                                ack_ite, rows_ite = await it.registrar( payload=kd,
                                                                        uf=uf_destino,
                                                                        nunota=nunota,
                                                                        sequencia=seq_pedido) 
                        else:
                            seq_pedido+=1                          
                            ack_ite, rows_ite = await it.registrar( payload=it_dict,
                                                                    uf=uf_destino,
                                                                    nunota=nunota,
                                                                    sequencia=seq_pedido)
                        if ack_ite:
                            rows_itens+=rows_ite
                    if rows_itens == len(payload["itens"]):
                        await self.atualiza_impostos(nunota)
                        ack_itens = True
                    else:
                        ack_itens = False
                        logger.error("Nem todos os itens do pedido %s inseridos.",nunota)        
                else:
                    ack_itens = True
                if payload["pagamento"].get("parcelas"):
                    rows_fins = 0
                    for i, fin_dict in enumerate(payload["pagamento"]["parcelas"]):                        
                        ack_fin, rows_fin = await pr.registrar(payload=fin_dict,
                                                                nunota=nunota,
                                                                numnota=numnota)
                        if ack_fin:
                            rows_fins+=rows_fin
                    if rows_fins == len(payload["pagamento"]["parcelas"]):
                        ack_fins = True
                    else:
                        ack_fins = False      
                else:
                    ack_fins = True
                if ack_cab and ack_itens and ack_fins:
                    if await self.atualiza_seqs(nunota_nextval=nunota,numnota_nextval=numnota):                        
                        return True, nunota
                    else:
                        logger.error("Erro ao atualizar sequencial NUNOTA e/ou NUMNOTA. Pedido %s importado com sucesso! Nº único %s",payload['numeroPedido'],nunota)
                        return False, nunota    
                else:
                    return False, None
            else:
                logger.error("Erro ao inserir cabeçalho do pedido %s.",nunota)        
                return False, nunota
        else:
            logger.error("Erro ao preparar dados para inserção do pedido %s.",payload["numeroPedido"])        
            return False, None

    async def confirmar(self, nunota:int=None, provisao:str=None) -> bool:
        proc = configSankhya.PROC_CONFIRMA_NOTA
        ack, _ = await self.db.callproc(procedure=proc,
                                        params_in=[nunota,provisao,1])
        if ack:
            logger.info("Pedido %s confirmado com sucesso!",nunota)
            return ack
        else:
            logger.error("Erro ao confirmar pedido %s",nunota)        
            return False

    async def valida_desmembramento(self, dados_nota:dict=None) -> bool:
        valida_itens = []
        for i, item in enumerate(dados_nota.get('itens')):
            valida_prod = int(item.get('codigo')) in [it.codprod for it in self.itens]
            valida_qtd = self.itens[i].qtdneg == int(item.get('quantidade'))
            valida_itens.append(True if valida_prod and valida_qtd else False)        
        return all(valida_itens)

    async def gerar_nota(self, pedido:int=None, payload:dict=None) -> tuple[bool,int]:

        ack, nunota_nota = await self.db.callproc(procedure=configSankhya.PROC_GERA_NOTA_VENDA,
                                                  params_in=[pedido,                                                             
                                                             payload.get('dataInclusao'),
                                                             payload.get('id'),
                                                             payload.get('numero')],
                                                  params_out_type=[int])                
        if ack and nunota_nota:
            nota = nunota_nota[0]
            for it in payload.get("itens", []):
                for lt in it.get("rastro", []):
                    if lt.get("lote") and lt.get("quantidade"):
                        lote_info = f"{it['codigo']}##{lt['lote']}##{lt['quantidade']}"
                        ack_item, _ = await self.db.callproc(procedure=configSankhya.PROC_LANCA_ITEM_VENDA,
                                                             params_in=[pedido,lote_info,nota])
                        if not ack_item:
                            logger.error("Erro ao lançar item %s na nota %s",it['codigo'],nota)
                            return False, 0
            ack_vinculo, _ = await self.db.callproc(procedure=configSankhya.PROC_VINCULA_VENDA,params_in=[pedido,nota])
            ack_fin, _ = await self.db.callproc(procedure=configSankhya.PROC_LANCA_FIN,params_in=[pedido])
            ack_imp, _ = await self.db.callproc(procedure=configSankhya.PROC_LANCA_IMP,params_in=[pedido])
            return all([ack_vinculo, ack_fin, ack_imp]), nota
        else:      
            return False, 0  

    async def importar_xml(self, nota:int=None, payload:dict=None) -> tuple[bool,int]:
        ack, _ = await self.db.callproc(procedure=configSankhya.PROC_IMPORTA_XML,
                                                  params_in=[int(nota),                                                             
                                                             int(payload.get('id')),
                                                             str(payload.get('dataInclusao')),
                                                             str(payload.get('chaveAcesso')),
                                                             str(payload.get('codChaveAcesso')),
                                                             payload.get('xml')])                
        if ack:            
            return True, nota
        else:
            logger.error("Erro ao importar XML da nota %s",nota)        
            return False, 0               
            