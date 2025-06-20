import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../data/base.db')

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Matricula FROM TB_Aluno;")
    result = cursor.fetchall()
    conn.close()
    return result

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    table_statements = [

        """CREATE TABLE IF NOT EXISTS TB_Departamento (
            CodDep INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT
        );""",

        """CREATE TABLE IF NOT EXISTS TB_Materia (
            CodMateria INTEGER PRIMARY KEY AUTOINCREMENT,
            CodDep INTEGER,
            Nome TEXT,
            FOREIGN KEY (CodDep) REFERENCES TB_Departamento(CodDep)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_Curso (
            CodCurso INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT
        );""",

        """CREATE TABLE IF NOT EXISTS TB_CursoDep (
            CodCurso INTEGER NOT NULL,
            CodDep INTEGER NOT NULL,
            PRIMARY KEY (CodCurso, CodDep),
            FOREIGN KEY (CodCurso) REFERENCES TB_Curso(CodCurso),
            FOREIGN KEY (CodDep) REFERENCES TB_Departamento(CodDep)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_Pessoa (
            CPF TEXT PRIMARY KEY,
            Nome TEXT NOT NULL,
            Senha TEXT NOT NULL,
            Curriculo BLOB
        );""",

        """CREATE TABLE IF NOT EXISTS TB_Docente (
            Matricula TEXT PRIMARY KEY,
            CodDep INTEGER NOT NULL,
            Nome TEXT NOT NULL,
            Senha TEXT NOT NULL,
            CPF TEXT NOT NULL,
            FOREIGN KEY (CodDep) REFERENCES TB_Departamento(CodDep),
            FOREIGN KEY (CPF) REFERENCES TB_Pessoa(CPF)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_Aluno (
            Matricula TEXT PRIMARY KEY,
            CodCurso INTEGER NOT NULL,
            Nome TEXT NOT NULL,
            CPF TEXT NOT NULL,
            Senha TEXT NOT NULL,
            IRA REAL NOT NULL,
            DataIngresso DATE NOT NULL,
            SemestreAtual INTEGER NOT NULL,
            FOREIGN KEY (CodCurso) REFERENCES TB_Curso(CodCurso),
            FOREIGN KEY (CPF) REFERENCES TB_Pessoa(CPF)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_HistoricoAluno (
            CodAluno TEXT NOT NULL,
            CodCurso INTEGER NOT NULL,
            Semestre INTEGER NOT NULL,
            Mencao TEXT NOT NULL,
            PRIMARY KEY (CodAluno, CodCurso, Semestre),
            FOREIGN KEY (CodAluno) REFERENCES TB_Aluno(Matricula),
            FOREIGN KEY (CodCurso) REFERENCES TB_Curso(CodCurso)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_EmailPessoa (
            Email TEXT NOT NULL,
            CodPessoa TEXT NOT NULL,
            PRIMARY KEY (Email, CodPessoa),
            FOREIGN KEY (CodPessoa) REFERENCES TB_Pessoa(CPF)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_EmailDocente (
            Email TEXT NOT NULL,
            CodDocente TEXT NOT NULL,
            PRIMARY KEY (Email, CodDocente),
            FOREIGN KEY (CodDocente) REFERENCES TB_Docente(Matricula)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_EmailAluno (
            Email TEXT NOT NULL,
            CodAluno TEXT NOT NULL,
            PRIMARY KEY (Email, CodAluno),
            FOREIGN KEY (CodAluno) REFERENCES TB_Aluno(Matricula)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_Local (
            CodLocal INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Tipo TEXT NOT NULL CHECK(Tipo IN ('Campus', 'Escola', 'Outro')),
            Estado TEXT NOT NULL,
            Municipio TEXT NOT NULL,
            Bairro TEXT NOT NULL,
            Complemento TEXT NOT NULL
        );""",

        """CREATE TABLE IF NOT EXISTS TB_Extensao (
            CodExt TEXT PRIMARY KEY,
            CodLocal INTEGER NOT NULL,
            Titulo TEXT NOT NULL,
            TipoAcao TEXT NOT NULL CHECK(TipoAcao IN ('Curso', 'Evento', 'Projeto')),
            Descricao TEXT NOT NULL,
            AreaTematica TEXT NOT NULL,
            PublicoInternoEst INTEGER NOT NULL,
            PublicoExternoEst INTEGER NOT NULL,
            PublicoInterno TEXT,
            PublicoExterno TEXT,
            InicioRealizacao DATE NOT NULL,
            FimRealizacao DATE NOT NULL,
            FOREIGN KEY (CodLocal) REFERENCES TB_Local(CodLocal)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_SituacaoExt (
            DataSit DATE NOT NULL,
            CodExt TEXT NOT NULL,
            Situacao TEXT,
            PRIMARY KEY (DataSit, CodExt),
            FOREIGN KEY (CodExt) REFERENCES TB_Extensao(CodExt)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_FuncaoPessoa (
            CodPessoa TEXT NOT NULL,
            CodExt TEXT NOT NULL,
            Funcao TEXT,
            EstadoInscricao TEXT CHECK(EstadoInscricao IN ('Deferido', 'Indeferido', 'Em Espera')),
            PRIMARY KEY (CodPessoa, CodExt),
            FOREIGN KEY (CodPessoa) REFERENCES TB_Pessoa(CPF),
            FOREIGN KEY (CodExt) REFERENCES TB_Extensao(CodExt)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_FuncaoDocente (
            CodDocente TEXT NOT NULL,
            CodExt TEXT NOT NULL,
            Funcao TEXT,
            EstadoInscricao TEXT CHECK(EstadoInscricao IN ('Deferido', 'Indeferido', 'Em Espera')),
            PRIMARY KEY (CodDocente, CodExt),
            FOREIGN KEY (CodDocente) REFERENCES TB_Docente(Matricula),
            FOREIGN KEY (CodExt) REFERENCES TB_Extensao(CodExt)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_FuncaoAluno (
            CodAluno TEXT NOT NULL,
            CodExt TEXT NOT NULL,
            Funcao TEXT,
            EstadoInscricao TEXT CHECK(EstadoInscricao IN ('Deferido', 'Indeferido', 'Em Espera')),
            PRIMARY KEY (CodAluno, CodExt),
            FOREIGN KEY (CodAluno) REFERENCES TB_Aluno(Matricula),
            FOREIGN KEY (CodExt) REFERENCES TB_Extensao(CodExt)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_Feedback (
            CodFeedback INTEGER PRIMARY KEY AUTOINCREMENT,
            CodExt TEXT NOT NULL,
            DataFeedback DATE NOT NULL DEFAULT (date('now')),
            Comentario TEXT NOT NULL,
            Nota INTEGER NOT NULL,
            FOREIGN KEY (CodExt) REFERENCES TB_Extensao(CodExt)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_FeedbackPessoa (
            CodFeedback INTEGER PRIMARY KEY,
            CodPessoa TEXT NOT NULL,
            FOREIGN KEY (CodPessoa) REFERENCES TB_Pessoa(CPF),
            FOREIGN KEY (CodFeedback) REFERENCES TB_Feedback(CodFeedback)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_FeedbackDocente (
            CodFeedback INTEGER PRIMARY KEY,
            CodDocente TEXT NOT NULL,
            FOREIGN KEY (CodDocente) REFERENCES TB_Docente(Matricula),
            FOREIGN KEY (CodFeedback) REFERENCES TB_Feedback(CodFeedback)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_FeedbackAluno (
            CodFeedback INTEGER PRIMARY KEY,
            CodAluno TEXT NOT NULL,
            FOREIGN KEY (CodAluno) REFERENCES TB_Aluno(Matricula),
            FOREIGN KEY (CodFeedback) REFERENCES TB_Feedback(CodFeedback)
        );""",

        """CREATE TABLE IF NOT EXISTS TB_Foto (
            CodFoto INTEGER PRIMARY KEY AUTOINCREMENT,
            CodExt TEXT NOT NULL,
            Descricao TEXT,
            Foto BLOB NOT NULL,
            FOREIGN KEY (CodExt) REFERENCES TB_Extensao(CodExt)
        );"""
    ]

    for statement in table_statements:
        try:
            cursor.execute(statement)
        except sqlite3.Error as e:
            print("Error executing statement:")
            print(statement)
            print("SQLite error:", e)

    conn.commit()
    conn.close()
