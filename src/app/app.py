import os
import re
import time
import json
import logging
from datetime                    import datetime
from src.sankhya.dbConfig        import dbConfig
from params                      import config,configUtils,configOlist,configSankhya
from src.olist.produto.produto   import Produto as olProduto
from src.olist.pedido.pedido     import Pedido  as olPedido
from src.sankhya.produto.produto import Produto as snkProduto
from src.sankhya.pedido.pedido   import Pedido  as snkPedido
from src.utils.sendMail          import sendMail
from src.utils.validaPath        import validaPath

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
                file_path_del   = configSankhya.PATH_UPDATE_PRODUTO_NEW
                delete_syncprod = self.app.valida_path.validar(path=file_path_del,method='full',mode='r')
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
                file_path   = configSankhya.PATH_UPDATE_PRODUTO_NEW
                new_syncprod = self.app.valida_path.validar(path=file_path,method='full',mode='r')
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
                
            #print("Iniciando busca dos produtos com alteração no Olist.")
            _olProd = olProduto()
            produtos_com_alteracao = await _olProd.enviar_alteracoes()
            if produtos_com_alteracao:
                #print(f"{len(produtos_com_alteracao)} produtos com alteração encontrados.")
                #print("Iniciando sincronização")

                for produto in produtos_com_alteracao:
                    #print("")                   
                    
                    snkProd = snkProduto()
                    olProd  = olProduto()
                    if produto["sku"]:
                        time.sleep(self.app.req_sleep)             
                        snkProd.sku = produto["sku"]
                        olProd.id   = produto["id"]

                        if await olProd.buscar():
                            if olProd.tipo == 'S' and olProd.sku and await snkProd.buscar():
                                                
                                #print(f"Comparando dados do produto {snkProd.sku}")     
                                olProd.ncm = re.sub(regex_cest_ncm, '', olProd.ncm)

                                new_id                          = olProd.id                          if int(snkProd.id or 0)                          != int(olProd.id or 0)                          else None
                                # new_sku                         = olProd.sku                         if int(snkProd.sku or 0)                         != int(olProd.sku or 0)                         else None
                                new_descricao                   = olProd.descricao                   if snkProd.descricao                             != olProd.descricao                             else None
                                new_descricaoComplementar       = olProd.descricaoComplementar       if snkProd.descricaoComplementar                 != olProd.descricaoComplementar                 else None
                                # new_tipo                        = olProd.tipo                        if snkProd.tipo                                  != olProd.tipo                                  else None
                                # new_situacao                    = olProd.situacao                    if snkProd.situacao                              != olProd.situacao                              else None
                                new_produtoPai_id               = olProd.produtoPai_id               if int(snkProd.produtoPai_id or 0)               != int(olProd.produtoPai_id or 0)               else None
                                new_unidade                     = olProd.unidade                     if snkProd.unidade                               != olProd.unidade                               else None
                                # new_unidadePorCaixa             = olProd.unidadePorCaixa             if int(snkProd.unidadePorCaixa or 0)             != int(olProd.unidadePorCaixa or 0)             else None
                                new_ncm                         = olProd.ncm                         if snkProd.ncm                                   != olProd.ncm                                   else None
                                new_gtin                        = olProd.gtin                        if snkProd.gtin                                  != olProd.gtin                                  else None
                                new_origem                      = olProd.origem                      if int(snkProd.origem or 0)                      != int(olProd.origem or 0)                      else None
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
                                    params['UNIDADE']                   = new_unidade
                                    params['ID_MARCA']                  = new_marca_id
                                    params['NCM']                       = new_ncm
                                    params['GTIN']                      = new_gtin
                                    params['ORIGEM']                    = new_origem
                                    params['CEST']                      = snkProd.cest
                                    params['ID_CATEGORIA']              = new_categoria_id
                                    params['LARGURA']                   = new_dimensoes_largura
                                    params['ALTURA']                    = new_dimensoes_altura
                                    params['ESPESSURA']                 = new_dimensoes_comprimento
                                    params['PESO_LIQUIDO']              = new_dimensoes_pesoLiquido
                                    params['PESO_BRUTO']                = new_dimensoes_pesoBruto
                                    params['QUANTIDADE_VOLUMES']        = new_dimensoes_quantidadeVolumes
                                    params['ESTOQUE_MINIMO']            = new_estoque_minimo
                                    params['ESTOQUE_MAXIMO']            = new_estoque_maximo                                
                                    params['FORNECEDOR_CODIGO_PRODUTO'] = new_fornecedor_codigo_produto     

                                necessita_atualizar = 0
                                for value in params.values():
                                    if not (value is None or value == ''): necessita_atualizar+=1
                                if necessita_atualizar > 1:
                                    #print(f"Atualizando produto {snkProd.sku}")
                                    ack, num = await snkProd.atualizar(params=params)
                                    if ack:
                                        res.append(f"Produto {snkProd.sku} atualizado com sucesso.")                                        
                                        #print(f"Produto {snkProd.sku} atualizado com sucesso.")
                                        await self.atualiza_historico(produto_alterado=snkProd.id,sentido=1)
                                    else:
                                        await self.app.email.notificar()
                                        res.append(f"Falha ao atualizar os dados do produto {snkProd.id} na base Sankhya. Verifique os logs.")
                                else:
                                    res.append(f"Produto {snkProd.id} sem atualizações a serem sincronizadas Olist > Sankhya")
                                    #print(f"Produto {snkProd.id} sem atualizações a serem sincronizadas Olist > Sankhya") 
                            else:
                                if olProd.tipo == 'V':
                                    res.append(f"Produto {olProd.id} é mestre (não tem vínculo com o Sankhya por SKU)") 
                                    #print(f"Produto {olProd.id} é mestre (não tem vínculo com o Sankhya por SKU)") 
                                else:
                                    await self.app.email.notificar()
                                    res.append(f"Produto {olProd.id} não tem vínculo com o Sankhya (SKU em branco ou inválido)") 
                                    #print(f"Produto {olProd.id} não tem vínculo com o Sankhya (SKU em branco ou inválido)") 
                        else:
                            await self.app.email.notificar()
                            res.append(f"Falha ao buscar os dados do produto {olProd.id} na base Olist. Verifique os logs.")
                    else:
                        await self.app.email.notificar()
                        res.append(f"Produto {produto["id"]} não tem vínculo com o Sankhya (sem SKU)")
                        #print(f"Produto {produto["id"]} não tem vínculo com o Sankhya (sem SKU)")
                print("Rotina concluída.")   
                return True, res        
            else: 
                res.append("Nenhum produto com alteração")
                #print("Nenhum produto com alteração")
                return True, res

        async def ol_atualizar_produtos(self) -> tuple[bool,list]:
            
            regex_cest_ncm = r"[.]"
            values = []
            fetch = None

            file_path_fetch = configSankhya.PATH_SCRIPT_SYNCPROD
                
            #print("Iniciando busca das alterações no Sankhya.")
            query_syncprod = await self.app.valida_path.validar(path=file_path_fetch,method='full',mode='r')

            fetch = await self.app.db.select(query=query_syncprod)
            
            if fetch:            
                # print(f"{len(fetch)} alterações encontradas.")
                # print("Iniciando sincronização")                        
                for f in fetch:
                    ackOl = ackSnk = None
                    # print("")
                    time.sleep(self.app.req_sleep)
                    if f["evento"] == 'A':                        
                        olProd  = olProduto()
                        snkProd = snkProduto()

                        olProd.id = f["idprod"]
                        if await olProd.buscar():
                            ackOl = True
                        else:
                            await self.app.email.notificar()
                            values.append(f"Falha ao buscar os dados do produto {f["idprod"]} na base Olist. Verifique os logs.")

                        snkProd.sku = f["codprod"]
                        if await snkProd.buscar():
                            ackSnk = True
                        else: 
                            await self.app.email.notificar()
                            values.append(f"Falha ao buscar os dados do produto {f["codprod"]} na base Sankhya. Verifique os logs.")

                        # print(f"Comparando dados do produto {olProd.id}")  
                        if ackOl and ackSnk:
                            olProd.ncm = re.sub(regex_cest_ncm, '', olProd.ncm)
                            olProd.descricao                   = snkProd.descricao                   if snkProd.descricao                             != olProd.descricao                             else olProd.descricao
                            olProd.descricaoComplementar       = snkProd.descricaoComplementar       if snkProd.descricaoComplementar                 != olProd.descricaoComplementar                 else olProd.descricaoComplementar
                            olProd.tipo                        = snkProd.tipo                        if snkProd.tipo                                  != olProd.tipo                                  else olProd.tipo
                            olProd.situacao                    = snkProd.situacao                    if snkProd.situacao                              != olProd.situacao                              else olProd.situacao
                            olProd.produtoPai_id               = snkProd.produtoPai_id               if int(snkProd.produtoPai_id or 0)               != int(olProd.produtoPai_id or 0)               else olProd.produtoPai_id
                            olProd.unidade                     = snkProd.unidade                     if snkProd.unidade                               != olProd.unidade                               else olProd.unidade
                            olProd.unidadePorCaixa             = snkProd.unidadePorCaixa             if int(snkProd.unidadePorCaixa or 0)             != int(olProd.unidadePorCaixa or 0)             else olProd.unidadePorCaixa
                            olProd.ncm                         = snkProd.ncm                         if snkProd.ncm                                   != olProd.ncm                                   else olProd.ncm
                            olProd.gtin                        = snkProd.gtin                        if snkProd.gtin                                  != olProd.gtin                                  else olProd.gtin
                            olProd.origem                      = snkProd.origem                      if int(snkProd.origem or 0)                      != int(olProd.origem or 0)                      else olProd.origem
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

                            # print(f"Atualizando produto {olProd.id}")
                            ackReceberOlist, val = await olProd.receber_alteracoes()
                            if ackReceberOlist and bool(val):
                                ackSync = await self.remove_syncprod(produto=f["codprod"],dhevento=f["dhevento"])
                                if ackSync:
                                    values.append(f"Produto {olProd.id} atualizado com sucesso.")
                                    #print(f"Produto {olProd.id} atualizado com sucesso.")
                                    await self.atualiza_historico(produto_alterado=f["idprod"],sentido=0)
                                else:
                                    await self.app.email.notificar()
                                    values.append(f"Erro: Produto {olProd.id} atualizado na base Olist mas não foi possível remover da lista de atualizações pendentes na base Sankhya. Verifique os logs.")
                            elif ackReceberOlist and val == 0:
                                await self.app.email.notificar()
                                values.append(f"Produto {olProd.id} não encontrado")
                            else:
                                await self.app.email.notificar()
                                values.append(f"Falha ao atualizar os dados do produto {olProd.id} na base Olist. Verifique os logs.")
                                                    
                    elif f["evento"] == 'E':
                        olProd  = olProduto()
                        snkProd = snkProduto()

                        olProd.id = f["idprod"]
                        if await olProd.buscar():
                            ackOl = True
                        else:
                            await self.app.email.notificar()                            
                            values.append(f"Falha ao buscar os dados do produto {f["idprod"]} na base Olist. Verifique os logs.")

                        if ackOl:
                            olProd.situacao = 'I'
                            olProd.acao = 'del'

                            #print(f"Inativando produto {olProd.id}")
                            ackReceberOlist, val = await olProd.receber_alteracoes()
                            if ackReceberOlist and bool(val):
                                ackSync = await self.remove_syncprod(produto=f["codprod"],dhevento=f["dhevento"])
                                if ackSync:
                                    values.append(f"Produto {olProd.id} inativado com sucesso.")
                                    #print(f"Produto {olProd.id} inativado com sucesso.")
                                    await self.atualiza_historico(produto_alterado=f["idprod"],sentido=0)
                                else:
                                    await self.app.email.notificar()
                                    values.append(f"Erro: Produto {olProd.id} inativado na base Olist mas não foi possível remover da lista de atualizações pendentes na base Sankhya. Verifique os logs.")
                            elif ackReceberOlist and val == 0:
                                await self.app.email.notificar()
                                values.append(f"Produto {olProd.id} não encontrado")
                            else:
                                await self.app.email.notificar()                            
                                values.append(f"Falha ao intivar os dados do produto {olProd.id} na base Olist. Verifique os logs.")
                        
                    elif f["evento"] == 'I':
                        olP  = olProduto()
                        snkProd = snkProduto()

                        olP.sku = f["codprod"]
                        if not await olP.buscar():
                            # print("Produto não está cadastrado na base Olist.")
                            ackOl = True
                        else:
                            await self.app.email.notificar() 
                            values.append(f"Produto {olProd.id} já cadastrado na base Olist com o mesmo sku {olProd.sku}.")

                        snkProd.sku = f["codprod"]
                        if await snkProd.buscar():
                            # print("Busca bem sucedida")
                            ackSnk = True
                        else: 
                            await self.app.email.notificar()
                            values.append(f"Falha ao buscar os dados do produto {f["codprod"]} na base Sankhya. Verifique os logs.")

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

                            # print(f"Incluindo produto {olProd.sku}")
                            ackReceberOlist, val = await olProd.receber_alteracoes()
                            if ackReceberOlist:
                                ackSync = await self.remove_syncprod(produto=f["codprod"],dhevento=f["dhevento"])
                                ackTgfpro = await self.atualiza_produto_novo(produto=f["codprod"],id=val)
                                if ackSync and ackTgfpro:
                                    values.append(f"Produto {f["codprod"]} incluído com sucesso no ID {val}.")
                                    #print(f"Produto {f["codprod"]} incluído com sucesso no ID {val}.")
                                    await self.atualiza_historico(produto_incluido=val)
                                elif ackSync and not ackTgfpro:
                                    self.app.email.notificar()
                                    values.append(f"Erro: Produto {f["codprod"]} incluído na base Olist mas não foi possível vincular o ID na base Sankhya. Verifique os logs.")
                                elif ackTgfpro and not ackSync:
                                    self.app.email.notificar()
                                    values.append(f"Erro: Produto {f["codprod"]} incluído na base Olist mas não foi possível remover da lista de atualizações pendentes na base Sankhya. Verifique os logs.")
                                else:
                                    self.app.email.notificar()
                                    values.append(f"Erro: Produto {f["codprod"]} incluído na base Olist mas não foi possível atualizar as informações na base Sankhya. Verifique os logs.")
                            else:
                                self.app.email.notificar()
                                values.append(f"Falha ao incluir produto {f["codprod"]} na base Olist. Verifique os logs.")
                #print("Rotina concluída.")
                return True, values
            else:
                values.append("Nenhum produto com alteração")
                return True, values

    class Pedido:

        def __init__(self, id:int=None):
            self.app = App()
            self.id = id
            
        async def atualiza_historico(self, pedido_alterado:int=None, pedido_incluido:int=None, sentido:int=None):
            file_path = configOlist.PATH_HISTORICO_PEDIDO
            historico = await self.app.valida_path.validar(path=file_path,mode='r',method='json')

            if pedido_alterado: # and not pedido_incluido:
                if sentido == 0: # SANKHYA > OLIST
                    historico["ultima_atualizacao_sankhya_olist"]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    historico["ultima_atualizacao_sankhya_olist"]["id"] = pedido_alterado
                elif sentido == 1: # OLIST > SANKHYA
                    historico["ultima_atualizacao_olist_sankhya"]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    historico["ultima_atualizacao_olist_sankhya"]["id"] = pedido_alterado
                else:
                    pass
            if pedido_incluido: # and not pedido_alterado:
                historico["ultima_importacao"]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                historico["ultima_importacao"]["id"] = pedido_incluido

            await self.app.valida_path.validar(path=file_path,mode='w',method='json',content=historico)

        async def busca_novos(self) -> tuple[bool,list]:

            olPd = olPedido()
            res = []

            ack_novos, pedidos_novos = await olPd.buscar_aprovados()
            ack_prep_envio, pedidos_prep_envio = await olPd.buscar_preparando_envio()

            if ack_novos:                
                file_path_exists = configSankhya.PATH_SCRIPT_SYNCPED_NOVO
                query_syncpedido_novo = await self.app.valida_path.validar(path=file_path_exists,method='full',mode='r')
                for novo_pedido in pedidos_novos:
                    self.id = novo_pedido
                    olPed = olPedido()
                    snkPed = snkPedido()
                    exists = await self.app.db.select(query=query_syncpedido_novo,
                                                      params={"AD_MKP_ID":novo_pedido})
                    if not exists:
                        #print("")
                        time.sleep(self.app.req_sleep)
                        if await olPed.buscar(id=novo_pedido):
                            dados_pedido = await olPed.encodificar()
                            ack2, num_unico = await snkPed.registrar(dados_pedido)            
                            if ack2:
                                res.append(f"Pedido #{dados_pedido["numeroPedido"]} importado no nº único {num_unico}") 
                            else:
                                await self.app.email.notificar()
                                res.append(f"Falha ao registrar pedido #{dados_pedido["numeroPedido"]}") 
                        else:
                            await self.app.email.notificar()
                            res.append(f"Falha ao buscar dados do pedido #{dados_pedido["numeroPedido"]}. Verifique os logs")
                        #print("")
                    else:
                        res.append(f"Pedido ID {novo_pedido} já foi importado para o Sankhya no nº único {exists[0].get('nunota')}.")
                    await self.atualiza_historico(pedido_incluido=novo_pedido)
            else:
                await self.app.email.notificar()
                res.append("Falha ao buscar relação dos pedidos novos")
            #print("Fim da rotina :D")

            if ack_prep_envio:    
                file_path_exists = configSankhya.PATH_SCRIPT_SYNCPED_CONF
                query_syncpedido_conf = await self.app.valida_path.validar(path=file_path_exists,method='full',mode='r')                            
                for pedido in pedidos_prep_envio:
                    self.id = pedido
                    olPed   = olPedido()
                    snkPed  = snkPedido()
                    exists  = await self.app.db.select(query=query_syncpedido_conf,
                                                       params={"AD_MKP_ID":pedido})
                    if not exists:
                        #print("")
                        time.sleep(self.app.req_sleep)
                        if await olPed.buscar(id=pedido):
                            dados_pedido = await olPed.encodificar()
                            ack2, num_unico = await snkPed.registrar(dados_pedido)            
                            if ack2:
                                if await snkPed.confirmar_nota(nunota=num_unico,provisao='S'):
                                    res.append(f"Pedido #{dados_pedido["numeroPedido"]} importado no nº único {num_unico}")
                                else:
                                    await self.app.email.notificar()
                                    res.append(f"Falha confirmar pedido. Pedido #{dados_pedido["numeroPedido"]} importado no nº único {num_unico}.")
                            else:
                                await self.app.email.notificar()
                                res.append(f"Falha ao registrar pedido #{dados_pedido["numeroPedido"]}") 
                        else:
                            await self.app.email.notificar()
                            res.append(f"Falha ao buscar dados do pedido #{dados_pedido["numeroPedido"]}. Verifique os logs")
                        #print("")
                    else:
                        if not bool(exists[0].get('confirmado')):
                            if await snkPed.confirmar_nota(nunota=exists[0].get('nunota'),provisao='S'):
                                res.append(f"Pedido ID {pedido} atualizado para confirmado. Nº único {exists[0].get('nunota')}.")
                            else:
                                await self.app.email.notificar()
                                res.append(f"Falha ao confirmar pedido ID {pedido} nº único {num_unico}.")                                
                        else:
                            res.append(f"Sem alterações necessárias no pedido ID {pedido}. Nº único {exists[0].get('nunota')}.")
                    await self.atualiza_historico(pedido_alterado=pedido,sentido=1)
            else:
                await self.app.email.notificar()
                res.append("Falha ao buscar relação dos pedidos em separação")            
            res.append("Importação concluída ✅")            
            return True, res

