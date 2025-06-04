import os
import time
import json
import logging
import requests
from src.olist.connect import Connect
from src.olist.pedido  import parcela, item, pedido
from params            import config, configOlist

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Pedido:

    def __init__(
        self,
        dataPrevista: str = None,
        dataEnvio: str = None,
        observacoes: str = None,
        observacoesInternas: str = None,
        situacao: int = None,
        data: str = None,
        dataEntrega: str = None,
        numeroOrdemCompra: str = None,
        valorDesconto: float = None,
        valorFrete: float = None,
        valorOutrasDespesas: float = None,
        id: int = None,
        numeroPedido: int = None,
        idNotaFiscal: int = None,
        dataFaturamento: str = None,
        valorTotalProdutos: float = None,
        valorTotalPedido: float = None,
        listaPreco_id: int = None,
        listaPreco_nome: str = None,
        listaPreco_acrescimoDesconto: float = None,
        cliente_nome: str = None,
        cliente_codigo: str = None,
        cliente_fantasia: str = None,
        cliente_tipoPessoa: str = None,
        cliente_cpfCnpj: str = None,
        cliente_inscricaoEstadual: str = None,
        cliente_rg: str = None,
        cliente_telefone: str = None,
        cliente_celular: str = None,
        cliente_email: str = None,
        cliente_endereco_endereco: str = None,
        cliente_endereco_numero: str = None,
        cliente_endereco_complemento: str = None,
        cliente_endereco_bairro: str = None,
        cliente_endereco_municipio: str = None,
        cliente_endereco_cep: str = None,
        cliente_endereco_uf: str = None,
        cliente_endereco_pais: str = None,
        cliente_id: int = None,
        enderecoEntrega_endereco: str = None,
        enderecoEntrega_numero: str = None,
        enderecoEntrega_complemento: str = None,
        enderecoEntrega_bairro: str = None,
        enderecoEntrega_municipio: str = None,
        enderecoEntrega_cep: str = None,
        enderecoEntrega_uf: str = None,
        enderecoEntrega_pais: str = None,
        enderecoEntrega_nomeDestinatario: str = None,
        enderecoEntrega_cpfCnpj: str = None,
        enderecoEntrega_tipoPessoa: str = None,
        ecommerce_id: int = None,
        ecommerce_nome: str = None,
        ecommerce_numeroPedidoEcommerce: str = None,
        ecommerce_numeroPedidoCanalVenda: str = None,
        ecommerce_canalVenda: str = None,
        transportador_id: int = None,
        transportador_nome: str = None,
        transportador_fretePorConta: str = None,
        transportador_formaEnvio_id: int = None,
        transportador_formaEnvio_nome: str = None,
        transportador_formaFrete_id: int = None,
        transportador_formaFrete_nome: str = None,
        transportador_codigoRastreamento: str = None,
        transportador_urlRastreamento: str = None,
        deposito_id: int = None,
        deposito_nome: str = None,
        vendedor_id: int = None,
        vendedor_nome: str = None,
        naturezaOperacao_id: int = None,
        naturezaOperacao_nome: str = None,
        intermediador_id: int = None,
        intermediador_nome: str = None,
        intermediador_cnpj: str = None,
        pagamento_formaPagamento_id: int = None,
        pagamento_formaPagamento_nome: str = None,
        pagamento_meioPagamento_id: int = None,
        pagamento_meioPagamento_nome: str = None,
        pagamento_condicaoPagamento: str = None
    ):
        self.con                           = Connect()  
        self.req_sleep                     = config.REQ_TIME_SLEEP  
        self.endpoint                      = config.API_URL+config.ENDPOINT_PEDIDOS        
        self.situacao_incial               = configOlist.SITUACAO_INICIAL
        self.dataPrevista = dataPrevista
        self.dataEnvio = dataEnvio
        self.observacoes = observacoes
        self.observacoesInternas = observacoesInternas
        self.situacao = situacao
        self.data = data
        self.dataEntrega = dataEntrega
        self.numeroOrdemCompra = numeroOrdemCompra
        self.valorDesconto = valorDesconto
        self.valorFrete = valorFrete
        self.valorOutrasDespesas = valorOutrasDespesas
        self.id = id
        self.numeroPedido = numeroPedido
        self.idNotaFiscal = idNotaFiscal
        self.dataFaturamento = dataFaturamento
        self.valorTotalProdutos = valorTotalProdutos
        self.valorTotalPedido = valorTotalPedido

        self.listaPreco_id = listaPreco_id
        self.listaPreco_nome = listaPreco_nome
        self.listaPreco_acrescimoDesconto = listaPreco_acrescimoDesconto

        self.cliente_nome = cliente_nome
        self.cliente_codigo = cliente_codigo
        self.cliente_fantasia = cliente_fantasia
        self.cliente_tipoPessoa = cliente_tipoPessoa
        self.cliente_cpfCnpj = cliente_cpfCnpj
        self.cliente_inscricaoEstadual = cliente_inscricaoEstadual
        self.cliente_rg = cliente_rg
        self.cliente_telefone = cliente_telefone
        self.cliente_celular = cliente_celular
        self.cliente_email = cliente_email
        self.cliente_endereco_endereco = cliente_endereco_endereco
        self.cliente_endereco_numero = cliente_endereco_numero
        self.cliente_endereco_complemento = cliente_endereco_complemento
        self.cliente_endereco_bairro = cliente_endereco_bairro
        self.cliente_endereco_municipio = cliente_endereco_municipio
        self.cliente_endereco_cep = cliente_endereco_cep
        self.cliente_endereco_uf = cliente_endereco_uf
        self.cliente_endereco_pais = cliente_endereco_pais
        self.cliente_id = cliente_id

        self.enderecoEntrega_endereco = enderecoEntrega_endereco
        self.enderecoEntrega_numero = enderecoEntrega_numero
        self.enderecoEntrega_complemento = enderecoEntrega_complemento
        self.enderecoEntrega_bairro = enderecoEntrega_bairro
        self.enderecoEntrega_municipio = enderecoEntrega_municipio
        self.enderecoEntrega_cep = enderecoEntrega_cep
        self.enderecoEntrega_uf = enderecoEntrega_uf
        self.enderecoEntrega_pais = enderecoEntrega_pais
        self.enderecoEntrega_nomeDestinatario = enderecoEntrega_nomeDestinatario
        self.enderecoEntrega_cpfCnpj = enderecoEntrega_cpfCnpj
        self.enderecoEntrega_tipoPessoa = enderecoEntrega_tipoPessoa

        self.ecommerce_id = ecommerce_id
        self.ecommerce_nome = ecommerce_nome
        self.ecommerce_numeroPedidoEcommerce = ecommerce_numeroPedidoEcommerce
        self.ecommerce_numeroPedidoCanalVenda = ecommerce_numeroPedidoCanalVenda
        self.ecommerce_canalVenda = ecommerce_canalVenda

        self.transportador_id = transportador_id
        self.transportador_nome = transportador_nome
        self.transportador_fretePorConta = transportador_fretePorConta
        self.transportador_formaEnvio_id = transportador_formaEnvio_id
        self.transportador_formaEnvio_nome = transportador_formaEnvio_nome
        self.transportador_formaFrete_id = transportador_formaFrete_id
        self.transportador_formaFrete_nome = transportador_formaFrete_nome
        self.transportador_codigoRastreamento = transportador_codigoRastreamento
        self.transportador_urlRastreamento = transportador_urlRastreamento

        self.deposito_id = deposito_id
        self.deposito_nome = deposito_nome

        self.vendedor_id = vendedor_id
        self.vendedor_nome = vendedor_nome

        self.naturezaOperacao_id = naturezaOperacao_id
        self.naturezaOperacao_nome = naturezaOperacao_nome

        self.intermediador_id = intermediador_id
        self.intermediador_nome = intermediador_nome
        self.intermediador_cnpj = intermediador_cnpj

        self.pagamento_formaPagamento_id = pagamento_formaPagamento_id
        self.pagamento_formaPagamento_nome = pagamento_formaPagamento_nome
        self.pagamento_meioPagamento_id = pagamento_meioPagamento_id
        self.pagamento_meioPagamento_nome = pagamento_meioPagamento_nome
        self.pagamento_condicaoPagamento = pagamento_condicaoPagamento

        self.pagamento_parcelas = []
        self.itens = []

        self.acao                          = None
        
    def decodificar(self,payload:dict=None) -> bool:
        
        if payload:
            #print(payload)
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
        if not os.path.exists(file_path):
            logger.error("Objeto do pedido não encontrado em %s",file_path)
            return {"status":"Erro"}
        else:    
            with open(file_path, "r", encoding="utf-8") as f:
                obj = json.load(f)        

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
                    itens_list.append(it.encodificar(self.acao))
                
                parcelas_list = list()
                for pr in self.pagamento_parcelas:
                    parcelas_list.append(pr.encodificar(self.acao))

                data["itens"]                 = itens_list
                data["pagamento"]["parcelas"] = parcelas_list
                
                return data               
            except Exception as e:
                logger.error("Erro ao formatar dict produto: %s",e)
                return {"status":"Erro"} 
                   
        elif self.acao in ['put','del']:
            try:
                data = obj['put']
                data["sku"]                                       = self.sku                       
                data["descricao"]                                 = self.descricao                 
                data["descricaoComplementar"]                     = self.descricaoComplementar     
                data["situacao"]                                  = self.situacao
                data["unidade"]                                   = self.unidade                   
                data["unidadePorCaixa"]                           = str(self.unidadePorCaixa)
                data["ncm"]                                       = self.ncm                       
                data["gtin"]                                      = self.gtin                      
                data["origem"]                                    = int(self.origem)
                data["codigoEspecificadorSubstituicaoTributaria"] = self.cest                      
                data["garantia"]                                  = self.garantia                  
                data["observacoes"]                               = self.observacoes               
                data["marca"]["id"]                               = self.marca_id                  
                data["categoria"]["id"]                           = int(self.categoria_id)
                data["precos"]["preco"]                           = self.preco                     
                data["precos"]["precoPromocional"]                = self.precoPromocional          
                data["precos"]["precoCusto"]                      = self.precoCusto                
                data["dimensoes"]["embalagem"]["id"]              = self.dimensoes_embalagem_id    
                data["dimensoes"]["embalagem"]["tipo"]            = self.dimensoes_embalagem_tipo  
                data["dimensoes"]["largura"]                      = self.dimensoes_largura         
                data["dimensoes"]["altura"]                       = self.dimensoes_altura          
                data["dimensoes"]["comprimento"]                  = self.dimensoes_comprimento     
                data["dimensoes"]["diametro"]                     = self.dimensoes_diametro        
                data["dimensoes"]["pesoLiquido"]                  = self.dimensoes_pesoLiquido     
                data["dimensoes"]["pesoBruto"]                    = self.dimensoes_pesoBruto       
                data["tributacao"]["gtinEmbalagem"]               = self.tributacao_gtinEmbalagem  
                data["tributacao"]["valorIPIFixo"]                = self.tributacao_valorIPIFixo   
                data["tributacao"]["classeIPI"]                   = self.tributacao_classeIPI      
                data["seo"]["titulo"]                             = self.seo_titulo                
                data["seo"]["descricao"]                          = self.seo_descricao             
                data["seo"]["keywords"]                           = self.seo_keywords or ["produto"]
                data["seo"]["linkVideo"]                          = self.seo_linkVideo             
                data["seo"]["slug"]                               = self.seo_slug                  
                data["estoque"]["controlar"]                      = bool(self.estoque_controlar)
                data["estoque"]["sobEncomenda"]                   = bool(self.estoque_sobEncomenda)
                data["estoque"]["diasPreparacao"]                 = self.estoque_diasPreparacao    
                data["estoque"]["localizacao"]                    = self.estoque_localizacao       
                data["estoque"]["minimo"]                         = self.estoque_minimo            
                data["estoque"]["maximo"]                         = self.estoque_maximo            

                data["fornecedores"] = [{
                    "id" : 753053887,
                    "codigoProdutoNoFornecedor" : self.fornecedores[0].codigoProdutoNoFornecedor,
                    "padrao" : True
                }]

                return data               
            except Exception as e:
                logger.error("Erro ao formatar dict produto: %s",e)
                return {"status":"Erro"} 
                   
        elif self.acao in 'post':
            try:
                data = obj['post']
                data["sku"]                                       = self.sku
                data["descricaoComplementar"]                     = self.descricaoComplementar
                data["unidade"]                                   = self.unidade
                data["unidadePorCaixa"]                           = str(self.unidadePorCaixa)
                data["ncm"]                                       = self.ncm
                data["gtin"]                                      = self.gtin
                data["origem"]                                    = int(self.origem)
                data["codigoEspecificadorSubstituicaoTributaria"] = self.cest
                data["garantia"]                                  = self.garantia
                data["observacoes"]                               = self.observacoes
                data["marca"]["id"]                               = self.marca_id
                data["categoria"]["id"]                           = int(self.categoria_id)
                data["precos"]["preco"]                           = self.preco
                data["precos"]["precoPromocional"]                = self.precoPromocional
                data["precos"]["precoCusto"]                      = self.precoCusto
                data["dimensoes"]["embalagem"]["id"]              = self.dimensoes_embalagem_id
                data["dimensoes"]["embalagem"]["tipo"]            = self.dimensoes_embalagem_tipo
                data["dimensoes"]["largura"]                      = self.dimensoes_largura
                data["dimensoes"]["altura"]                       = self.dimensoes_altura
                data["dimensoes"]["comprimento"]                  = self.dimensoes_comprimento
                data["dimensoes"]["diametro"]                     = self.dimensoes_diametro
                data["dimensoes"]["pesoLiquido"]                  = self.dimensoes_pesoLiquido
                data["dimensoes"]["pesoBruto"]                    = self.dimensoes_pesoBruto
                data["tributacao"]["gtinEmbalagem"]               = self.tributacao_gtinEmbalagem
                data["tributacao"]["valorIPIFixo"]                = self.tributacao_valorIPIFixo
                data["tributacao"]["classeIPI"]                   = self.tributacao_classeIPI
                data["seo"]["titulo"]                             = self.seo_titulo
                data["seo"]["descricao"]                          = self.seo_descricao
                data["seo"]["keywords"]                           = self.seo_keywords or ["produto"]
                data["seo"]["linkVideo"]                          = self.seo_linkVideo
                data["seo"]["slug"]                               = self.seo_slug
                data["descricao"]                                 = self.descricao
                data["tipo"]                                      = self.tipo
                data["estoque"]["controlar"]                      = True
                data["estoque"]["sobEncomenda"]                   = False
                data["estoque"]["minimo"]                         = self.estoque_minimo
                data["estoque"]["maximo"]                         = self.estoque_maximo
                data["estoque"]["diasPreparacao"]                 = self.estoque_diasPreparacao
                data["estoque"]["localizacao"]                    = self.estoque_localizacao
                
                data["fornecedores"] = [{
                    "id" : 753240684,
                    "codigoProdutoNoFornecedor" : self.sku,
                    "padrao" : True
                }]

                data["grade"] = ["."]

                return data               
            except Exception as e:
                logger.error("Erro ao formatar dict produto: %s",e)
                return {"status":"Erro"} 
        else:
            return {"status":"Ação não configurada"} 

    async def buscar(self, id:int=None) -> bool:
        
        url = self.endpoint+f"/{id or self.id}"        
        #print(url)
        try:
            token = self.con.get_latest_valid_token_or_refresh()
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

    async def buscar_novos(self) -> tuple[bool, list]:

        url = self.endpoint+f"?situacao={self.situacao_incial}"
        try:
            token = self.con.get_latest_valid_token_or_refresh()
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
                    return True, [p["id"] for p in get_pedido.json()['itens']]
                else:                      
                    logger.error("Erro %s: %s cod %s", get_pedido.status_code, get_pedido.json().get("mensagem","Erro desconhecido"), self.id)
                    return False, []
            else:
                logger.warning("Endpoint da API ou token de acesso faltantes")
                return False, []
        except Exception as e:
            logger.error("Erro relacionado ao token de acesso. %s",e)
            return False, []

    async def enviar_alteracoes(self) -> list:
        pass

    async def receber_alteracoes(self) -> tuple[bool,int]:
        pass

    async def buscar_todos(self) -> list:
        pass