CREATE OR REPLACE PROCEDURE AD_STP_MKP_IMPORTA_XML_VENDA(
                    P_NUNOTA       IN  NUMBER,   -- Número único da nota no Sankhya
                    P_NULOTE       IN  NUMBER,   -- Número do lote da NFe
                    P_DHRECEB      IN  VARCHAR2, -- Data e hora do recebimento da NFe no Olist
                    P_CHAVENFE     IN  VARCHAR2, -- Chave de acesso da NFe no Olist
                    P_NUMALEATORIO IN  NUMBER,   -- Número aleatório da NFe no Olist
                    P_XML          IN  CLOB      -- XML da NFe
) AS
BEGIN

    /*******************************************************************************

    @Autor: Rodrigo Vieira <rodrigo.vieira@grupoeisen.com.br>
    @Data: 02/07/2025
    @Objetivo: Importa dos dados da NFe para o Sankhya

    ********************************************************************************/

    INSERT INTO TGFLNF ( DHRECEB, NULOTE ) VALUES ( TO_DATE(P_DHRECEB,'YYYY-MM-DD HH24:MI:SS'), P_NULOTE );

    INSERT INTO TGFNFE ( CHAVENFE, NUNOTA, XML ) VALUES ( P_CHAVENFE, P_NUNOTA, P_XML );

    UPDATE TGFCAB
    SET    CHAVENFE      = P_CHAVENFE,
           DTALTER       = CURRENT_DATE,
           NUMALEATORIO  = P_NUMALEATORIO,
           TPAMBNFE      = 2,
           TPEMISNFE     = 1,
           NULOTENFE     = P_NULOTE,
           VLRLIQITEMNFE = 'N',
           STATUSNFE     = 'A'
    WHERE  TGFCAB.NUNOTA = P_NUNOTA;
END;