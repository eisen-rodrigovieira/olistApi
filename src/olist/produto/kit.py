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

class Kit:
    """
    Classe que representa um item de kit de produto, com referência a outro produto, quantidade e informações de identificação.

    Atributos:
        produto_id (int): ID do produto que compõe o kit.
        produto_sku (str): SKU do produto que compõe o kit.
        produto_descricao (str): Descrição do produto.
        quantidade (int): Quantidade do produto no kit.
    """    
    def __init__(self
                ,produto_id        :int = None
                ,produto_sku       :str = None
                ,produto_descricao :str = None
                ,quantidade        :int = None
                ):
        self.produto_id        = produto_id
        self.produto_sku       = produto_sku
        self.produto_descricao = produto_descricao
        self.quantidade        = quantidade

    def decodificar(self,payload:dict=None) -> bool:
        """
        Preenche os atributos do kit a partir de um dicionário de dados.

        Returns:
            bool: True se os dados foram extraídos com sucesso, False em caso de erro.
        """        
        if payload:
            try:
                self.produto_id        = payload["produto"]["id"]
                self.produto_sku       = payload["produto"]["sku"]
                self.produto_descricao = payload["produto"]["descricao"]
                self.quantidade        = payload["quantidade"]
                return True
            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    def encodificar(self) -> dict:
        """
        Constrói e retorna um dicionário com os dados do kit baseado em um template JSON.

        Returns:
            dict: Dados formatados ou {"erro": True} em caso de falha.
        """        
        data = {}
        try:
            if not os.path.exists(configOlist.PATH_OBJECT_PRODUTO_KIT):
                logger.error("Objeto do kit de produto não encontrado em %s",configOlist.PATH_OBJECT_PRODUTO_KIT)
                return {"erro":True}
            else:    
                with open(configOlist.PATH_OBJECT_PRODUTO_KIT, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["produto"]["id"]        = self.produto_id
                data["produto"]["sku"]       = self.produto_sku
                data["produto"]["descricao"] = self.produto_descricao
                data["quantidade"]        = self.quantidade
                return data               
        except Exception as e:
            logger.error("Erro ao formatar dicionario kit de produto: %s",e)
            return {"erro":True} 
