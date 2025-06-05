import os
import json
import logging
from params                    import config, configSankhya
from src.olist.pedido.item import Item
from src.sankhya.pedido        import item, parcela
from src.sankhya.dbConfig      import dbConfig

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

class Pedido:

    def __init__(self,
                 nunota           :int   = None,
                 numnota          :int   = None,
                 ad_mkp_id        :int   = None,
                 ad_mkp_numped    :int   = None,
                 ad_mkp_codped    :str   = None,
                 ad_mkp_origem    :str   = None,
                 codemp           :int   = None,
                 codcencus        :int   = None,
                 dtneg            :str   = None,
                 dtmov            :str   = None,
                 dtalter          :str   = None,
                 codempnegoc      :int   = None,
                 codparc          :int   = None,
                 codtipoper       :int   = None,
                 dhtipoper        :str   = None,
                 tipmov           :str   = None,
                 codtipvenda      :int   = None,
                 dhtipvenda       :str   = None,
                 codvend          :int   = None,
                 observacao       :str   = None,
                 vlrdesctot       :float = None,
                 vlrdesctotitem   :float = None,
                 vlrfrete         :float = None,
                 cif_fob          :str   = None,
                 vlrnota          :float = None,
                 qtdvol           :int   = None,
                 aliqicms         :int   = None,
                 baseicms         :float = None,
                 vlricms          :float = None,
                 baseipi          :float = None,
                 vlripi           :float = None,
                 issretido        :str   = None,
                 baseiss          :float = None,
                 vlriss           :float = None,
                 aprovado         :str   = None,
                 codusu           :int   = None,
                 irfretido        :str   = None,
                 vlrirf           :float = None,
                 volume           :str   = None,
                 vlrsubst         :float = None,
                 basesubstit      :float = None,
                 peso             :float = None,
                 codnat           :int   = None,
                 vlrfretecpl      :float = None,
                 codusuinc        :int   = None,
                 baseirf          :float = None,
                 aliqirf          :float = None,
                 pesobruto        :float = None,
                 hrentsai         :str   = None,
                 libconf          :str   = None,
                 vlricmsdifaldest :float = None,
                 vlricmsdifalrem  :float = None,
                 vlricmsfcp       :float = None,
                 codcidorigem     :int   = None,
                 codciddestino    :int   = None,
                 codcidentrega    :int   = None,
                 coduforigem      :int   = None,
                 codufdestino     :int   = None,
                 codufentrega     :int   = None,
                 classificms      :str   = None,
                 vlricmsfcpint    :float = None,
                 vlrstfcpintant   :float = None,
                 statuscfe        :str   = None,
                 histconfig       :str   = None,
                 ad_idshopee      :str   = None,
                 ad_taxashopee    :float = None,
                 qtdite           :int   = None,
                 qtdfin           :int   = None
                 ):
        self.db               = dbConfig()
        self.nunota           = nunota
        self.numnota          = numnota
        self.ad_mkp_id        = ad_mkp_id
        self.ad_mkp_numped    = ad_mkp_numped
        self.ad_mkp_codped    = ad_mkp_codped
        self.ad_mkp_origem    = ad_mkp_origem
        self.codemp           = codemp
        self.codcencus        = codcencus
        self.dtneg            = dtneg
        self.dtmov            = dtmov
        self.dtalter          = dtalter
        self.codempnegoc      = codempnegoc
        self.codparc          = codparc
        self.codtipoper       = codtipoper
        self.dhtipoper        = dhtipoper
        self.tipmov           = tipmov
        self.codtipvenda      = codtipvenda
        self.dhtipvenda       = dhtipvenda
        self.codvend          = codvend
        self.observacao       = observacao
        self.vlrdesctot       = vlrdesctot
        self.vlrdesctotitem   = vlrdesctotitem
        self.vlrfrete         = vlrfrete
        self.cif_fob          = cif_fob
        self.vlrnota          = vlrnota
        self.qtdvol           = qtdvol
        self.aliqicms         = aliqicms
        self.baseicms         = baseicms
        self.vlricms          = vlricms
        self.baseipi          = baseipi
        self.vlripi           = vlripi
        self.issretido        = issretido
        self.baseiss          = baseiss
        self.vlriss           = vlriss
        self.aprovado         = aprovado
        self.codusu           = codusu
        self.irfretido        = irfretido
        self.vlrirf           = vlrirf
        self.volume           = volume
        self.vlrsubst         = vlrsubst
        self.basesubstit      = basesubstit
        self.peso             = peso
        self.codnat           = codnat
        self.vlrfretecpl      = vlrfretecpl
        self.codusuinc        = codusuinc
        self.baseirf          = baseirf
        self.aliqirf          = aliqirf
        self.pesobruto        = pesobruto
        self.hrentsai         = hrentsai
        self.libconf          = libconf
        self.vlricmsdifaldest = vlricmsdifaldest
        self.vlricmsdifalrem  = vlricmsdifalrem
        self.vlricmsfcp       = vlricmsfcp
        self.codcidorigem     = codcidorigem
        self.codciddestino    = codciddestino
        self.codcidentrega    = codcidentrega
        self.coduforigem      = coduforigem
        self.codufdestino     = codufdestino
        self.codufentrega     = codufentrega
        self.classificms      = classificms
        self.vlricmsfcpint    = vlricmsfcpint
        self.vlrstfcpintant   = vlrstfcpintant
        self.statuscfe        = statuscfe
        self.histconfig       = histconfig
        self.ad_idshopee      = ad_idshopee
        self.ad_taxashopee    = ad_taxashopee
        self.qtdite           = qtdite
        self.qtdfin           = qtdfin
        self.itens            = []
        self.parcelas         = []

    async def decodificar(self,data:dict=None) -> bool:
        if data:
            try:
                self.nunota           = data["nunota"]
                self.numnota          = data["numnota"]
                self.ad_mkp_id        = data["ad_mkp_id"]
                self.ad_mkp_numped    = data["ad_mkp_numped"]
                self.ad_mkp_codped    = data["ad_mkp_codped"]
                self.ad_mkp_origem    = data["ad_mkp_origem"]
                self.codemp           = data["codemp"]
                self.codcencus        = data["codcencus"]
                self.dtneg            = data["dtneg"]
                self.dtmov            = data["dtmov"]
                self.dtalter          = data["dtalter"]
                self.codempnegoc      = data["codempnegoc"]
                self.codparc          = data["codparc"]
                self.codtipoper       = data["codtipoper"]
                self.dhtipoper        = data["dhtipoper"]
                self.tipmov           = data["tipmov"]
                self.codtipvenda      = data["codtipvenda"]
                self.dhtipvenda       = data["dhtipvenda"]
                self.codvend          = data["codvend"]
                self.observacao       = data["observacao"]
                self.vlrdesctot       = data["vlrdesctot"]
                self.vlrdesctotitem   = data["vlrdesctotitem"]
                self.vlrfrete         = data["vlrfrete"]
                self.cif_fob          = data["cif_fob"]
                self.vlrnota          = data["vlrnota"]
                self.qtdvol           = data["qtdvol"]
                self.baseicms         = data["baseicms"]
                self.vlricms          = data["vlricms"]
                self.baseipi          = data["baseipi"]
                self.vlripi           = data["vlripi"]
                self.issretido        = data["issretido"]
                self.baseiss          = data["baseiss"]
                self.vlriss           = data["vlriss"]
                self.aprovado         = data["aprovado"]
                self.codusu           = data["codusu"]
                self.irfretido        = data["irfretido"]
                self.vlrirf           = data["vlrirf"]
                self.volume           = data["volume"]
                self.vlrsubst         = data["vlrsubst"]
                self.basesubstit      = data["basesubstit"]
                self.peso             = data["peso"]
                self.codnat           = data["codnat"]
                self.vlrfretecpl      = data["vlrfretecpl"]
                self.codusuinc        = data["codusuinc"]
                self.baseirf          = data["baseirf"]
                self.aliqirf          = data["aliqirf"]
                self.pesobruto        = data["pesobruto"]
                self.hrentsai         = data["hrentsai"]
                self.libconf          = data["libconf"]
                self.vlricmsdifaldest = data["vlricmsdifaldest"]
                self.vlricmsdifalrem  = data["vlricmsdifalrem"]
                self.vlricmsfcp       = data["vlricmsfcp"]
                self.codcidorigem     = data["codcidorigem"]
                self.codciddestino    = data["codciddestino"]
                self.codcidentrega    = data["codcidentrega"]
                self.coduforigem      = data["coduforigem"]
                self.codufdestino     = data["codufdestino"]
                self.codufentrega     = data["codufentrega"]
                self.classificms      = data["classificms"]
                self.vlricmsfcpint    = data["vlricmsfcpint"]
                self.vlrstfcpintant   = data["vlrstfcpintant"]
                self.statuscfe        = data["statuscfe"]
                self.histconfig       = data["histconfig"]
                self.ad_idshopee      = data["ad_idshopee"]
                self.ad_taxashopee    = data["ad_taxashopee"]
                self.qtdite           = data["qtdite"]
                self.qtdfin           = data["qtdfin"]

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

    async def buscar(self,nunota:int=None) -> bool:
        file_path = configSankhya.PATH_SCRIPT_PEDIDO_CAB

        if not os.path.exists(file_path):
            logger.error("Script da TGFCAB não encontrado em %s",file_path)
            return False
        else:    
            with open(file_path, "r", encoding="utf-8") as f:
                query = f.read()
                
                try:
                    params = {"NUNOTA": nunota or self.nunota}
                    rows = await self.db.select(query=query,params=params)
                                        
                    if rows: return await self.decodificar(rows[0])
                    else:    return False
                except:
                    logger.error("Nº único do pedido %s",self.nunota)
                    return False

    async def buscar_parametros(self,**kwargs) -> dict: 
        file_path = configSankhya.PATH_PARAMS_PEDIDO
        empresa_padrao = configSankhya.CODEMP

        if not os.path.exists(file_path):
            raise FileNotFoundError("Script de parâmetros não encontrado em %s.",file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            query_tipoper, query_tipvenda, query_nunota, query_numnota, query_destino = f.read().splitlines()

        if query_tipoper and query_tipvenda and query_nunota and query_numnota and query_destino:
            try:
                dhalter_top     = await self.db.select(query=query_tipoper,params={"CODTIPOPER":kwargs['codtipoper']})
                dhalter_tpv     = await self.db.select(query=query_tipvenda,params={"CODTIPVENDA":kwargs['codtipvenda']})
                nunota_nextval  = await self.db.select(query=query_nunota)
                numnota_nextval = await self.db.select(query=query_numnota,params={"CODEMP":empresa_padrao})
                cid_destino     = await self.db.select(query=query_destino,params={"CIDADE":kwargs['ciddestino']})            

                res = {
                    "dhalter_top"     : dhalter_top[0]['dhalter'].strftime('%Y-%m-%d %H:%M:%S'),
                    "dhalter_tpv"     : dhalter_tpv[0]['dhalter'].strftime('%Y-%m-%d %H:%M:%S'),
                    "nunota_nextval"  : nunota_nextval[0]['nunota_next'],
                    "numnota_nextval" : numnota_nextval[0]['numnota_next'], 
                    "cid_destino"     : cid_destino[0]['codcid']
                }       

            except Exception as e:
                logger.error("Erro ao buscar parametros: %s",e)
                res = {}            
            finally:
                return res
        else:
            raise ValueError("Erro ao extrair scripts de consulta dos parâmetros.")

    async def preparacao(self,payload_olist:dict=None) -> tuple[bool,dict]:
        file_path = configSankhya.PATH_PARAMS_INS_PEDIDO_CAB

        if payload_olist:
            try:
                if not os.path.exists(file_path):
                    raise FileNotFoundError("Parametros de inserção de pedido não encontrados.")
                with open(file_path, "r", encoding="utf-8") as f:
                    ins_tgfcab = json.load(f)
            except Exception as e:
                print(f"Erro: {e}")    

            parametros = await self.buscar_parametros( codtipoper  = ins_tgfcab['CODTIPOPER'],
                                                       codtipvenda = ins_tgfcab['CODTIPVENDA'],
                                                       ciddestino  = payload_olist["cliente"]["endereco"]["municipio"]
                                                    )
            if parametros:
                valores_insert = {
                    "NUNOTA"           : parametros["nunota_nextval"],
                    "NUMNOTA"          : parametros["numnota_nextval"],
                    "AD_MKP_ID"        : int(payload_olist["id"]),
                    "AD_MKP_NUMPED"    : int(payload_olist["numeroPedido"]),
                    "AD_MKP_CODPED"    : payload_olist["ecommerce"]["numeroPedidoEcommerce"],
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
                    "AD_MKP_DESTINO"   : parametros["cid_destino"],
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
            print("Dados olist faltantes")
            return False, {}

    async def atualiza_seqs(self,**kwargs):

        seq1 = await self.db.dml(query='''
                        UPDATE TGFNUM
                        SET    ULTCOD = :P_PROXCOD
                        WHERE  ARQUIVO = :P_TABELA
                    ''',
                    params= {"P_PROXCOD":int(kwargs["nunota_nextval"]),
                             "P_TABELA":"TGFCAB"})

        seq2 = await self.db.dml(query='''
                        UPDATE TGFNUM
                        SET    ULTCOD = :P_PROXCOD
                        WHERE  ARQUIVO = :P_TABELA AND CODEMP = 31
                    ''',
                    params= {"P_PROXCOD":int(kwargs["numnota_nextval"]),
                             "P_TABELA":"PEDVEN"})        
        
        return True if seq1[0] and seq2[0] else False
    
    async def atualiza_impostos(self,nunota:int=None):

        res = await self.db.dml(query='''
                                UPDATE TGFCAB CAB
                                SET CAB.VLRICMS = (SELECT ROUND(SUM(ITE.VLRICMS),3)
                                                   FROM TGFITE ITE
                                                   WHERE ITE.NUNOTA = CAB.NUNOTA)
                                WHERE CAB.NUNOTA = :NUNOTA
                            ''',
                            params={"NUNOTA":nunota}
                          )

        return res[0]
    
    async def registrar(self, payload:dict=None) -> tuple[bool,int]:
        file_path = configSankhya.PATH_INSERT_PEDIDO_CAB
        it = item.Item()
        pr = parcela.Parcela()

        if not os.path.exists(file_path):
            logger.error("Script de insert da TGFCAB não encontrado em %s",file_path)
            return False, None
        else: 
            print("> Preparando os dados...")
            ack, data = await self.preparacao(payload_olist=payload)
            if ack:
                with open(file_path, "r", encoding="utf-8") as f:
                    query = f.read()
                nunota = data["NUNOTA"]
                numnota = data["NUMNOTA"]
                print("> Inserindo dados do cabeçalho...")
                ack_cab, rows_cab = await self.db.dml(query=query,params=data)
                if ack_cab:
                    print(f">> Cabeçalho do pedido {nunota} inserido com sucesso!")
                    logger.info("Cabeçalho do pedido %s inserido com sucesso.",nunota)
                    if payload.get("itens"):
                        print("> Lançando produtos no pedido...")
                        rows_itens = 0
                        seq_pedido = 0
                        uf_destino = payload["cliente"]["endereco"]["uf"]                        
                        for i, it_dict in enumerate(payload["itens"]): 
                            olItm = Item()
                            ack_kit, kit_dict = olItm.valida_kit(id=int(it_dict["produto"]["id"]),lcto_item=it_dict)
                            if ack_kit:
                                print(f">> Produto {it_dict["produto"]["id"]} é kit. Desmembrando...")
                                for kd in kit_dict:
                                    seq_pedido+=1
                                    ack_ite, rows_ite = await it.registrar( payload=kd,
                                                                            uf=uf_destino,
                                                                            nunota=nunota,
                                                                            sequencia=seq_pedido)                                
                                print(f">>> Kit desmembrado em {len(kit_dict)} produtos")
                            else:
                                seq_pedido+=1                          
                                ack_ite, rows_ite = await it.registrar( payload=it_dict,
                                                                        uf=uf_destino,
                                                                        nunota=nunota,
                                                                        sequencia=seq_pedido)
                            if ack_ite:
                                rows_itens+=rows_ite
                        if rows_itens == len(payload["itens"]):
                            print(f">> Todos os itens do pedido {nunota} inseridos com sucesso!")
                            await self.atualiza_impostos(nunota)
                            ack_itens = True
                        else:
                            ack_itens = False
                            print(f">>Nem todos os itens do pedido {nunota} inseridos. Verifique os logs.")
                            logger.error("Nem todos os itens do pedido %s inseridos.",nunota)        
                    else:
                        ack_itens = True
                        print(f">> Não tem itens no pedido!")

                    if payload["pagamento"].get("parcelas"):
                        print("> Lançando financeiro do pedido...")
                        rows_fins = 0
                        for i, fin_dict in enumerate(payload["pagamento"]["parcelas"]):
                            ack_fin, rows_fin = await pr.registrar(payload=fin_dict,
                                                                   nunota=nunota,
                                                                   numnota=numnota)
                            if ack_fin:
                                rows_fins+=rows_fin
                        if rows_fins == len(payload["pagamento"]["parcelas"]):
                            ack_fins = True
                            print(f">> Todos os financeiros do pedido {nunota} inseridos com sucesso!")
                        else:
                            ack_fins = False
                            print(f">>Nem todos os financeiros do pedido {nunota} inseridos. Verifique os logs.")                            
                    else:
                        ack_fins = True
                        print(f">> Não tem financeiro no pedido!")
                    if ack_cab and ack_itens and ack_fins:
                        await self.atualiza_seqs(nunota_nextval=nunota,numnota_nextval=numnota)
                        print(f"----------> Pedido {payload['numeroPedido']} importado com sucesso! Nº único {nunota}")
                        logger.info("Pedido %s importado com sucesso! Nº único %s",payload['numeroPedido'],nunota)
                        return True, nunota
                    else:
                        return False, None
                else:
                    print(f"Erro ao inserir cabeçalho do pedido {nunota}. Verifique os logs")
                    logger.error("Erro ao inserir cabeçalho do pedido %s.",nunota)        
                    return False, None
            else:
                print(f"Erro ao preparar dados para inserção do pedido {payload["numeroPedido"]}. Verifique os logs")
                logger.error("Erro ao preparar dados para inserção do pedido %s.",payload["numeroPedido"])        
                return False, None

    async def confirmar_nota(self, nunota:int=None):
        ack = await self.db.call(query='''call STP_CONFIRMANOTA2(:NUNOTA,'S',1)''',
                                 params={"NUNOTA":nunota})
        print(f"----------> Pedido {nunota} confirmado com sucesso!")
        logger.info("Pedido %s confirmado com sucesso!",nunota)        
        return ack
            