CREATE OR REPLACE PROCEDURE AD_STP_MKP_GERA_NOTA_TRANSF AS
    V_NEWNUNOTA INT;
BEGIN

    /*******************************************************************************

    @Autor: Rodrigo Vieira <rodrigo.vieira@grupoeisen.com.br>
    @Data: 01/07/2025
    @Objetivo: Gera uma nota de venda da Matriz pra Storya para ressuprimento dos produtos

    ********************************************************************************/

    STP_KEYGEN_TGFNUM('TGFCAB',1,'TGFCAB','NUNOTA',0, V_NEWNUNOTA);

    INSERT INTO TGFCAB (NUNOTA,
                        SERIENOTA,
                        CODEMP,
                        CODEMPNEGOC,
                        CODPARC,
                        CODNAT,
                        CODTIPVENDA,
                        CODTIPOPER,
                        DHTIPOPER,
                        DTNEG,
                        DTALTER,
                        CODVEND,
                        NUMNOTA,
                        CODOBSPADRAO,
                        TIPMOV,
                        CIF_FOB,
                        TIPFRETE,
                        OBSERVACAO)
                VALUES (V_NEWNUNOTA,
                        1,
                        1,
                        31,
                        27730,
                        1010101,
                        0,
                        1419,
                        (SELECT MAX(DHALTER) FROM TGFTOP WHERE CODTIPOPER = 1419),
                        TO_DATE(TO_CHAR(SYSDATE, 'DD/MM/YYYY')),
                        SYSDATE,
                        1,
                        0,
                        0,
                        'T',
                        'C',
                        'N',
                        'Transferencia entre empresas para ressuprimento e atendimento de pedidos Shopee.'
                        );
END;