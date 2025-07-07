CREATE OR REPLACE PROCEDURE insert_extensao(
	IN iCodLocal integer,
	IN iTitulo varchar(200),
	IN iTipoAcao Tipo_Acao,
	IN iDescricao varchar(2000),
	IN iAreaTematica varchar(200),
	IN iPublicoInternoEst integer,
	IN iPublicoExternoEst integer,
	IN iPublicoInterno varchar(500),
	IN iPublicoExterno varchar(500),
	IN iInicioRealizacao date,
	IN iFimRealizacao date,
    IN iData date,
    IN iHora time
)
LANGUAGE plpgsql
AS $$
DECLARE 
    vCodExt char(10);
    vAno char(4);
    vAcaoPre char(2);
    vIndex int;
    vData date;
    vHora time;
BEGIN
    -- Checa se data de criação foi fornecida 
    IF iData IS NULL THEN
        vData := CURRENT_DATE;
    ELSE
        vData := iData;
    END IF;

    -- Checa se hora foi fornecida
    IF iHora IS NULL THEN
        vHora := CURRENT_TIME;
    ELSE
        vHora := iHora;
    END IF;
    
    vAno := to_char(vData,'YYYY');
    
    -- checa tipo de ação e atribui sigla correta
    CASE iTipoAcao
        WHEN 'Curso' THEN
            vAcaoPre := 'CR';
        WHEN 'Evento' THEN
            vAcaoPre := 'EV';
        ELSE
            vAcaoPre := 'PJ';
    END CASE;

    -- Escolhe o índice para a extensão baseado nas extensões do mesmo tipo e ano já existentes
    SELECT COALESCE(MAX(CAST(SUBSTRING(CodExt FROM 3 FOR 3) AS INT)), 0) + 1
    INTO vIndex
    FROM TB_Extensao
    WHERE SUBSTRING(CodExt FROM 1 FOR 2) = vAcaoPre
      AND SUBSTRING(CodExt FROM 7 FOR 4) = vAno;

    vCodExt := vAcaoPre || lpad(vIndex::text, 3, '0') || '-' || vAno;

    INSERT INTO TB_Extensao (
        CodExt, CodLocal, Titulo, TipoAcao, Descricao, AreaTematica,
        PublicoInternoEst, PublicoExternoEst, PublicoInterno,
        PublicoExterno, InicioRealizacao, FimRealizacao
    )
    VALUES (
        vCodExt, iCodLocal, iTitulo, iTipoAcao, iDescricao, iAreaTematica, iPublicoInternoEst,
        iPublicoExternoEst, iPublicoInterno, iPublicoExterno, iInicioRealizacao, iFimRealizacao
    );

    INSERT INTO TB_SituacaoExt (DataSit, HorarioSit, CodExt, Situacao)
    VALUES (vData, vHora, vCodExt, 'CADASTRO EM ANDAMENTO');

END;
$$;