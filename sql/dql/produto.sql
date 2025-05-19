SELECT --*
    DECODE(PRO.AD_MKP_INTEGRADO,'S',1,0) AS INTEGRAR_MKP,
    PRO.AD_MKP_IDPROD                    AS ID,
    PRO.CODPROD                          AS SKU,
    INITCAP(TRIM(
        CASE
            WHEN PRO.MARCA = 'Q BELA MAN' THEN REPLACE(PRO.DESCRPROD,'Q BELA MANUELA','')
            WHEN PRO.MARCA = 'PHA BEAUTY' THEN REPLACE(PRO.DESCRPROD,'PHALLE BEAUTY','')
            WHEN PRO.MARCA = 'AIR PURE'   THEN REPLACE(PRO.DESCRPROD,'AIRPURE','')
            WHEN PRO.MARCA = 'A HICKMAN'  THEN REPLACE(PRO.DESCRPROD,'ANA HICKMANN','')
            WHEN PRO.MARCA = 'GP REMOVE'  THEN REPLACE(PRO.DESCRPROD,'CARMESIM','')
            ELSE REPLACE(PRO.DESCRPROD,PRO.MARCA,'')
        END
    ))                                  AS DESCRICAO_FORMATADA,
    AD_MKP_NOME                         AS DESCRICAO,
    AD_MKP_DESCRICAO                    AS DESCRICAO_COMPLEMENTAR,
    'S'                                 AS TIPO,
    'A'                                 AS SITUACAO,
    AD_MKP_IDPRODPAI                    AS PRODUTO_PAI,
    PRO.CODVOL                          AS UNIDADE,
    1                                   AS UNIDADE_POR_CAIXA,
    PRO.NCM                             AS NCM,
    PRO.REFERENCIA                      AS GTIN,
    PRO.ORIGPROD                        AS ORIGEM,
    PRO.CODESPECST                      AS CEST,
    NULL                                AS GARANTIA,
    NULL                                AS OBSERVACOES,
    AD_MKP_CATEGORIA                    AS ID_CATEGORIA,
    DECODE( PRO.MARCA,
        'Q BELA MAN','Q BELA MANUELA',
        'PHA BEAUTY','PHALLE BEAUTY',
        'AIR PURE','AIRPURE',
        'A HICKMAN','ANA HICKMANN',
        'GP REMOVE','CARMESIM',
        PRO.MARCA )                     AS MARCA_NOME,
    2                                   AS EMBALAGEM_TIPO,
    LARGURA                             AS LARGURA,
    ALTURA                              AS ALTURA,
    ESPESSURA                           AS COMPRIMENTO,
    NULL                                AS DIAMETRO,
    PESOLIQ                             AS PESO_LIQUIDO,
    PESOBRUTO                           AS PESO_BRUTO,    
    QTDEMB                              AS QUANTIDADE_VOLUMES,
    -- (   -- PREÇO MAIS RECENTE DO PRODUTO NA TABELA OUTBEAUTY
    --     SELECT DISTINCT
    --         FIRST_VALUE(EXC.VLRVENDA) OVER (ORDER BY TAB.DTVIGOR DESC) 
    --     FROM TGFTAB TAB INNER JOIN TGFEXC EXC ON TAB.NUTAB = EXC.NUTAB
    --     WHERE TAB.CODTAB = 21 AND EXC.CODPROD = PRO.CODPROD
    -- )                                   AS PRECO,
    0 AS PRECO,
    (   -- PREÇO DE CUSTO MAIS RECENTE DO PRODUTO
        SELECT DISTINCT 
            FIRST_VALUE(CUS.CUSMED) OVER (ORDER BY CUS.DTATUAL DESC)
        FROM TGFCUS CUS
        WHERE CUS.CODEMP IN (1,31) AND CUS.CODPROD = PRO.CODPROD
    )                                   AS PRECO_CUSTO,
    'True'                              AS ESTOQUE_CONTROLAR,
    'False'                             AS ESTOQUE_SOB_ENCOMENDA,
    0                                   AS ESTOQUE_DIAS_PREPARACAO,
    NULL                                AS ESTOQUE_LOCALIZACAO,
    PRO.ESTMIN                          AS ESTOQUE_MINIMO,
    PRO.ESTMAX                          AS ESTOQUE_MAXIMO,
    NULL                                AS ESTOQUE_QUANTIDADE,
    NULL                                AS ESTOQUE_INICIAL,
    753053887                           AS FORNECEDOR_ID,
    PRO.REFFORN                         AS FORNECEDOR_CODIGO_PRODUTO,
    PRO.REFERENCIA                      AS GTIN_EMBALAGEM   
FROM TGFPRO PRO   
WHERE 1=1
    AND (PRO.CODPROD = :COD OR PRO.AD_MKP_IDPROD = :ID)