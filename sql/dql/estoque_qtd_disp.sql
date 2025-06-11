SELECT
    CODPROD,
    AD_MKP_IDPROD,
    CASE
        -- Política de estoque = TODO O ESTOQUE
        WHEN BASE.AD_MKP_ESTPOL = 'T' THEN (SELECT SUM(ESTOQUE-RESERVADO)
                                            FROM TGFEST EST
                                            WHERE EST.CODPROD = BASE.CODPROD
                                                AND EST.CODLOCAL = 101
                                                AND NVL(EST.CODPARC,0) = 0
                                                AND EST.CODEMP IN (1,31))
        -- Política de estoque = APENAS VALIDADE CURTA
        WHEN BASE.AD_MKP_ESTPOL = 'V' THEN (SELECT SUM(ESTOQUE-RESERVADO)
                                            FROM TGFEST EST
                                            WHERE EST.CODPROD = BASE.CODPROD
                                                AND EST.CODLOCAL = 101
                                                AND EST.CODEMP IN (1,31)
                                                AND NVL(EST.CODPARC,0) = 0
                                                AND TRUNC(EST.DTVAL) - TRUNC(CURRENT_DATE) <= 365)
        -- Política de estoque = REGRA DE BARREIRA
        WHEN BASE.AD_MKP_ESTPOL = 'B' THEN 
            CASE
                -- Tipo de barreira = PORCENTAGEM > calcula estoque mínimo + valor da barreira como ponto de corte
                WHEN BASE.AD_MKP_ESTREGBARTIP = 'P' THEN (SELECT CASE WHEN QTD <= ROUND(BASE.ESTMIN * (BASE.AD_MKP_ESTREGBARVAL/100+1)) THEN 0 ELSE QTD - ROUND(BASE.ESTMIN * (BASE.AD_MKP_ESTREGBARVAL/100+1)) END
                                                        FROM (SELECT SUM(ESTOQUE-RESERVADO) QTD
                                                              FROM TGFEST EST
                                                              WHERE EST.CODPROD = BASE.CODPROD
                                                                AND EST.CODLOCAL = 101
                                                                AND NVL(EST.CODPARC,0) = 0
                                                                AND EST.CODEMP IN (1,31)))
                -- Tipo de barreira = QUANTIDADE > utiliza o valor da barreira como ponto de corte
                WHEN BASE.AD_MKP_ESTREGBARTIP = 'Q' THEN (SELECT CASE WHEN QTD <= BASE.AD_MKP_ESTREGBARVAL THEN 0 ELSE QTD-BASE.AD_MKP_ESTREGBARVAL END
                                                        FROM (SELECT SUM(ESTOQUE-RESERVADO) QTD
                                                              FROM TGFEST EST
                                                              WHERE EST.CODPROD = BASE.CODPROD
                                                                AND EST.CODLOCAL = 101
                                                                AND NVL(EST.CODPARC,0) = 0
                                                                AND EST.CODEMP IN (1,31)))
                 ELSE NULL END
        ELSE NULL
    END QTD
FROM (SELECT CODPROD, AD_MKP_IDPROD, AD_MKP_ESTPOL, AD_MKP_ESTREGBAR, AD_MKP_ESTREGBARVAL, AD_MKP_ESTREGBARTIP, ESTMIN
      FROM TGFPRO PRO WHERE CODPROD = NVL(:P_CODPROD,CODPROD)) BASE
