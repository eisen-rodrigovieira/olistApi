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

class Producao:
    """
    Classe que representa um processo de produção de produto, incluindo etapas de produção.

    Atributos:
        produto_id (int): ID do produto.
        produto_sku (str): SKU do produto.
        produto_descricao (str): Descrição do produto.
        quantidade (int): Quantidade a ser produzida.
        etapas (list): Lista de etapas do processo de produção.
    """    
    def __init__(self
                ,produto_id        :int  = None
                ,produto_sku       :str  = None
                ,produto_descricao :str  = None
                ,quantidade        :int  = None
                ,etapas            :list = None
                ):
        self.produto_id        = produto_id
        self.produto_sku       = produto_sku
        self.produto_descricao = produto_descricao
        self.quantidade        = quantidade
        self.etapas            = etapas

    def decodificar(self,payload:dict=None) -> bool:
        """
        Preenche os atributos da produção a partir de um dicionário de dados.

        Returns:
            bool: True se os dados foram extraídos com sucesso, False em caso de erro.
        """        
        if payload:
            try:
                self.produto_id        = payload["produto_id"]
                self.produto_sku       = payload["produto_sku"]
                self.produto_descricao = payload["produto_descricao"]
                self.quantidade        = payload["quantidade"]
                self.etapas            = payload["etapas"]
                return True
            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    def encodificar(self) -> dict:
        """
        Constrói e retorna um dicionário com os dados de produção baseado em um template JSON.

        Returns:
            dict: Dados formatados ou {"erro": True} em caso de falha.
        """        
        data = {}
        try:
            if not os.path.exists(configOlist.PATH_OBJECT_PRODUTO_PRODUCAO):
                logger.error("Objeto do kit de produto não encontrado em %s",configOlist.PATH_OBJECT_PRODUTO_PRODUCAO)
                return {"erro":True}
            else:    
                with open(configOlist.PATH_OBJECT_PRODUTO_PRODUCAO, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["produto_id"]        = self.produto_id
                data["produto_sku"]       = self.produto_sku
                data["produto_descricao"] = self.produto_descricao
                data["quantidade"]        = self.quantidade
                data["etapas"]            = self.etapas
                return data               
        except Exception as e:
            logger.error("Erro ao formatar dicionario producao de produto: %s",e)
            return {"erro":True} 
