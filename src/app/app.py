import os
import json
import logging
from datetime                    import datetime
from src.olist.produto.produto   import Produto as olProduto
from src.sankhya.produto.produto import Produto as snkProduto
from params                      import config,configOlist,configSankhya

logger = logging.getLogger(__name__)
logging.basicConfig(filename=config.PATH_LOGS,
                    encoding='utf-8',
                    format=config.LOGGER_FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

class App:

    def __init__(self):
        pass

    def atualiza_historico(self, produtos_alterados:list=None):

        if not os.path.exists(configOlist.PATH_HISTORICO_PRODUTO):
            logger.error("Histórico de produtos não encontrado em %s",configOlist.PATH_HISTORICO_PRODUTO)
            return {"status":"Erro"}
        else:    
            with open(configOlist.PATH_HISTORICO_PRODUTO, "r", encoding="utf-8") as f:
                historico = json.load(f)        

        if produtos_alterados:
            historico["ultima_atualizacao_olist_sankhya"]["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            historico["ultima_atualizacao_olist_sankhya"]["id"] = produtos_alterados[0]["id"]
            with open(configOlist.PATH_HISTORICO_PRODUTO, "w", encoding="utf-8") as f:
                json.dump(historico, f, indent=4, ensure_ascii=False)
        else:
            pass 

        

    async def snk_atualizar_produtos(self):
            
        print("Iniciando busca dos produtos com alteração no Olist.")
        _olProd = olProduto()
        produtos_com_alteracao = await _olProd.buscar_alteracoes()
        if produtos_com_alteracao:
            print(f"{len(produtos_com_alteracao)} produtos com alteração encontrados.")
            print("Iniciando sincronização")

            for produto in produtos_com_alteracao:
                snkProd = snkProduto()
                olProd  = olProduto()
                if produto:                
                    snkProd.sku = produto["sku"]
                    olProd.id   = produto["id"]

                    if await olProd.buscar():
                        if olProd.tipo == 'S' and await snkProd.buscar():
                            print("")                    
                            print(f"Comparando dados do produto {snkProd.sku}")                    
                            new_id                          = olProd.id                          if int(snkProd.id or 0)                          != int(olProd.id or 0)                          else None
                            #new_sku                         = olProd.sku                         if int(snkProd.sku or 0)                         != int(olProd.sku or 0)                         else None
                            new_descricao                   = olProd.descricao                   if snkProd.descricao                             != olProd.descricao                             else None
                            new_descricaoComplementar       = olProd.descricaoComplementar       if snkProd.descricaoComplementar                 != olProd.descricaoComplementar                 else None
                            new_tipo                        = olProd.tipo                        if snkProd.tipo                                  != olProd.tipo                                  else None
                            new_situacao                    = olProd.situacao                    if snkProd.situacao                              != olProd.situacao                              else None
                            new_produtoPai_id               = olProd.produtoPai_id               if int(snkProd.produtoPai_id or 0)               != int(olProd.produtoPai_id or 0)               else None
                            new_unidade                     = olProd.unidade                     if snkProd.unidade                               != olProd.unidade                               else None
                            new_unidadePorCaixa             = olProd.unidadePorCaixa             if int(snkProd.unidadePorCaixa or 0)             != int(olProd.unidadePorCaixa or 0)             else None
                            new_ncm                         = olProd.ncm                         if snkProd.ncm                                   != olProd.ncm                                   else None
                            new_gtin                        = olProd.gtin                        if snkProd.gtin                                  != olProd.gtin                                  else None
                            new_origem                      = olProd.origem                      if int(snkProd.origem or 0)                      != int(olProd.origem or 0)                      else None
                            new_cest                        = olProd.cest                        if snkProd.cest                                  != olProd.cest                                  else None
                            new_garantia                    = olProd.garantia                    if snkProd.garantia                              != olProd.garantia                              else None
                            new_observacoes                 = olProd.observacoes                 if snkProd.observacoes                           != olProd.observacoes                           else None
                            new_categoria_id                = olProd.categoria_id                if int(snkProd.categoria_id or 0)                != int(olProd.categoria_id or 0)                else None
                            new_categoria_nome              = olProd.categoria_nome              if snkProd.categoria_nome                        != olProd.categoria_nome                        else None
                            new_marca_id                    = olProd.marca_id                    if int(snkProd.marca_id or 0)                    != int(olProd.marca_id or 0)                    else None
                            new_marca_nome                  = olProd.marca_nome                  if snkProd.marca_nome                            != olProd.marca_nome                            else None
                            new_dimensoes_embalagem_tipo    = olProd.dimensoes_embalagem_tipo    if snkProd.dimensoes_embalagem_tipo              != olProd.dimensoes_embalagem_tipo              else None
                            new_dimensoes_largura           = olProd.dimensoes_largura           if float(snkProd.dimensoes_largura or 0)         != float(olProd.dimensoes_largura or 0)         else None
                            new_dimensoes_altura            = olProd.dimensoes_altura            if float(snkProd.dimensoes_altura or 0)          != float(olProd.dimensoes_altura or 0)          else None
                            new_dimensoes_comprimento       = olProd.dimensoes_comprimento       if float(snkProd.dimensoes_comprimento or 0)     != float(olProd.dimensoes_comprimento or 0)     else None
                            new_dimensoes_pesoLiquido       = olProd.dimensoes_pesoLiquido       if float(snkProd.dimensoes_pesoLiquido or 0)     != float(olProd.dimensoes_pesoLiquido or 0)     else None
                            new_dimensoes_pesoBruto         = olProd.dimensoes_pesoBruto         if float(snkProd.dimensoes_pesoBruto or 0)       != float(olProd.dimensoes_pesoBruto or 0)       else None
                            new_dimensoes_quantidadeVolumes = olProd.dimensoes_quantidadeVolumes if int(snkProd.dimensoes_quantidadeVolumes or 0) != int(olProd.dimensoes_quantidadeVolumes or 0) else None
                            new_preco                       = olProd.preco                       if float(snkProd.preco or 0)                     != float(olProd.preco or 0)                     else None
                            new_precoCusto                  = olProd.precoCusto                  if float(snkProd.precoCusto or 0)                != float(olProd.precoCusto or 0)                else None
                            new_estoque_controlar           = olProd.estoque_controlar           if snkProd.estoque_controlar                     != olProd.estoque_controlar                     else None
                            new_estoque_sobEncomenda        = olProd.estoque_sobEncomenda        if snkProd.estoque_sobEncomenda                  != olProd.estoque_sobEncomenda                  else None
                            new_estoque_diasPreparacao      = olProd.estoque_diasPreparacao      if int(snkProd.estoque_diasPreparacao or 0)      != int(olProd.estoque_diasPreparacao or 0)      else None
                            new_estoque_localizacao         = olProd.estoque_localizacao         if snkProd.estoque_localizacao                   != olProd.estoque_localizacao                   else None
                            new_estoque_minimo              = olProd.estoque_minimo              if int(snkProd.estoque_minimo or 0)              != int(olProd.estoque_minimo or 0)              else None
                            new_estoque_maximo              = olProd.estoque_maximo              if int(snkProd.estoque_maximo or 0)              != int(olProd.estoque_maximo or 0)              else None
                            new_estoque_quantidade          = olProd.estoque_quantidade          if int(snkProd.estoque_quantidade or 0)          != int(olProd.estoque_quantidade or 0)          else None
                            new_estoque_inicial             = olProd.estoque_inicial             if int(snkProd.estoque_inicial or 0)             != int(olProd.estoque_inicial or 0)             else None
                            new_tributacao_gtinEmbalagem    = olProd.tributacao_gtinEmbalagem    if snkProd.tributacao_gtinEmbalagem              != olProd.tributacao_gtinEmbalagem              else None

                            if olProd.fornecedores:
                                new_fornecedor_id             = olProd.fornecedores[0].id  if int(snkProd.fornecedor_id or 0) != int(olProd.fornecedores[0].id or 0) else None
                                new_fornecedor_codigo_produto = olProd.fornecedores[0].codigoProdutoNoFornecedor if snkProd.fornecedor_codigo_produto != olProd.fornecedores[0].codigoProdutoNoFornecedor else None
                            else:
                                new_fornecedor_id             = None
                                new_fornecedor_codigo_produto = None  

                            with open(configSankhya.PATH_PARAMS_UPDATE_PRODUTO, "r", encoding="utf-8") as f:
                                params = json.load(f)
                                params['COD']                       = snkProd.sku
                                params['ID']                        = new_id
                                params['DESCRICAO']                 = new_descricao
                                params['DESCRICAO_COMPLEMENTAR']    = new_descricaoComplementar
                                params['PRODUTO_PAI_ID']            = new_produtoPai_id
                                params['UNIDADE']                   = new_unidade
                                params['NCM']                       = new_ncm
                                params['GTIN']                      = new_gtin
                                params['ORIGEM']                    = new_origem
                                params['CEST']                      = new_cest
                                params['CATEGORIA_NOME']            = new_categoria_nome
                                params['LARGURA']                   = new_dimensoes_largura
                                params['ALTURA']                    = new_dimensoes_altura
                                params['ESPESSURA']                 = new_dimensoes_comprimento
                                params['PESO_LIQUIDO']              = new_dimensoes_pesoLiquido
                                params['PESO_BRUTO']                = new_dimensoes_pesoBruto
                                params['QUANTIDADE_VOLUMES']        = new_dimensoes_quantidadeVolumes
                                params['ESTOQUE_MINIMO']            = new_estoque_minimo
                                params['ESTOQUE_MAXIMO']            = new_estoque_maximo
                                params['FORNECEDOR_ID']             = new_fornecedor_id
                                params['FORNECEDOR_CODIGO_PRODUTO'] = new_fornecedor_codigo_produto     

                            necessita_atualizar = 0
                            for value in params.values():
                                if not (value is None or value == ''): necessita_atualizar+=1
                            if necessita_atualizar > 1:
                                print(f"Atualizando produto {snkProd.sku}")
                                ack, num = await snkProd.atualizar(params=params)
                                if ack:
                                    print(f"Produto {snkProd.sku} atualizado com sucesso.")
                                else:
                                    raise Exception(f"Falha ao atualziar os dados do produto {snkProd.sku} na base Sankhya. Verifique os logs.")
                            else:
                                print(f"Produto {snkProd.sku} sem atualizações a serem sincronizadas Olist > Sankhya") 
                        else:
                            if olProd.tipo == 'S':
                                print(f"Produto {olProd.id} é mestre (não tem vínculo com o Sankhya por SKU)") 
                            else:
                                print(f"Produto {olProd.id} não tem vínculo com o Sankhya (SKU em branco)") 
                    else:
                        raise Exception(f"Falha ao buscar os dados do produto {snkProd.sku} na base Sankhya. Verifique os logs.")
                else:
                    pass                    
            print("Rotina concluída.") 
            self.atualiza_historico(produtos_alterados=produtos_com_alteracao)
        else: 
            print("Nenhum produto com alteração")