/*******************************************************************************

@Autor: Rodrigo Vieira <rodrigo.vieira@grupoeisen.com.br>
@Data: 10/06/2025
@Objetivo: Criar tabela para registrar alterações no estoque dos produtos 
    integrados no Olist.

********************************************************************************/
CREATE TABLE AD_MKP_SYNCESTOQUE
(   CODPROD  NUMBER(10,0)   NOT NULL,
    IDPROD   NUMBER(10,0),
    DHEVENTO DATE           DEFAULT CURRENT_DATE NOT NULL
);