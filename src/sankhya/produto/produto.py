import os
import logging
import pandas as pd
from params               import config, configSankhya
from src.sankhya.dbConfig import dbConfig

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

class Produto:

    """
    Classe que representa um produto com todas as informações relevantes para integração com marketplace,
    controle de estoque, tributação e dimensões físicas.

    Atributos:
        integrar_mkp                (bool): Indica se o produto deve ser integrado ao marketplace.
        id                          (str): Identificador único do produto.
        sku                         (str): Código SKU do produto.
        descricao                   (str): Descrição do produto.
        descricao_formatada         (str): Descrição formatada do produto.
        descricaoComplementar       (str): Descrição complementar.
        tipo                        (str): Tipo de produto.
        situacao                    (str): Situação atual do produto (ativo, inativo etc.).
        produtoPai_id               (int): ID do produto pai, se for uma variação.
        unidade                     (str): Unidade de medida.
        unidadePorCaixa             (int): Quantidade por caixa.
        ncm                         (str): Código NCM.
        gtin                        (str): Código GTIN (EAN).
        origem                      (int): Código de origem do produto.
        cest                        (str): Código CEST.
        garantia                    (str): Informações sobre garantia.
        observacoes                 (str): Observações adicionais.
        categoria_id                (int): ID da categoria.
        categoria_nome              (str): Nome da categoria.
        marca_id                    (int): ID da marca.
        marca_nome                  (str): Nome da marca.
        dimensoes_embalagem_tipo    (int): Tipo da embalagem.
        dimensoes_largura           (float): Largura do produto.
        dimensoes_altura            (float): Altura do produto.
        dimensoes_comprimento       (float): Comprimento do produto.
        dimensoes_pesoLiquido       (float): Peso líquido.
        dimensoes_pesoBruto         (float): Peso bruto.
        dimensoes_quantidadeVolumes (int): Número de volumes.
        preco                       (float): Preço de venda.
        precoCusto                  (float): Preço de custo.
        estoque_controlar           (bool): Indica se deve haver controle de estoque.
        estoque_sobEncomenda        (bool): Produto sob encomenda.
        estoque_diasPreparacao      (int): Dias necessários para preparação.
        estoque_localizacao         (str): Localização física no estoque.
        estoque_minimo              (int): Estoque mínimo.
        estoque_maximo              (int): Estoque máximo.
        estoque_quantidade          (int): Quantidade atual em estoque.
        estoque_inicial             (int): Quantidade inicial.
        fornecedor_id               (int): ID do fornecedor.
        fornecedor_codigo_produto   (int): Código do produto no fornecedor.
        tributacao_gtinEmbalagem    (str): GTIN da embalagem para tributação.
    """      

    def __init__(
            self
            ,integrar_mkp                   :bool  = None
            ,id                             :str   = None
            ,sku                            :str   = None
            ,descricao                      :str   = None
            ,descricao_formatada            :str   = None
            ,descricaoComplementar          :str   = None
            ,tipo                           :str   = None
            ,situacao                       :str   = None
            ,produtoPai_id                  :int   = None
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
            ,marca_id                       :int   = None
            ,marca_nome                     :str   = None
            ,dimensoes_embalagem_tipo       :int   = None
            ,dimensoes_largura              :float = None
            ,dimensoes_altura               :float = None
            ,dimensoes_comprimento          :float = None
            ,dimensoes_pesoLiquido          :float = None
            ,dimensoes_pesoBruto            :float = None
            ,dimensoes_quantidadeVolumes    :int   = None
            ,preco                          :float = None
            ,precoCusto                     :float = None
            ,estoque_controlar              :bool  = None
            ,estoque_sobEncomenda           :bool  = None
            ,estoque_diasPreparacao         :int   = None
            ,estoque_localizacao            :str   = None
            ,estoque_minimo                 :int   = None
            ,estoque_maximo                 :int   = None
            ,estoque_quantidade             :int   = None
            ,estoque_inicial                :int   = None
            ,fornecedor_id                  :int   = None
            ,fornecedor_codigo_produto      :int   = None            
            ,tributacao_gtinEmbalagem       :str   = None            
        ):

        self.integrar_mkp                  = integrar_mkp
        self.id                            = id
        self.sku                           = sku
        self.descricao                     = descricao
        self.descricaoFormatada            = descricao_formatada
        self.descricaoComplementar         = descricaoComplementar
        self.tipo                          = tipo
        self.situacao                      = situacao
        self.produtoPai_id                 = produtoPai_id
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
        self.marca_id                      = marca_id
        self.marca_nome                    = marca_nome
        self.dimensoes_embalagem_tipo      = dimensoes_embalagem_tipo
        self.dimensoes_largura             = dimensoes_largura
        self.dimensoes_altura              = dimensoes_altura
        self.dimensoes_comprimento         = dimensoes_comprimento
        self.dimensoes_pesoLiquido         = dimensoes_pesoLiquido
        self.dimensoes_pesoBruto           = dimensoes_pesoBruto
        self.dimensoes_quantidadeVolumes   = dimensoes_quantidadeVolumes
        self.preco                         = preco
        self.precoCusto                    = precoCusto
        self.estoque_controlar             = estoque_controlar
        self.estoque_sobEncomenda          = estoque_sobEncomenda
        self.estoque_diasPreparacao        = estoque_diasPreparacao
        self.estoque_localizacao           = estoque_localizacao
        self.estoque_minimo                = estoque_minimo
        self.estoque_maximo                = estoque_maximo
        self.estoque_quantidade            = estoque_quantidade
        self.estoque_inicial               = estoque_inicial
        self.fornecedor_id                 = fornecedor_id
        self.fornecedor_codigo_produto     = fornecedor_codigo_produto
        self.tributacao_gtinEmbalagem      = tributacao_gtinEmbalagem

    def decodificar(self,data:dict=None) -> bool:
        """
        Preenche os atributos do objeto a partir de um dicionário de dados.

        Args:
            data (dict): Dicionário com os dados do produto.

        Returns:
            bool: True se os dados foram decodificados com sucesso, False caso contrário.
        """        

        if data:
            try:
                self.integrar_mkp                  = bool(data["integrar_mkp"])
                self.id                            = data["id"]
                self.sku                           = data["sku"]
                self.descricao                     = data["descricao"]
                self.descricao_formatada           = data["descricao_formatada"]
                self.descricaoComplementar         = data["descricao_complementar"]
                self.tipo                          = data["tipo"]
                self.situacao                      = data["situacao"]
                self.produtoPai_id                 = data["produto_pai"]
                self.unidade                       = data["unidade"]
                self.unidadePorCaixa               = data["unidade_por_caixa"]
                self.ncm                           = data["ncm"]
                self.gtin                          = data["gtin"]
                self.origem                        = data["origem"]
                self.cest                          = data["cest"]
                self.garantia                      = data["garantia"]
                self.observacoes                   = data["observacoes"]
                self.categoria_id                  = data["id_categoria"]
                self.marca_id                      = data["marca_id"]
                self.dimensoes_embalagem_tipo      = data["embalagem_tipo"]
                self.dimensoes_largura             = data["largura"]
                self.dimensoes_altura              = data["altura"]
                self.dimensoes_comprimento         = data["comprimento"]
                self.dimensoes_pesoLiquido         = data["peso_liquido"]
                self.dimensoes_pesoBruto           = data["peso_bruto"]
                self.dimensoes_quantidadeVolumes   = data["quantidade_volumes"]
                self.preco                         = data["preco"]
                self.precoCusto                    = data["preco_custo"]
                self.estoque_controlar             = data["estoque_controlar"]
                self.estoque_sobEncomenda          = data["estoque_sob_encomenda"]
                self.estoque_diasPreparacao        = data["estoque_dias_preparacao"]
                self.estoque_localizacao           = data["estoque_localizacao"]
                self.estoque_minimo                = data["estoque_minimo"]
                self.estoque_maximo                = data["estoque_maximo"]
                self.estoque_quantidade            = data["estoque_quantidade"]
                self.estoque_inicial               = data["estoque_inicial"]
                self.fornecedor_id                 = data["fornecedor_id"]
                self.fornecedor_codigo_produto     = data["fornecedor_codigo_produto"]
                self.tributacao_gtinEmbalagem      = data["gtin_embalagem"]

                return True

            except Exception as e:
                logger.error("Erro ao extrair dados do produto. Cód. %s. %s",data["sku"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    async def buscar(self, codprod:int=None) -> bool:
        """
        Busca os dados do produto no banco de dados utilizando os scripts e configurações Sankhya.

        Returns:
            bool: True se os dados foram encontrados e carregados, False caso contrário.
        """

        if not os.path.exists(configSankhya.PATH_SCRIPT_PRODUTO):
            logger.error("Script da TGFPRO não encontrado em %s",configSankhya.PATH_SCRIPT_PRODUTO)
            return pd.DataFrame()
        else:    
            db = dbConfig()
            with open(configSankhya.PATH_SCRIPT_PRODUTO, "r", encoding="utf-8") as f:
                query = f.read()
                
                try:
                    params = {
                        "COD": codprod or int(self.sku),
                        "ID": self.id
                    }
                    rows = await db.select(query=query,params=params)
                                        
                    if rows:
                        return self.decodificar(rows[0])
                    else:
                        return False
                except:
                    logger.error("Código do produto inválido %s",self.sku)
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
        
            