import os
import requests
import logging
from dotenv import load_dotenv
from olistApi.src.sankhya.connectTEST import Connect

load_dotenv('keys/.env')
logger = logging.getLogger(__name__)
logging.basicConfig(filename=os.getenv('PATH_LOGS'),
                    encoding='utf-8',
                    format=os.getenv('LOGGER_FORMAT'),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class Produto:

    def __init__(self):   
        self.con = Connect()     
        self.campos_lista = ["AD_MKP_CATEGORIA","AD_MKP_DESCRICAO","AD_MKP_DHATUALIZADO","AD_MKP_ESTPOL","AD_MKP_ESTREGBAR","AD_MKP_ESTMINTIP","AD_MKP_ESTMINVAL","AD_MKP_IDPROD","AD_MKP_IDPRODPAI","AD_MKP_INTEGRADO","AD_MKP_MARCA","AD_MKP_NOME","ALTURA","CODESPECST","CODPROD","CODVOL","DESCRPROD","ESPESSURA","ESTMAX","ESTMIN","LARGURA","NCM","ORIGPROD","PESOBRUTO","PESOLIQ","QTDEMB","REFERENCIA","REFFORN"]
        #self.campos_lista = ["AD_MKP_CATEGORIA","AD_MKP_DESCRICAO","AD_MKP_DHATUALIZADO","AD_MKP_ESTPOL","AD_MKP_ESTREGBAR","AD_MKP_ESTREGBARTIP","AD_MKP_ESTREGBARVAL","AD_MKP_IDPROD","AD_MKP_IDPRODPAI","AD_MKP_INTEGRADO","AD_MKP_MARCA","AD_MKP_NOME","ALTURA","CODESPECST","CODPROD","CODVOL","DESCRPROD","ESPESSURA","ESTMAX","ESTMIN","LARGURA","NCM","ORIGPROD","PESOBRUTO","PESOLIQ","QTDEMB","REFERENCIA","REFFORN"]

    def decodificar(self,data:dict=None) -> bool:
        if data.get('status') == str(1):
            columns = data['responseBody']['entities']['metadata']['fields']['field']
            rows = data['responseBody']['entities']['entity']
            dados_produto = {}
            for i, column in enumerate(columns):
                dados_produto[str.lower(column['name'])] = rows.get(f'f{i}').get('$')
            return dados_produto
        else:
            logger.error("Erro ao carregar dados do produto. %s",data.get('statusMessage'))
            return False

    async def buscar(self, codprod:int=None) -> bool:
        token = self.con.get_token()
        url = os.getenv('SANKHYA_URL_LOAD_RECORDS')
        res = requests.get(
            url=url,
            headers={ 'Authorization': token },
            json={
                "serviceName": "CRUDServiceProvider.loadRecords",
                "requestBody": {
                    "dataSet": {
                        "rootEntity": "Produto",
                        "includePresentationFields": "N",
                        "offsetPage": "0",
                        "criteria": {
                            "expression": {
                                "$": "this.CODPROD = ?"
                            },
                            "parameter": [
                                {
                                    "$": f"{codprod}",
                                    "type": "I"
                                }
                            ]
                        },
                        "entity": {
                            "fieldset": {
                                "list": ','.join(self.campos_lista)
                            }
                        }
                    }
                }
            })

        if res.status_code != 200:
            logger.error("Erro ao buscar produto. Cód. %s. %s",codprod,res.text)
            return False   
        else:
            return res.json()

    def prepapar_dados(self,payload:dict=None):
        dados = {}
        for i in payload:
            dados[f'{self.campos_lista.index(str.upper(i))}'] = f'{payload.get(i)}'
        return dados

    async def atualizar(self, codprod:int=None, payload:dict=None) -> bool:
        token = self.con.get_token()
        url = os.getenv('SANKHYA_URL_SAVE')
        res = requests.post(
            url=url,
            headers={ 'Authorization': token },
            json={
                "serviceName":"DatasetSP.save",
                "requestBody":{
                    "entityName":"Produto",
                    "standAlone":False,
                    "fields":self.campos_lista,
                    "records":[
                        {
                            "pk": {
                                "CODPROD": str(codprod)
                            },
                            "values": payload
                        }
                    ]
                }
            }
        )

        if res.status_code in (200,201):
            return True
        else:
            #logger.error("Erro ao atualizar produto. Cód. %s. %s",codprod,res.text)
            print(f"Erro ao atualizar produto. Cód. {codprod}. {res.text}")
            return False        
            