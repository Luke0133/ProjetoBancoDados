CREATE TYPE Tipo_Acao AS ENUM('Curso','Evento','Projeto');
CREATE TYPE Tipo_Local AS ENUM('Campus','Escola','Outro');
CREATE TYPE Tipo_Estado AS ENUM('Deferido','Indeferido','Em Espera');

CREATE TABLE TB_Materia(
	CodMateria SERIAL PRIMARY KEY,
	CodDep SERIAL NOT NULL,
	Nome varchar(100) NOT NULL,
	Sigla varchar(10) NOT NULL
);

CREATE TABLE TB_Departamento(
	CodDep SERIAL PRIMARY KEY,
	Nome varchar(100) NOT NULL,
	Sigla varchar(10) NOT NULL
);

CREATE TABLE TB_CursoDep(
	CodCurso SERIAL NOT NULL,
	CodDep SERIAL NOT NULL,
	PRIMARY KEY(CodCurso,CodDep)
);

CREATE TABLE TB_EmailPessoa(
	Email varchar(100) NOT NULL,
	CodPessoa char(11) NOT NULL,
	PRIMARY KEY (Email,CodPessoa)
);

CREATE TABLE TB_EmailDocente(
	Email varchar(100) NOT NULL,
	CodDocente char(11) NOT NULL,
	PRIMARY KEY (Email,CodDocente)
);

CREATE TABLE TB_EmailAluno(
	Email varchar(100) NOT NULL,
	CodAluno char(9) NOT NULL,
	PRIMARY KEY (Email,CodAluno)
);

CREATE TABLE TB_Pessoa(
	CPF char(11) PRIMARY KEY,
	Nome varchar(100) NOT NULL,
	Senha varchar(30) NOT NULL,
	Curriculo bytea
);

CREATE TABLE TB_Docente(
	Matricula char(11) PRIMARY KEY,
	CodDep serial NOT NULL,
	Nome varchar(100) NOT NULL,
	Senha varchar(30) NOT NULL,
	CPF char(11) NOT NULL UNIQUE
);

CREATE TABLE TB_HistoricoAluno(
	CodAluno char(11) NOT NULL,
	CodMateria serial NOT NULL,
	Semestre integer NOT NULL,
	Mencao char(2) NOT NULL,
	PRIMARY KEY(CodAluno, CodMateria, Semestre)
);

CREATE TABLE TB_Aluno(
	Matricula char(9) PRIMARY KEY,
	CodCurso serial NOT NULL,
	Nome varchar(100) NOT NULL,
	CPF char(11) NOT NULL UNIQUE,
	Senha varchar(30) NOT NULL,
	IRA real NOT NULL,
	DataIngresso date NOT NULL,
	SemestreAtual integer NOT NULL
);

CREATE TABLE TB_Curso(
	CodCurso SERIAL PRIMARY KEY,
	Nome varchar(100)
);

CREATE TABLE TB_FuncaoPessoa(
	CodPessoa char(11) NOT NULL,
	CodExt char(10) NOT NULL,
	Funcao varchar(50),
	EstadoInscricao Tipo_Estado,
	PRIMARY KEY(CodPessoa,CodExt)
);

CREATE TABLE TB_FuncaoDocente(
	CodDocente char(11) NOT NULL,
	CodExt char(10) NOT NULL,
	Funcao varchar(50),
	EstadoInscricao Tipo_Estado,
	PRIMARY KEY(CodDocente,CodExt)
);

CREATE TABLE TB_FuncaoAluno(
	CodAluno char(9) NOT NULL,
	CodExt char(10) NOT NULL,
	Funcao varchar(50),
	EstadoInscricao Tipo_Estado,
	PRIMARY KEY(CodAluno,CodExt)
);

CREATE TABLE TB_SituacaoExt(
	DataSit DATE NOT NULL,
	HorarioSit TIME NOT NULL,
	CodExt char(10) NOT NULL,
	Situacao varchar(100),
	PRIMARY KEY(DataSit,HorarioSit,CodExt)
);

