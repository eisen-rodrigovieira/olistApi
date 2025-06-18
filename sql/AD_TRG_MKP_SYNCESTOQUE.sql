CREATE OR REPLACE TRIGGER AD_TRG_MKP_SYNCESTOQUE
AFTER INSERT OR UPDATE ON TGFEST
FOR EACH ROW

    /*******************************************************************************

    @Autor: Rodrigo Vieira <rodrigo.vieira@grupoeisen.com.br>
    @Data: 10/06/2025
    @Objetivo: Monitorar movimentações de estoque dos produtos que estão marcados para
      sincronizar com o Olist.

    ********************************************************************************/

DECLARE
    V_VALPRODUTO INT;
    V_VALESTOQUE INT;
    V_IDPROD INT;

BEGIN
    
    -- Verifica se o produto está integrado
    SELECT COUNT(*) INTO V_VALPRODUTO 
    FROM   TGFPRO PRO
    WHERE  PRO.CODPROD = :NEW.CODPROD
       AND NVL(PRO.AD_MKP_INTEGRADO,'N') = 'S';

    IF V_VALPRODUTO > 0 THEN
        IF :NEW.CODEMP IN (1,31) AND :NEW.CODLOCAL = 101 THEN

            -- Verifica se já tem registro de aleração de estoque na tabela
            SELECT COUNT(*) INTO V_VALESTOQUE
            FROM AD_MKP_SYNCESTOQUE SYNCEST
            WHERE SYNCEST.CODPROD = :NEW.CODPROD;

            IF V_VALESTOQUE = 0 THEN
                SELECT PRO.AD_MKP_IDPROD INTO V_IDPROD
                FROM TGFPRO PRO
                WHERE PRO.CODPROD = :NEW.CODPROD;

                INSERT INTO AD_MKP_SYNCESTOQUE (CODPROD, IDPROD)
                                        VALUES (:NEW.CODPROD,V_IDPROD);
            END IF;
        END IF;
    END IF;
END;