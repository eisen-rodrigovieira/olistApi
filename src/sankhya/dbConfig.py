from keys import keys
from params import config, configSankhya
import oracledb
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logging.basicConfig( filename = config.PATH_LOGS,
                     encoding = 'utf-8',
                     format   = config.LOGGER_FORMAT,
                     datefmt  = '%Y-%m-%d %H:%M:%S',
                     level    = logging.INFO)

class dbConfig(object):
    """
    Classe responsável por configurar a conexão com o banco de dados Oracle e executar consultas.
    """

    def __init__(self):
        """
        Inicializa a configuração da conexão utilizando variáveis do módulo config.
        """
        self.usr = keys.DATABASE_USERNAME
        self.pwd = keys.DATABASE_PASSWORD
        self.dns = keys.DATABASE_HOST

    def select(self, query: str, params:str= None) -> list:
        """
        Executa uma consulta SQL no banco de dados Oracle.

        Args:
            query (str): Consulta SQL a ser executada.
            params (str): Parâmetros para a consulta SQL.

        Returns:
            tuple: Uma tupla contendo:
                - lista de registros retornados,
                - metadados das colunas (descrição).

        Raises:
            oracledb.DatabaseError: Se ocorrer um erro na conexão ou execução da consulta.
        """
        try:
            # Estabelece conexão com o banco de dados Oracle
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
            # Exibe erro detalhado caso ocorra uma exceção
            print("Erro ao executar a consulta:", e)
            raise  # Relança a exceção para que o chamador possa lidar com ela

    def dml(self, query: str, params: str) -> tuple[bool,int]:
        try:
            # Estabelece conexão com o banco de dados Oracle
            with oracledb.connect(user=self.usr, password=self.pwd, dsn=self.dns) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    registros = cursor.rowcount
                    if registros:
                        connection.commit()
                        return True, registros
                    else:
                        connection.rollback()
                        return False, None            
        except oracledb.DatabaseError as e:
            # Exibe erro detalhado caso ocorra uma exceção
            print("Erro ao executar script:", e)
            raise  # Relança a exceção para que o chamador possa lidar com ela
    
    def format_dataframe(self, columns: list, rows: list) -> pd.DataFrame:
        """
        Formata os resultados de uma consulta SQL em um DataFrame do Pandas.

        Args:
            columns (list): Metadados das colunas (normalmente de cursor.description).
            rows (list): Lista de registros retornados pela consulta.

        Returns:
            pd.DataFrame: DataFrame contendo os dados formatados.

        Raises:
            ValueError: Se os dados de entrada forem inválidos.
        """
        try:
            if not rows:
                return pd.DataFrame()
            #    raise ValueError("A lista de linhas está vazia.")
            #if not columns:
            #    raise ValueError("A lista de colunas está vazia.")

            # Constrói o DataFrame a partir da primeira linha e transpoõe
            data = pd.DataFrame(rows[0]).T
            data.columns = [str(col[0]).lower() for col in columns]
            return data
        except Exception as e:
            print("Erro ao formatar os dados em DataFrame:", e)
            raise
