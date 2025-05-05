from keys import keys
import oracledb
import pandas as pd

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

    def select(self, query: str, params:str= None) -> tuple[list, list]:
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
                    rows = cursor.fetchall()
                    cols = cursor.description
            return rows, cols
        except oracledb.DatabaseError as e:
            # Exibe erro detalhado caso ocorra uma exceção
            print("Erro ao executar a consulta:", e)
            raise  # Relança a exceção para que o chamador possa lidar com ela

    def insert(self, query: str, params: str) -> int:
        try:
            # Estabelece conexão com o banco de dados Oracle
            with oracledb.connect(user=self.usr, password=self.pwd, dsn=self.dns) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    registros = cursor.rowcount
            return registros
        except oracledb.DatabaseError as e:
            # Exibe erro detalhado caso ocorra uma exceção
            print("Erro ao inserir novos registros:", e)
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
            data.columns = [col[0] for col in columns]
            return data
        except Exception as e:
            print("Erro ao formatar os dados em DataFrame:", e)
            raise
