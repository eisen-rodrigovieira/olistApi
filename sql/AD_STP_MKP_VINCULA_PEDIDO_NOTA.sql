CREATE OR REPLACE PROCEDURE AD_STP_MKP_VINCULA_PEDIDO_NOTA(
    P_NUNOTA_PEDIDO IN NUMBER, -- Número único do pedido
    P_NUNOTA_NOTA   IN NUMBER  -- Número único da nota
) AS    
BEGIN
    /*******************************************************************************

    @Autor: Rodrigo Vieira <rodrigo.vieira@grupoeisen.com.br>
    @Data: 01/07/2025
    @Objetivo: Vincular o Pedido com a Nota

    ********************************************************************************/

    -- CRIANDO VINCULO PEDIDO X NOTA
    FOR VINCULO IN ( SELECT NOTA.CODPROD,
                            NOTA.QTDNEG,
                            PED.SEQUENCIA SEQPED,
                            NOTA.SEQUENCIA SEQNOTA
                    FROM TGFITE NOTA
                        INNER JOIN TGFITE PED ON NOTA.CODPROD = PED.CODPROD
                                             AND PED.NUNOTA = P_NUNOTA_PEDIDO
                    WHERE NOTA.NUNOTA = P_NUNOTA_NOTA )
        LOOP
        BEGIN
            INSERT INTO TGFVAR (NUNOTA       ,NUNOTAORIG     ,QTDATENDIDA   ,SEQUENCIA      ,SEQUENCIAORIG ,STATUSNOTA)
                        VALUES (P_NUNOTA_NOTA,P_NUNOTA_PEDIDO,VINCULO.QTDNEG,VINCULO.SEQNOTA,VINCULO.SEQPED,'P');
        END;
    END LOOP; 

END;