CREATE TABLE TB_Extensao(
	CodExt char(10) PRIMARY KEY,
	CodLocal serial NOT NULL,
	Titulo varchar(200) NOT NULL,
	TipoAcao Tipo_Acao NOT NULL,
	Descricao varchar(2000) NOT NULL,
	AreaTematica varchar(200) NOT NULL,
	PublicoInternoEst integer NOT NULL,
	PublicoExternoEst integer NOT NULL,
	PublicoInterno varchar(500),
	PublicoExterno varchar(500),
	InicioRealizacao date NOT NULL,
	FimRealizacao date NOT NULL
);

CREATE TABLE TB_FeedbackPessoa(
	CodFeedback serial PRIMARY KEY,
	CodPessoa char(11) NOT NULL
);

CREATE TABLE TB_FeedbackDocente(
	CodFeedback serial PRIMARY KEY,
	CodDocente char(11) NOT NULL
);

CREATE TABLE TB_FeedbackAluno(
	CodFeedback serial PRIMARY KEY,
	CodAluno char(9) NOT NULL
);

CREATE TABLE TB_Feedback(
	CodFeedback serial PRIMARY KEY,
	CodExt char(10) NOT NULL,
	DataFeedback DATE NOT NULL DEFAULT CURRENT_DATE,
	Comentario varchar(1000) NOT NULL,
	Nota integer NOT NULL
);

CREATE TABLE TB_Local(
	CodLocal serial PRIMARY KEY,
	Nome varchar(100) NOT NULL UNIQUE,
	Tipo Tipo_Local NOT NULL,
	Estado char(2) NOT NULL,
	Municipio varchar(50) NOT NULL,
	Bairro varchar(50) NOT NULL,
	Complemento varchar(100)
);

CREATE TABLE TB_Foto(
	CodFoto serial PRIMARY KEY,
	CodExt char(10) NOT NULL,
	Descricao varchar(1000),
	Foto bytea NOT NULL
);

ALTER TABLE TB_EmailPessoa
ADD FOREIGN KEY(CodPessoa)
REFERENCES TB_Pessoa(CPF)
ON DELETE CASCADE;

ALTER TABLE TB_EmailDocente
ADD FOREIGN KEY(CodDocente)
REFERENCES TB_Docente(Matricula)
ON DELETE CASCADE;

ALTER TABLE TB_EmailAluno
ADD FOREIGN KEY(CodAluno)
REFERENCES TB_Aluno(Matricula)
ON DELETE CASCADE;

ALTER TABLE TB_Materia
ADD FOREIGN KEY(CodDep)
REFERENCES TB_Departamento(CodDep)
ON DELETE CASCADE;

ALTER TABLE TB_CursoDep
ADD FOREIGN KEY(CodCurso)
REFERENCES TB_Curso(CodCurso),
ADD FOREIGN KEY(CodDep)
REFERENCES TB_Departamento(CodDep)
ON DELETE CASCADE;

ALTER TABLE TB_Docente
ADD FOREIGN KEY(CodDep)
REFERENCES TB_Departamento(CodDep)
ON DELETE CASCADE;

ALTER TABLE TB_HistoricoAluno
ADD FOREIGN KEY(CodAluno)
REFERENCES TB_Aluno(Matricula),
ADD FOREIGN KEY(CodMateria)
REFERENCES TB_Materia(CodMateria)
ON DELETE CASCADE;

ALTER TABLE TB_Aluno
ADD FOREIGN KEY(CodCurso)
REFERENCES TB_Curso(CodCurso)
ON DELETE CASCADE;

ALTER TABLE TB_FuncaoPessoa
ADD FOREIGN KEY(CodPessoa)
REFERENCES TB_Pessoa(CPF),
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt)
ON DELETE CASCADE;

ALTER TABLE TB_FuncaoDocente
ADD FOREIGN KEY(CodDocente)
REFERENCES TB_Docente(Matricula),
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt)
ON DELETE CASCADE;

ALTER TABLE TB_FuncaoAluno
ADD FOREIGN KEY(CodAluno)
REFERENCES TB_Aluno(Matricula),
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt)
ON DELETE CASCADE;

