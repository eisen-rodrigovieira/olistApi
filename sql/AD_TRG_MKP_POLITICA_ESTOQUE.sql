CREATE OR REPLACE TRIGGER AD_TRG_MKP_POLITICA_ESTOQUE
BEFORE INSERT OR UPDATE ON TGFPRO
FOR EACH ROW

    /*******************************************************************************

    @Autor: Rodrigo Vieira <rodrigo.vieira@grupoeisen.com.br>
    @Data: 10/06/2025
    @Objetivo: Tratar a política de estoque dos produtos integrados no Olist.

    ********************************************************************************/

BEGIN

    IF :NEW.AD_MKP_ESTPOL IN ('T','V') THEN
        :NEW.AD_MKP_ESTREGBAR := NULL;
        :NEW.AD_MKP_ESTREGBARVAL := NULL;
        :NEW.AD_MKP_ESTREGBARTIP := NULL;
    END IF;

    IF :NEW.AD_MKP_ESTPOL = 'B' THEN

        IF (:OLD.AD_MKP_ESTREGBAR IS NULL     AND :NEW.AD_MKP_ESTREGBAR IS NULL) OR
           (:OLD.AD_MKP_ESTREGBAR IS NOT NULL AND :NEW.AD_MKP_ESTREGBAR IS NULL) THEN
            RAISE_APPLICATION_ERROR(-20101, FC_FORMATAHTML(P_MENSAGEM => 'Operação não permitida!', 
                                                           P_MOTIVO   => '</br>Quando a <b>Política de estoque</b> for "Regra de barreira", o campo <b>Regra de barreira</b> não pode ficar em branco',
                                                           P_SOLUCAO  => 'Revise os campos.')  );
        END IF;

        IF :NEW.AD_MKP_ESTREGBAR = 'D' THEN
            :NEW.AD_MKP_ESTREGBARVAL := 10;
            :NEW.AD_MKP_ESTREGBARTIP := 'P';
        END IF;

        IF :NEW.AD_MKP_ESTREGBAR = 'C' THEN
            IF (:OLD.AD_MKP_ESTREGBARVAL IS NULL     AND :NEW.AD_MKP_ESTREGBARVAL IS NULL) OR
               (:OLD.AD_MKP_ESTREGBARVAL IS NOT NULL AND :NEW.AD_MKP_ESTREGBARVAL IS NULL) OR
               (:OLD.AD_MKP_ESTREGBARTIP IS NULL     AND :NEW.AD_MKP_ESTREGBARTIP IS NULL) OR
               (:OLD.AD_MKP_ESTREGBARTIP IS NOT NULL AND :NEW.AD_MKP_ESTREGBARTIP IS NULL) THEN
                RAISE_APPLICATION_ERROR(-20101, FC_FORMATAHTML(P_MENSAGEM => 'Operação não permitida!', 
                                                            P_MOTIVO   => '</br>Quando a <b>Regra de barreira</b> for "Usar valor personalizado", os campos <b>Valor barreira de estoque</b> e <b>Tipo barreira de estoque</b> não podem ficar em branco',
                                                            P_SOLUCAO  => 'Revise os campos.')  );            
            END IF;
        END IF;
    
    END IF;

END;