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
        self.db               = dbConfig()
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
            with open(file_path, "r", encoding="utf-8") as f:
                query = f.read()
                
                try:
                    params = {"NUNOTA": nunota or self.nunota}
                    rows = await self.db.select(query=query,params=params)
                                        
                    if rows:
                        return await self.decodificar(rows[0])
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

            dhalter_tpv = await self.db.select(query='''
                                                    SELECT MAX(DHALTER) DHALTER
                                                    FROM TGFTPV
                                                    WHERE CODTIPVENDA = :CODTIPVENDA
                                                ''',
                                                params={"CODTIPVENDA":kwargs['codtipvenda']})

            nunota_nextval = await self.db.select(query='''
                                                        SELECT ULTCOD + 1 nunota_next
                                                        FROM TGFNUM
                                                        WHERE ARQUIVO = 'TGFCAB'
                                                    ''')

            numnota_nextval = await self.db.select(query='''
                                                        SELECT ULTCOD + 1 numnota_next
                                                        FROM TGFNUM
                                                        WHERE ARQUIVO = 'PEDVEN' AND CODEMP = 31
                                                    ''')

            uf_destino = await self.db.select(query='''
                                                    SELECT CODUF
                                                    FROM TSIUFS
                                                    WHERE UF = :UF
                                            ''',
                                            params={"UF":kwargs['ufdestino']})

            uf_entrega = await self.db.select(query='''
                                                    SELECT CODUF
                                                    FROM TSIUFS
                                                    WHERE UF = :UF
                                            ''',
                                            params={"UF":kwargs['ufentrega']})

            cid_destino = await self.db.select(query='''
                                                    SELECT CODCID
                                                    FROM TSICID
                                                    WHERE (DESCRICAOCORREIO =    TRANSLATE(UPPER(:CIDADE), 'ÁÀÃÂÉÈÊÍÌÓÒÕÔÚÙÛÇ','AAAAEEEIIOOOOUUUC') OR
                                                           DESCRICAOCORREIO LIKE TRANSLATE(UPPER(:CIDADE), 'ÁÀÃÂÉÈÊÍÌÓÒÕÔÚÙÛÇ','AAAAEEEIIOOOOUUUC')||'%')
                                                ''',
                                                params={"CIDADE":kwargs['ciddestino']})

            cid_entrega = await self.db.select(query='''
                                                    SELECT CODCID
                                                    FROM TSICID
                                                    WHERE (DESCRICAOCORREIO = TRANSLATE(UPPER(:CIDADE), 'ÁÀÃÂÉÈÊÍÌÓÒÕÔÚÙÛÇ','AAAAEEEIIOOOOUUUC') OR
                                                           DESCRICAOCORREIO LIKE TRANSLATE(UPPER(:CIDADE), 'ÁÀÃÂÉÈÊÍÌÓÒÕÔÚÙÛÇ','AAAAEEEIIOOOOUUUC')||'%')
                                                ''',
                                                params={"CIDADE":kwargs['cidentrega']})
            

            res = {
                "dhalter_top":dhalter_top[0]['dhalter'].strftime('%Y-%m-%d %H:%M:%S'),
                "dhalter_tpv":dhalter_tpv[0]['dhalter'].strftime('%Y-%m-%d %H:%M:%S'),
                "nunota_nextval":nunota_nextval[0]['nunota_next'],
                "numnota_nextval":numnota_nextval[0]['numnota_next'],
                "uf_destino":uf_destino[0]['coduf'],
                "uf_entrega":uf_entrega[0]['coduf'],
                "cid_destino":cid_destino[0]['codcid'],
                "cid_entrega":cid_entrega[0]['codcid']
            }       

        except Exception as e:
            logger.error("Erro ao buscar parametros: %s",e)
            res = {}            
        finally:
            return res

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
                                                       ufdestino   = payload_olist["cliente"]["endereco"]["uf"],
                                                       ufentrega   = payload_olist["enderecoEntrega"]["uf"] or payload_olist["cliente"]["endereco"]["uf"],
                                                       ciddestino  = payload_olist["cliente"]["endereco"]["municipio"],
                                                       cidentrega  = payload_olist["enderecoEntrega"]["municipio"] or payload_olist["cliente"]["endereco"]["municipio"]
                                                    )
            if parametros:
                valores_insert = {
                    "nunota"           : parametros["nunota_nextval"],
                    "numnota"          : parametros["numnota_nextval"],
                    "ad_mkp_id"        : int(payload_olist["id"]),
                    "ad_mkp_numped"    : int(payload_olist["numeroPedido"]),
                    "ad_mkp_codped"    : payload_olist["ecommerce"]["numeroPedidoEcommerce"],
                    "ad_mkp_origem"    : int(payload_olist["ecommerce"]["id"]),
                    "codemp"           : ins_tgfcab["CODEMP"],
                    "codcencus"        : ins_tgfcab["CODCENCUS"],
                    "dtneg"            : payload_olist["data"],
                    "dtmov"            : payload_olist["data"],
                    "dtalter"          : payload_olist["data"],
                    "codempnegoc"      : ins_tgfcab["CODEMP"],
                    "codparc"          : ins_tgfcab["CODPARC"],
                    "codtipoper"       : ins_tgfcab["CODTIPOPER"],
                    "dhtipoper"        : parametros["dhalter_top"],
                    "tipmov"           : ins_tgfcab["TIPMOV"],
                    "codtipvenda"      : ins_tgfcab["CODTIPVENDA"],
                    "dhtipvenda"       : parametros["dhalter_tpv"],
                    "codvend"          : ins_tgfcab["CODVEND"],
                    "observacao"       : f"#{int(payload_olist["numeroPedido"])} - TESTE IMPORTAÇÃO API OLIST",
                    "vlrdesctot"       : float(payload_olist["valorDesconto"]),
                    "vlrdesctotitem"   : float(payload_olist["valorDesconto"]),
                    "vlrfrete"         : float(payload_olist["valorFrete"]),
                    "cif_fob"          : "C" if payload_olist["transportador"]["fretePorConta"] == "R" else "F" if payload_olist["transportador"]["fretePorConta"] == "D" else "",
                    "vlrnota"          : float(payload_olist["valorTotalPedido"]),
                    "qtdvol"           : 0,
                    "baseicms"         : float(payload_olist["valorTotalPedido"]),
                    "vlricms"          : float(payload_olist["valorTotalPedido"] * 0.12),
                    "baseipi"          : float(0),
                    "vlripi"           : float(0),
                    "issretido"        : "N",
                    "baseiss"          : float(0),
                    "vlriss"           : float(0),
                    "aprovado"         : ins_tgfcab["APROVADO"],
                    "codusu"           : ins_tgfcab["CODUSU"],
                    "irfretido"        : "N",
                    "vlrirf"           : float(0),
                    "volume"           : ins_tgfcab["VOLUME"],
                    "vlrsubst"         : float(0),
                    "basesubstit"      : float(0),
                    "peso"             : 0,
                    "codnat"           : ins_tgfcab["CODNAT"],
                    "vlrfretecpl"      : float(0),
                    "codusuinc"        : ins_tgfcab["CODUSU"],
                    "baseirf"          : float(0),
                    "aliqirf"          : float(0),
                    "pesobruto"        : 0,
                    "hrentsai"         : payload_olist["data"],
                    "libconf"          : "N",
                    "vlricmsdifaldest" : float(0),
                    "vlricmsdifalrem"  : float(0),
                    "vlricmsfcp"       : float(0),
                    "codcidorigem"     : ins_tgfcab["CODCID"],
                    "coduforigem"      : ins_tgfcab["CODUF"],
                    "codciddestino"    : parametros["cid_destino"],
                    "codufdestino"     : parametros["uf_destino"],
                    "codcidentrega"    : parametros["cid_entrega"],
                    "codufentrega"     : parametros["uf_entrega"],
                    "classificms"      : ins_tgfcab["CLASSIFICMS"],
                    "vlricmsfcpint"    : float(0),
                    "vlrstfcpintant"   : float(0),
                    "statuscfe"        : "N",
                    "histconfig"       : "S",
                    "ad_idshopee"      : payload_olist["ecommerce"]["numeroPedidoEcommerce"],
                    "ad_taxashopee"    : float(0) 
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
                print("> Inserindo dados do cabeçalho...")
                ack_cab, rows_cab = await self.db.dml(query=query,params=data)
                if ack_cab:
                    print(f">> Cabeçalho do pedido {data["nunota"]} inserido com sucesso!")
                    logger.info("Cabeçalho do pedido %s inserido com sucesso.",data["nunota"])
                    if payload.get("itens"):
                        print("> Lançando produtos no pedido...")
                        rows_itens = 0
                        seq_pedido = 0
                        for i, it_dict in enumerate(payload["itens"]):                            
                            #print(i)
                            #print(it_dict)
                            #print("")
                            olItm = Item()
                            ack_kit, kit_dict = olItm.valida_kit(id=int(it_dict["produto"]["id"]),lcto_item=it_dict)
                            #print(kit_dict)
                            if ack_kit:
                                print(f">> Produto {it_dict["produto"]["id"]} é kit. Desmembrando...")
                                for kd in kit_dict:
                                    seq_pedido+=1
                                    #print(kd)
                                    ack_ite, rows_ite = await it.registrar(payload=kd,
                                                                            nunota=data["nunota"],
                                                                            sequencia=seq_pedido)                                
                                print(f">>> Kit desmembrado em {len(kit_dict)} produtos")
                            else:
                                seq_pedido+=1
                                ack_ite, rows_ite = await it.registrar(payload=it_dict,
                                                                        nunota=data["nunota"],
                                                                        sequencia=seq_pedido+1)
                            if ack_ite:
                                rows_itens+=rows_ite
                        if rows_itens == len(payload["itens"]):
                            ack_itens = True
                            print(f">> Todos os itens do pedido {data["nunota"]} inseridos com sucesso!")
                        else:
                            ack_itens = False
                            print(f">>Nem todos os itens do pedido {data["nunota"]} inseridos. Verifique os logs.")
                    else:
                        ack_itens = True
                        print(f">> Não tem itens no pedido!")

                    if payload["pagamento"].get("parcelas"):
                        print("> Lançando financeiro do pedido...")
                        rows_fins = 0
                        for i, fin_dict in enumerate(payload["pagamento"]["parcelas"]):
                            #print(fin_dict)
                            ack_fin, rows_fin = await pr.registrar(payload=fin_dict,
                                                                   nunota=data["nunota"],
                                                                   numnota=data["numnota"]
                                                                   )
                            if ack_fin:
                                rows_fins+=rows_fin
                        if rows_fins == len(payload["pagamento"]["parcelas"]):
                            ack_fins = True
                            print(f">> Todos os financeiros do pedido {data["nunota"]} inseridos com sucesso!")
                        else:
                            ack_fins = False
                            print(f">>Nem todos os financeiros do pedido {data["nunota"]} inseridos. Verifique os logs.")                            
                    else:
                        ack_fins = True
                        print(f">> Não tem financeiro no pedido!")
                    
                    # return True, data["nunota"] if ack_cab and ack_itens and ack_fins else False, None
                    if ack_cab and ack_itens and ack_fins:
                        await self.atualiza_seqs(nunota_nextval=data["nunota"],numnota_nextval=data["numnota"])
                        print(f"----------> Pedido {payload['numeroPedido']} importado com sucesso! Nº único {data["nunota"]}")
                        return True, data["nunota"]
                    else:
                        return False, None
                else:
                    print(f"Erro ao inserir cabeçalho do pedido {data["nunota"]}. Verifique os logs")
                    logger.error("Erro ao inserir cabeçalho do pedido %s.",data["nunota"])        
                    return False, None
            else:
                print(f"Erro preparar dados para inserção do pedido {payload["numeroPedido"]}. Verifique os logs")
                logger.error("Erro preparar dados para inserção do pedido %s.",payload["numeroPedido"])        
                return False, None

                


            