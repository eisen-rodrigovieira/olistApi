import logging
from params               import config, configOlist
from src.utils.validaPath import validaPath

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Anexo:
    """
    Classe que representa um anexo de produto, contendo a URL do recurso e a indicação
    se ele é externo.

    Atributos:
        url (str): Endereço do recurso anexo.
        externo (bool): Indica se o anexo está hospedado externamente.
    """

    def __init__(self):
        self.url         = None
        self.externo     = None
        self.valida_path = validaPath()        

    def decodificar(self,payload:dict=None):
        """
        Preenche os atributos do anexo a partir de um dicionário de dados (payload).

        Args:
            payload (dict): Dicionário contendo os dados do anexo.

        Returns:
            bool: True se os dados foram extraídos com sucesso, False em caso de erro.
        """        
        if payload:
            try:
                self.url     = payload["url"]
                self.externo = payload["externo"]
            except Exception as e:
                logger.error("Erro ao extrair dados do payload. ID %s. %s",payload["id"],e)
                return False
        else:
            logger.error("Não foram informados dados para decodificar")
            return False

    async def encodificar(self) -> dict:
        """
        Constrói e retorna um dicionário com os dados do anexo, baseado em um template JSON.

        Returns:
            dict: Dicionário com os dados do anexo formatado ou {"erro": True} em caso de falha.
        """        
        data = {}
        file_path = configOlist.PATH_OBJECT_PRODUTO_ANEXO        
        try:
            data = await self.valida_path.validar(path=file_path,mode='r',method='json')
            data["url"]     = self.url
            data["externo"] = self.externo
            return data               
        except Exception as e:
            logger.error("Erro ao formatar dicionario anexo de produto: %s",e)
            return {"erro":True} 