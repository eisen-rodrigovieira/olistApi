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
    """      

    def __init__(self):
        self.integrar_mkp                  = None
        self.id                            = None
        self.sku                           = None
        self.descricao                     = None
        self.descricaoFormatada            = None
        self.descricaoComplementar         = None
        self.tipo                          = None
        self.situacao                      = None
        self.produtoPai_id                 = None
        self.unidade                       = None
        self.unidadePorCaixa               = None
        self.ncm                           = None
        self.gtin                          = None
        self.origem                        = None
        self.cest                          = None
        self.garantia                      = None
        self.observacoes                   = None
        self.categoria_id                  = None
        self.categoria_nome                = None
        self.marca_id                      = None
        self.marca_nome                    = None
        self.dimensoes_embalagem_tipo      = None
        self.dimensoes_largura             = None
        self.dimensoes_altura              = None
        self.dimensoes_comprimento         = None
        self.dimensoes_pesoLiquido         = None
        self.dimensoes_pesoBruto           = None
        self.dimensoes_quantidadeVolumes   = None
        self.preco                         = None
        self.precoCusto                    = None
        self.estoque_controlar             = None
        self.estoque_sobEncomenda          = None
        self.estoque_diasPreparacao        = None
        self.estoque_localizacao           = None
        self.estoque_minimo                = None
        self.estoque_maximo                = None
        self.estoque_quantidade            = None
        self.estoque_inicial               = None
        self.fornecedor_id                 = None
        self.fornecedor_codigo_produto     = None
        self.tributacao_gtinEmbalagem      = None

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
        
            