ALTER TABLE TB_SituacaoExt
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt)
ON DELETE CASCADE;

ALTER TABLE TB_Extensao
ADD FOREIGN KEY(CodLocal)
REFERENCES TB_Local(CodLocal)
ON DELETE CASCADE;

ALTER TABLE TB_Foto
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt)
ON DELETE CASCADE;

ALTER TABLE TB_FeedbackPessoa
ADD FOREIGN KEY(CodPessoa)
REFERENCES TB_Pessoa(CPF),
ADD FOREIGN KEY(CodFeedback)
REFERENCES TB_Feedback(CodFeedback)
ON DELETE CASCADE;

ALTER TABLE TB_FeedbackDocente
ADD FOREIGN KEY(CodDocente)
REFERENCES TB_Docente(Matricula),
ADD FOREIGN KEY(CodFeedback)
REFERENCES TB_Feedback(CodFeedback)
ON DELETE CASCADE;

ALTER TABLE TB_FeedbackAluno
ADD FOREIGN KEY(CodAluno)
REFERENCES TB_Aluno(Matricula),
ADD FOREIGN KEY(CodFeedback)
REFERENCES TB_Feedback(CodFeedback)
ON DELETE CASCADE;

ALTER TABLE TB_Feedback
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt)
ON DELETE CASCADE;

/*Criação das Views*/
CREATE OR REPLACE VIEW tb_infoextensao AS
SELECT ext.codExt,tipoAcao,titulo,dep.sigla AS departamento,doc.nome AS Coordenador FROM tb_extensao ext
	JOIN tb_funcaodocente fdoc
	ON fdoc.codext = ext.codext
	JOIN tb_docente doc
	ON doc.matricula = fdoc.coddocente AND fdoc.funcao = 'Coordenador(a)'
	JOIN tb_departamento dep
	ON doc.CodDep = dep.CodDep;

	
CREATE OR REPLACE VIEW tb_feedback_detalhado AS
	/* Tabela com todos os feedbacks de pessoas e informações relevantes da pessoa */
	SELECT f.CodExt, f.CodFeedback, f.DataFeedback, f.Comentario, f.Nota, p.Nome, fp.Funcao
	FROM TB_Feedback f JOIN TB_FeedbackPessoa fpessoa 
	ON f.CodFeedback = fpessoa.CodFeedback
	JOIN TB_Pessoa p 
	ON fpessoa.CodPessoa = p.CPF
	LEFT JOIN TB_FuncaoPessoa fp 
	ON fp.CodPessoa = p.CPF AND fp.CodExt = f.CodExt

	UNION ALL  /* União entre as tabelas (compatíveis pois nome e funcao são equivalentes em todas as tabelas) */

	/* Tabela com todos os feedbacks de docentes e informações relevantes do docente */
	SELECT f.CodExt, f.CodFeedback, f.DataFeedback, f.Comentario, f.Nota, d.Nome, fd.Funcao
	FROM TB_Feedback f JOIN TB_FeedbackDocente fdoc 
	ON f.CodFeedback = fdoc.CodFeedback
	JOIN TB_Docente d 
	ON fdoc.CodDocente = d.Matricula
	LEFT JOIN TB_FuncaoDocente fd 
	ON fd.CodDocente = d.Matricula AND fd.CodExt = f.CodExt

	UNION ALL  /* União entre as tabelas (compatíveis pois nome e funcao são equivalentes em todas as tabelas) */

	/* Tabela com todos os feedbacks de alunos e informações relevantes do aluno */
	SELECT f.CodExt, f.CodFeedback, f.DataFeedback, f.Comentario, f.Nota, a.Nome, fa.Funcao
	FROM TB_Feedback f
	JOIN TB_FeedbackAluno faluno 
	ON f.CodFeedback = faluno.CodFeedback
	JOIN TB_Aluno a 
	ON faluno.CodAluno = a.Matricula
	LEFT JOIN TB_FuncaoAluno fa 
	ON fa.CodAluno = a.Matricula AND fa.CodExt = f.CodExt;
	
/*Criação da Procedure*/
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