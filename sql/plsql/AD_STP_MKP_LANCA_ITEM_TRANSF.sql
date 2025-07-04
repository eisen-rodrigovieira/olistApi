CREATE OR REPLACE PROCEDURE AD_STP_MKP_LANCA_ITEM_TRANSF(
                    P_PRODUTO IN  NUMBER,   -- Número único da nota
                    P_LOTE    IN  VARCHAR2, -- Lotes do produto
                    P_CODVOL  IN  VARCHAR2, -- Código do volume
                    P_QTD     IN  NUMBER    -- Quantidade a ser lançada
) AS
    V_NUNOTA INT;
    V_EXISTEITEM INT;    
BEGIN  

    SELECT NUNOTA
    INTO V_NUNOTA
    FROM TGFCAB
    WHERE TIPMOV       = 'T'
      AND CODEMP       = 1
      AND CODEMPNEGOC  = 31
      AND CODTIPOPER   = 1419
      AND STATUSNOTA   = 'P'    
      AND TRUNC(DTNEG) = TRUNC(CURRENT_DATE)
      AND ROWNUM = 1;

    FOR X IN (WITH DADOS AS ( 
                    SELECT P_PRODUTO AS CODPROD, 
                           31 AS CODEMP, 
                           P_CODVOL AS CODVOL, 
                           101 AS CODLOCALORIG, 
                           P_LOTE AS CONTROLE, 
                           P_QTD AS QTDNEG 
                    FROM DUAL
                ) 
                SELECT D.CODPROD,
                        D.CODVOL,
                        D.CODLOCALORIG,
                        D.CONTROLE,
                        D.QTDNEG - NVL((SELECT SUM(ESTOQUE)
                                        FROM TGFEST 
                                        WHERE CODPROD = D.CODPROD 
                                            AND CODEMP = D.CODEMP 
                                            AND CODLOCAL = D.CODLOCALORIG 
                                            AND CONTROLE = D.CONTROLE),0) AS QTDRESSUPRIR, 
                        NVL((SELECT SUM(ESTOQUE) 
                                FROM TGFEST 
                                WHERE CODPROD = D.CODPROD 
                                AND CODEMP = 1 
                                AND CODLOCAL = D.CODLOCALORIG 
                                AND CONTROLE = D.CONTROLE),0) AS QTDEMP1,
                        NVL((SELECT ROUND(EXC.VLRVENDA,2)
                            FROM TGFTAB TAB 
                            INNER JOIN TGFEXC EXC ON EXC.NUTAB = TAB.NUTAB 
                            WHERE TAB.CODTAB = 101 
                            AND EXC.CODPROD = D.CODPROD
                            AND TAB.DTVIGOR= (SELECT MAX(T.DTVIGOR) 
                                                FROM TGFTAB T 
                                                INNER JOIN TGFEXC E ON E.NUTAB = T.NUTAB 
                                                WHERE T.CODTAB = 101 
                                                AND E.CODPROD = D.CODPROD)),0) AS VLRCUSTO
                FROM DADOS D 
                WHERE D.QTDNEG - NVL((SELECT SUM(ESTOQUE) 
                                        FROM TGFEST 
                                        WHERE CODPROD = D.CODPROD 
                                        AND CODEMP = D.CODEMP 
                                        AND CODLOCAL = D.CODLOCALORIG 
                                        AND CONTROLE = D.CONTROLE),0) > 0
    )
    LOOP
            IF X.QTDEMP1 - X.QTDRESSUPRIR < 0 THEN
                RETURN; --    RAISE_APPLICATION_ERROR(-20101, 'Estoque da empresa 1 suficiente para atender ressuprimento');
            ELSE
                    IF X.VLRCUSTO > 0 THEN
                        SELECT COUNT(*)
                        INTO V_EXISTEITEM
                        FROM TGFITE
                        WHERE NUNOTA = V_NUNOTA AND CODPROD = X.CODPROD AND CONTROLE = X.CONTROLE;

                        IF V_EXISTEITEM > 0 THEN
                            UPDATE TGFITE
                            SET QTDNEG = QTDNEG + X.QTDRESSUPRIR,
                                VLRTOT = VLRTOT + (ROUND(X.VLRCUSTO,2) * X.QTDRESSUPRIR)
                            WHERE NUNOTA = V_NUNOTA AND CODPROD = X.CODPROD AND CONTROLE = X.CONTROLE;
                        ELSE
                            -- Inserindo novo item na nota fiscal
                            INSERT INTO TGFITE (NUNOTA,
                                                CODEMP,
                                                SEQUENCIA,
                                                CODPROD,
                                                QTDNEG,
                                                CODVOL,
                                                VLRUNIT,
                                                VLRTOT,
                                                CODLOCALORIG,
                                                --CODLOCALDEST,
                                                RESERVA,
                                                ATUALESTOQUE,
                                                CONTROLE)
                                        VALUES (V_NUNOTA,
                                                1,
                                                (SELECT NVL(MAX(SEQUENCIA),0) + 1 FROM TGFITE WHERE NUNOTA = V_NUNOTA),
                                                X.CODPROD,
                                                X.QTDRESSUPRIR,
                                                X.CODVOL,
                                                ROUND(X.VLRCUSTO,2),
                                                ROUND(X.VLRCUSTO,2) * X.QTDRESSUPRIR,
                                                X.CODLOCALORIG,
                                                --X.CODLOCALORIG,
                                                'N',
                                                -1,
                                                X.CONTROLE);
                            COMMIT;
                        END IF;
                    ELSE
                                RAISE_APPLICATION_ERROR(-20101,'Produto não possui custo cadastrado para empresa 1');
                    END IF;
            END IF;
    END LOOP;
END;