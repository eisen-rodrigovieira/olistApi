import logging
import requests
from src.olist.connect    import Connect
from src.olist.pedido     import parcela, item
from params               import config, configOlist
from src.utils.validaPath import validaPath
from datetime             import datetime, timedelta

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Pedido:

    def __init__(self):
        self.con                              = Connect()  
        self.valida_path                      = validaPath()                 
        self.req_sleep                        = config.REQ_TIME_SLEEP  
        self.endpoint                         = config.API_URL+config.ENDPOINT_PEDIDOS        
        self.situacao_aprovado                = configOlist.SITUACAO_PEDIDO_APROVADO
        self.situacao_preparando_envio        = configOlist.SITUACAO_PEDIDO_PREP_ENVIO
        self.dataPrevista                     = None
        self.dataEnvio                        = None
        self.observacoes                      = None
        self.observacoesInternas              = None
        self.situacao                         = None
        self.data                             = None
        self.dataEntrega                      = None
        self.numeroOrdemCompra                = None
        self.valorDesconto                    = None
        self.valorFrete                       = None
        self.valorOutrasDespesas              = None
        self.id                               = None
        self.numeroPedido                     = None
        self.idNotaFiscal                     = None
        self.dataFaturamento                  = None
        self.valorTotalProdutos               = None
        self.valorTotalPedido                 = None
        self.listaPreco_id                    = None
        self.listaPreco_nome                  = None
        self.listaPreco_acrescimoDesconto     = None
        self.cliente_nome                     = None
        self.cliente_codigo                   = None
        self.cliente_fantasia                 = None
        self.cliente_tipoPessoa               = None
        self.cliente_cpfCnpj                  = None
        self.cliente_inscricaoEstadual        = None
        self.cliente_rg                       = None
        self.cliente_telefone                 = None
        self.cliente_celular                  = None
        self.cliente_email                    = None
        self.cliente_endereco_endereco        = None
        self.cliente_endereco_numero          = None
        self.cliente_endereco_complemento     = None
        self.cliente_endereco_bairro          = None
        self.cliente_endereco_municipio       = None
        self.cliente_endereco_cep             = None
        self.cliente_endereco_uf              = None
        self.cliente_endereco_pais            = None
        self.cliente_id                       = None
        self.enderecoEntrega_endereco         = None
        self.enderecoEntrega_numero           = None
        self.enderecoEntrega_complemento      = None
        self.enderecoEntrega_bairro           = None
        self.enderecoEntrega_municipio        = None
        self.enderecoEntrega_cep              = None
        self.enderecoEntrega_uf               = None
        self.enderecoEntrega_pais             = None
        self.enderecoEntrega_nomeDestinatario = None
        self.enderecoEntrega_cpfCnpj          = None
        self.enderecoEntrega_tipoPessoa       = None
        self.ecommerce_id                     = None
        self.ecommerce_nome                   = None
        self.ecommerce_numeroPedidoEcommerce  = None
        self.ecommerce_numeroPedidoCanalVenda = None
        self.ecommerce_canalVenda             = None
        self.transportador_id                 = None
        self.transportador_nome               = None
        self.transportador_fretePorConta      = None
        self.transportador_formaEnvio_id      = None
        self.transportador_formaEnvio_nome    = None
        self.transportador_formaFrete_id      = None
        self.transportador_formaFrete_nome    = None
        self.transportador_codigoRastreamento = None
        self.transportador_urlRastreamento    = None
        self.deposito_id                      = None
        self.deposito_nome                    = None
        self.vendedor_id                      = None
        self.vendedor_nome                    = None
        self.naturezaOperacao_id              = None
        self.naturezaOperacao_nome            = None
        self.intermediador_id                 = None
        self.intermediador_nome               = None
        self.intermediador_cnpj               = None
        self.pagamento_formaPagamento_id      = None
        self.pagamento_formaPagamento_nome    = None
        self.pagamento_meioPagamento_id       = None
        self.pagamento_meioPagamento_nome     = None
        self.pagamento_condicaoPagamento      = None
        self.pagamento_parcelas               = []
        self.itens                            = []
        self.acao                             = None
        
    def decodificar(self,payload:dict=None) -> bool:
      
        if payload:
            try:
                self.dataPrevista                = payload["dataPrevista"]
                self.dataEnvio                   = payload["dataEnvio"]
                self.observacoes                 = payload["observacoes"]
                self.observacoesInternas         = payload["observacoesInternas"]
                self.situacao                    = payload["situacao"]
                self.data                        = payload["data"]
                self.dataEntrega                 = payload["dataEntrega"]
                self.numeroOrdemCompra           = payload["numeroOrdemCompra"]
                self.valorDesconto               = payload["valorDesconto"]
                self.valorFrete                  = payload["valorFrete"]
                self.valorOutrasDespesas         = payload["valorOutrasDespesas"]
                self.id                          = payload["id"]
                self.numeroPedido                = payload["numeroPedido"]
                self.idNotaFiscal                = payload["idNotaFiscal"]
                self.dataFaturamento             = payload["dataFaturamento"]
                self.valorTotalProdutos          = payload["valorTotalProdutos"]
                self.valorTotalPedido            = payload["valorTotalPedido"]

                if payload.get("listaPreco"):
                    self.listaPreco_id                  = payload["listaPreco"]["id"]
                    self.listaPreco_nome                = payload["listaPreco"]["nome"]
                    self.listaPreco_acrescimoDesconto   = payload["listaPreco"]["acrescimoDesconto"]
                else:
                    self.listaPreco_id = self.listaPreco_nome = self.listaPreco_acrescimoDesconto = None

                if payload.get("cliente"):
                    self.cliente_nome                   = payload["cliente"]["nome"]
                    self.cliente_codigo                 = payload["cliente"]["codigo"]
                    self.cliente_fantasia               = payload["cliente"]["fantasia"]
                    self.cliente_tipoPessoa             = payload["cliente"]["tipoPessoa"]
                    self.cliente_cpfCnpj                = payload["cliente"]["cpfCnpj"]
                    self.cliente_inscricaoEstadual      = payload["cliente"]["inscricaoEstadual"]
                    self.cliente_rg                     = payload["cliente"]["rg"]
                    self.cliente_telefone               = payload["cliente"]["telefone"]
                    self.cliente_celular                = payload["cliente"]["celular"]
                    self.cliente_email                  = payload["cliente"]["email"]
                    self.cliente_id                     = payload["cliente"]["id"]

                    if payload["cliente"].get("endereco"):
                        self.cliente_endereco_endereco      = payload["cliente"]["endereco"]["endereco"]
                        self.cliente_endereco_numero        = payload["cliente"]["endereco"]["numero"]
                        self.cliente_endereco_complemento   = payload["cliente"]["endereco"]["complemento"]
                        self.cliente_endereco_bairro        = payload["cliente"]["endereco"]["bairro"]
                        self.cliente_endereco_municipio     = payload["cliente"]["endereco"]["municipio"]
                        self.cliente_endereco_cep           = payload["cliente"]["endereco"]["cep"]
                        self.cliente_endereco_uf            = payload["cliente"]["endereco"]["uf"]
                        self.cliente_endereco_pais          = payload["cliente"]["endereco"]["pais"]

                if payload.get("enderecoEntrega"):
                    self.enderecoEntrega_endereco           = payload["enderecoEntrega"]["endereco"]
                    self.enderecoEntrega_numero             = payload["enderecoEntrega"]["numero"]
                    self.enderecoEntrega_complemento        = payload["enderecoEntrega"]["complemento"]
                    self.enderecoEntrega_bairro             = payload["enderecoEntrega"]["bairro"]
                    self.enderecoEntrega_municipio          = payload["enderecoEntrega"]["municipio"]
                    self.enderecoEntrega_cep                = payload["enderecoEntrega"]["cep"]
                    self.enderecoEntrega_uf                 = payload["enderecoEntrega"]["uf"]
                    self.enderecoEntrega_pais               = payload["enderecoEntrega"]["pais"]
                    self.enderecoEntrega_nomeDestinatario   = payload["enderecoEntrega"]["nomeDestinatario"]
                    self.enderecoEntrega_cpfCnpj            = payload["enderecoEntrega"]["cpfCnpj"]
                    self.enderecoEntrega_tipoPessoa         = payload["enderecoEntrega"]["tipoPessoa"]

                if payload.get("ecommerce"):
                    self.ecommerce_id                       = payload["ecommerce"]["id"]
                    self.ecommerce_nome                     = payload["ecommerce"]["nome"]
                    self.ecommerce_numeroPedidoEcommerce    = payload["ecommerce"]["numeroPedidoEcommerce"]
                    self.ecommerce_numeroPedidoCanalVenda   = payload["ecommerce"]["numeroPedidoCanalVenda"]
                    self.ecommerce_canalVenda               = payload["ecommerce"]["canalVenda"]

                if payload.get("transportador"):
                    self.transportador_id                   = payload["transportador"]["id"]
                    self.transportador_nome                 = payload["transportador"]["nome"]
                    self.transportador_fretePorConta        = payload["transportador"]["fretePorConta"]
                    self.transportador_codigoRastreamento   = payload["transportador"]["codigoRastreamento"]
                    self.transportador_urlRastreamento      = payload["transportador"]["urlRastreamento"]

                    if payload["transportador"].get("formaEnvio"):
                        self.transportador_formaEnvio_id    = payload["transportador"]["formaEnvio"]["id"]
                        self.transportador_formaEnvio_nome  = payload["transportador"]["formaEnvio"]["nome"]
                    else:
                        self.transportador_formaEnvio_id = self.transportador_formaEnvio_nome = None                        

                    if payload["transportador"].get("formaFrete"):
                        self.transportador_formaFrete_id    = payload["transportador"]["formaFrete"]["id"]
                        self.transportador_formaFrete_nome  = payload["transportador"]["formaFrete"]["nome"]
                    else:
                        self.transportador_formaFrete_id = self.transportador_formaFrete_nome = None

                if payload.get("deposito"):
                    self.deposito_id                        = payload["deposito"]["id"]
                    self.deposito_nome                      = payload["deposito"]["nome"]
                else:
                    self.deposito_id = self.deposito_nome = None

                if payload.get("vendedor"):
                    self.vendedor_id                        = payload["vendedor"]["id"]
                    self.vendedor_nome                      = payload["vendedor"]["nome"]
                else:
                    self.vendedor_id = self.vendedor_nome = None                    

                if payload.get("naturezaOperacao"):
                    self.naturezaOperacao_id                = payload["naturezaOperacao"]["id"]
                    self.naturezaOperacao_nome              = payload["naturezaOperacao"]["nome"]
                else:
                    self.naturezaOperacao_id = self.naturezaOperacao_nome = None                       

                if payload.get("intermediador"):
                    self.intermediador_id                   = payload["intermediador"]["id"]
                    self.intermediador_nome                 = payload["intermediador"]["nome"]
                    self.intermediador_cnpj                 = payload["intermediador"]["cnpj"]
                else:
                    self.intermediador_id = self.intermediador_nome = self.intermediador_cnpj = None                    

                if payload.get("pagamento"):
                    self.pagamento_condicaoPagamento         = payload["pagamento"]["condicaoPagamento"]

                    if payload["pagamento"].get("formaPagamento"):
                        self.pagamento_formaPagamento_id     = payload["pagamento"]["formaPagamento"]["id"]
                        self.pagamento_formaPagamento_nome   = payload["pagamento"]["formaPagamento"]["nome"]
                    else:
                        self.pagamento_formaPagamento_id = self.pagamento_formaPagamento_nome = None                            

                    if payload["pagamento"].get("meioPagamento"):
                        self.pagamento_meioPagamento_id       = payload["pagamento"]["meioPagamento"]["id"]
                        self.pagamento_meioPagamento_nome     = payload["pagamento"]["meioPagamento"]["nome"]
                    else:
                        self.pagamento_meioPagamento_id = self.pagamento_meioPagamento_nome = None

                for p in payload["pagamento"]["parcelas"]:
                    pa = parcela.Parcela()
                    pa.decodificar(p)
                    self.pagamento_parcelas.append(pa)
                
                for i in payload["itens"]:
                    it = item.Item()
                    it.decodificar(i)
                    self.itens.append(it)

                return True

            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    async def encodificar(self) -> dict:
        obj = {}
        data = {}
        file_path = configOlist.PATH_OBJECT_PEDIDO
        obj = await self.valida_path.validar(path=file_path,mode='r',method='json')      

        if self.acao == 'get':
            try:
                data = obj[self.acao]
                data["dataPrevista"]                        = self.dataPrevista
                data["dataEnvio"]                           = self.dataEnvio
                data["observacoes"]                         = self.observacoes
                data["observacoesInternas"]                 = self.observacoesInternas
                data["situacao"]                            = self.situacao
                data["data"]                                = self.data
                data["dataEntrega"]                         = self.dataEntrega
                data["numeroOrdemCompra"]                   = self.numeroOrdemCompra
                data["valorDesconto"]                       = self.valorDesconto
                data["valorFrete"]                          = self.valorFrete
                data["valorOutrasDespesas"]                 = self.valorOutrasDespesas
                data["id"]                                  = self.id
                data["numeroPedido"]                        = self.numeroPedido
                data["idNotaFiscal"]                        = self.idNotaFiscal
                data["dataFaturamento"]                     = self.dataFaturamento
                data["valorTotalProdutos"]                  = self.valorTotalProdutos
                data["valorTotalPedido"]                    = self.valorTotalPedido
                data["listaPreco"]["id"]                    = self.listaPreco_id
                data["listaPreco"]["nome"]                  = self.listaPreco_nome
                data["listaPreco"]["acrescimoDesconto"]     = self.listaPreco_acrescimoDesconto
                data["cliente"]["nome"]                     = self.cliente_nome
                data["cliente"]["codigo"]                   = self.cliente_codigo
                data["cliente"]["fantasia"]                 = self.cliente_fantasia
                data["cliente"]["tipoPessoa"]               = self.cliente_tipoPessoa
                data["cliente"]["cpfCnpj"]                  = self.cliente_cpfCnpj
                data["cliente"]["inscricaoEstadual"]        = self.cliente_inscricaoEstadual
                data["cliente"]["rg"]                       = self.cliente_rg
                data["cliente"]["telefone"]                 = self.cliente_telefone
                data["cliente"]["celular"]                  = self.cliente_celular
                data["cliente"]["email"]                    = self.cliente_email
                data["cliente"]["endereco"]["endereco"]     = self.cliente_endereco_endereco
                data["cliente"]["endereco"]["numero"]       = self.cliente_endereco_numero
                data["cliente"]["endereco"]["complemento"]  = self.cliente_endereco_complemento
                data["cliente"]["endereco"]["bairro"]       = self.cliente_endereco_bairro
                data["cliente"]["endereco"]["municipio"]    = self.cliente_endereco_municipio
                data["cliente"]["endereco"]["cep"]          = self.cliente_endereco_cep
                data["cliente"]["endereco"]["uf"]           = self.cliente_endereco_uf
                data["cliente"]["endereco"]["pais"]         = self.cliente_endereco_pais
                data["cliente"]["id"]                       = self.cliente_id
                data["enderecoEntrega"]["endereco"]         = self.enderecoEntrega_endereco
                data["enderecoEntrega"]["numero"]           = self.enderecoEntrega_numero
                data["enderecoEntrega"]["complemento"]      = self.enderecoEntrega_complemento
                data["enderecoEntrega"]["bairro"]           = self.enderecoEntrega_bairro
                data["enderecoEntrega"]["municipio"]        = self.enderecoEntrega_municipio
                data["enderecoEntrega"]["cep"]              = self.enderecoEntrega_cep
                data["enderecoEntrega"]["uf"]               = self.enderecoEntrega_uf
                data["enderecoEntrega"]["pais"]             = self.enderecoEntrega_pais
                data["enderecoEntrega"]["nomeDestinatario"] = self.enderecoEntrega_nomeDestinatario
                data["enderecoEntrega"]["cpfCnpj"]          = self.enderecoEntrega_cpfCnpj
                data["enderecoEntrega"]["tipoPessoa"]       = self.enderecoEntrega_tipoPessoa
                data["ecommerce"]["id"]                     = self.ecommerce_id
                data["ecommerce"]["nome"]                   = self.ecommerce_nome
                data["ecommerce"]["numeroPedidoEcommerce"]  = self.ecommerce_numeroPedidoEcommerce
                data["ecommerce"]["numeroPedidoCanalVenda"] = self.ecommerce_numeroPedidoCanalVenda
                data["ecommerce"]["canalVenda"]             = self.ecommerce_canalVenda
                data["transportador"]["id"]                 = self.transportador_id
                data["transportador"]["nome"]               = self.transportador_nome
                data["transportador"]["fretePorConta"]      = self.transportador_fretePorConta
                data["transportador"]["formaEnvio"]["id"]   = self.transportador_formaEnvio_id
                data["transportador"]["formaEnvio"]["nome"] = self.transportador_formaEnvio_nome
                data["transportador"]["formaFrete"]["id"]   = self.transportador_formaFrete_id
                data["transportador"]["formaFrete"]["nome"] = self.transportador_formaFrete_nome
                data["transportador"]["codigoRastreamento"] = self.transportador_codigoRastreamento
                data["transportador"]["urlRastreamento"]    = self.transportador_urlRastreamento
                data["deposito"]["id"]                      = self.deposito_id
                data["deposito"]["nome"]                    = self.deposito_nome
                data["vendedor"]["id"]                      = self.vendedor_id
                data["vendedor"]["nome"]                    = self.vendedor_nome
                data["naturezaOperacao"]["id"]              = self.naturezaOperacao_id
                data["naturezaOperacao"]["nome"]            = self.naturezaOperacao_nome
                data["intermediador"]["id"]                 = self.intermediador_id
                data["intermediador"]["nome"]               = self.intermediador_nome
                data["intermediador"]["cnpj"]               = self.intermediador_cnpj
                data["pagamento"]["formaPagamento"]["id"]   = self.pagamento_formaPagamento_id
                data["pagamento"]["formaPagamento"]["nome"] = self.pagamento_formaPagamento_nome
                data["pagamento"]["meioPagamento"]["id"]    = self.pagamento_meioPagamento_id
                data["pagamento"]["meioPagamento"]["nome"]  = self.pagamento_meioPagamento_nome
                data["pagamento"]["condicaoPagamento"]      = self.pagamento_condicaoPagamento      
                
                itens_list = list()
                for it in self.itens:
                    itens_list.append(await it.encodificar(self.acao))
                
                parcelas_list = list()
                for pr in self.pagamento_parcelas:
                    parcelas_list.append(await pr.encodificar(self.acao))

                data["itens"]                 = itens_list
                data["pagamento"]["parcelas"] = parcelas_list
                
                return data               
            except Exception as e:
                logger.error("Erro ao formatar dict produto: %s",e)
                return {"status":"Erro"}                   
        elif self.acao in ['put','del']:
            pass
        elif self.acao in 'post':
            pass
        else:
            return {"status":"Ação não configurada"} 

    async def buscar(self, id:int=None) -> bool:        
        url = self.endpoint+f"/{id or self.id}"
        try:
            token = await self.con.get_latest_valid_token_or_refresh()
            if url and token:                
                get_pedido = requests.get(
                    url=url,
                    headers={
                        "Authorization":f"Bearer {token}",
                        "Content-Type":"application/json",
                        "Accept":"application/json"
                    }
                )
                if get_pedido.status_code == 200:
                        if self.decodificar(get_pedido.json()):
                            self.acao = 'get'
                            return True
                        else:
                            logger.error("Erro ao decodificar pedido %s", self.id)
                            return False
                else:                      
                    logger.error("Erro %s: %s cod %s", get_pedido.status_code, get_pedido.json().get("mensagem","Erro desconhecido"), self.id)
                    return False                    
            else:
                logger.warning("Endpoint da API ou token de acesso faltantes")
                return False                    
        except Exception as e:
            logger.error("Erro relacionado ao token de acesso. %s",e)
            return False     

    async def buscar_lista(self,situacao:str='A',atual:bool=True) -> tuple[bool, list]:
        """
        Busca pedidos na API de acordo com a situação informada.

        Esta função realiza uma requisição GET para a API e retorna uma lista de pedidos
        com base no código de situação correspondente ao parâmetro fornecido.

        Parâmetros:
            situacao (str): Código da situação para filtrar os pedidos:
                Valores aceitos:
                    - A: Aprovados (padrão)
                    - S: Em separação
                    - F: Faturado
            atual (bool): Se deve considerar somente os pedidos com data D-1 ou todos

        Retorna:
            tuple:
                - bool: Indica se a requisição foi bem-sucedida.
                - list: Lista de pedidos (lista de IDs) ou lista vazia em caso de falha.

        Exceções:
            Retorna (False, []) e registra logs em caso de erro de token, conexão ou resposta da API.
        """
        match situacao:
            case "A":
                cod_situacao = 3
            case "S":
                cod_situacao = 4
            case "F":
                cod_situacao = 1
            case _:  # Default case
                cod_situacao = None

        dataInicial = datetime.strftime(datetime.today()-timedelta(days=1),'%Y-%m-%d') if atual else ''
        url = self.endpoint+f"?situacao={cod_situacao}&dataInicial={dataInicial}"
        try:
            token = await self.con.get_latest_valid_token_or_refresh()
            if url and token:                
                get_pedido = requests.get(
                    url=url,
                    headers={
                        "Authorization":f"Bearer {token}",
                        "Content-Type":"application/json",
                        "Accept":"application/json"
                    }
                )
                if get_pedido.status_code == 200:
                    pedidos = [p["id"] for p in get_pedido.json()['itens']]
                    pedidos.reverse()
                    return True, pedidos
                else:                      
                    logger.error("Erro %s ao buscar lista de pedidos: %s cod %s", get_pedido.status_code, get_pedido.json().get("mensagem","Erro desconhecido"), self.id)
                    return False, []
            else:
                logger.warning("Endpoint da API ou token de acesso faltantes")
                return False, []
        except Exception as e:
            logger.error("Erro relacionado ao token de acesso. %s",e)
            return False, []

