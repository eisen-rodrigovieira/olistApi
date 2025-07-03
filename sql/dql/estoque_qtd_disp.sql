SELECT
    CODPROD,
    AD_MKP_IDPROD,
    CONTROLA_LOTE,
    CONTROLE,
    DTVAL,
    DTFABRICACAO,
    SUM(CASE WHEN AD_MKP_ESTPOL IN ('T','V') THEN ESTOQUE
         ELSE ROUND(ESTOQUE_TOTAL * PROPORCAO)
    END) ESTOQUE,
    ESTOQUE_TOTAL,
    RESERVADO
FROM
(   SELECT
        BASE.CODPROD,
        BASE.AD_MKP_IDPROD,
        BASE.CONTROLE,
        BASE.DTVAL,
        BASE.DTFABRICACAO,    
        BASE.AD_MKP_ESTPOL,
        BASE.AD_MKP_ESTREGBARTIP,
        BASE.CONTROLA_LOTE,
        BASE.ESTOQUE,
        BASE.PROPORCAO,
        CASE
            -- Política de estoque = TODO O ESTOQUE
            WHEN BASE.AD_MKP_ESTPOL = 'T' THEN ESTOQUE_TOTAL
            -- Política de estoque = APENAS VALIDADE CURTA
            WHEN BASE.AD_MKP_ESTPOL = 'V' THEN ESTOQUE_TOTAL - (SELECT SUM(ESTOQUE)
                                                                FROM TGFEST EST
                                                                WHERE EST.CODPROD = BASE.CODPROD
                                                                    AND EST.CODLOCAL = 101
                                                                    AND EST.CODEMP IN (1,31)
                                                                    AND NVL(EST.CODPARC,0) = 0
                                                                    AND TRUNC(EST.DTVAL) - TRUNC(CURRENT_DATE) > 365)
            -- Política de estoque = REGRA DE BARREIRA
            WHEN BASE.AD_MKP_ESTPOL = 'B' THEN 
                CASE
                    -- Tipo de barreira = PORCENTAGEM > calcula estoque mínimo + valor da barreira como ponto de corte
                    WHEN BASE.AD_MKP_ESTREGBARTIP = 'P' THEN CASE WHEN ESTOQUE_TOTAL <= ROUND(BASE.ESTMIN * (BASE.AD_MKP_ESTREGBARVAL/100+1)) THEN 0
                                                                  ELSE ESTOQUE_TOTAL - ROUND(BASE.ESTMIN * (BASE.AD_MKP_ESTREGBARVAL/100+1)) END
                    -- Tipo de barreira = QUANTIDADE > utiliza o valor da barreira como ponto de corte
                    WHEN BASE.AD_MKP_ESTREGBARTIP = 'Q' THEN CASE WHEN ESTOQUE_TOTAL <= BASE.AD_MKP_ESTREGBARVAL THEN 0
                                                                  ELSE ESTOQUE_TOTAL - BASE.AD_MKP_ESTREGBARVAL END
                    ELSE NULL
                END
            ELSE NULL
        END ESTOQUE_TOTAL,
        BASE.RESERVADO
    FROM
    (   SELECT
            PRO.CODPROD,
            PRO.AD_MKP_IDPROD,
            PRO.AD_MKP_ESTPOL,
            PRO.AD_MKP_ESTREGBAR,
            PRO.AD_MKP_ESTREGBARVAL,
            PRO.AD_MKP_ESTREGBARTIP,
            PRO.ESTMIN,
            DECODE(PRO.TIPCONTEST,'L','S','N') CONTROLA_LOTE,
            EST.CONTROLE,
            EST.DTVAL,
            EST.DTFABRICACAO,
            EST.ESTOQUE,
            NVL(ROUND(EST.ESTOQUE / NULLIF(SUM(EST.ESTOQUE) OVER (PARTITION BY EST.CODPROD),0),2),0) PROPORCAO,
            SUM(EST.ESTOQUE) OVER (PARTITION BY EST.CODPROD) ESTOQUE_TOTAL,
            SUM(EST.RESERVADO) OVER (PARTITION BY EST.CODPROD) RESERVADO
        FROM TGFPRO PRO
            INNER JOIN TGFEST EST ON PRO.CODPROD = EST.CODPROD
        WHERE PRO.CODPROD            = NVL(:P_CODPROD,PRO.CODPROD)
            AND EST.CODLOCAL         = 101
            AND NVL(EST.CODPARC,0)   = 0
            AND EST.ESTOQUE          >= 0
            AND PRO.AD_MKP_INTEGRADO = 'S'
            AND EST.CODEMP           IN (1,31)
    ) BASE 
    WHERE BASE.ESTOQUE > 0 OR NVL(BASE.CONTROLE,'') != '' 
) GROUP BY CODPROD,AD_MKP_IDPROD,CONTROLA_LOTE,CONTROLE,DTVAL,DTFABRICACAO,ESTOQUE_TOTAL,RESERVADO   
ORDER BY DTVAL DESC
