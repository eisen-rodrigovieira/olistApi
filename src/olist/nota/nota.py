import re
import logging
import requests
from src.olist.connect    import Connect
from src.olist.nota       import item, parcela
from params               import config, configOlist
from datetime             import datetime, timedelta
from src.utils.validaPath import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Nota(object):

    def __init__(self):
        self.con                              = Connect()
        self.valida_path                      = validaPath()
        self.req_sleep                        = config.REQ_TIME_SLEEP  
        self.endpoint                         = config.API_URL+config.ENDPOINT_NOTAS
        self.regex_cNF                        = r'(<cNF>)(\d+)(<\/cNF>)'
        self.situacao                         = None
        self.tipo                             = None
        self.numero                           = None
        self.serie                            = None
        self.chaveAcesso                      = None
        self.dataEmissao                      = None
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
        self.valor                            = None
        self.valorProdutos                    = None
        self.valorFrete                       = None
        self.vendedor_id                      = None
        self.vendedor_nome                    = None
        self.idFormaEnvio                     = None
        self.idFormaFrete                     = None
        self.codigoRastreamento               = None
        self.urlRastreamento                  = None
        self.fretePorConta                    = None
        self.qtdVolumes                       = None
        self.pesoBruto                        = None
        self.pesoLiquido                      = None
        self.id                               = None
        self.finalidade                       = None
        self.regimeTributario                 = None
        self.dataInclusao                     = None
        self.baseIcms                         = None
        self.valorIcms                        = None
        self.baseIcmsSt                       = None
        self.valorIcmsSt                      = None
        self.valorServicos                    = None
        self.valorSeguro                      = None
        self.valorOutras                      = None
        self.valorIpi                         = None
        self.valorIssqn                       = None
        self.valorDesconto                    = None
        self.valorFaturado                    = None
        self.idIntermediador                  = None
        self.idNaturezaOperacao               = None
        self.idFormaPagamento                 = None
        self.idMeioPagamento                  = None
        self.observacoes                      = None
        self.condicaoPagamento                = None
        self.itens                            = []
        self.parcelas                         = []
        self.ecommerce_id                     = None
        self.ecommerce_nome                   = None
        self.ecommerce_numeroPedidoEcommerce  = None
        self.ecommerce_numeroPedidoCanalVenda = None
        self.ecommerce_canalVenda             = None
        self.xml                              = None
        self.codChaveAcesso                   = None
        self.acao                             = None
        
    def decodificar(self,payload:dict=None) -> bool:
        
        if payload:
            try:
                self.situacao    = payload.get("situacao")
                self.tipo        = payload.get("tipo")
                self.numero      = payload.get("numero")
                self.serie       = payload.get("serie")
                self.chaveAcesso = payload.get("chaveAcesso")
                self.dataEmissao = payload.get("dataEmissao")

                if payload.get("cliente"):
                    self.cliente_nome              = payload["cliente"].get("nome")
                    self.cliente_codigo            = payload["cliente"].get("codigo")
                    self.cliente_fantasia          = payload["cliente"].get("fantasia")
                    self.cliente_tipoPessoa        = payload["cliente"].get("tipoPessoa")
                    self.cliente_cpfCnpj           = payload["cliente"].get("cpfCnpj")
                    self.cliente_inscricaoEstadual = payload["cliente"].get("inscricaoEstadual")
                    self.cliente_rg                = payload["cliente"].get("rg")
                    self.cliente_telefone          = payload["cliente"].get("telefone")
                    self.cliente_celular           = payload["cliente"].get("celular")
                    self.cliente_email             = payload["cliente"].get("email")
                    self.cliente_id                = payload["cliente"].get("id")

                    if payload["cliente"].get("endereco"):
                        self.cliente_endereco_endereco    = payload["cliente"]["endereco"].get("endereco")
                        self.cliente_endereco_numero      = payload["cliente"]["endereco"].get("numero")
                        self.cliente_endereco_complemento = payload["cliente"]["endereco"].get("complemento")
                        self.cliente_endereco_bairro      = payload["cliente"]["endereco"].get("bairro")
                        self.cliente_endereco_municipio   = payload["cliente"]["endereco"].get("municipio")
                        self.cliente_endereco_cep         = payload["cliente"]["endereco"].get("cep")
                        self.cliente_endereco_uf          = payload["cliente"]["endereco"].get("uf")
                        self.cliente_endereco_pais        = payload["cliente"]["endereco"].get("pais")

                if payload.get("enderecoEntrega"):
                    self.enderecoEntrega_endereco         = payload["enderecoEntrega"].get("endereco")
                    self.enderecoEntrega_numero           = payload["enderecoEntrega"].get("numero")
                    self.enderecoEntrega_complemento      = payload["enderecoEntrega"].get("complemento")
                    self.enderecoEntrega_bairro           = payload["enderecoEntrega"].get("bairro")
                    self.enderecoEntrega_municipio        = payload["enderecoEntrega"].get("municipio")
                    self.enderecoEntrega_cep              = payload["enderecoEntrega"].get("cep")
                    self.enderecoEntrega_uf               = payload["enderecoEntrega"].get("uf")
                    self.enderecoEntrega_pais             = payload["enderecoEntrega"].get("pais")
                    self.enderecoEntrega_nomeDestinatario = payload["enderecoEntrega"].get("nomeDestinatario")
                    self.enderecoEntrega_cpfCnpj          = payload["enderecoEntrega"].get("cpfCnpj")
                    self.enderecoEntrega_tipoPessoa       = payload["enderecoEntrega"].get("tipoPessoa")

                self.valor         = payload.get("valor")
                self.valorProdutos = payload.get("valorProdutos")
                self.valorFrete    = payload.get("valorFrete")

                if payload.get("vendedor"):
                    self.vendedor_id    = payload["vendedor"].get("id")
                    self.vendedor_nome  = payload["vendedor"].get("nome")

                self.idFormaEnvio       = payload.get("idFormaEnvio")
                self.idFormaFrete       = payload.get("idFormaFrete")
                self.codigoRastreamento = payload.get("codigoRastreamento")
                self.urlRastreamento    = payload.get("urlRastreamento")
                self.fretePorConta      = payload.get("fretePorConta")
                self.qtdVolumes         = payload.get("qtdVolumes")
                self.pesoBruto          = payload.get("pesoBruto")
                self.pesoLiquido        = payload.get("pesoLiquido")

                self.id               = payload.get("id")
                self.finalidade       = payload.get("finalidade")
                self.regimeTributario = payload.get("regimeTributario")
                self.dataInclusao     = payload.get("dataInclusao")

                self.baseIcms      = payload.get("baseIcms")
                self.valorIcms     = payload.get("valorIcms")
                self.baseIcmsSt    = payload.get("baseIcmsSt")
                self.valorIcmsSt   = payload.get("valorIcmsSt")
                self.valorServicos = payload.get("valorServicos")
                self.valorSeguro   = payload.get("valorSeguro")
                self.valorOutras   = payload.get("valorOutras")
                self.valorIpi      = payload.get("valorIpi")
                self.valorIssqn    = payload.get("valorIssqn")
                self.valorDesconto = payload.get("valorDesconto")
                self.valorFaturado = payload.get("valorFaturado")

                self.idIntermediador    = payload.get("idIntermediador")
                self.idNaturezaOperacao = payload.get("idNaturezaOperacao")
                self.idFormaPagamento   = payload.get("idFormaPagamento")
                self.idMeioPagamento    = payload.get("idMeioPagamento")

                self.observacoes       = payload.get("observacoes")
                self.condicaoPagamento = payload.get("condicaoPagamento")

                if payload.get("ecommerce"):
                    self.ecommerce_id                     = payload["ecommerce"].get("id")
                    self.ecommerce_nome                   = payload["ecommerce"].get("nome")
                    self.ecommerce_numeroPedidoEcommerce  = payload["ecommerce"].get("numeroPedidoEcommerce")
                    self.ecommerce_numeroPedidoCanalVenda = payload["ecommerce"].get("numeroPedidoCanalVenda")
                    self.ecommerce_canalVenda             = payload["ecommerce"].get("canalVenda")
            
                for i in payload["itens"]:
                    it = item.Item()
                    it.decodificar(i)
                    self.itens.append(it)

                for p in payload["parcelas"]:
                    pa = parcela.Parcela()
                    pa.decodificar(p)
                    self.parcelas.append(pa)
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
        file_path = configOlist.PATH_OBJECT_SEPARACAO
        obj = await self.valida_path.validar(path=file_path,mode='r',method='json')

        if self.acao == 'get':
            try:
                data                = obj[self.acao]
                data["situacao"]    = self.situacao
                data["tipo"]        = self.tipo
                data["numero"]      = self.numero
                data["serie"]       = self.serie
                data["chaveAcesso"] = self.chaveAcesso
                data["dataEmissao"] = self.dataEmissao

                # Cliente
                data["cliente"] = {
                    "nome": self.cliente_nome,
                    "codigo": self.cliente_codigo,
                    "fantasia": self.cliente_fantasia,
                    "tipoPessoa": self.cliente_tipoPessoa,
                    "cpfCnpj": self.cliente_cpfCnpj,
                    "inscricaoEstadual": self.cliente_inscricaoEstadual,
                    "rg": self.cliente_rg,
                    "telefone": self.cliente_telefone,
                    "celular": self.cliente_celular,
                    "email": self.cliente_email,
                    "id": self.cliente_id,
                    "endereco": {
                        "endereco": self.cliente_endereco_endereco,
                        "numero": self.cliente_endereco_numero,
                        "complemento": self.cliente_endereco_complemento,
                        "bairro": self.cliente_endereco_bairro,
                        "municipio": self.cliente_endereco_municipio,
                        "cep": self.cliente_endereco_cep,
                        "uf": self.cliente_endereco_uf,
                        "pais": self.cliente_endereco_pais,
                    }
                }

                # Endereço de Entrega
                data["enderecoEntrega"] = {
                    "endereco": self.enderecoEntrega_endereco,
                    "numero": self.enderecoEntrega_numero,
                    "complemento": self.enderecoEntrega_complemento,
                    "bairro": self.enderecoEntrega_bairro,
                    "municipio": self.enderecoEntrega_municipio,
                    "cep": self.enderecoEntrega_cep,
                    "uf": self.enderecoEntrega_uf,
                    "pais": self.enderecoEntrega_pais,
                    "nomeDestinatario": self.enderecoEntrega_nomeDestinatario,
                    "cpfCnpj": self.enderecoEntrega_cpfCnpj,
                    "tipoPessoa": self.enderecoEntrega_tipoPessoa
                }

                data["valor"]         = self.valor
                data["valorProdutos"] = self.valorProdutos
                data["valorFrete"]    = self.valorFrete

                # Vendedor
                data["vendedor"] = {
                    "id": self.vendedor_id,
                    "nome": self.vendedor_nome
                }

                data["idFormaEnvio"]       = self.idFormaEnvio
                data["idFormaFrete"]       = self.idFormaFrete
                data["codigoRastreamento"] = self.codigoRastreamento
                data["urlRastreamento"]    = self.urlRastreamento
                data["fretePorConta"]      = self.fretePorConta
                data["qtdVolumes"]         = self.qtdVolumes
                data["pesoBruto"]          = self.pesoBruto
                data["pesoLiquido"]        = self.pesoLiquido

                data["id"]               = self.id
                data["finalidade"]       = self.finalidade
                data["regimeTributario"] = self.regimeTributario
                data["dataInclusao"]     = self.dataInclusao

                data["baseIcms"]      = self.baseIcms
                data["valorIcms"]     = self.valorIcms
                data["baseIcmsSt"]    = self.baseIcmsSt
                data["valorIcmsSt"]   = self.valorIcmsSt
                data["valorServicos"] = self.valorServicos
                data["valorSeguro"]   = self.valorSeguro
                data["valorOutras"]   = self.valorOutras
                data["valorIpi"]      = self.valorIpi
                data["valorIssqn"]    = self.valorIssqn
                data["valorDesconto"] = self.valorDesconto
                data["valorFaturado"] = self.valorFaturado

                data["idIntermediador"]    = self.idIntermediador
                data["idNaturezaOperacao"] = self.idNaturezaOperacao
                data["idFormaPagamento"]   = self.idFormaPagamento
                data["idMeioPagamento"]    = self.idMeioPagamento

                data["observacoes"]        = self.observacoes
                data["condicaoPagamento"]  = self.condicaoPagamento

                # Ecommerce
                data["ecommerce"] = {
                    "id": self.ecommerce_id,
                    "nome": self.ecommerce_nome,
                    "numeroPedidoEcommerce": self.ecommerce_numeroPedidoEcommerce,
                    "numeroPedidoCanalVenda": self.ecommerce_numeroPedidoCanalVenda,
                    "canalVenda": self.ecommerce_canalVenda
                }
                
                itens_list = list()
                for it in self.itens:
                    itens_list.append(await it.encodificar(self.acao))
                data["itens"] = itens_list
                
                parcelas_list = list()
                for pa in self.itens:
                    parcelas_list.append(await pa.encodificar(self.acao))
                data["parcelas"] = parcelas_list
                
                return data               
            except Exception as e:
                logger.error("Erro ao formatar dict nfe: %s",e)
                return {"status":"Erro"} 
        else:
            return {"status":"Ação não configurada"} 

    async def buscar(self, id:int=None) -> bool:        
        url = self.endpoint+f"/{id or self.id}"
        try:
            token = await self.con.get_latest_valid_token_or_refresh()
            if url and token:                
                get_nota = requests.get(
                    url = url,
                    headers = {
                        "Authorization":f"Bearer {token}",
                        "Content-Type":"application/json",
                        "Accept":"application/json"
                    }
                )
                if get_nota.status_code == 200:
                    if self.decodificar(get_nota.json()):
                        self.acao = 'get'
                    else:
                        logger.error("Erro ao decodificar separação %s", self.id)
                else:                      
                    logger.error("Erro %s: %s cod %s", get_nota.status_code, get_nota.json().get("mensagem","Erro desconhecido"), self.id)

                get_xml = requests.get(
                    url = url+"/xml",
                    headers = {
                        "Authorization":f"Bearer {token}",
                        "Content-Type":"application/json",
                        "Accept":"application/json"
                    }
                )
                if get_xml.status_code == 200:
                    self.xml = get_xml.json().get('xmlNfe')
                    self.codChaveAcesso = int(re.search(self.regex_cNF,self.xml).group(2))
                else:                      
                    logger.error("Erro %s: %s cod %s", get_xml.status_code, get_xml.json().get("mensagem","Erro desconhecido"), self.id)                
                return True if get_nota.status_code == get_xml.status_code == 200 else False
            else:
                logger.warning("Endpoint da API ou token de acesso faltantes")
                return False                    
        except Exception as e:
            logger.error("Erro relacionado ao token de acesso. %s",e)
            return False  
