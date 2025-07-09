import logging
from params               import config, configOlist
from src.utils.validaPath import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Variacao:
    """
    Classe que representa uma variação de produto com preços, estoque e informações complementares.
    """    
    def __init__(self):
        self.valida_path            = validaPath() 
        self.id                     = None
        self.sku                    = None

    def decodificar(self,payload:dict=None) -> bool:
        """
        Preenche os atributos da variação a partir de um dicionário de dados.

        Returns:
            bool: True se os dados foram extraídos com sucesso, False em caso de erro.
        """        
        if payload:
            try:
                self.id                     = payload["id"]
                self.descricao              = payload["descricao"]
                self.sku                    = payload["sku"]
                self.gtin                   = payload["gtin"]
                self.preco                  = payload["precos"]["preco"]
                self.precoPromocional       = payload["precos"]["precoPromocional"]
                self.precoCusto             = payload["precos"]["precoCusto"]
                self.precoCustoMedio        = payload["precos"]["precoCustoMedio"]
                self.estoque_controlar      = payload["estoque"]["controlar"]
                self.estoque_sobEncomenda   = payload["estoque"]["sobEncomenda"]
                self.estoque_diasPreparacao = payload["estoque"]["diasPreparacao"]
                self.estoque_localizacao    = payload["estoque"]["localizacao"]
                self.estoque_minimo         = payload["estoque"]["minimo"]
                self.estoque_maximo         = payload["estoque"]["maximo"]
                self.estoque_quantidade     = payload["estoque"]["quantidade"]
                if payload.get('grade'):
                    self.grade = payload["grade"]
                else:
                    self.grade = None
            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    async def encodificar(self) -> dict:
        """
        Constrói e retorna um dicionário com os dados da variação baseado em um template JSON.

        Returns:
            dict: Dados formatados ou {"erro": True} em caso de falha.
        """        
        file_path = configOlist.PATH_OBJECT_PRODUTO_VARIACAO
        try:
            data = await self.valida_path.validar(path=file_path,mode='r',method='json')
            data = data.get('get')
            data["id"]                         = self.id
            data["descricao"]                  = self.descricao
            data["sku"]                        = self.sku
            data["gtin"]                       = self.gtin
            data["precos"]["preco"]            = self.preco
            data["precos"]["precoPromocional"] = self.precoPromocional
            data["precos"]["precoCusto"]       = self.precoCusto
            data["precos"]["precoCustoMedio"]  = self.precoCustoMedio
            data["estoque"]["controlar"]       = self.estoque_controlar
            data["estoque"]["sobEncomenda"]    = self.estoque_sobEncomenda
            data["estoque"]["diasPreparacao"]  = self.estoque_diasPreparacao
            data["estoque"]["localizacao"]     = self.estoque_localizacao
            data["estoque"]["minimo"]          = self.estoque_minimo
            data["estoque"]["maximo"]          = self.estoque_maximo
            data["estoque"]["quantidade"]      = self.estoque_quantidade
            data["grade"]                      = self.grade
            return data
        except Exception as e:
            logger.error("Erro ao formatar dicionario variacao de produto: %s",e)
            return {"erro":True} 