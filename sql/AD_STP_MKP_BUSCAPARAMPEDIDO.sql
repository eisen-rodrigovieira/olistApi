CREATE OR REPLACE PROCEDURE AD_STP_MKP_BUSCAPARAMPEDIDO(
    P_CODTIPOPER  IN  NUMBER,
    P_CODTIPVENDA IN  NUMBER,
    P_CODEMP      IN  NUMBER,
    P_CIDADE      IN  VARCHAR2,
    P_UF          IN  VARCHAR2,
    P_DHTIPOPER   OUT DATE,
    P_DHTIPVENDA  OUT DATE,
    P_NUNOTA      OUT NUMBER,
    P_NUMNOTA     OUT NUMBER,
    P_CODCID      OUT NUMBER    
) AS

BEGIN

    /*******************************************************************************

    @Autor: Rodrigo Vieira <rodrigo.vieira@grupoeisen.com.br>
    @Data: 17/06/2025
    @Objetivo: Busca os parâmetros para inserir um novo pedido de venda da empresa 31.

    ********************************************************************************/

    -- DATA DA TOP
    SELECT MAX(DHALTER) DHALTER
    INTO P_DHTIPOPER
    FROM TGFTOP 
    WHERE CODTIPOPER = P_CODTIPOPER;

    -- DATA DO TIPO DE NEGOCIAÇÃO
    SELECT MAX(DHALTER) DHALTER 
    INTO P_DHTIPVENDA
    FROM TGFTPV
    WHERE CODTIPVENDA = P_CODTIPVENDA;

    -- PRÓXIMO NUNOTA
    SELECT ULTCOD + 1
    INTO P_NUNOTA
    FROM TGFNUM
    WHERE ARQUIVO = 'TGFCAB';

    -- PRÓXIMO NÚMERO DO PEDIDO
    SELECT ULTCOD + 1
    INTO P_NUMNOTA
    FROM TGFNUM
    WHERE ARQUIVO = 'PEDVEN'
        AND CODEMP = P_CODEMP;

    -- CÓDIGO DA CIDADE DO CLIENTE
    SELECT MIN(CODCID)
    INTO P_CODCID
    FROM TSICID CID
        INNER JOIN TSIUFS UFS ON CID.UF = UFS.CODUF
    WHERE UFS.UF = UPPER(P_UF) AND
        (( DESCRICAOCORREIO =    TRANSLATE(UPPER(P_CIDADE), 'ÁÀÃÂÉÈÊÍÌÓÒÕÔÚÙÛÇ','AAAAEEEIIOOOOUUUC') 
        OR DESCRICAOCORREIO LIKE TRANSLATE(UPPER(P_CIDADE), 'ÁÀÃÂÉÈÊÍÌÓÒÕÔÚÙÛÇ','AAAAEEEIIOOOOUUUC')||'%')
        OR (NOMECID =            TRANSLATE(UPPER(P_CIDADE), 'ÁÀÃÂÉÈÊÍÌÓÒÕÔÚÙÛÇ','AAAAEEEIIOOOOUUUC')
        OR NOMECID          LIKE TRANSLATE(UPPER(P_CIDADE), 'ÁÀÃÂÉÈÊÍÌÓÒÕÔÚÙÛÇ','AAAAEEEIIOOOOUUUC')||'%'));
END;