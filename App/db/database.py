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
        elif comando.strip().lower().startswith(("update", "insert", "delete", "call")):
            if "returning" in comando.lower():
                result = cur.fetchone()
                conn.commit()
                return result
            else:
                conn.commit()
                return None

    except Exception as error:
        raise Exception(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# Cria extensão e retorna o seu código
def criar_extensao(codLocal, titulo, tipo, descricao, areaTematica, publicoInternoEstimado,
                   publicoExternoEstimado,publicoInterno,publicoExterno, inicioRealizacao, fimRealizacao):
    comandoSQL(f"""CALL insert_extensao('{codLocal}', '{titulo}', '{tipo}', '{descricao}','{areaTematica}', {publicoInternoEstimado}, 
               {publicoExternoEstimado}, '{publicoInterno}', '{publicoExterno}', '{inicioRealizacao}' , '{fimRealizacao}', null, null)""")
    
    return comandoSQL(f"""SELECT codext from tb_extensao ORDER BY CriadoEm DESC LIMIT 1;""")

# Deleta extensão
def deletar_extensao(codExt):
    comandoSQL(f"DELETE FROM TB_Extensao WHERE CodExt = '{codExt}'")

# Atualiza os dados de uma extensão
def atualizar_extensao(codExt, codLocal, titulo, tipo, descricao, areaTematica, publicoInternoEstimado,
                   publicoExternoEstimado,publicoInterno,publicoExterno, inicioRealizacao, fimRealizacao):
    comandoSQL(f"""UPDATE TB_Extensao SET CodLocal = '{codLocal}', Titulo = '{titulo}', TipoAcao = '{tipo}', Descricao = '{descricao}', 
                AreaTematica = '{areaTematica}', PublicoInternoEst = {publicoInternoEstimado}, PublicoExternoEst = {publicoExternoEstimado},
                PublicoInterno = '{publicoInterno}', PublicoExterno = '{publicoExterno}', InicioRealizacao = '{inicioRealizacao}',
                FimRealizacao = '{fimRealizacao}' WHERE CodExt = '{codExt}' """)
    return

# Retorna todas as extensões
def get_extensoes():
    return comandoSQL("SELECT * FROM tb_extensao ORDER BY CodExt")
# Retorna uma extensão
def get_extensao(codext):
    return comandoSQL(f"SELECT * FROM tb_extensao WHERE CodExt = '{codext}'")

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

# Procuram funções de participantes ativos de uma extensão
def get_funcoes_aluno_deferido(codExt):
    return comandoSQL(f"SELECT * FROM tb_funcaoaluno WHERE CodExt = '{codExt}' AND EstadoInscricao = 'Deferido' ")
def get_funcoes_docente_deferido(codExt):
    return comandoSQL(f"SELECT * FROM tb_funcaodocente WHERE CodExt = '{codExt}' AND EstadoInscricao = 'Deferido'")
def get_funcoes_pessoa_deferido(codExt):
    return comandoSQL(f"SELECT * FROM tb_funcaopessoa WHERE CodExt = '{codExt}' AND EstadoInscricao = 'Deferido'")

# Procuram funções de participantes ativos de uma extensão
def get_funcoes_aluno_espera(codExt):
    return comandoSQL(f"SELECT * FROM tb_funcaoaluno WHERE CodExt = '{codExt}' AND EstadoInscricao = 'Em Espera' ")
def get_funcoes_docente_espera(codExt):
    return comandoSQL(f"SELECT * FROM tb_funcaodocente WHERE CodExt = '{codExt}' AND EstadoInscricao = 'Em Espera'")
def get_funcoes_pessoa_espera(codExt):
    return comandoSQL(f"SELECT * FROM tb_funcaopessoa WHERE CodExt = '{codExt}' AND EstadoInscricao = 'Em Espera'")

# Apagam função do usuário
def deletar_funcao_aluno(codExt,matricula):
    return comandoSQL(f"DELETE FROM tb_funcaoaluno WHERE CodExt = '{codExt}' AND CodAluno = '{matricula}'")
def deletar_funcao_docente(codExt,matricula):
    return comandoSQL(f"DELETE FROM tb_funcaodocente WHERE CodExt = '{codExt}' AND CodDocente = '{matricula}'")
def deletar_funcao_pessoa(codExt,cpf):
    return comandoSQL(f"DELETE FROM tb_funcaopessoa WHERE CodExt = '{codExt}' AND CodPessoa = '{cpf}'")

# Cria função do usuário
def set_funcao_aluno(codExt,codAluno,funcao,estadoinscricao):
    comandoSQL(f"INSERT INTO tb_funcaoaluno (CodExt, CodAluno,Funcao,EstadoInscricao) VALUES ('{codExt}','{codAluno}',{'NULL' if funcao is None else f"'{funcao}'"},'{estadoinscricao}')")
def set_funcao_docente(codExt,codDocente,funcao,estadoinscricao):
    comandoSQL(f"INSERT INTO tb_funcaodocente (CodExt, CodDocente,Funcao,EstadoInscricao) VALUES ('{codExt}','{codDocente}',{'NULL' if funcao is None else f"'{funcao}'"},'{estadoinscricao}')")
def set_funcao_pessoa(codExt,codPessoa,funcao,estadoinscricao):
    comandoSQL(f"INSERT INTO tb_funcaopessoa (CodExt, CodPessoa,Funcao,EstadoInscricao) VALUES ('{codExt}','{codPessoa}',{'NULL' if funcao is None else f"'{funcao}'"},'{estadoinscricao}')")

# Atualiza função do usuário
def update_funcao_aluno(codExt,codAluno,funcao,estadoinscricao):
    comandoSQL(f"UPDATE tb_funcaoaluno SET Funcao = {'NULL' if funcao is None else f"'{funcao}'"}, EstadoInscricao = '{estadoinscricao}' WHERE CodExt = '{codExt}' AND CodAluno = '{codAluno}'")
def update_funcao_docente(codExt,codDocente,funcao,estadoinscricao):
    comandoSQL(f"UPDATE tb_funcaodocente SET Funcao = {'NULL' if funcao is None else f"'{funcao}'"}, EstadoInscricao = '{estadoinscricao}' WHERE CodExt = '{codExt}' AND CodDocente = '{codDocente}'")
def update_funcao_pessoa(codExt,codPessoa,funcao,estadoinscricao):
    comandoSQL(f"UPDATE tb_funcaopessoa SET Funcao = {'NULL' if funcao is None else f"'{funcao}'"}, EstadoInscricao = '{estadoinscricao}' WHERE CodExt = '{codExt}' AND CodPessoa = '{codPessoa}'")




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

# Retorna todos os locais
def get_locais():
    return comandoSQL(f"SELECT * FROM tb_local")

# Cria um local e retorna o seu código (com/sem complemento)
def create_local_complemento(nome,tipo,estado,municipio,bairro,complemento):
    return comandoSQL(f"""INSERT INTO tb_local (nome, tipo, estado, municipio, bairro, complemento) 
                          values ('{nome}','{tipo}','{estado}','{municipio}','{bairro}','{complemento}')
                          RETURNING CodLocal""")

def create_local(nome,tipo,estado,municipio,bairro):
    return comandoSQL(f"""INSERT INTO tb_local (nome, tipo, estado, municipio, bairro) 
                          values ('{nome}','{tipo}','{estado}','{municipio}','{bairro}')
                          RETURNING CodLocal""") 
                
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

# Retorna todas as situações de uma determinada extensao
def get_situacoes(codExt):
    return comandoSQL(f"SELECT * FROM TB_SituacaoExt WHERE codExt = '{codExt}' ORDER BY DataSit, HorarioSit")

# Retorna todas as situações de uma determinada extensao
def set_situacao(codExt,situacao):
    comandoSQL(f"""INSERT INTO TB_SituacaoExt (DataSit, HorarioSit, CodExt, Situacao) VALUES (CURRENT_DATE, CURRENT_TIME, '{codExt}', '{situacao}')""")

# Insere PDF no currículo da pessoa
def update_curriculo(pdf,cpf):
    comandoSQL(f"UPDATE tb_pessoa SET curriculo = {pdf} WHERE cpf = '{cpf}'")

def get_curriculo(cpf):
    return comandoSQL(f"SELECT * FROM tb_pessoa WHERE cpf = '{cpf}'")

def inserir_foto(codExt,desc,foto):
    comandoSQL(f"INSERT INTO tb_foto (codext, descricao, foto) VALUES ('{codExt}', '{desc}', {foto})")

def get_fotos(codExt):
    return comandoSQL(f"SELECT * FROM tb_foto WHERE codExt = '{codExt}'")

