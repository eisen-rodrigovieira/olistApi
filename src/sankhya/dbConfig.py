import logging
import oracledb
import pandas as pd
from keys   import keys
from params import config

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

class dbConfig(object):

    """
    Classe responsável pela configuração e execução de operações com banco de dados Oracle.

    Essa classe fornece métodos para realizar consultas (SELECT), comandos DML (INSERT, UPDATE)
    e exclusões (DELETE), além de formatar os resultados em DataFrames do Pandas.
    """

    def __init__(self):
        """
        Inicializa a configuração de conexão ao banco de dados utilizando as credenciais fornecidas no módulo `keys`.
        """        
        self.usr = keys.DATABASE_USERNAME
        self.pwd = keys.DATABASE_PASSWORD
        self.dns = keys.DATABASE_HOST

    async def select(self, query: str, params:str= None) -> list:
        """
        Executa uma consulta SELECT no banco de dados Oracle.

        Args:
            query (str): Consulta SQL a ser executada.
            params (str, opcional): Parâmetros para a consulta.

        Returns:
            list: Lista de dicionários representando os registros retornados.
        """        
        try:
            with oracledb.connect(user=self.usr, password=self.pwd, dsn=self.dns) as connection:
                with connection.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    
                    cols = [col.name.lower() for col in cursor.description]
                    cursor.rowfactory = lambda *args: dict(zip(cols, args))
                    rows = cursor.fetchall()
                    for r in rows:
                        for k in r.keys():
                            if type(r[k]) == oracledb.LOB:
                                r[k] = r[k].read()                    
            return rows
        except oracledb.DatabaseError as e:
            logger.error("Erro ao executar a consulta:", e)
            return []

    async def dml(self, query: str, params: str=None) -> tuple[bool,int]:
        """
        Executa um comando DML (INSERT, UPDATE ou DELETE) no banco de dados Oracle.

        Args:
            query (str): Comando SQL DML a ser executado.
            params (str, opcional): Parâmetros para o comando.

        Returns:
            tuple: Tupla contendo um booleano indicando sucesso e o número de registros afetados ou None.
        """        
        try:
            with oracledb.connect(user=self.usr, password=self.pwd, dsn=self.dns) as connection:
                with connection.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    registros = cursor.rowcount
                    if registros:
                        connection.commit()
                        return True, registros
                    else:
                        connection.rollback()
                        return False, None            
        except oracledb.DatabaseError as e:
            logger.error("Erro ao executar script:", e)
            return False, None

    async def call(self, query: str, params: str=None) -> bool:
        """
        Executa uma chamada de procedure no banco de dados Oracle.

        Args:
            query (str): Comando SQL a ser executado.
            params (str, opcional): Parâmetros para o comando.

        Returns:
            bool: Um booleano indicando sucesso
        """        
        try:
            with oracledb.connect(user=self.usr, password=self.pwd, dsn=self.dns) as connection:
                with connection.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    connection.commit()
                    return True
        except oracledb.DatabaseError as e:
            logger.error("Erro ao executar chamada de procedure:", e)
            return False
