CREATE OR REPLACE TRIGGER AD_TRG_MKP_SYNCPRODUTO
BEFORE INSERT OR UPDATE OR DELETE ON TGFPRO
FOR EACH ROW


    /*******************************************************************************

    @Autor: Rodrigo Vieira <rodrigo.vieira@grupoeisen.com.br>
    @Data: 10/06/2025
    @Objetivo: Monitorar alterações no cadastro dos produtos que estão marcados para
        sincronizar com o Olist.

    ********************************************************************************/

BEGIN  

    IF :NEW.AD_MKP_DHATUALIZADO < CURRENT_DATE OR :NEW.AD_MKP_DHATUALIZADO IS NULL THEN
        /*
            Quando um produto é marcado para integrar no momento do cadastro:
            Evento > (I)nclusão
        */
        IF INSERTING AND :NEW.AD_MKP_INTEGRADO = 'S' THEN
            BEGIN
                INSERT INTO AD_MKP_SYNCPRODUTO (CODPROD, EVENTO) VALUES (:NEW.CODPROD, 'I');
            END;
        END IF;

        IF UPDATING THEN 
            /* 
                Quando um produto é marcado para integrar depois de estar cadastrado
                Evento > (I)nclusão    
            */
            IF :OLD.AD_MKP_INTEGRADO = 'N' AND :NEW.AD_MKP_INTEGRADO = 'S' THEN
                BEGIN
                    INSERT INTO AD_MKP_SYNCPRODUTO (CODPROD, IDPROD, EVENTO) VALUES (:NEW.CODPROD, NVL(:NEW.AD_MKP_IDPROD,NULL), 'I');
                END; 
            END IF;

            /* 
                Quando um produto é DESmarcado para integrar
                Evento > (E)xclusão (inativar)
            */

            IF :OLD.AD_MKP_INTEGRADO = 'S' AND :NEW.AD_MKP_INTEGRADO = 'N' THEN
                BEGIN
                    INSERT INTO AD_MKP_SYNCPRODUTO (CODPROD, IDPROD, EVENTO) VALUES (:NEW.CODPROD, :NEW.AD_MKP_IDPROD, 'E');
                END; 
            END IF;        

            /* 
                Quando um produto já integrado tem alteração em algum campo que precisa estar espelhado no Olist
                Evento > (A)lteração
            */    

            IF :OLD.AD_MKP_INTEGRADO = 'S' AND :NEW.AD_MKP_INTEGRADO = 'S' AND
                ( :NEW.AD_MKP_INTEGRADO != :OLD.AD_MKP_INTEGRADO OR
                  :NEW.AD_MKP_IDPROD    != :OLD.AD_MKP_IDPROD    OR
                  :NEW.AD_MKP_NOME      != :OLD.AD_MKP_NOME      OR
                  :NEW.AD_MKP_DESCRICAO != :OLD.AD_MKP_DESCRICAO OR
                  :NEW.AD_MKP_IDPRODPAI != :OLD.AD_MKP_IDPRODPAI OR
                  :NEW.CODVOL           != :OLD.CODVOL           OR
                  :NEW.NCM              != :OLD.NCM              OR
                  :NEW.REFERENCIA       != :OLD.REFERENCIA       OR
                  :NEW.ORIGPROD         != :OLD.ORIGPROD         OR
                  :NEW.CODESPECST       != :OLD.CODESPECST       OR
                  :NEW.AD_MKP_CATEGORIA != :OLD.AD_MKP_CATEGORIA OR
                  :NEW.LARGURA          != :OLD.LARGURA          OR
                  :NEW.ALTURA           != :OLD.ALTURA           OR
                  :NEW.ESPESSURA        != :OLD.ESPESSURA        OR
                  :NEW.PESOLIQ          != :OLD.PESOLIQ          OR
                  :NEW.PESOBRUTO        != :OLD.PESOBRUTO        OR
                  :NEW.QTDEMB           != :OLD.QTDEMB           OR
                  :NEW.ESTMIN           != :OLD.ESTMIN           OR
                  :NEW.ESTMAX           != :OLD.ESTMAX           OR
                  :NEW.CODPARCFORN      != :OLD.CODPARCFORN      OR
                  :NEW.REFFORN          != :OLD.REFFORN
                ) THEN

                BEGIN
                    INSERT INTO AD_MKP_SYNCPRODUTO (CODPROD, IDPROD, EVENTO) VALUES (:NEW.CODPROD, :NEW.AD_MKP_IDPROD, 'A');
                END; 
            END IF;
        END IF;    

        /* 
            Quando um produto já integrado é excluído
            Evento > (E)xclusão (inativar)
        */   

        IF DELETING AND :OLD.AD_MKP_INTEGRADO = 'S' THEN
            BEGIN
                INSERT INTO AD_MKP_SYNCPRODUTO (CODPROD, IDPROD, EVENTO) VALUES (:OLD.CODPROD, :OLD.AD_MKP_IDPROD, 'E');
            END;  
        END IF; 
    END IF;
END;