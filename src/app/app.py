import re
import time
import json
import logging
from datetime                    import datetime
from selenium                    import webdriver
from params                      import config,configUtils,configOlist,configSankhya
from src.olist.produto.produto   import Produto as olProduto
from src.olist.pedido.pedido     import Pedido  as olPedido
from src.olist.estoque.estoque   import Estoque as olEstoque
from src.olist.nota.nota         import Nota    as olNota
from src.sankhya.produto.produto import Produto as snkProduto
from src.sankhya.pedido.pedido   import Pedido  as snkPedido
from src.sankhya.estoque.estoque import Estoque as snkEstoque
from src.sankhya.dbConfig        import dbConfig
from src.utils.sendMail          import sendMail
from src.utils.validaPath        import validaPath
from src.utils.bot               import Bot

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class App:

    def __init__(self):
        self.req_sleep       = config.REQ_TIME_SLEEP
        self.db              = dbConfig()
        self.email_body_path = configUtils.BODY_HTML
        self.email           = sendMail()
        self.valida_path     = validaPath()   

    class Produto:

        def __init__(self):
            self.app = App()
            self.contexto = '#Produtos# '

        async def atualiza_historico(self, produto_alterado:int=None, produto_incluido:int=None, sentido:int=None):
            file_path = configOlist.PATH_HISTORICO_PRODUTO
            historico = await self.app.valida_path.validar(path=file_path,mode='r',method='json')

            if not historico:
                return {"status":"Erro"}
            else:
                if produto_alterado and not produto_incluido:
                    if sentido == 0: # SANKHYA > OLIST
                        historico["ultima_atualizacao_sankhya_olist"]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        historico["ultima_atualizacao_sankhya_olist"]["id"] = produto_alterado
                    elif sentido == 1: # OLIST > SANKHYA
                        historico["ultima_atualizacao_olist_sankhya"]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        historico["ultima_atualizacao_olist_sankhya"]["id"] = produto_alterado
                    else:
                        pass
                elif produto_incluido and not produto_alterado:
                    historico["ultima_inclusao_olist"]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    historico["ultima_inclusao_olist"]["id"] = produto_incluido

                await self.app.valida_path.validar(path=file_path,mode='w',method='json',content=historico)

        async def remove_syncprod(self,produto:int=None,dhevento:datetime=None) -> bool:
            if produto and dhevento:
                file_path_del   = configSankhya.PATH_DELETE_SYNCPROD
                delete_syncprod = await self.app.valida_path.validar(path=file_path_del,method='full',mode='r')
                params = {
                    "CODPROD" : produto,
                    "DHEVENTO" : dhevento
                }
                ack, rows = await self.app.db.dml(query=delete_syncprod,params=params)
                return ack
            else:
                return False
            
        async def atualiza_produto_novo(self,produto:int=None,id:int=None) -> bool:
            if produto and id:
                file_path = configSankhya.PATH_UPDATE_PRODUTO_NEW
                new_syncprod = await self.app.valida_path.validar(path=file_path,method='full',mode='r')
                params = {
                    "CODPROD" : produto,
                    "AD_MKP_IDPROD" : id
                }
                ack, rows = await self.app.db.dml(query=new_syncprod,params=params)
                return ack
            else:
                return False

        async def snk_atualizar_produtos(self) -> tuple[bool,list]:

            regex_cest_ncm = r"[.]"
            res = []
                
            print("Iniciando busca dos produtos com alteração no Olist.")
            _olProd = olProduto()
            produtos_com_alteracao = await _olProd.enviar_alteracoes()
            if produtos_com_alteracao:
                print(f"{len(produtos_com_alteracao)} produtos com alteração encontrados.")
                for produto in produtos_com_alteracao:
                    snkProd = snkProduto()
                    olProd  = olProduto()
                    if produto["sku"]:
                        time.sleep(self.app.req_sleep)             
                        snkProd.sku = produto["sku"]
                        olProd.id   = produto["id"]
                        if await olProd.buscar():
                            if olProd.tipo == 'S' and olProd.sku and await snkProd.buscar():
                                olProd.ncm = re.sub(regex_cest_ncm, '', olProd.ncm)
                                new_id                          = olProd.id                          if int(snkProd.id or 0)                          != int(olProd.id or 0)                          else None
                                # new_sku                         = olProd.sku                         if int(snkProd.sku or 0)                         != int(olProd.sku or 0)                         else None
                                new_descricao                   = olProd.descricao                   if snkProd.descricao                             != olProd.descricao                             else None
                                new_descricaoComplementar       = olProd.descricaoComplementar       if snkProd.descricaoComplementar                 != olProd.descricaoComplementar                 else None
                                # new_tipo                        = olProd.tipo                        if snkProd.tipo                                  != olProd.tipo                                  else None
                                # new_situacao                    = olProd.situacao                    if snkProd.situacao                              != olProd.situacao                              else None
                                new_produtoPai_id               = olProd.produtoPai_id               if int(snkProd.produtoPai_id or 0)               != int(olProd.produtoPai_id or 0)               else None
                                #new_unidade                     = olProd.unidade                     if snkProd.unidade                               != olProd.unidade                               else None
                                # new_unidadePorCaixa             = olProd.unidadePorCaixa             if int(snkProd.unidadePorCaixa or 0)             != int(olProd.unidadePorCaixa or 0)             else None
                                #new_ncm                         = olProd.ncm                         if snkProd.ncm                                   != olProd.ncm                                   else None
                                #new_gtin                        = olProd.gtin                        if snkProd.gtin                                  != olProd.gtin                                  else None
                                #new_origem                      = olProd.origem                      if int(snkProd.origem or 0)                      != int(olProd.origem or 0)                      else None
                                # new_cest                        = olProd.cest                        if snkProd.cest                                  != olProd.cest                                  else None
                                # new_garantia                    = olProd.garantia                    if snkProd.garantia                              != olProd.garantia                              else None
                                # new_observacoes                 = olProd.observacoes                 if snkProd.observacoes                           != olProd.observacoes                           else None
                                new_categoria_id                = olProd.categoria_id                if int(snkProd.categoria_id or 0)                != int(olProd.categoria_id or 0)                else None
                                #new_categoria_nome              = olProd.categoria_caminhoCompleto   if snkProd.categoria_nome                        != olProd.categoria_nome                        else None
                                new_marca_id                    = olProd.marca_id                    if int(snkProd.marca_id or 0)                    != int(olProd.marca_id or 0)                    else None
                                # new_marca_nome                  = olProd.marca_nome                  if snkProd.marca_nome                            != olProd.marca_nome                            else None
                                # new_dimensoes_embalagem_tipo    = olProd.dimensoes_embalagem_tipo    if snkProd.dimensoes_embalagem_tipo              != olProd.dimensoes_embalagem_tipo              else None
                                new_dimensoes_largura           = olProd.dimensoes_largura           if float(snkProd.dimensoes_largura or 0)         != float(olProd.dimensoes_largura or 0)         else None
                                new_dimensoes_altura            = olProd.dimensoes_altura            if float(snkProd.dimensoes_altura or 0)          != float(olProd.dimensoes_altura or 0)          else None
                                new_dimensoes_comprimento       = olProd.dimensoes_comprimento       if float(snkProd.dimensoes_comprimento or 0)     != float(olProd.dimensoes_comprimento or 0)     else None
                                new_dimensoes_pesoLiquido       = olProd.dimensoes_pesoLiquido       if float(snkProd.dimensoes_pesoLiquido or 0)     != float(olProd.dimensoes_pesoLiquido or 0)     else None
                                new_dimensoes_pesoBruto         = olProd.dimensoes_pesoBruto         if float(snkProd.dimensoes_pesoBruto or 0)       != float(olProd.dimensoes_pesoBruto or 0)       else None
                                new_dimensoes_quantidadeVolumes = olProd.dimensoes_quantidadeVolumes if int(snkProd.dimensoes_quantidadeVolumes or 0) != int(olProd.dimensoes_quantidadeVolumes or 0) else None
                                # new_preco                       = olProd.preco                       if float(snkProd.preco or 0)                     != float(olProd.preco or 0)                     else None
                                # new_precoCusto                  = olProd.precoCusto                  if float(snkProd.precoCusto or 0)                != float(olProd.precoCusto or 0)                else None
                                # new_estoque_controlar           = olProd.estoque_controlar           if snkProd.estoque_controlar                     != olProd.estoque_controlar                     else None
                                # new_estoque_sobEncomenda        = olProd.estoque_sobEncomenda        if snkProd.estoque_sobEncomenda                  != olProd.estoque_sobEncomenda                  else None
                                # new_estoque_diasPreparacao      = olProd.estoque_diasPreparacao      if int(snkProd.estoque_diasPreparacao or 0)      != int(olProd.estoque_diasPreparacao or 0)      else None
                                # new_estoque_localizacao         = olProd.estoque_localizacao         if snkProd.estoque_localizacao                   != olProd.estoque_localizacao                   else None
                                new_estoque_minimo              = olProd.estoque_minimo              if int(snkProd.estoque_minimo or 0)              != int(olProd.estoque_minimo or 0)              else None
                                new_estoque_maximo              = olProd.estoque_maximo              if int(snkProd.estoque_maximo or 0)              != int(olProd.estoque_maximo or 0)              else None
                                # new_estoque_quantidade          = olProd.estoque_quantidade          if int(snkProd.estoque_quantidade or 0)          != int(olProd.estoque_quantidade or 0)          else None
                                # new_estoque_inicial             = olProd.estoque_inicial             if int(snkProd.estoque_inicial or 0)             != int(olProd.estoque_inicial or 0)             else None
                                # new_tributacao_gtinEmbalagem    = olProd.tributacao_gtinEmbalagem    if snkProd.tributacao_gtinEmbalagem              != olProd.tributacao_gtinEmbalagem              else None

                                if olProd.fornecedores:
                                    # new_fornecedor_id             = olProd.fornecedores[0].id  if int(snkProd.fornecedor_id or 0) != int(olProd.fornecedores[0].id or 0) else None
                                    new_fornecedor_codigo_produto = olProd.fornecedores[0].codigoProdutoNoFornecedor if snkProd.fornecedor_codigo_produto != olProd.fornecedores[0].codigoProdutoNoFornecedor else None
                                else:
                                    #new_fornecedor_id             = None
                                    new_fornecedor_codigo_produto = None  

                                with open(configSankhya.PATH_PARAMS_UPDATE_PRODUTO, "r", encoding="utf-8") as f:
                                    params = json.load(f)
                                params['COD']                       = snkProd.sku
                                params['ID']                        = new_id
                                params['DESCRICAO']                 = new_descricao
                                params['DESCRICAO_COMPLEMENTAR']    = new_descricaoComplementar
                                params['PRODUTO_PAI_ID']            = new_produtoPai_id
                                #params['UNIDADE']                   = new_unidade
                                params['ID_MARCA']                  = new_marca_id
                                #params['NCM']                       = new_ncm
                                #params['GTIN']                      = new_gtin
                                #params['ORIGEM']                    = new_origem
                                #params['CEST']                      = snkProd.cest
                                params['ID_CATEGORIA']              = new_categoria_id
                                # params['LARGURA']                   = new_dimensoes_largura
                                # params['ALTURA']                    = new_dimensoes_altura
                                # params['ESPESSURA']                 = new_dimensoes_comprimento
                                # params['PESO_LIQUIDO']              = new_dimensoes_pesoLiquido
                                # params['PESO_BRUTO']                = new_dimensoes_pesoBruto
                                # params['QUANTIDADE_VOLUMES']        = new_dimensoes_quantidadeVolumes
                                # params['ESTOQUE_MINIMO']            = new_estoque_minimo
                                # params['ESTOQUE_MAXIMO']            = new_estoque_maximo                                
                                # params['FORNECEDOR_CODIGO_PRODUTO'] = new_fornecedor_codigo_produto     

                                necessita_atualizar = 0
                                for value in params.values():
                                    if not (value is None or value == ''): necessita_atualizar+=1
                                if necessita_atualizar > 1:
                                    ack, num = await snkProd.atualizar(params=params)
                                    if ack:
                                        logger.info(self.contexto+"Produto %s atualizado com sucesso.",snkProd.sku)
                                        res.append(f"Produto {snkProd.sku} atualizado com sucesso.")                                        
                                        print(f"Produto {snkProd.sku} atualizado com sucesso.")
                                        await self.atualiza_historico(produto_alterado=snkProd.id,sentido=1)
                                    else:
                                        logger.error(self.contexto+"Falha ao atualizar os dados do produto %s na base Sankhya. Verifique os logs.",snkProd.id)
                                        await self.app.email.notificar()
                                        res.append(f"Falha ao atualizar os dados do produto {snkProd.id} na base Sankhya. Verifique os logs.")
                                        print(f"Falha ao atualizar os dados do produto {snkProd.id} na base Sankhya. Verifique os logs.")
                                else:
                                    logger.info(self.contexto+"Produto %s sem atualizações a serem sincronizadas Olist > Sankhya",snkProd.id) 
                                    res.append(f"Produto {snkProd.id} sem atualizações a serem sincronizadas Olist > Sankhya")
                                    print(f"Produto {snkProd.id} sem atualizações a serem sincronizadas Olist > Sankhya") 
                            else:
                                logger.warning(self.contexto+"Produto %s não tem vínculo com o Sankhya (SKU em branco ou inválido)",olProd.id) 
                                await self.app.email.notificar(tipo='alerta')
                                res.append(f"Produto {olProd.id} não tem vínculo com o Sankhya (SKU em branco ou inválido)") 
                                print(f"Produto {olProd.id} não tem vínculo com o Sankhya (SKU em branco ou inválido)") 
                        else:
                            logger.error(self.contexto+"Falha ao buscar os dados do produto %s na base Olist. Verifique os logs.",olProd.id)
                            await self.app.email.notificar()
                            res.append(f"Falha ao buscar os dados do produto {olProd.id} na base Olist. Verifique os logs.")
                            print(f"Falha ao buscar os dados do produto {olProd.id} na base Olist. Verifique os logs.")
                    else:
                        olProd.id = produto["id"]
                        await olProd.buscar()
                        if olProd.tipo == 'K':
                            logger.warning(self.contexto+"Produto %s é Kit (não tem vínculo com o Sankhya por SKU)",olProd.id)
                            res.append(f"Produto {olProd.id} é Kit (não tem vínculo com o Sankhya por SKU)") 
                            print(f"Produto {olProd.id} é mestre (não tem vínculo com o Sankhya por SKU)") 
                        elif olProd.tipo == 'V':
                            logger.warning(self.contexto+"Produto %s é Mestre (não tem vínculo com o Sankhya por SKU)",olProd.id)
                            res.append(f"Produto {olProd.id} é Mestre (não tem vínculo com o Sankhya por SKU)") 
                            print(f"Produto {olProd.id} é mestre (não tem vínculo com o Sankhya por SKU)") 
                        elif olProd.tipo == 'S':
                            logger.warning(self.contexto+"Produto %s é Simples mas não tem vínculo com o Sankhya por SKU",olProd.id) 
                            await self.app.email.notificar(tipo='alerta')
                            res.append(f"Produto {olProd.id} é Simples mas não tem vínculo com o Sankhya por SKU")
                            print(f"Produto {olProd.id} é Simples mas não tem vínculo com o Sankhya por SKU")
                        else:
                            logger.warning(self.contexto+"Produto %s não tem vínculo com o Sankhya (sem SKU)",produto["id"])
                            await self.app.email.notificar(tipo='alerta')
                            res.append(f"Produto {produto["id"]} não tem vínculo com o Sankhya (sem SKU)")
                            print(f"Produto {produto["id"]} não tem vínculo com o Sankhya (sem SKU)")
                print("Rotina concluída.")   
                return True, res        
            else: 
                res.append("Nenhuma alteração para ser importada no Sankhya")
                print("Nenhuma alteração para ser importada no Sankhya")
                return True, res

        async def ol_atualizar_produtos(self) -> tuple[bool,list]:
            
            regex_cest_ncm = r"[.]"
            values = []
            fetch = None
            file_path_fetch = configSankhya.PATH_SCRIPT_SYNCPROD 
            query_syncprod = await self.app.valida_path.validar(path=file_path_fetch,method='full',mode='r')
            fetch = await self.app.db.select(query=query_syncprod)            
            if fetch:            
                print(f"{len(fetch)} alterações encontradas.")           
                for f in fetch:
                    ackOl = ackSnk = None
                    time.sleep(self.app.req_sleep)
                    if f["evento"] == 'A':                        
                        olProd  = olProduto()
                        snkProd = snkProduto()
                        olProd.id = f["idprod"]
                        if await olProd.buscar():
                            ackOl = True
                        else:
                            logger.error(self.contexto+"Falha ao buscar os dados do produto %s na base Olist. Verifique os logs.",f["idprod"])
                            await self.app.email.notificar()
                            values.append(f"Falha ao buscar os dados do produto {f["idprod"]} na base Olist. Verifique os logs.")
                            print(f"Falha ao buscar os dados do produto {f["idprod"]} na base Olist. Verifique os logs.")
                        snkProd.sku = f["codprod"]
                        if await snkProd.buscar():
                            ackSnk = True
                        else: 
                            logger.error(self.contexto+"Falha ao buscar os dados do produto %s na base Sankhya. Verifique os logs.",f["codprod"])
                            await self.app.email.notificar()
                            values.append(f"Falha ao buscar os dados do produto {f["codprod"]} na base Sankhya. Verifique os logs.")
                            print(f"Falha ao buscar os dados do produto {f["codprod"]} na base Sankhya. Verifique os logs.")
                        if ackOl and ackSnk:
                            olProd.ncm = re.sub(regex_cest_ncm, '', olProd.ncm)
                            olProd.descricao                   = snkProd.descricao                   if snkProd.descricao                             != olProd.descricao                             else olProd.descricao
                            olProd.descricaoComplementar       = snkProd.descricaoComplementar       if snkProd.descricaoComplementar                 != olProd.descricaoComplementar                 else olProd.descricaoComplementar
                            olProd.tipo                        = snkProd.tipo                        if snkProd.tipo                                  != olProd.tipo                                  else olProd.tipo
                            olProd.situacao                    = snkProd.situacao                    if snkProd.situacao                              != olProd.situacao                              else olProd.situacao
                            # olProd.produtoPai_id               = snkProd.produtoPai_id               if int(snkProd.produtoPai_id or 0)               != int(olProd.produtoPai_id or 0)               else olProd.produtoPai_id
                            olProd.unidade                     = snkProd.unidade                     if snkProd.unidade                               != olProd.unidade                               else olProd.unidade
                            olProd.unidadePorCaixa             = snkProd.unidadePorCaixa             if int(snkProd.unidadePorCaixa or 0)             != int(olProd.unidadePorCaixa or 0)             else olProd.unidadePorCaixa
                            olProd.ncm                         = snkProd.ncm                         if snkProd.ncm                                   != olProd.ncm                                   else olProd.ncm
                            olProd.gtin                        = snkProd.gtin                        if snkProd.gtin                                  != olProd.gtin                                  else olProd.gtin
                            olProd.origem                      = snkProd.origem                      if snkProd.origem                                != olProd.origem                                else olProd.origem
                            olProd.cest                        = str(snkProd.cest)
                            olProd.garantia                    = snkProd.garantia                    if snkProd.garantia                              != olProd.garantia                              else olProd.garantia
                            olProd.observacoes                 = snkProd.observacoes                 if snkProd.observacoes                           != olProd.observacoes                           else olProd.observacoes
                            olProd.categoria_id                = snkProd.categoria_id                if snkProd.categoria_id                          != olProd.categoria_id                          else olProd.categoria_id
                            olProd.marca_id                    = snkProd.marca_id                    if snkProd.marca_id                              != olProd.marca_id                              else olProd.marca_id
                            olProd.dimensoes_embalagem_tipo    = snkProd.dimensoes_embalagem_tipo    if snkProd.dimensoes_embalagem_tipo              != olProd.dimensoes_embalagem_tipo              else olProd.dimensoes_embalagem_tipo
                            olProd.dimensoes_largura           = snkProd.dimensoes_largura           if float(snkProd.dimensoes_largura or 0)         != float(olProd.dimensoes_largura or 0)         else olProd.dimensoes_largura
                            olProd.dimensoes_altura            = snkProd.dimensoes_altura            if float(snkProd.dimensoes_altura or 0)          != float(olProd.dimensoes_altura or 0)          else olProd.dimensoes_altura
                            olProd.dimensoes_comprimento       = snkProd.dimensoes_comprimento       if float(snkProd.dimensoes_comprimento or 0)     != float(olProd.dimensoes_comprimento or 0)     else olProd.dimensoes_comprimento
                            olProd.dimensoes_pesoLiquido       = snkProd.dimensoes_pesoLiquido       if float(snkProd.dimensoes_pesoLiquido or 0)     != float(olProd.dimensoes_pesoLiquido or 0)     else olProd.dimensoes_pesoLiquido
                            olProd.dimensoes_pesoBruto         = snkProd.dimensoes_pesoBruto         if float(snkProd.dimensoes_pesoBruto or 0)       != float(olProd.dimensoes_pesoBruto or 0)       else olProd.dimensoes_pesoBruto
                            olProd.dimensoes_quantidadeVolumes = snkProd.dimensoes_quantidadeVolumes if int(snkProd.dimensoes_quantidadeVolumes or 0) != int(olProd.dimensoes_quantidadeVolumes or 0) else olProd.dimensoes_quantidadeVolumes
                            olProd.preco                       = snkProd.preco                       if float(snkProd.preco or 0)                     != float(olProd.preco or 0)                     else olProd.preco
                            olProd.precoCusto                  = snkProd.precoCusto                  if float(snkProd.precoCusto or 0)                != float(olProd.precoCusto or 0)                else olProd.precoCusto
                            olProd.estoque_controlar           = True
                            olProd.estoque_sobEncomenda        = False
                            olProd.estoque_diasPreparacao      = snkProd.estoque_diasPreparacao      if int(snkProd.estoque_diasPreparacao or 0)      != int(olProd.estoque_diasPreparacao or 0)      else olProd.estoque_diasPreparacao
                            olProd.estoque_localizacao         = snkProd.estoque_localizacao         if snkProd.estoque_localizacao                   != olProd.estoque_localizacao                   else olProd.estoque_localizacao
                            olProd.estoque_minimo              = snkProd.estoque_minimo              if int(snkProd.estoque_minimo or 0)              != int(olProd.estoque_minimo or 0)              else olProd.estoque_minimo
                            olProd.estoque_maximo              = snkProd.estoque_maximo              if int(snkProd.estoque_maximo or 0)              != int(olProd.estoque_maximo or 0)              else olProd.estoque_maximo
                            olProd.estoque_quantidade          = snkProd.estoque_quantidade          if int(snkProd.estoque_quantidade or 0)          != int(olProd.estoque_quantidade or 0)          else olProd.estoque_quantidade
                            olProd.estoque_inicial             = snkProd.estoque_inicial             if int(snkProd.estoque_inicial or 0)             != int(olProd.estoque_inicial or 0)             else olProd.estoque_inicial
                            olProd.tributacao_gtinEmbalagem    = snkProd.tributacao_gtinEmbalagem    if snkProd.tributacao_gtinEmbalagem              != olProd.tributacao_gtinEmbalagem              else olProd.tributacao_gtinEmbalagem
                            olProd.seo_keywords = ["produto"]
                            olProd.acao = 'put'
                            ackReceberOlist, val = await olProd.receber_alteracoes()
                            if ackReceberOlist and bool(val):
                                ackSync = await self.remove_syncprod(produto=f["codprod"],dhevento=f["dhevento"])
                                if ackSync:
                                    logger.info(self.contexto+"Produto %s atualizado com sucesso.",olProd.id)
                                    values.append(f"Produto {olProd.id} atualizado com sucesso.")
                                    print(f"Produto {olProd.id} atualizado com sucesso.")
                                    await self.atualiza_historico(produto_alterado=f["idprod"],sentido=0)
                                else:
                                    logger.error(self.contexto+"Erro: Produto %s atualizado na base Olist mas não foi possível remover da lista de atualizações pendentes na base Sankhya. Verifique os logs.",olProd.id)
                                    await self.app.email.notificar()
                                    values.append(f"Erro: Produto {olProd.id} atualizado na base Olist mas não foi possível remover da lista de atualizações pendentes na base Sankhya. Verifique os logs.")
                                    print(f"Erro: Produto {olProd.id} atualizado na base Olist mas não foi possível remover da lista de atualizações pendentes na base Sankhya. Verifique os logs.")
                            elif ackReceberOlist and val == 0:
                                logger.warning(self.contexto+"Produto %s não encontrado",olProd.id)
                                await self.app.email.notificar(tipo='alerta')
                                values.append(f"Produto {olProd.id} não encontrado")
                                print(f"Produto {olProd.id} não encontrado")
                            else:
                                logger.error(self.contexto+"Falha ao atualizar os dados do produto %s na base Olist. Verifique os logs.",olProd.id)
                                await self.app.email.notificar()
                                values.append(f"Falha ao atualizar os dados do produto {olProd.id} na base Olist. Verifique os logs.")
                                print(f"Falha ao atualizar os dados do produto {olProd.id} na base Olist. Verifique os logs.")                                                    
                    elif f["evento"] == 'E':
                        logger.warning(self.contexto+"Evento de inativação não disponível via API. Inative o produto %s manualmente no site.",f["idprod"])
                        await self.app.email.notificar(tipo='alerta')
                        values.append(f"Evento de inativação não disponível via API. Inative o produto {f["idprod"]} manualmente no site.")
                        print(f"Evento de inativação não disponível via API. Inative o produto {f["idprod"]} manualmente no site.")
                        
                    elif f["evento"] == 'I':
                        olP  = olProduto()
                        snkProd = snkProduto()
                        olP.sku = f["codprod"]
                        if not await olP.buscar():
                            ackOl = True
                        else:
                            logger.warning(self.contexto+"Produto %s já cadastrado na base Olist com o mesmo sku %s.",olProd.id,olProd.sku)
                            await self.app.email.notificar(tipo='alerta') 
                            values.append(f"Produto {olProd.id} já cadastrado na base Olist com o mesmo sku {olProd.sku}.")
                            print(f"Produto {olProd.id} já cadastrado na base Olist com o mesmo sku {olProd.sku}.")
                        snkProd.sku = f["codprod"]
                        if await snkProd.buscar():
                            ackSnk = True
                        else: 
                            logger.error(self.contexto+"Falha ao buscar os dados do produto %s na base Sankhya. Verifique os logs.",f["codprod"])
                            await self.app.email.notificar()
                            values.append(f"Falha ao buscar os dados do produto {f["codprod"]} na base Sankhya. Verifique os logs.")
                            print(f"Falha ao buscar os dados do produto {f["codprod"]} na base Sankhya. Verifique os logs.")
                        if ackOl and ackSnk:
                            olProd = olProduto()
                            olProd.sku                         = snkProd.sku
                            olProd.descricaoComplementar       = snkProd.descricaoComplementar
                            olProd.unidade                     = snkProd.unidade
                            olProd.unidadePorCaixa             = snkProd.unidadePorCaixa
                            olProd.ncm                         = re.sub(regex_cest_ncm, '', snkProd.ncm)
                            olProd.gtin                        = snkProd.gtin
                            olProd.origem                      = snkProd.origem
                            olProd.cest                        = str(snkProd.cest)
                            olProd.garantia                    = snkProd.garantia
                            olProd.observacoes                 = snkProd.observacoes
                            olProd.marca_id                    = snkProd.marca_id     
                            olProd.categoria_id                = snkProd.categoria_id
                            olProd.preco                       = snkProd.preco
                            # olProd.precoPromocional            = None
                            olProd.precoCusto                  = snkProd.precoCusto
                            # olProd.dimensoes_embalagem_id      = None
                            olProd.dimensoes_embalagem_tipo    = snkProd.dimensoes_embalagem_tipo
                            olProd.dimensoes_largura           = snkProd.dimensoes_largura
                            olProd.dimensoes_altura            = snkProd.dimensoes_altura
                            olProd.dimensoes_comprimento       = snkProd.dimensoes_comprimento
                            olProd.dimensoes_pesoLiquido       = snkProd.dimensoes_pesoLiquido
                            olProd.dimensoes_pesoBruto         = snkProd.dimensoes_pesoBruto
                            olProd.tributacao_gtinEmbalagem    = snkProd.tributacao_gtinEmbalagem
                            # olProd.tributacao_valorIPIFixo     = None
                            # olProd.tributacao_classeIPI        = None
                            # olProd.seo_titulo                  = None
                            # olProd.seo_descricao               = None
                            # olProd.seo_keywords                = ["produto"]
                            # olProd.seo_linkVideo               = None
                            # olProd.seo_slug                    = None
                            # olProd.fornecedores                = None
                            olProd.descricao                   = snkProd.descricao
                            olProd.tipo                        = snkProd.tipo
                            olProd.estoque_controlar           = True
                            olProd.estoque_sobEncomenda        = False
                            olProd.estoque_minimo              = snkProd.estoque_minimo
                            olProd.estoque_maximo              = snkProd.estoque_maximo
                            olProd.estoque_diasPreparacao      = snkProd.estoque_diasPreparacao
                            olProd.estoque_localizacao         = snkProd.estoque_localizacao
                            olProd.estoque_inicial             = snkProd.estoque_inicial
                            # olProd.anexos
                            # olProd.grade
                            # olProd.producao
                            # olProd.kits
                            # olProd.variacoes
                            olProd.acao = 'post'
                            ackReceberOlist, val = await olProd.receber_alteracoes()
                            if ackReceberOlist:
                                ackSync = await self.remove_syncprod(produto=f["codprod"],dhevento=f["dhevento"])
                                ackTgfpro = await self.atualiza_produto_novo(produto=f["codprod"],id=val)
                                if ackSync and ackTgfpro:
                                    logger.info(self.contexto+"Produto %s incluído com sucesso no ID %s.",f["codprod"],val)
                                    values.append(f"Produto {f["codprod"]} incluído com sucesso no ID {val}.")
                                    print(f"Produto {f["codprod"]} incluído com sucesso no ID {val}.")
                                    await self.atualiza_historico(produto_incluido=val)
                                elif ackSync and not ackTgfpro:
                                    logger.error(self.contexto+"Erro: Produto %s incluído na base Olist mas não foi possível vincular o ID na base Sankhya. Verifique os logs.",f["codprod"])
                                    self.app.email.notificar()
                                    values.append(f"Erro: Produto {f["codprod"]} incluído na base Olist mas não foi possível vincular o ID na base Sankhya. Verifique os logs.")
                                    print(f"Erro: Produto {f["codprod"]} incluído na base Olist mas não foi possível vincular o ID na base Sankhya. Verifique os logs.")
                                elif ackTgfpro and not ackSync:
                                    logger.error(self.contexto+"Erro: Produto %s incluído na base Olist mas não foi possível remover da lista de atualizações pendentes na base Sankhya. Verifique os logs.",f["codprod"])
                                    self.app.email.notificar()
                                    values.append(f"Erro: Produto {f["codprod"]} incluído na base Olist mas não foi possível remover da lista de atualizações pendentes na base Sankhya. Verifique os logs.")
                                    print(f"Erro: Produto {f["codprod"]} incluído na base Olist mas não foi possível remover da lista de atualizações pendentes na base Sankhya. Verifique os logs.")
                                else:
                                    logger.error(self.contexto+"Erro: Produto %s incluído na base Olist mas não foi possível atualizar as informações na base Sankhya. Verifique os logs.",f["codprod"])
                                    self.app.email.notificar()
                                    values.append(f"Erro: Produto {f["codprod"]} incluído na base Olist mas não foi possível atualizar as informações na base Sankhya. Verifique os logs.")
                                    print(f"Erro: Produto {f["codprod"]} incluído na base Olist mas não foi possível atualizar as informações na base Sankhya. Verifique os logs.")
                            else:
                                logger.error(self.contexto+"Falha ao incluir produto %s na base Olist. Verifique os logs.",f["codprod"])
                                self.app.email.notificar()
                                values.append(f"Falha ao incluir produto {f["codprod"]} na base Olist. Verifique os logs.")
                                print(f"Falha ao incluir produto {f["codprod"]} na base Olist. Verifique os logs.")
                print("Rotina concluída.")
                return True, values
            else:
                values.append("Nenhuma alteração para ser enviada para Tiny/Olist")
                print("Nenhuma alteração para ser enviada para Tiny/Olist")
                return True, values

    class Pedido():
        def __init__(self, id:int=None):
            self.app = App()
            self.id = id
            self.contexto = '#Pedidos# '            
            
        async def atualiza_historico(self, pedido_alterado:int=None, pedido_incluido:int=None, sentido:int=None):
            file_path = configOlist.PATH_HISTORICO_PEDIDO
            historico = await self.app.valida_path.validar(path=file_path,mode='r',method='json')
            if pedido_alterado:
                if sentido == 0: # SANKHYA > OLIST
                    historico["ultima_atualizacao_sankhya_olist"]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    historico["ultima_atualizacao_sankhya_olist"]["id"] = pedido_alterado
                elif sentido == 1: # OLIST > SANKHYA
                    historico["ultima_atualizacao_olist_sankhya"]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    historico["ultima_atualizacao_olist_sankhya"]["id"] = pedido_alterado
                else:
                    pass
            if pedido_incluido:
                historico["ultima_importacao"]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                historico["ultima_importacao"]["id"] = pedido_incluido
            await self.app.valida_path.validar(path=file_path,mode='w',method='json',content=historico)

        async def registra_pedido_novo(self, pedido_aprovado:int, confirmado:bool=False) -> tuple[bool, int]:
            olPed = olPedido()
            snkPed = snkPedido()

            time.sleep(self.app.req_sleep)
            if await olPed.buscar(id=pedido_aprovado):
                dados_pedido = await olPed.encodificar()
                ack, num_unico = await snkPed.registrar(dados_pedido)            
                if ack:
                    if confirmado:
                        if await snkPed.confirmar(nunota=num_unico,provisao='S'):
                            logger.info(self.contexto+"Pedido #%s importado e confirmado no nº único %s",dados_pedido["numeroPedido"],num_unico)
                        else:
                            logger.warning(self.contexto+"Falha ao confirmar pedido. Pedido #%s importado no nº único %s.",dados_pedido["numeroPedido"],num_unico)
                    else:
                        logger.info(self.contexto+"Pedido #%s importado no nº único %s",dados_pedido["numeroPedido"],num_unico)
                else:
                    logger.error(self.contexto+"Falha ao registrar pedido #%s. Verifique os logs.",dados_pedido["numeroPedido"]) 
                    return False, None
            else:
                logger.warning(self.contexto+"Falha ao buscar dados do pedido #%s. Verifique os logs.",dados_pedido["numeroPedido"])
                return False, None
            await self.atualiza_historico(pedido_incluido=pedido_aprovado)
            return ack, num_unico

        async def registra_nota(self, dados_snk:dict=None) -> tuple[bool, int]:
            olNotas = olNota()
            snkPed = snkPedido()
            contexto = '#Notas# '
            
            time.sleep(self.app.req_sleep)
            if await olNotas.buscar(id_ecommerce=dados_snk.get('ad_mkp_codped')):
                dados_nota = await olNotas.encodificar()
                ack = await snkPed.buscar(dados_snk.get('nunota'))

            valida_itens = []
            if dados_nota and ack:
                for i, item in enumerate(dados_nota.get('itens')):
                    valida_prod = int(item.get('codigo')) in [it.codprod for it in snkPed.itens]
                    valida_qtd  = snkPed.itens[i].qtdneg == int(item.get('quantidade'))
                    valida_itens.append(True if valida_prod and valida_qtd else False)
                if all(valida_itens):
                    ackNota, nunota_nota = await snkPed.gerar_nota(pedido=snkPed.nunota,payload=dados_nota)
                    if ackNota:
                        ack, nunota = await snkPed.importar_xml(nota=nunota_nota,payload=dados_nota)
                        if ack:
                            logger.info(contexto+"Pedido #%s faturado com sucesso! ",dados_snk.get('ad_mkp_numped'))
                            return True, nunota
                        else:
                            logger.error(contexto+"Pedido #%s com erro ao importar XML da nota. Verifique os logs",dados_snk.get('ad_mkp_numped'))
                            return False, nunota
                    else:
                        logger.error(contexto+"Erro ao faturar Pedido #%s. Verifique os logs",dados_snk.get('ad_mkp_numped'))
                        return False, None
                else:
                    logger.error(contexto+"Erro ao faturar Pedido %s. Quantidades dos itens desmembrados na nota não bate com o pedido",dados_snk.get('ad_mkp_numped'))
                    return False, None
            else:
                logger.error(contexto+"Erro ao receber dados da Nota Fiscal do Pedido #%s.",dados_snk.get('ad_mkp_numped'))
                return False, None

        async def importa_aprovados(self) -> tuple[bool,list]:
            olPedidos = olPedido()
            res = []
            ack, pedidos_aprovados = await olPedidos.buscar_lista(situacao='A')#,atual=False)
            if ack and pedidos_aprovados:
                file_path_exists = configSankhya.PATH_SCRIPT_SYNCPEDIDO
                query_syncpedido = await self.app.valida_path.validar(path=file_path_exists,method='full',mode='r')
                for pedido_aprovado in pedidos_aprovados:
                    self.id = pedido_aprovado
                    exists = await self.app.db.select(query=query_syncpedido, params={"AD_MKP_ID":pedido_aprovado})
                    if not exists:
                        ack, num_pedido = await self.registra_pedido_novo(pedido_aprovado)
                        if ack:
                            res.append(f"Pedido {pedido_aprovado} importado no nº único {num_pedido}")
                            print(f"Pedido {pedido_aprovado} importado no nº único {num_pedido}")
                        else:
                            await self.app.email.notificar()
                            res.append(f"Falha ao importar pedido {pedido_aprovado}. Verifique os logs.")
                            print(f"Falha ao importar pedido {pedido_aprovado}. Verifique os logs.")
                    else:
                        pass
                return True, res
            elif ack and not pedidos_aprovados:
                res.append("Sem novos pedidos com status Aprovado.")
                print("Sem novos pedidos com status Aprovado.")
                return True, res
            else:
                logger.error(self.contexto+" Falha ao buscar relação dos pedidos aprovados. Verifique os logs.")
                await self.app.email.notificar()
                res.append("Falha ao buscar relação dos pedidos aprovados")
                print("Falha ao buscar relação dos pedidos aprovados")
                return False, res
            
        async def importa_prep_envio(self) -> tuple[bool,list]:
            olPedidos = olPedido()
            res = []            
            ack, pedidos_prep_envio = await olPedidos.buscar_lista(situacao='S')#,atual=False)
            if ack and pedidos_prep_envio:  
                file_path_exists = configSankhya.PATH_SCRIPT_SYNCPEDIDO
                query_syncpedido = await self.app.valida_path.validar(path=file_path_exists,method='full',mode='r')                            
                for pedido in pedidos_prep_envio:
                    self.id = pedido
                    exists  = await self.app.db.select(query=query_syncpedido,params={"AD_MKP_ID":pedido})
                    if not exists:
                        ack, num_pedido = await self.registra_pedido_novo(pedido)
                        if ack:
                            res.append(f"Pedido {pedido} importado no nº único {num_pedido}")
                            print(f"Pedido {pedido} importado no nº único {num_pedido}")
                        else:
                            await self.app.email.notificar()
                            res.append(f"Falha ao importar pedido {pedido}. Verifique os logs.")
                            print(f"Falha ao importar pedido {pedido}. Verifique os logs.")
                    else:
                        if not bool(exists[0].get('confirmado')):
                            num_pedido = exists[0].get('nunota')
                            snkPed = snkPedido()
                            if await snkPed.confirmar(nunota=num_pedido,provisao='S'):
                                logger.info(self.contexto+" Pedido ID %s atualizado para confirmado. Nº único %s.",pedido,num_pedido)
                                res.append(f"Pedido ID {pedido} atualizado para confirmado. Nº único {num_pedido}.")
                                print(f"Pedido ID {pedido} atualizado para confirmado. Nº único {num_pedido}.")
                            else:
                                logger.warning(self.contexto+" Falha ao confirmar pedido ID %s Nº único %s.",pedido,num_pedido)
                                await self.app.email.notificar(tipo='alerta')
                                res.append(f"Falha ao confirmar pedido ID {pedido} nº único {num_pedido}.")
                                print(f"Falha ao confirmar pedido ID {pedido} nº único {num_pedido}.")
                    await self.atualiza_historico(pedido_alterado=pedido,sentido=1)
                return True, res
            elif ack and not pedidos_prep_envio:
                res.append("Sem novos pedidos com status Preparando envio.")
                print("Sem novos pedidos com status Preparando envio.")
                return True, res
            else:
                logger.error(self.contexto+" Falha ao buscar relação dos pedidos Preparando envio")
                await self.app.email.notificar()
                res.append("Falha ao buscar relação dos pedidos Preparando envio")
                print("Falha ao buscar relação dos pedidos Preparando envio")
                return False, res
            
        async def importa_pronto_envio(self) -> tuple[bool,list]:
            olPedidos = olPedido()
            res = []            
            ack, pedidos_pronto_envio = await olPedidos.buscar_lista(situacao='P')#,atual=False)
            if ack and pedidos_pronto_envio:  
                file_path_exists = configSankhya.PATH_SCRIPT_SYNCPEDIDO
                query_syncpedido = await self.app.valida_path.validar(path=file_path_exists,method='full',mode='r')                            
                for pedido in pedidos_pronto_envio:
                    self.id = pedido
                    exists  = await self.app.db.select(query=query_syncpedido,params={"AD_MKP_ID":pedido})
                    if not exists:
                        ack, num_pedido = await self.registra_pedido_novo(pedido)
                        if ack:
                            res.append(f"Pedido {pedido} importado no nº único {num_pedido}")
                            print(f"Pedido {pedido} importado no nº único {num_pedido}")
                        else:
                            await self.app.email.notificar()
                            res.append(f"Falha ao importar pedido {pedido}. Verifique os logs.")
                            print(f"Falha ao importar pedido {pedido}. Verifique os logs.")
                    else:
                        if not bool(exists[0].get('confirmado')):
                            num_pedido = exists[0].get('nunota')
                            snkPed = snkPedido()
                            if await snkPed.confirmar(nunota=num_pedido,provisao='S'):
                                logger.info(self.contexto+" Pedido ID %s atualizado para confirmado. Nº único %s.",pedido,num_pedido)
                                res.append(f"Pedido ID {pedido} atualizado para confirmado. Nº único {num_pedido}.")
                                print(f"Pedido ID {pedido} atualizado para confirmado. Nº único {num_pedido}.")
                            else:
                                logger.warning(self.contexto+" Falha ao confirmar pedido ID %s Nº único %s.",pedido,num_pedido)
                                await self.app.email.notificar(tipo='alerta')
                                res.append(f"Falha ao confirmar pedido ID {pedido} nº único {num_pedido}.")
                                print(f"Falha ao confirmar pedido ID {pedido} nº único {num_pedido}.")                        
                    await self.atualiza_historico(pedido_alterado=pedido,sentido=1)
                return True, res
            elif ack and not pedidos_pronto_envio:
                res.append("Sem novos pedidos com status Pronto para envio.")
                print("Sem novos pedidos com status Pronto para envio.")
                return True, res
            else:
                logger.error(self.contexto+" Falha ao buscar relação dos pedidos Pronto para envio.")
                await self.app.email.notificar()
                res.append("Falha ao buscar relação dos pedidos Pronto para envio.")
                print("Falha ao buscar relação dos pedidos Pronto para envio.")
                return False, res
            
        async def importa_faturados(self) -> tuple[bool,list]:
            olPedidos = olPedido()
            res = []
            ack, pedidos_faturados = await olPedidos.buscar_lista(situacao='F')#,atual=False)
            if ack and pedidos_faturados:  
                file_path_exists = configSankhya.PATH_SCRIPT_SYNCPEDIDO
                query_syncpedido = await self.app.valida_path.validar(path=file_path_exists,method='full',mode='r')                            
                for pedido_faturado in pedidos_faturados:
                    self.id = pedido_faturado
                    exists  = await self.app.db.select(query=query_syncpedido,params={"AD_MKP_ID":pedido_faturado})
                    if not exists:
                        ack, num_pedido = await self.registra_pedido_novo(pedido_faturado,confirmado=True)
                        if ack:
                            dados_snk = await self.app.db.select(query=query_syncpedido,params={"NUNOTA":num_pedido})
                            ack, num_nota = await self.registra_nota(dados_snk=dados_snk[0])
                            if ack:
                                res.append(f"Pedido {pedido_faturado} importado no nº único {num_pedido} e Nota {num_nota} registrada.")                                
                                print(f"Pedido {pedido_faturado} importado no nº único {num_pedido} e Nota {num_nota} registrada.")                                
                            else:
                                await self.app.email.notificar()
                                res.append(f"Falha ao registrar Nota para o pedido {pedido_faturado}.")                                
                                print(f"Falha ao registrar Nota para o pedido {pedido_faturado}. Verifique os logs.")                                
                        else:
                            await self.app.email.notificar()
                            res.append(f"Falha ao importar pedido {pedido_faturado}.")                            
                            print(f"Falha ao importar pedido {pedido_faturado}. Verifique os logs.")                            
                    else:
                        if bool(exists[0].get('faturado')):
                            res.append(f"Pedido #{exists[0].get('ad_mkp_numped')} já faturado.")
                            print(f"Pedido #{exists[0].get('ad_mkp_numped')} já faturado.")
                        else:
                            if bool(exists[0].get('confirmado')):
                                ack, num_nota = await self.registra_nota(dados_snk=exists[0])
                                if ack:
                                    res.append(f"Nota registrada para Pedido #{exists[0].get('ad_mkp_numped')}.")
                                    print(f"Nota registrada para Pedido #{exists[0].get('ad_mkp_numped')}.")
                                else:
                                    await self.app.email.notificar()
                                    res.append(f"Falha ao registrar Nota para o Pedido #{exists[0].get('ad_mkp_numped')}.")
                                    print(f"Falha ao registrar Nota para o Pedido #{exists[0].get('ad_mkp_numped')}. Verifique os logs.")
                            else:
                                snkPed = snkPedido()
                                if await snkPed.confirmar(nunota=exists[0].get('nunota'),provisao='S'):
                                    ack, num_nota = await self.registra_nota(dados_snk=exists[0])
                                    if ack:
                                        res.append(f"Pedido #{exists[0].get('ad_mkp_numped')} confirmado e Nota registrada.")
                                        print(f"Pedido #{exists[0].get('ad_mkp_numped')} confirmado e Nota registrada.")
                                    else:
                                        await self.app.email.notificar()
                                        res.append(f"Pedido #{exists[0].get('ad_mkp_numped')} confirmado. Falha ao registrar a Nota.")
                                        print(f"Pedido #{exists[0].get('ad_mkp_numped')} confirmado. Falha ao registrar a Nota. Verifique os logs")
                                else:
                                    await self.app.email.notificar()
                                    res.append(f"Falha ao confirmar Pedido #{exists[0].get('ad_mkp_numped')}.")
                                    print(f"Falha ao confirmar Pedido #{exists[0].get('ad_mkp_numped')}.")
                    await self.atualiza_historico(pedido_alterado=pedido_faturado,sentido=1)
                return True, res
            elif ack and not pedidos_faturados:
                res.append("Sem novos pedidos com status Faturado.")
                print("Sem novos pedidos com status Faturado.")
                return True, res            
            else:
                logger.error(self.contexto+"Falha ao buscar relação dos pedidos faturados")
                await self.app.email.notificar()
                res.append("Falha ao buscar relação dos pedidos faturados")
                print("Falha ao buscar relação dos pedidos faturados")
                return False, res        

    class Estoque:

        def __init__(self):
            self.app = App()
            self.bot = Bot()
            self.contexto = '#Estoque# '            

        async def atualiza_historico(self, produto:int=None):
            file_path = configOlist.PATH_HISTORICO_ESTOQUE
            historico = await self.app.valida_path.validar(path=file_path,mode='r',method='json')
            if produto:
                historico["ultima_atualizacao"]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                historico["ultima_atualizacao"]["id"] = int(produto)
            await self.app.valida_path.validar(path=file_path,mode='w',method='json',content=historico)            

        async def remove_syncestoque(self,produto:int=None,dhevento:datetime=None) -> bool:
            if produto and dhevento:
                file_path_del   = configSankhya.PATH_DELETE_SYNCESTOQUE
                delete_syncest = await self.app.valida_path.validar(path=file_path_del,method='full',mode='r')
                params = {
                    "CODPROD" : produto,
                    "DHEVENTO" : dhevento
                }
                ack, rows = await self.app.db.dml(query=delete_syncest,params=params)
                return ack
            else:
                return False            

        async def atualizar(self, codprod:int=None) -> tuple[bool,list]:
            
            if codprod:
                values = []
                snkEst = snkEstoque()                
                estoque_sankhya = await snkEst.buscar_disponivel(codprod=codprod)
                #print(estoque_sankhya)
                if estoque_sankhya[0].get('controla_lote') == 'N':
                    estoque_snk = estoque_sankhya[0]
                    olEst = olEstoque()
                    if await olEst.buscar(id=estoque_snk.get('ad_mkp_idprod')):
                        estoque_olist = await olEst.encodificar()
                        ajuste_estoque = {                        
                            "id": int(estoque_snk.get('ad_mkp_idprod')),
                            "deposito": int(estoque_olist.get('depositos')[0].get('id')),
                            "tipo":'B',
                            "quantidade":estoque_snk.get('estoque_total')
                        }
                        olEst.tipo = ajuste_estoque.get('tipo')
                        olEst.quantidade = ajuste_estoque.get('quantidade')
                        olEst.acao = 'post'
                        if await olEst.enviar_saldo():
                            logger.info(self.contexto+"Estoque do produto %s sincronizado com sucesso",estoque_olist.get('codigo'))
                            values.append(f"Estoque do produto {estoque_olist.get('codigo')} sincronizado com sucesso.")
                            print(f"Estoque do produto {estoque_olist.get('codigo')} sincronizado com sucesso")
                        else:
                            logger.error(self.contexto+"Falha ao sincronizar estoque do produto %s. Verifique os logs.",estoque_olist.get('codigo'))
                            await self.app.email.notificar()
                            values.append(f"Falha ao sincronizar estoque do produto {estoque_olist.get('codigo')}. Verifique os logs.")
                            print(f"Falha ao sincronizar estoque do produto {estoque_olist.get('codigo')}. Verifique os logs.")
                    else:
                        logger.error(self.contexto+"Falha ao buscar dados de estoque do produto %s na base Olist. Verifique os logs.",mvto.get('codprod'))
                        await self.app.email.notificar()
                        values.append(f"Falha ao buscar dados de estoque do produto {mvto.get('codprod')} na base Olist. Verifique os logs.")
                        print(f"Falha ao buscar dados de estoque do produto {mvto.get('codprod')} na base Olist. Verifique os logs.")    
                else:
                    estoque_snk = estoque_sankhya
                    driver = webdriver.Firefox()
                    driver.maximize_window()                                
                    ack_login, driver = await self.bot.login(driver=driver)
                    if ack_login:
                        controle = []
                        valida_reservas = estoque_snk[0].get('reservado') or 0
                        qtd_lote = None
                        pop = []
                        for iter, lote in enumerate(estoque_snk):                  
                            qtd_lote = lote.get('estoque')
                            while valida_reservas > 0 and qtd_lote > 0:
                                qtd_lote -= 1
                                valida_reservas -= 1
                            if qtd_lote > 0:
                                controle.append({
                                    "numeroLote": lote.get('controle'),
                                    "dataFabricacao": lote.get('dtfabricacao').strftime('%d/%m/%Y'),
                                    "dataValidade": lote.get('dtval').strftime('%d/%m/%Y'),
                                    "quantidade": qtd_lote
                                })
                            else:
                                pop.append(lote)
                        for i,j in enumerate(pop):
                            estoque_snk.pop(estoque_snk.index(j))

                        if estoque_snk:
                            ajuste_estoque = {
                                "idproduto": estoque_snk[0].get('ad_mkp_idprod'),
                                "qtd": estoque_snk[0].get('estoque_total')-estoque_snk[0].get('reservado'),
                                "controle": controle
                            }
                        else:
                            ajuste_estoque = {
                                "idproduto": estoque_sankhya[0].get('ad_mkp_idprod'),
                                "qtd": 0
                            }

                        if ajuste_estoque:                                
                            ack_estoque, driver = await self.bot.lanca_estoque(driver=driver,dados_produto=ajuste_estoque)
                            if ack_estoque:
                                if ajuste_estoque.get('qtd') == 0:
                                    ack_lotes = True
                                else:
                                    ack_lotes, driver = await self.bot.lanca_lotes(driver=driver,dados_lote=ajuste_estoque.get('controle'))
                                if ack_lotes:
                                    await self.atualiza_historico(produto=estoque_sankhya[0].get('idprod'))
                                    logger.info(self.contexto+"Estoque do produto %s sincronizado com sucesso",estoque_sankhya[0].get('codprod'))
                                    values.append(f"Estoque do produto {estoque_sankhya[0].get('codprod')} sincronizado com sucesso.")                                    
                                    print(f"Estoque do produto {estoque_sankhya[0].get('codprod')} sincronizado com sucesso")                                    
                                else:
                                    logger.error(self.contexto+"Falha ao sincronizar estoque do produto %s no lançamento dos lotes. Verifique os logs.",estoque_sankhya[0].get('codprod'))
                                    await self.app.email.notificar()
                                    values.append(f"Falha ao sincronizar estoque do produto {estoque_sankhya[0].get('codprod')} no lançamento dos lotes. Verifique os logs.")
                                    print(f"Falha ao sincronizar estoque do produto {estoque_sankhya[0].get('codprod')} no lançamento dos lotes. Verifique os logs.")                              
                            else:
                                if await self.bot.valida_configuracao_lote(driver=driver,codigo=ajuste_estoque.get('idproduto')):
                                    ack_estoque, driver = await self.bot.lanca_estoque(driver=driver,dados_produto=ajuste_estoque)
                                    if ack_estoque:
                                        ack_lotes, driver = await self.bot.lanca_lotes(driver=driver,dados_lote=ajuste_estoque.get('controle'))
                    await self.bot.logout(driver=driver)
            else:
                olEst = olEstoque()
                snkEst = snkEstoque()
                values = []
                mvto_sem_lote = await snkEst.buscar_movimentacoes(controla_lote='N')
                mvto_com_lote = await snkEst.buscar_movimentacoes()
                print(f"Encontrados {len(mvto_com_lote)} produtos com lote e {len(mvto_sem_lote)} produtos sem lote")
                if mvto_sem_lote:
                    for mvto in mvto_sem_lote:
                        estoque_snk = await snkEst.buscar_disponivel(codprod=mvto.get('codprod'))
                        estoque_snk = estoque_snk[0]
                        snk_qtd_est = estoque_snk.get('estoque_total') - estoque_snk.get('reservado')
                        olEst = olEstoque()
                        if await olEst.buscar(id=estoque_snk.get('ad_mkp_idprod')):
                            estoque_olist = await olEst.encodificar()
                            ol_qtd_est = estoque_olist.get('disponivel')
                            #ol_qtd_est = estoque_olist.get('saldo')
                            if ol_qtd_est != snk_qtd_est:
                                variacao = ol_qtd_est - snk_qtd_est
                                ajuste_estoque = {
                                        "id": int(estoque_snk.get('ad_mkp_idprod')),
                                        "deposito": int(estoque_olist.get('depositos')[0].get('id')),
                                        "tipo":None,
                                        "quantidade":abs(variacao)
                                    }    
                                if variacao > 0:
                                    ajuste_estoque["tipo"] = "S"
                                elif variacao < 0:
                                    ajuste_estoque["tipo"] = "E"
                                else:
                                    pass
                                olEst.tipo = ajuste_estoque.get('tipo')
                                olEst.quantidade = ajuste_estoque.get('quantidade')
                                olEst.acao = 'post'
                                if await olEst.enviar_saldo():
                                    ackSync = await self.remove_syncestoque(produto=mvto["codprod"],dhevento=mvto["dhevento"])
                                    if ackSync:
                                        await self.atualiza_historico(produto=estoque_olist.get('codigo'))
                                        logger.info(self.contexto+"Estoque do produto %s sincronizado com sucesso",estoque_olist.get('codigo'))
                                        values.append(f"Estoque do produto {estoque_olist.get('codigo')} sincronizado com sucesso.")                                    
                                        print(f"Estoque do produto {estoque_olist.get('codigo')} sincronizado com sucesso")                                    
                                    else:
                                        logger.error(self.contexto+"Estoque do produto %s sincronizado mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.",estoque_olist.get('codigo'))
                                        await self.app.email.notificar()
                                        values.append(f"Estoque do produto {estoque_olist.get('codigo')} sincronizado mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")
                                        print(f"Estoque do produto {estoque_olist.get('codigo')} sincronizado mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")
                                else:
                                    logger.error(self.contexto+"Falha ao sincronizar estoque do produto %s. Verifique os logs.",estoque_olist.get('codigo'))
                                    await self.app.email.notificar()
                                    values.append(f"Falha ao sincronizar estoque do produto {estoque_olist.get('codigo')}. Verifique os logs.")
                                    print(f"Falha ao sincronizar estoque do produto {estoque_olist.get('codigo')}. Verifique os logs.")
                            else:
                                ackSync = await self.remove_syncestoque(produto=mvto["codprod"],dhevento=mvto["dhevento"])
                                if ackSync:
                                    await self.atualiza_historico(produto=estoque_olist.get('codigo'))
                                    logger.info(self.contexto+"Estoque do produto %s sem alteração.",estoque_olist.get('codigo'))
                                    values.append(f"Estoque do produto {estoque_olist.get('codigo')} sem alteração.")
                                    print(f"Estoque do produto {estoque_olist.get('codigo')} sem alteração.")
                                else:
                                    logger.warning(self.contexto+"Estoque do produto %s sem alteração mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.",estoque_olist.get('codigo'))
                                    await self.app.email.notificar(tipo='alerta')
                                    values.append(f"Estoque do produto {estoque_olist.get('codigo')} sem alteração mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")                        
                                    print(f"Estoque do produto {estoque_olist.get('codigo')} sem alteração mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")
                        else:
                            logger.error(self.contexto+"Falha ao buscar dados de estoque do produto %s na base Olist. Verifique os logs.",mvto.get('codprod'))
                            await self.app.email.notificar()
                            values.append(f"Falha ao buscar dados de estoque do produto {mvto.get('codprod')} na base Olist. Verifique os logs.")
                            print(f"Falha ao buscar dados de estoque do produto {mvto.get('codprod')} na base Olist. Verifique os logs.")

                if mvto_com_lote:
                    driver = webdriver.Firefox()
                    driver.maximize_window()                                
                    ack_login, driver = await self.bot.login(driver=driver)
                    if ack_login:
                        for mvto in mvto_com_lote:
                            estoque_snk = await snkEst.buscar_disponivel(codprod=mvto.get('codprod'))
                            if estoque_snk:
                                if estoque_snk[0].get('estoque_total') - estoque_snk[0].get('reservado') >= 300:
                                    ackSync = await self.remove_syncestoque(produto=mvto.get('codprod'),dhevento=mvto.get('dhevento'))
                                    continue
                                snk_qtd_est = estoque_snk[0].get('estoque_total')
                                pular = True if snk_qtd_est < estoque_snk[0].get('reservado') else False
                                olEst = olEstoque()
                                if await olEst.buscar(id=estoque_snk[0].get('ad_mkp_idprod')):
                                    estoque_olist = await olEst.encodificar()
                                    ol_qtd_est = estoque_olist.get('saldo')
                                    if ol_qtd_est != snk_qtd_est:
                                        if pular:
                                            ajuste_estoque = {
                                                "idproduto": mvto.get('idprod'),
                                                "qtd": 0
                                            }
                                        else:
                                            controle = []
                                            valida_reservas = estoque_snk[0].get('reservado') or 0
                                            qtd_lote = None
                                            pop = []
                                            for iter, lote in enumerate(estoque_snk):
                                                qtd_lote = lote.get('estoque')
                                                while valida_reservas > 0 and qtd_lote > 0:
                                                    qtd_lote -= 1
                                                    valida_reservas -= 1
                                                if qtd_lote > 0:
                                                    controle.append({
                                                        "numeroLote": lote.get('controle'),
                                                        "dataFabricacao": lote.get('dtfabricacao').strftime('%d/%m/%Y'),
                                                        "dataValidade": lote.get('dtval').strftime('%d/%m/%Y'),
                                                        "quantidade": qtd_lote
                                                    })
                                                else:
                                                    pop.append(lote)

                                            for i,j in enumerate(pop):
                                                estoque_snk.pop(estoque_snk.index(j))

                                            if estoque_snk:

                                                ajuste_estoque = {
                                                    "idproduto": estoque_snk[0].get('ad_mkp_idprod'),
                                                    "qtd": estoque_snk[0].get('estoque_total')-estoque_snk[0].get('reservado'),
                                                    "controle": controle
                                                }
                                            else:
                                                ajuste_estoque = {
                                                    "idproduto": mvto.get('idprod'),
                                                    "qtd": 0
                                                }

                                        if ajuste_estoque:                                
                                            ack_estoque, driver = await self.bot.lanca_estoque(driver=driver,dados_produto=ajuste_estoque)
                                            if ack_estoque:
                                                if ajuste_estoque.get('qtd') == 0:
                                                    ack_lotes = True
                                                else:
                                                    ack_lotes, driver = await self.bot.lanca_lotes(driver=driver,dados_lote=ajuste_estoque.get('controle'))
                                                if ack_lotes:
                                                    ackSync = await self.remove_syncestoque(produto=mvto.get('codprod'),dhevento=mvto.get('dhevento'))
                                                    if ackSync:
                                                        await self.atualiza_historico(produto=mvto.get('idprod'))
                                                        logger.info(self.contexto+"Estoque do produto %s sincronizado com sucesso",mvto.get('codprod'))
                                                        values.append(f"Estoque do produto {mvto.get('codprod')} sincronizado com sucesso.")                                    
                                                        print(f"Estoque do produto {mvto.get('codprod')} sincronizado com sucesso")                                    
                                                    else:
                                                        logger.error(self.contexto+"Estoque do produto %s sincronizado mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.",mvto.get('codprod'))
                                                        await self.app.email.notificar()
                                                        values.append(f"Estoque do produto {mvto.get('codprod')} sincronizado mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")
                                                        print(f"Estoque do produto {mvto.get('codprod')} sincronizado mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")                                    
                                                else:
                                                    logger.error(self.contexto+"Falha ao sincronizar estoque do produto %s no lançamento dos lotes. Verifique os logs.",mvto.get('codprod'))
                                                    await self.app.email.notificar()
                                                    values.append(f"Falha ao sincronizar estoque do produto {mvto.get('codprod')} no lançamento dos lotes. Verifique os logs.")
                                                    print(f"Falha ao sincronizar estoque do produto {mvto.get('codprod')} no lançamento dos lotes. Verifique os logs.")                                                
                                            else:
                                                if await self.bot.valida_configuracao_lote(driver=driver,codigo=ajuste_estoque.get('idproduto')):
                                                    ack_estoque, driver = await self.bot.lanca_estoque(driver=driver,dados_produto=ajuste_estoque)
                                                    if ack_estoque:
                                                        ack_lotes, driver = await self.bot.lanca_lotes(driver=driver,dados_lote=ajuste_estoque.get('controle'))
                                                        if ack_lotes:
                                                            ackSync = await self.remove_syncestoque(produto=mvto.get('codprod'),dhevento=mvto.get('dhevento'))
                                                            if ackSync:
                                                                await self.atualiza_historico(produto=mvto.get('idprod'))
                                                                logger.info(self.contexto+"Estoque do produto %s sincronizado com sucesso",mvto.get('codprod'))
                                                                values.append(f"Estoque do produto {mvto.get('codprod')} sincronizado com sucesso.")                                    
                                                                print(f"Estoque do produto {mvto.get('codprod')} sincronizado com sucesso")                                    
                                                            else:
                                                                logger.error(self.contexto+"Estoque do produto %s sincronizado mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.",mvto.get('codprod'))
                                                                await self.app.email.notificar()
                                                                values.append(f"Estoque do produto {mvto.get('codprod')} sincronizado mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")
                                                                print(f"Estoque do produto {mvto.get('codprod')} sincronizado mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")                                    
                                                        else:
                                                            logger.error(self.contexto+"Falha ao sincronizar estoque do produto %s no lançamento dos lotes. Verifique os logs.",mvto.get('codprod'))
                                                            await self.app.email.notificar()
                                                            values.append(f"Falha ao sincronizar estoque do produto {mvto.get('codprod')} no lançamento dos lotes. Verifique os logs.")
                                                            print(f"Falha ao sincronizar estoque do produto {mvto.get('codprod')} no lançamento dos lotes. Verifique os logs.")                                                        
                                                else:
                                                    logger.error(self.contexto+"Falha ao sincronizar estoque do produto %s no lançamento do estoque. Verifique os logs.",mvto.get('codprod'))
                                                    await self.app.email.notificar()
                                                    values.append(f"Falha ao sincronizar estoque do produto {mvto.get('codprod')} no lançamento do estoque. Verifique os logs.")
                                                    print(f"Falha ao sincronizar estoque do produto {mvto.get('codprod')} no lançamento do estoque. Verifique os logs.")                                
                                        else:
                                            logger.error("Falha validar informações para ajuste de estoque do produto %s.",mvto.get('codprod'))
                                            logger.error(self.contexto+"Falha ao sincronizar estoque do produto %s. Verifique os logs.",mvto.get('codprod'))
                                            await self.app.email.notificar()
                                            values.append(f"Falha ao sincronizar estoque do produto {mvto.get('codprod')}. Verifique os logs.")
                                            print(f"Falha ao sincronizar estoque do produto {mvto.get('codprod')}. Verifique os logs.")
                                    else:
                                        ackSync = await self.remove_syncestoque(produto=mvto["codprod"],dhevento=mvto["dhevento"])
                                        if ackSync:
                                            await self.atualiza_historico(produto=estoque_olist.get('codigo'))
                                            logger.info(self.contexto+"Estoque do produto %s sem alteração.",estoque_olist.get('codigo'))
                                            values.append(f"Estoque do produto {estoque_olist.get('codigo')} sem alteração.")
                                            print(f"Estoque do produto {estoque_olist.get('codigo')} sem alteração.")
                                        else:
                                            logger.warning(self.contexto+"Estoque do produto %s sem alteração mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.",estoque_olist.get('codigo'))
                                            await self.app.email.notificar(tipo='alerta')
                                            values.append(f"Estoque do produto {estoque_olist.get('codigo')} sem alteração mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")                        
                                            print(f"Estoque do produto {estoque_olist.get('codigo')} sem alteração mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")                            
                                else:
                                    logger.error(self.contexto+"Falha ao buscar dados de estoque do produto %s na base Olist. Verifique os logs.",mvto.get('codprod'))
                                    await self.app.email.notificar()
                                    values.append(f"Falha ao buscar dados de estoque do produto {mvto.get('codprod')} na base Olist. Verifique os logs.")
                                    print(f"Falha ao buscar dados de estoque do produto {mvto.get('codprod')} na base Olist. Verifique os logs.")                        
                            else:
                                ajuste_estoque = {
                                    "idproduto": mvto.get('idprod'),
                                    "qtd": 0
                                }
                                ack_estoque, driver = await self.bot.lanca_estoque(driver=driver,dados_produto=ajuste_estoque)
                                if ack_estoque:
                                    ackSync = await self.remove_syncestoque(produto=mvto.get('codprod'),dhevento=mvto.get('dhevento'))
                                    if ackSync:
                                        await self.atualiza_historico(produto=mvto.get('idprod'))
                                        logger.info(self.contexto+"Produto %s sem estoque disponível",mvto.get('codprod'))
                                        values.append(f"Produto {mvto.get('codprod')} sem estoque disponível.")                                    
                                        print(f"Produto {mvto.get('codprod')} sem estoque disponível.")                                    
                                    else:
                                        logger.error(self.contexto+"Produto %s sem estoque disponível mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.",mvto.get('codprod'))
                                        await self.app.email.notificar()
                                        values.append(f"Produto {mvto.get('codprod')} sem estoque disponível mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")
                                        print(f"Produto {mvto.get('codprod')} sem estoque disponível mas não foi possível remover da lista de atualizações pendentes. Verifique os logs.")
                        await self.bot.logout(driver=driver)
                    else:
                        logger.error(self.contexto+"Erro ao fazer login no Olist. Verifique os logs.")
                        await self.app.email.notificar()
                        values.append("Erro ao fazer login no Olist. Verifique os logs.")
                        print("Erro ao fazer login no Olist. Verifique os logs.")
            print(f"Sincronização concluída!")
            return True, values

        async def balanco(self,produto:int=None) -> tuple[bool,list]:
        #     values = []
        #     if produto:
        #         snkEst = snkEstoque()                
        #         estoque_snk = await snkEst.buscar_disponivel(codprod=produto)
        #         estoque_snk = estoque_snk[0]
        #         snk_qtd_disponivel = estoque_snk.get('qtd')
        #         olEst = olEstoque()
        #         if await olEst.buscar(id=estoque_snk.get('ad_mkp_idprod')):
        #             estoque_olist = await olEst.encodificar()
        #             ol_qtd_disponivel = estoque_olist.get('disponivel')                    
        #             if ol_qtd_disponivel != snk_qtd_disponivel:
        #                 ol_qtd_reservado = estoque_olist.get('reservado')
        #                 saldo = snk_qtd_disponivel + ol_qtd_reservado
        #                 ajuste_estoque = {
        #                     "id": int(estoque_snk.get('ad_mkp_idprod')),
        #                     "deposito": int(estoque_olist.get('depositos')[0].get('id')),
        #                     "tipo":"B",
        #                     "quantidade":saldo
        #                 }
        #                 olEst.tipo = ajuste_estoque.get('tipo')
        #                 olEst.quantidade = ajuste_estoque.get('quantidade')
        #                 olEst.acao = 'post'
        #                 if await olEst.enviar_saldo():
        #                     await self.remove_syncestoque(produto=estoque_snk.get('codprod'))
        #                     await self.atualiza_historico(produto=produto)
        #                     logger.info(self.contexto+"Estoque do produto %s sincronizado com sucesso",estoque_olist.get('codigo'))
        #                     values.append(f"Estoque do produto {estoque_olist.get('codigo')} sincronizado com sucesso.")
        #                     print(f"Estoque do produto {estoque_olist.get('codigo')} sincronizado com sucesso")
        #                 else:
        #                     print(f"Falha ao sincronizar estoque do produto {estoque_olist.get('codigo')}. Verifique os logs.")
        #                     logger.error(self.contexto+"Falha ao sincronizar estoque do produto %s. Verifique os logs.",estoque_olist.get('codigo'))
        #                     await self.app.email.notificar()
        #                     values.append(f"Falha ao sincronizar estoque do produto {estoque_olist.get('codigo')}. Verifique os logs.")
        #                     print(f"Falha ao sincronizar estoque do produto {estoque_olist.get('codigo')}. Verifique os logs.")
        #             else: 
        #                 await self.atualiza_historico(produto=estoque_snk.get('codprod'))
        #                 logger.info(self.contexto+"Estoque do produto %s já está atualizado.",estoque_snk.get('codprod'))
        #                 values.append(f"Estoque do produto {estoque_snk.get('codprod')} já está atualizado.")
        #                 print(f"Estoque do produto {estoque_snk.get('codprod')} já está atualizado.")
        #         else:
        #             logger.error(self.contexto+"Falha ao buscar dados de estoque do produto %s na base Olist. Verifique os logs.",produto)
        #             await self.app.email.notificar()
        #             values.append(f"Falha ao buscar dados de estoque do produto {produto} na base Olist. Verifique os logs.")
        #             print(f"Falha ao buscar dados de estoque do produto {produto} na base Olist. Verifique os logs.")
        #     else:                
        #         snkEstoques = snkEstoque()                
        #         estoques_snk = await snkEstoques.buscar_disponivel()
        #         for e in estoques_snk:
        #             time.sleep(self.app.req_sleep)                   
        #             snk_qtd_disponivel = e.get('qtd')
        #             olEst = olEstoque()
        #             if await olEst.buscar(id=e.get('ad_mkp_idprod')):
        #                 estoque_olist = await olEst.encodificar()
        #                 ol_qtd_disponivel = estoque_olist.get('disponivel')                        
        #                 if ol_qtd_disponivel != snk_qtd_disponivel:
        #                     ol_qtd_reservado = estoque_olist.get('reservado')
        #                     saldo = snk_qtd_disponivel + ol_qtd_reservado
        #                     ajuste_estoque = {
        #                         "id": int(e.get('ad_mkp_idprod')),
        #                         "deposito": int(estoque_olist.get('depositos')[0].get('id')),
        #                         "tipo":"B",
        #                         "quantidade":saldo
        #                     }
        #                     olEst.tipo = ajuste_estoque.get('tipo')
        #                     olEst.quantidade = ajuste_estoque.get('quantidade')
        #                     olEst.acao = 'post'
        #                     if await olEst.enviar_saldo():
        #                         await self.remove_syncestoque(produto=e.get('codprod'))
        #                         await self.atualiza_historico(produto=e.get('codprod'))
        #                         logger.info(self.contexto+"Estoque do produto %s sincronizado com sucesso.",e.get('codprod'))
        #                         values.append(f"Estoque do produto {e.get('codprod')} sincronizado com sucesso.")                                
        #                         print(f"Estoque do produto {e.get('codprod')} sincronizado com sucesso.")
        #                     else:
        #                         logger.error(self.contexto+"Erro: Falha ao sincronizar estoque do produto %s. Verifique os logs.",e.get('codprod'))
        #                         await self.app.email.notificar()
        #                         values.append(f"Erro: Falha ao sincronizar estoque do produto {e.get('codprod')}. Verifique os logs.")                
        #                         print(f"Erro: Falha ao sincronizar estoque do produto {e.get('codprod')}. Verifique os logs.")
        #                 else:
        #                     await self.atualiza_historico(produto=e.get('codprod'))
        #                     logger.info(self.contexto+"Estoque do produto %s já está atualizado.",e.get('codprod'))
        #                     values.append(f"Estoque do produto {e.get('codprod')} já está atualizado.")
        #                     print(f"Estoque do produto {e.get('codprod')} já está atualizado.")
        #             else:
        #                 logger.error(self.contexto+"Erro: Falha ao buscar dados do estoque do produto %s no Olist. Verifique os logs.",e.get('ad_mkp_idprod'))
        #                 await self.app.email.notificar()
        #                 values.append(f"Falha ao buscar dados do estoque do produto {e.get('ad_mkp_idprod')} no Olist. Verifique os logs.")
        #                 print(f"Falha ao buscar dados do estoque do produto {e.get('ad_mkp_idprod')} no Olist. Verifique os logs.")
        #     print(f"Sincronização concluída!")
        #     return True, values
            pass