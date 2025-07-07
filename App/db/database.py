import psycopg2
import psycopg2.extras #Esse modulo permite a gente obter um dicionario quando fazemos um select,
#dai ao inves de precisarmos saber qual a posicao da coluna na lista, podemos so fazer
#"nome_variavel"["name"], embaixo, dentro do try, tem um exemplo.

def comandoSQL(comando):
    hostname = 'localhost'
    database = 'BDExtensao'
    username = 'postgres'
    pwd = 'adminext'
    port_id = 5432
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        #Tratamendo dos comandos SQL
        cur.execute(comando)
        if comando[:3].lower() == "sel":
            return cur.fetchall()
        elif comando[:3].lower() == "upd":
            conn.commit()
            #print("Valor(es) atualizados com sucesso")
        elif comando[:3].lower() == "ins":
            if "returning" in comando.lower():
                result = cur.fetchone()
                conn.commit()
                return result
            else:
                conn.commit()
                return None
        elif comando[:3].lower() == "del":
            conn.commit()
            print("Registro(s) deletado(s) com sucesso")
            

    except Exception as error:
        raise Exception(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def get_extensoes():
    return comandoSQL("SELECT * FROM tb_extensao ORDER BY CodExt")

def get_extensoes_aluno(matricula):
    return comandoSQL(f"""SELECT ext.CodExt, CodLocal, Titulo, TipoAcao, Descricao, AreaTematica, PublicoInternoEst, 
                      PublicoExternoEst, PublicoInterno, PublicoExterno, InicioRealizacao, FimRealizacao
                      FROM tb_extensao ext JOIN tb_funcaoaluno faluno ON faluno.codext = ext.codext 
                      WHERE CodAluno = '{matricula}' ORDER BY faluno.EstadoInscricao, ext.CodExt""")

def get_extensoes_docente(matricula):
    return comandoSQL(f"""SELECT ext.CodExt, CodLocal, Titulo, TipoAcao, Descricao, AreaTematica, PublicoInternoEst, 
                      PublicoExternoEst, PublicoInterno, PublicoExterno, InicioRealizacao, FimRealizacao
                      FROM tb_extensao ext JOIN tb_funcaodocente fdocente ON fdocente.codext = ext.codext 
                      WHERE CodDocente = '{matricula}' ORDER BY fdocente.EstadoInscricao, ext.CodExt""")

def get_extensoes_pessoa(cpf):
    return comandoSQL(f"""SELECT ext.CodExt, CodLocal, Titulo, TipoAcao, Descricao, AreaTematica, PublicoInternoEst, 
                      PublicoExternoEst, PublicoInterno, PublicoExterno, InicioRealizacao, FimRealizacao
                      FROM tb_extensao ext JOIN tb_funcaopessoa fpessoa ON fpessoa.codext = ext.codext 
                      WHERE CodPessoa = '{cpf}' ORDER BY fpessoa.EstadoInscricao, ext.CodExt""")

def get_infoextensao(codExt):
    return comandoSQL(f"SELECT * FROM tb_infoextensao WHERE CodExt = '{codExt}'")

# Procuram informações de uma função/inscrição a uma extensão
def get_funcao_aluno(codExt,matricula):
    return comandoSQL(f"SELECT * FROM tb_funcaoaluno WHERE CodExt = '{codExt}' AND CodAluno = '{matricula}'")
def get_funcao_docente(codExt,matricula):
    return comandoSQL(f"SELECT * FROM tb_funcaodocente WHERE CodExt = '{codExt}' AND CodDocente = '{matricula}'")
def get_funcao_pessoa(codExt,cpf):
    return comandoSQL(f"SELECT * FROM tb_funcaopessoa WHERE CodExt = '{codExt}' AND CodPessoa = '{cpf}'")

# Tenta encontrar aluno e, se encontrar, retorna o aluno
def get_aluno(id):
    return comandoSQL(f"SELECT * FROM tb_aluno WHERE matricula = '{id}' or cpf = '{id}'")

# Atualiza senha do aluno 
def update_senha_aluno(id,senha):
    comandoSQL(f"UPDATE tb_aluno SET senha = '{senha}' WHERE matricula = '{id}' or cpf = '{id}'")
    return

# Tenta encontrar docente e, se encontrar, retorna o docente
def get_docente(id):
    return comandoSQL(f"SELECT * FROM tb_docente WHERE matricula = '{id}' or cpf = '{id}'")

# Atualiza senha do docente 
def update_senha_docente(id,senha):
    comandoSQL(f"UPDATE tb_docente SET senha = '{senha}' WHERE matricula = '{id}' or cpf = '{id}'")
    return

# Tenta encontrar pessoa e, se encontrar, retorna a pessoa
def get_pessoa(id):
    return comandoSQL(f"SELECT * FROM tb_pessoa WHERE cpf = '{id}'")

# Cria uma pessoa
def create_pessoa(cpf,nome,senha):
    comandoSQL(f"INSERT INTO tb_pessoa (CPF,Nome,Senha) VALUES ('{cpf}','{nome}','{senha}')")
    return

# Atualiza senha de uma pessoa
def update_senha_pessoa(id,senha):
    comandoSQL(f"UPDATE tb_pessoa SET senha = '{senha}' WHERE cpf = '{id}'")
    return

# Deleta uma pessoa
def delete_pessoa(cpf):
    comandoSQL(f"DELETE FROM tb_pessoa WHERE cpf = '{cpf}'")
    return

# Retorna o curso a partir de um id
def get_curso(id):
    return comandoSQL(f"SELECT * FROM tb_curso WHERE codCurso = '{id}'")

# Retorna o departamento a partir de um id
def get_dep(id):
    return comandoSQL(f"SELECT * FROM tb_departamento WHERE codDep = '{id}'")

# Retorna a materia a partir de um id
def get_materia(id):
    return comandoSQL(f"SELECT * FROM tb_materia WHERE codMateria = '{id}'")

# Insere email na tabela de email de alunos
def criar_email_aluno(id,email):
    comandoSQL(f"INSERT INTO tb_emailaluno (Email, CodAluno) VALUES ('{email}', '{id}')")
    return

# Retorna todos os emails relacionados a um aluno
def get_emails_aluno(id):
    return comandoSQL(f"SELECT * FROM tb_emailaluno WHERE CodAluno = '{id}'")

# Deleta email da tabela de email de alunos
def deletar_email_aluno(id,email):
    comandoSQL(f"DELETE FROM tb_emailaluno WHERE email = '{email}' and CodAluno = '{id}'")
    return

# Insere email na tabela de email de docentes
def criar_email_docente(id,email):
    comandoSQL(f"INSERT INTO tb_emaildocente (Email, CodDocente) VALUES ('{email}', '{id}')")
    return

# Retorna todos os emails relacionados a um docente
def get_emails_docente(id):
    return comandoSQL(f"SELECT * FROM tb_emaildocente WHERE CodDocente = '{id}'")

# Deleta email da tabela de email de docentes
def deletar_email_docente(id,email):
    comandoSQL(f"DELETE FROM tb_emaildocente WHERE email = '{email}' and CodDocente = '{id}'")
    return

# Insere email na tabela de email de pessoas
def criar_email_pessoa(id,email):
    comandoSQL(f"INSERT INTO tb_emailpessoa (Email, CodPessoa) VALUES ('{email}', '{id}')")
    return

# Retorna todos os emails relacionados a uma pessoa
def get_emails_pessoa(id):
    return comandoSQL(f"SELECT * FROM tb_emailpessoa WHERE CodPessoa = '{id}'")

# Deleta email da tabela de email de pessoas
def deletar_email_pessoa(id,email):
    comandoSQL(f"DELETE FROM tb_emailpessoa WHERE email = '{email}' and CodPessoa = '{id}'")
    return

# Retorna todas as turmas associadas ao aluno, em ordem do semestre
def get_historico(matricula):
    return comandoSQL(f"SELECT * FROM tb_historicoaluno WHERE codaluno = '{matricula}' ORDER BY semestre")

# Retorna um local
def get_local(codLocal):
    return comandoSQL(f"SELECT * FROM tb_local WHERE codlocal = '{codLocal}'")

# Retorna versão detalhada dos feedbacks
def get_feedbacks(codExt):
    return comandoSQL(f"SELECT * FROM tb_feedback_detalhado WHERE codExt = '{codExt}'")

# Retorna o código de um feedback criado
def criar_feedback(codExt,nota,comentario):
    return comandoSQL(f"INSERT INTO TB_Feedback (CodExt, Comentario, Nota) VALUES ('{codExt}', '{comentario}', '{nota}') RETURNING CodFeedback")

# Efetiva a criação do feedback, conectando-o ao devido autor
def conectar_feedback_aluno(codFeedback,matricula):
    comandoSQL(f"INSERT INTO TB_FeedbackAluno (CodFeedback, CodAluno) VALUES ('{codFeedback}', '{matricula}')")

def conectar_feedback_docente(codFeedback,matricula):
    comandoSQL(f"INSERT INTO TB_FeedbackDocente (CodFeedback, CodDocente) VALUES ('{codFeedback}', '{matricula}')")

def conectar_feedback_pessoa(codFeedback,cpf):
    comandoSQL(f"INSERT INTO TB_FeedbackPessoa (CodFeedback, CodPessoa) VALUES ('{codFeedback}', '{cpf}')")