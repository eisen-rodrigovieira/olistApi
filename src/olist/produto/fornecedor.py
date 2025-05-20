import os
import json
import logging
from params import config, configOlist

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Fornecedor:
    """
    Classe que representa um fornecedor de produto, contendo informações como nome, código do produto
    no fornecedor e se é o fornecedor padrão.

    Atributos:
        id (int): Identificador único do fornecedor.
        nome (str): Nome do fornecedor.
        codigoProdutoNoFornecedor (str): Código do produto no sistema do fornecedor.
        padrao (bool): Indica se é o fornecedor padrão.
    """    
    def __init__(self
                ,id:int=None
                ,nome:str=None
                ,codigoProdutoNoFornecedor:str=None
                ,padrao:bool=None
                ):
        """
        Inicializa um objeto Fornecedor com os dados fornecidos.

        Args:
            id (int): Identificador do fornecedor.
            nome (str): Nome do fornecedor.
            codigoProdutoNoFornecedor (str): Código do produto no fornecedor.
            padrao (bool): Indica se é o fornecedor padrão.
        """        
        self.id                        = id
        self.nome                      = nome
        self.codigoProdutoNoFornecedor = codigoProdutoNoFornecedor
        self.padrao                    = padrao

    def decodificar(self,payload:dict=None) -> bool:
        """
        Preenche os atributos do fornecedor a partir de um dicionário de dados (payload).

        Args:
            payload (dict): Dicionário com os dados do fornecedor.

        Returns:
            bool: True se os dados foram extraídos com sucesso, False em caso de erro.
        """        
        if payload:
            try:
                self.id                        = payload["id"]
                self.nome                      = payload["nome"]
                self.codigoProdutoNoFornecedor = payload["codigoProdutoNoFornecedor"]
                # self.padrao                    = payload["padrao"]
            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    def encodificar(self) -> dict:
        """
        Constrói e retorna um dicionário com os dados do fornecedor, baseado em um template JSON.

        Returns:
            dict: Dicionário com os dados do fornecedor ou {"erro": True} em caso de falha.
        """        
        data = {}
        try:
            if not os.path.exists(configOlist.PATH_OBJECT_PRODUTO_FORNECEDOR):
                logger.error("Objeto do fornecedor de produto não encontrado em %s",configOlist.PATH_OBJECT_PRODUTO_FORNECEDOR)
                return {"erro":True}
            else:    
                with open(configOlist.PATH_OBJECT_PRODUTO_FORNECEDOR, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["id"]                        = self.id
                data["nome"]                      = self.nome
                data["codigoProdutoNoFornecedor"] = self.codigoProdutoNoFornecedor
                data["padrao"]                    = self.padrao           
                return data               
        except Exception as e:
            logger.error("Erro ao formatar dicionario fornecedor de produto: %s",e)
            return {"erro":True}