import os
import time
import json
import logging
import requests
from datetime          import datetime
from src.olist.connect import Connect
from src.olist.produto import fornecedor, anexo, kit, variacao, producao
from params            import config, configOlist

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Produto:

    def __init__(
            self
            ,id                             :int   = None
            ,sku                            :str   = None
            ,descricao                      :str   = None
            ,descricaoComplementar          :str   = None
            ,tipo                           :str   = None
            ,situacao                       :str   = None
            ,produtoPai_id                  :int   = None
            ,produtoPai_sku                 :str   = None
            ,produtoPai_descricao           :str   = None
            ,unidade                        :str   = None
            ,unidadePorCaixa                :int   = None
            ,ncm                            :str   = None
            ,gtin                           :str   = None
            ,origem                         :int   = None
            ,cest                           :str   = None
            ,garantia                       :str   = None
            ,observacoes                    :str   = None
            ,categoria_id                   :int   = None
            ,categoria_nome                 :str   = None
            ,categoria_caminhoCompleto      :str   = None
            ,marca_id                       :int   = None
            ,marca_nome                     :str   = None
            ,dimensoes_embalagem_id         :int   = None
            ,dimensoes_embalagem_tipo       :int   = None
            ,dimensoes_embalagem_descricao  :str   = None
            ,dimensoes_largura              :float = None
            ,dimensoes_altura               :float = None
            ,dimensoes_comprimento          :float = None
            ,dimensoes_diametro             :float = None
            ,dimensoes_pesoLiquido          :float = None
            ,dimensoes_pesoBruto            :float = None
            ,dimensoes_quantidadeVolumes    :int   = None
            ,preco                          :float = None
            ,precoPromocional               :float = None
            ,precoCusto                     :float = None
            ,precoCustoMedio                :float = None
            ,estoque_controlar              :bool  = None
            ,estoque_sobEncomenda           :bool  = None
            ,estoque_diasPreparacao         :int   = None
            ,estoque_localizacao            :str   = None
            ,estoque_minimo                 :int   = None
            ,estoque_maximo                 :int   = None
            ,estoque_quantidade             :int   = None
            ,estoque_inicial                :int   = None
            ,seo_titulo                     :str   = None
            ,seo_descricao                  :str   = None
            ,seo_keywords                   :list  = None
            ,seo_linkVideo                  :str   = None
            ,seo_slug                       :str   = None
            ,tributacao_gtinEmbalagem       :str   = None
            ,tributacao_valorIPIFixo        :float = None
            ,tributacao_classeIPI           :str   = None
        ):  

        self.con                           = Connect()  
        self.req_sleep                     = config.REQ_TIME_SLEEP  
        self.endpoint                      = config.API_URL+config.ENDPOINT_PRODUTOS
        self.id                            = id
        self.sku                           = sku
        self.descricao                     = descricao
        self.descricaoComplementar         = descricaoComplementar
        self.tipo                          = tipo
        self.situacao                      = situacao
        self.produtoPai_id                 = produtoPai_id
        self.produtoPai_sku                = produtoPai_sku
        self.produtoPai_descricao          = produtoPai_descricao
        self.unidade                       = unidade
        self.unidadePorCaixa               = unidadePorCaixa
        self.ncm                           = ncm
        self.gtin                          = gtin
        self.origem                        = origem
        self.cest                          = cest
        self.garantia                      = garantia
        self.observacoes                   = observacoes
        self.categoria_id                  = categoria_id
        self.categoria_nome                = categoria_nome
        self.categoria_caminhoCompleto     = categoria_caminhoCompleto
        self.marca_id                      = marca_id
        self.marca_nome                    = marca_nome
        self.dimensoes_embalagem_id        = dimensoes_embalagem_id
        self.dimensoes_embalagem_tipo      = dimensoes_embalagem_tipo
        self.dimensoes_embalagem_descricao = dimensoes_embalagem_descricao
        self.dimensoes_largura             = dimensoes_largura
        self.dimensoes_altura              = dimensoes_altura
        self.dimensoes_comprimento         = dimensoes_comprimento
        self.dimensoes_diametro            = dimensoes_diametro
        self.dimensoes_pesoLiquido         = dimensoes_pesoLiquido
        self.dimensoes_pesoBruto           = dimensoes_pesoBruto
        self.dimensoes_quantidadeVolumes   = dimensoes_quantidadeVolumes
        self.preco                         = preco
        self.precoPromocional              = precoPromocional
        self.precoCusto                    = precoCusto
        self.precoCustoMedio               = precoCustoMedio
        self.estoque_controlar             = estoque_controlar
        self.estoque_sobEncomenda          = estoque_sobEncomenda
        self.estoque_diasPreparacao        = estoque_diasPreparacao
        self.estoque_localizacao           = estoque_localizacao
        self.estoque_minimo                = estoque_minimo
        self.estoque_maximo                = estoque_maximo
        self.estoque_quantidade            = estoque_quantidade
        self.estoque_inicial               = estoque_inicial
        self.fornecedores                  = []
        self.seo_titulo                    = seo_titulo
        self.seo_descricao                 = seo_descricao
        self.seo_keywords                  = seo_keywords
        self.seo_linkVideo                 = seo_linkVideo
        self.seo_slug                      = seo_slug
        self.tributacao_gtinEmbalagem      = tributacao_gtinEmbalagem
        self.tributacao_valorIPIFixo       = tributacao_valorIPIFixo
        self.tributacao_classeIPI          = tributacao_classeIPI
        self.anexos                        = []
        self.variacoes                     = []
        self.kits                          = []
        self.producao                      = []
        self.acao = None
        
    def decodificar(self,payload:dict=None) -> bool:
        
        if payload:
            try:
                #logger.debug("iniciando decode basico")
                self.id                                = payload["id"]
                self.sku                               = payload["sku"]
                self.descricao                         = payload["descricao"]            
                self.descricaoComplementar             = payload["descricaoComplementar"]
                self.tipo                              = payload["tipo"]                 
                self.situacao                          = payload["situacao"]             
                if payload["produtoPai"]:                
                    self.produtoPai_id                 = payload["produtoPai"]["id"]
                    self.produtoPai_sku                = payload["produtoPai"]["sku"]      
                    self.produtoPai_descricao          = payload["produtoPai"]["descricao"]
                else:                
                    self.produtoPai_id                 = None
                    self.produtoPai_sku                = None
                    self.produtoPai_descricao          = None
                self.unidade                           = payload["unidade"]                             
                self.unidadePorCaixa                   = payload["unidadePorCaixa"]
                self.ncm                               = payload["ncm"]                                 
                self.gtin                              = payload["gtin"]                                
                self.origem                            = payload["origem"]
                if "codigoEspecificadorSubstituicaoTributaria" in payload.keys():
                    self.cest                          = payload["codigoEspecificadorSubstituicaoTributaria"]
                else:
                    self.cest                          = None
                self.garantia                          = payload["garantia"]                            
                self.observacoes                       = payload["observacoes"]                         
                if payload["categoria"]:
                    self.categoria_id                  = payload["categoria"]["id"]
                    self.categoria_nome                = payload["categoria"]["nome"]           
                    self.categoria_caminhoCompleto     = payload["categoria"]["caminhoCompleto"]
                else:
                    self.categoria_id                  = None
                    self.categoria_nome                = None
                    self.categoria_caminhoCompleto     = None
                if payload["marca"]:
                    self.marca_id                      = payload["marca"]["id"]
                    self.marca_nome                    = payload["marca"]["nome"]
                else:
                    self.marca_id                      = None
                    self.marca_nome                    = None
                if payload["dimensoes"]:
                    self.dimensoes_embalagem_id        = payload["dimensoes"]["embalagem"]["id"]
                    self.dimensoes_embalagem_tipo      = payload["dimensoes"]["embalagem"]["tipo"]     
                    self.dimensoes_embalagem_descricao = payload["dimensoes"]["embalagem"]["descricao"]
                    self.dimensoes_largura             = payload["dimensoes"]["largura"]
                    self.dimensoes_altura              = payload["dimensoes"]["altura"]
                    self.dimensoes_comprimento         = payload["dimensoes"]["comprimento"]
                    self.dimensoes_diametro            = payload["dimensoes"]["diametro"]
                    self.dimensoes_pesoLiquido         = payload["dimensoes"]["pesoLiquido"]
                    self.dimensoes_pesoBruto           = payload["dimensoes"]["pesoBruto"]
                    self.dimensoes_quantidadeVolumes   = payload["dimensoes"]["quantidadeVolumes"]
                else:
                    self.dimensoes_embalagem_id        = None
                    self.dimensoes_embalagem_tipo      = None
                    self.dimensoes_embalagem_descricao = None
                    self.dimensoes_largura             = None
                    self.dimensoes_altura              = None
                    self.dimensoes_comprimento         = None
                    self.dimensoes_diametro            = None
                    self.dimensoes_pesoLiquido         = None
                    self.dimensoes_pesoBruto           = None
                    self.dimensoes_quantidadeVolumes   = None
                if payload["precos"]:
                    self.preco                         = payload["precos"]["preco"]
                    self.precoPromocional              = payload["precos"]["precoPromocional"]
                    self.precoCusto                    = payload["precos"]["precoCusto"]
                    self.precoCustoMedio               = payload["precos"]["precoCustoMedio"]
                else:
                    self.preco                         = None
                    self.precoPromocional              = None
                    self.precoCusto                    = None
                    self.precoCustoMedio               = None
                if payload["estoque"]:
                    self.estoque_controlar             = payload["estoque"]["controlar"]     
                    self.estoque_sobEncomenda          = payload["estoque"]["sobEncomenda"]  
                    self.estoque_diasPreparacao        = payload["estoque"]["diasPreparacao"]
                    self.estoque_localizacao           = payload["estoque"]["localizacao"]   
                    self.estoque_minimo                = payload["estoque"]["minimo"]
                    self.estoque_maximo                = payload["estoque"]["maximo"]
                    self.estoque_quantidade            = payload["estoque"]["quantidade"]
                    #self.estoque_inicial               = payload["estoque"]["inicial"]
                else:
                    self.estoque_controlar             = None
                    self.estoque_sobEncomenda          = None
                    self.estoque_diasPreparacao        = None
                    self.estoque_localizacao           = None
                    self.estoque_minimo                = None
                    self.estoque_maximo                = None
                    self.estoque_quantidade            = None
                    # self.estoque_inicial               = None
                if payload["seo"]:
                    self.seo_titulo                    = payload["seo"]["titulo"]            
                    self.seo_descricao                 = payload["seo"]["descricao"]         
                    self.seo_keywords                  = payload["seo"]["keywords"] or ["produto"]
                    self.seo_linkVideo                 = payload["seo"]["linkVideo"]         
                    self.seo_slug                      = payload["seo"]["slug"]              
                else:
                    self.seo_titulo                    = None
                    self.seo_descricao                 = None
                    self.seo_keywords                  = None
                    self.seo_linkVideo                 = None
                    self.seo_slug                      = None
                if payload["tributacao"]:
                    self.tributacao_gtinEmbalagem      = payload["tributacao"]["gtinEmbalagem"] 
                    self.tributacao_valorIPIFixo       = payload["tributacao"]["valorIPIFixo"]
                    self.tributacao_classeIPI          = payload["tributacao"]["classeIPI"]     
                else:
                    self.tributacao_gtinEmbalagem      = None
                    self.tributacao_valorIPIFixo       = None
                    self.tributacao_classeIPI          = None
                #logger.debug("finalizado decode basico")

                #logger.debug("iniciando decode %s fornecedores",len(payload["fornecedores"]))
                for f in payload["fornecedores"]:
                    fo = fornecedor.Fornecedor()
                    fo.decodificar(f)
                    self.fornecedores.append(fo)
                #logger.debug("finalizado decode fornecedores")
                
                #logger.debug("iniciando decode %s anexos",len(payload["anexos"]))
                for a in payload["anexos"]:
                    an = anexo.Anexo()
                    an.decodificar(a)
                    self.anexos.append(an)

                #logger.debug("iniciando decode %s variacoes",len(payload["variacoes"]))
                for v in payload["variacoes"]:
                    va = variacao.Variacao()
                    va.decodificar(v)
                    self.variacoes.append(va)

                #logger.debug("iniciando decode %s kits",len(payload["kit"]))
                for k in payload["kit"]:
                    ki = kit.Kit()
                    ki.decodificar(k)
                    self.kits.append(ki) 

                #logger.debug("iniciando decode %s producao",len(payload["producao"]))
                if payload["producao"]:
                    for p in payload["producao"]:
                        pr = producao.Producao()
                        pr.decodificar(p)
                        self.producao.append(pr) 
                return True

            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    def encodificar(self) -> dict:
        obj = {}
        data = {}
        if not os.path.exists(configOlist.PATH_OBJECT_PRODUTO):
            logger.error("Objeto do produto não encontrado em %s",configOlist.PATH_OBJECT_PRODUTO)
            return {"status":"Erro"}
        else:    
            with open(configOlist.PATH_OBJECT_PRODUTO, "r", encoding="utf-8") as f:
                obj = json.load(f)        

        if self.acao == 'get':
            try:
                data = obj[self.acao]
                data["id"]                                        = self.id                           
                data["sku"]                                       = self.sku                          
                data["descricao"]                                 = self.descricao                    
                data["descricaoComplementar"]                     = self.descricaoComplementar        
                data["tipo"]                                      = self.tipo                         
                data["situacao"]                                  = self.situacao                     
                data["produtoPai"]["id"]                          = self.produtoPai_id                
                data["produtoPai"]["sku"]                         = self.produtoPai_sku               
                data["produtoPai"]["descricao"]                   = self.produtoPai_descricao         
                data["unidade"]                                   = self.unidade                      
                data["unidadePorCaixa"]                           = self.unidadePorCaixa              
                data["ncm"]                                       = self.ncm                          
                data["gtin"]                                      = self.gtin                         
                data["origem"]                                    = self.origem                       
                data["codigoEspecificadorSubstituicaoTributaria"] = self.cest                           
                data["garantia"]                                  = self.garantia                     
                data["observacoes"]                               = self.observacoes                  
                data["categoria"]["id"]                           = self.categoria_id                 
                data["categoria"]["nome"]                         = self.categoria_nome               
                data["categoria"]["caminhoCompleto"]              = self.categoria_caminhoCompleto    
                data["marca"]["id"]                               = self.marca_id                     
                data["marca"]["nome"]                             = self.marca_nome                   
                data["dimensoes"]["embalagem"]["id"]              = self.dimensoes_embalagem_id       
                data["dimensoes"]["embalagem"]["tipo"]            = self.dimensoes_embalagem_tipo     
                data["dimensoes"]["embalagem"]["descricao"]       = self.dimensoes_embalagem_descricao
                data["dimensoes"]["largura"]                      = self.dimensoes_largura            
                data["dimensoes"]["altura"]                       = self.dimensoes_altura             
                data["dimensoes"]["comprimento"]                  = self.dimensoes_comprimento        
                data["dimensoes"]["diametro"]                     = self.dimensoes_diametro           
                data["dimensoes"]["pesoLiquido"]                  = self.dimensoes_pesoLiquido        
                data["dimensoes"]["pesoBruto"]                    = self.dimensoes_pesoBruto          
                data["dimensoes"]["quantidadeVolumes"]            = self.dimensoes_quantidadeVolumes  
                data["precos"]["preco"]                           = self.preco                        
                data["precos"]["precoPromocional"]                = self.precoPromocional             
                data["precos"]["precoCusto"]                      = self.precoCusto                   
                data["precos"]["precoCustoMedio"]                 = self.precoCustoMedio              
                data["estoque"]["controlar"]                      = self.estoque_controlar            
                data["estoque"]["sobEncomenda"]                   = self.estoque_sobEncomenda         
                data["estoque"]["diasPreparacao"]                 = self.estoque_diasPreparacao       
                data["estoque"]["localizacao"]                    = self.estoque_localizacao          
                data["estoque"]["minimo"]                         = self.estoque_minimo               
                data["estoque"]["maximo"]                         = self.estoque_maximo               
                data["estoque"]["quantidade"]                     = self.estoque_quantidade           
                data["estoque"]["inicial"]                        = self.estoque_inicial           
                data["seo"]["titulo"]                             = self.seo_titulo                   
                data["seo"]["descricao"]                          = self.seo_descricao                
                data["seo"]["keywords"]                           = self.seo_keywords                 
                data["seo"]["linkVideo"]                          = self.seo_linkVideo                
                data["seo"]["slug"]                               = self.seo_slug                     
                data["tributacao"]["gtinEmbalagem"]               = self.tributacao_gtinEmbalagem     
                data["tributacao"]["valorIPIFixo"]                = self.tributacao_valorIPIFixo      
                data["tributacao"]["classeIPI"]                   = self.tributacao_classeIPI         
                
                fornecedores_list = list()
                for fo in self.fornecedores:
                    fornecedores_list.append(fo.encodificar())
                
                anexos_list = list()
                for an in self.anexos:
                    anexos_list.append(an.encodificar())
                
                variacoes_list = list()
                for va in self.variacoes:
                    variacoes_list.append(va.encodificar())
                
                kits_list = list()
                for ki in self.kits:
                    kits_list.append(ki.encodificar())

                data["fornecedores"]                        = fornecedores_list
                data["anexos"]                              = anexos_list                       
                data["variacoes"]                           = variacoes_list                    
                data["kit"]                                 = kits_list
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

    async def buscar(self) -> bool:

        if self.id:
            url = self.endpoint+f"/{self.id}"
        elif self.sku:
            url = self.endpoint+f"/?codigo={self.sku}"
        
        print(url)
        try:
            token = self.con.get_latest_valid_token_or_refresh()
            if url and token:                
                get_produto = requests.get(
                    url=url,
                    headers={
                        "Authorization":f"Bearer {token}",
                        "Content-Type":"application/json",
                        "Accept":"application/json"
                    }
                )
                if get_produto.status_code == 200:
                        if self.decodificar(get_produto.json()):
                            self.acao = 'get'
                            return True
                        else:
                            logger.error("Erro ao decodificar produto %s", self.id or self.sku)
                            return False
                else:                      
                    logger.error("Erro %s: %s cod %s", get_produto.status_code, get_produto.json().get("mensagem","Erro desconhecido"), self.id or self.sku)
                    return False                    
            else:
                logger.warning("Endpoint da API ou token de acesso faltantes")
                return False                    
        except Exception as e:
            logger.error("Erro relacionado ao token de acesso. %s",e)
            return False     

    async def enviar_alteracoes(self) -> list:

        if not os.path.exists(configOlist.PATH_HISTORICO_PRODUTO):
            logger.error("Histórico de produtos não encontrado em %s",configOlist.PATH_HISTORICO_PRODUTO)
            return {"status":"Erro"}
        else:    
            with open(configOlist.PATH_HISTORICO_PRODUTO, "r", encoding="utf-8") as f:
                historico = json.load(f)
                
            token = self.con.get_latest_valid_token_or_refresh()
            status = 200
            paginacao = {}
            itens = []

            while status == 200:
                if paginacao:        
                    if paginacao["limit"] + paginacao["offset"] < paginacao ["total"]:
                        offset = paginacao["limit"] + paginacao["offset"]
                        url = config.API_URL+config.ENDPOINT_PRODUTOS+f"?situacao=A&dataAlteracao={historico["ultima_atualizacao_olist_sankhya"]["data"]}&offset={offset}"
                    else:
                        url = None
                else:
                    url = config.API_URL+config.ENDPOINT_PRODUTOS+f"?situacao=A&dataAlteracao={historico["ultima_atualizacao_olist_sankhya"]["data"]}"
                if url:
                    get_alteracoes = requests.get(url=url,
                                                  headers={
                                                      "Authorization":f"Bearer {token}",
                                                      "Content-Type":"application/json",
                                                      "Accept":"application/json"
                                                  })
                    self.acao = 'get'
                    status=get_alteracoes.status_code
                    itens += get_alteracoes.json()["itens"]
                    paginacao = get_alteracoes.json()["paginacao"]
                    time.sleep(self.req_sleep)
                else:
                    status = 0
            
            itens.sort(key=lambda i: i['dataAlteracao'],reverse=True)
            
            return [{"id":i["id"],"sku":i["sku"]} for i in itens]

    async def receber_alteracoes(self) -> tuple[bool,int]:

        if not os.path.exists(configOlist.PATH_HISTORICO_PRODUTO):
            logger.error("Histórico de produtos não encontrado em %s",configOlist.PATH_HISTORICO_PRODUTO)
            return {"status":"Erro"}
        else:    
            with open(configOlist.PATH_HISTORICO_PRODUTO, "r", encoding="utf-8") as f:
                historico = json.load(f)
                
            token = self.con.get_latest_valid_token_or_refresh()
            payload = self.encodificar()

            if self.acao == 'put':
                if self.produtoPai_id: # se for variacao
                    url = config.API_URL+config.ENDPOINT_PRODUTOS+f"/{self.produtoPai_id}/variacoes/{self.id}"
                else:
                    url = config.API_URL+config.ENDPOINT_PRODUTOS+f"/{self.id}"                
                if url:
                    put_alteracoes = requests.put(url=url,
                                                  headers={
                                                      "Authorization":f"Bearer {token}",
                                                      "Content-Type":"application/json",
                                                      "Accept":"application/json"
                                                  },
                                                  data=json.dumps(payload))
                    if put_alteracoes.status_code == 204:                                         
                        return True, 1
                    elif put_alteracoes.status_code in [404,409]:
                        logger.warning("Erro %s: %s ID %s", put_alteracoes.status_code, put_alteracoes.json(), self.id)
                        logger.info(json.dumps(payload))
                        return True, 0
                    else:
                        print(f"Falha ao atualizar produto {self.id}")
                        logger.error("Erro %s: %s ID %s", put_alteracoes.status_code, put_alteracoes.json(), self.id)
                        logger.info(json.dumps(payload))
                        return False, 0
                else:
                    print("Falha ao montar URL")
                    logger.error("Erro: Falha ao montar URL")
                    return False, 0
            elif self.acao == 'post':
                print(payload)
                url = config.API_URL+config.ENDPOINT_PRODUTOS
                logger.info("url %s and token %s -ok",token,url)
                if url:
                    post_novo = requests.post(url=url,
                                              headers={
                                                  "Authorization":f"Bearer {token}",
                                                  "Content-Type":"application/json",
                                                  "Accept":"application/json"
                                              },
                                              data=json.dumps(payload))
                    if post_novo.status_code == 201:                    
                        return True, post_novo.json()["id"]
                    else:
                        print(f"Falha ao incluir produto {payload["sku"]}")
                        logger.error("Erro %s: %s cod %s", post_novo.status_code, post_novo.json(), payload["sku"])
                        return False,0
                else:
                    print("Falha ao montar URL")
                    logger.error("Erro: Falha ao montar URL")
                    return False,0

            elif self.acao == 'del':
                print(payload)
                url = config.API_URL+config.ENDPOINT_PRODUTOS+f"/{self.id}"
                if url:
                    put_alteracoes = requests.put(url=url,
                                                  headers={
                                                      "Authorization":f"Bearer {token}",
                                                      "Content-Type":"application/json",
                                                      "Accept":"application/json"
                                                  },
                                                  data=json.dumps(payload))
                    if put_alteracoes.status_code == 204:                                       
                        return True
                    else:
                        print(f"Falha ao inativar produto {self.id}")
                        logger.error("Erro %s: %s", put_alteracoes.status_code, put_alteracoes.json())
                        return False
                else:
                    print("Falha ao montar URL")
                    logger.error("Erro: Falha ao montar URL")
                    return False             
            else:
                print("Evento não configurado")
                logger.error("Erro: Evento de atualização não configurado")
                return False        

    async def buscar_todos(self) -> list:
                
        token = self.con.get_latest_valid_token_or_refresh()
        status = 200
        paginacao = {}
        itens = []

        while status == 200:
            if paginacao:        
                if paginacao["limit"] + paginacao["offset"] < paginacao ["total"]:
                    offset = paginacao["limit"] + paginacao["offset"]
                    url = config.API_URL+config.ENDPOINT_PRODUTOS+f"?offset={offset}"
                else:
                    url = None
            else:
                url = config.API_URL+config.ENDPOINT_PRODUTOS
            if url:
                get_alteracoes = requests.get(url=url,
                                            headers={
                                                "Authorization":f"Bearer {token}",
                                                "Content-Type":"application/json",
                                                "Accept":"application/json"
                                            })
                status=get_alteracoes.status_code
                itens += get_alteracoes.json()["itens"]
                paginacao = get_alteracoes.json()["paginacao"]
                print(f"{len(itens)}/{paginacao["total"]}")
                time.sleep(self.req_sleep)
            else:
                status=0
                print(f"Fim. {len(itens)} produtos encontratos")            
        return itens