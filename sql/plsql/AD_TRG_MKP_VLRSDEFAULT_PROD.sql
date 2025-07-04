CREATE OR REPLACE TRIGGER AD_TRG_MKP_VLRSDEFAULT_PROD
BEFORE INSERT OR UPDATE ON TGFPRO
FOR EACH ROW

    /*******************************************************************************

    @Autor: Rodrigo Vieira <rodrigo.vieira@grupoeisen.com.br>
    @Data: 10/06/2025
    @Objetivo: Setar valores default para os campos Categoria, Marca, Descrição e
        Política de estoque da aba Marketplace do cadastro de produtos.

    ********************************************************************************/

BEGIN
    IF NVL(:OLD.AD_MKP_INTEGRADO,'N') = 'N' AND :NEW.AD_MKP_INTEGRADO = 'S' THEN
        IF :OLD.AD_MKP_CATEGORIA IS NULL AND :NEW.AD_MKP_CATEGORIA IS NULL THEN
            :NEW.AD_MKP_CATEGORIA := 341974963;
        END IF;
        IF :OLD.AD_MKP_MARCA IS NULL AND :NEW.AD_MKP_MARCA IS NULL THEN
            :NEW.AD_MKP_MARCA := 25197;
        END IF;
        IF :OLD.AD_MKP_DESCRICAO IS NULL AND :NEW.AD_MKP_DESCRICAO IS NULL THEN
            :NEW.AD_MKP_DESCRICAO := :NEW.DESCRPROD;
        END IF;
        IF :OLD.AD_MKP_ESTPOL IS NULL AND :NEW.AD_MKP_ESTPOL IS NULL THEN
            :NEW.AD_MKP_ESTPOL := 'T';
        END IF;
    END IF;
END;