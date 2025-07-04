/*******************************************************************************

@Autor: Rodrigo Vieira <rodrigo.vieira@grupoeisen.com.br>
@Data: 10/06/2025
@Objetivo: Criar tabela para registrar alterações no cadastro dos produtos 
    integrados no Olist.

********************************************************************************/
CREATE TABLE AD_MKP_SYNCPRODUTO
(   CODPROD  NUMBER(10,0)                      NOT NULL,
    IDPROD   NUMBER(10,0),                     
    EVENTO   VARCHAR2(1)                       NOT NULL,
    DHEVENTO DATE         DEFAULT CURRENT_DATE NOT NULL
);