CREATE TYPE Tipo_Acao AS ENUM('Curso','Evento','Projeto');
CREATE TYPE Tipo_Local AS ENUM('Campus','Escola','Outro');
CREATE TYPE Tipo_Estado AS ENUM('Deferido','Indeferido','Em Espera');

CREATE TABLE TB_Materia(
	CodMateria SERIAL PRIMARY KEY,
	CodDep SERIAL,
	Nome varchar(100)
);

CREATE TABLE TB_Departamento(
	CodDep SERIAL PRIMARY KEY,
	Nome varchar(100)
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
	CPF char(11) NOT NULL
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
	CPF char(11) NOT NULL,
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
	CodExt char(10) NOT NULL,
	Situacao varchar(100),
	PRIMARY KEY(DataSit,CodExt)
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
	Nome varchar(100) NOT NULL,
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
REFERENCES TB_Pessoa(CPF);

ALTER TABLE TB_EmailDocente
ADD FOREIGN KEY(CodDocente)
REFERENCES TB_Docente(Matricula);

ALTER TABLE TB_EmailAluno
ADD FOREIGN KEY(CodAluno)
REFERENCES TB_Aluno(Matricula);

ALTER TABLE TB_Materia
ADD FOREIGN KEY(CodDep)
REFERENCES TB_Departamento(CodDep);

ALTER TABLE TB_CursoDep
ADD FOREIGN KEY(CodCurso)
REFERENCES TB_Curso(CodCurso),
ADD FOREIGN KEY(CodDep)
REFERENCES TB_Departamento(CodDep);

ALTER TABLE TB_Docente
ADD FOREIGN KEY(CodDep)
REFERENCES TB_Departamento(CodDep);

ALTER TABLE TB_HistoricoAluno
ADD FOREIGN KEY(CodAluno)
REFERENCES TB_Aluno(Matricula),
ADD FOREIGN KEY(CodMateria)
REFERENCES TB_Materia(CodMateria);

ALTER TABLE TB_Aluno
ADD FOREIGN KEY(CodCurso)
REFERENCES TB_Curso(CodCurso);

ALTER TABLE TB_FuncaoPessoa
ADD FOREIGN KEY(CodPessoa)
REFERENCES TB_Pessoa(CPF),
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt);

ALTER TABLE TB_FuncaoDocente
ADD FOREIGN KEY(CodDocente)
REFERENCES TB_Docente(Matricula),
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt);

ALTER TABLE TB_FuncaoAluno
ADD FOREIGN KEY(CodAluno)
REFERENCES TB_Aluno(Matricula),
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt);

ALTER TABLE TB_SituacaoExt
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt);

ALTER TABLE TB_Extensao
ADD FOREIGN KEY(CodLocal)
REFERENCES TB_Local(CodLocal);

ALTER TABLE TB_Foto
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt);

ALTER TABLE TB_FeedbackPessoa
ADD FOREIGN KEY(CodPessoa)
REFERENCES TB_Pessoa(CPF),
ADD FOREIGN KEY(CodFeedback)
REFERENCES TB_Feedback(CodFeedback);

ALTER TABLE TB_FeedbackDocente
ADD FOREIGN KEY(CodDocente)
REFERENCES TB_Docente(Matricula),
ADD FOREIGN KEY(CodFeedback)
REFERENCES TB_Feedback(CodFeedback);

ALTER TABLE TB_FeedbackAluno
ADD FOREIGN KEY(CodAluno)
REFERENCES TB_Aluno(Matricula),
ADD FOREIGN KEY(CodFeedback)
REFERENCES TB_Feedback(CodFeedback);

ALTER TABLE TB_Feedback
ADD FOREIGN KEY(CodExt)
REFERENCES TB_Extensao(CodExt);
