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

class Variacao:
    """
    Classe que representa uma variação de produto com preços, estoque e informações complementares.

    Atributos:
        id (int): ID da variação.
        descricao (str): Descrição da variação.
        sku (str): SKU da variação.
        gtin (str): Código GTIN (EAN).
        preco (float): Preço de venda.
        precoPromocional (float): Preço promocional.
        precoCusto (float): Preço de custo.
        precoCustoMedio (float): Preço de custo médio.
        estoque_controlar (bool): Controle de estoque habilitado.
        estoque_sobEncomenda (bool): Produto sob encomenda.
        estoque_diasPreparacao (int): Dias de preparação.
        estoque_localizacao (str): Localização no estoque.
        estoque_minimo (int): Estoque mínimo.
        estoque_maximo (int): Estoque máximo.
        estoque_quantidade (int): Quantidade disponível.
        estoque_inicial (int): Quantidade inicial.
        grade (list): Lista de variações por grade.
    """    
    def __init__(self
                ,id                     :int   = None
                ,descricao              :str   = None
                ,sku                    :str   = None
                ,gtin                   :str   = None
                ,preco                  :float = None
                ,precoPromocional       :float = None
                ,precoCusto             :float = None
                ,precoCustoMedio        :float = None
                ,estoque_controlar      :bool  = None
                ,estoque_sobEncomenda   :bool  = None
                ,estoque_diasPreparacao :int   = None
                ,estoque_localizacao    :str   = None
                ,estoque_minimo         :int   = None
                ,estoque_maximo         :int   = None
                ,estoque_quantidade     :int   = None
                ,estoque_inicial        :int   = None
                ,grade                  :list  = None
                ):
        self.id                     = id
        self.descricao              = descricao
        self.sku                    = sku
        self.gtin                   = gtin
        self.preco                  = preco
        self.precoPromocional       = precoPromocional
        self.precoCusto             = precoCusto
        self.precoCustoMedio        = precoCustoMedio
        self.estoque_controlar      = estoque_controlar
        self.estoque_sobEncomenda   = estoque_sobEncomenda
        self.estoque_diasPreparacao = estoque_diasPreparacao
        self.estoque_localizacao    = estoque_localizacao
        self.estoque_minimo         = estoque_minimo
        self.estoque_maximo         = estoque_maximo
        self.estoque_quantidade     = estoque_quantidade
        self.estoque_inicial        = estoque_inicial
        self.grade                  = grade

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
                self.estoque_inicial        = payload["estoque"]["inicial"]
                self.grade                  = payload["grade"]
            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    def encodificar(self) -> dict:
        """
        Constrói e retorna um dicionário com os dados da variação baseado em um template JSON.

        Returns:
            dict: Dados formatados ou {"erro": True} em caso de falha.
        """        
        data = {}
        try:
            if not os.path.exists(configOlist.PATH_OBJECT_PRODUTO_VARIACAO):
                logger.error("Objeto da variacao de produto não encontrado em %s",configOlist.PATH_OBJECT_PRODUTO_VARIACAO)
                return {"erro":True}
            else:    
                with open(configOlist.PATH_OBJECT_PRODUTO_VARIACAO, "r", encoding="utf-8") as f:
                    data = json.load(f)

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
                data["estoque"]["inicial"]         = self.estoque_inicial    
                data["grade"]                      = self.grade 
                return data               
        except Exception as e:
            logger.error("Erro ao formatar dicionario variacao de produto: %s",e)
            return {"erro":True} 