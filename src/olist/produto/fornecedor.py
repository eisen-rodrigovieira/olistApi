import logging
from params               import config, configOlist
from src.utils.validaPath import validaPath

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
    def __init__(self):
        """
        Inicializa um objeto Fornecedor com os dados fornecidos.

        Args:
            id (int): Identificador do fornecedor.
            nome (str): Nome do fornecedor.
            codigoProdutoNoFornecedor (str): Código do produto no fornecedor.
            padrao (bool): Indica se é o fornecedor padrão.
        """        
        self.id                        = None
        self.nome                      = None
        self.codigoProdutoNoFornecedor = None
        self.padrao                    = None
        self.valida_path               = validaPath()         

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

    async def encodificar(self) -> dict:
        """
        Constrói e retorna um dicionário com os dados do fornecedor, baseado em um template JSON.

        Returns:
            dict: Dicionário com os dados do fornecedor ou {"erro": True} em caso de falha.
        """        
        data = {}
        file_path = configOlist.PATH_OBJECT_PRODUTO_FORNECEDOR

        try:
            data = await self.valida_path.validar(path=file_path,mode='r',method='json')
            data["id"]                        = self.id
            data["nome"]                      = self.nome
            data["codigoProdutoNoFornecedor"] = self.codigoProdutoNoFornecedor
            data["padrao"]                    = self.padrao           
            return data               
        except Exception as e:
            logger.error("Erro ao formatar dicionario fornecedor de produto: %s",e)
            return {"erro":True}