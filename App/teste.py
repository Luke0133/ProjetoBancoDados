import usuario as user
import database as db
from domains import Email
from domains import Data
from extensao import Feedback
def add_email_usuario(usuario):
    
    #Função para adicionar um novo email para um usuário do tipo Aluno, Docente ou Pessoa
    
    s = input("Digite email: ").strip()
    novo_email = Email()
    novo_email.set(s)

    if novo_email.get() is None:
        print("Email invalido")
        return
    try:
        # Verifica qual é o tipo do usuário para inseri-lo na respectiva tabela
        if isinstance(usuario, user.Aluno):
            chave = usuario.getAll()[0]
            db.comandoSQL(f"INSERT INTO tb_emailaluno (Email, MatriculaAluno) VALUES ('{novo_email.get()}', '{chave}')")

        elif isinstance(usuario, user.Docente):
            chave = usuario.getAll()[0]
            db.comandoSQL(f" INSERT INTO tb_emaildocente (Email, MatriculaDocente) VALUES ('{novo_email.get()}', '{chave}')")

        elif isinstance(usuario, user.Pessoa):
            chave = usuario.getAll()[0]
            db.comandoSQL(f"INSERT INTO tb_emailpessoa (Email, CodPessoa) VALUES ('{novo_email.get()}', '{chave}')")

        else:
            print("Tipo de usuário não reconhecido.")
            return

        # Atualiza a instância do usuário com o novo email
        usuario.addEmail(novo_email)
        print("Email adicionado com sucesso!")
        print("Os email atuais cadastrados sao:", [str(e) for e in usuario.getAll()[3]])

    except Exception as e:
        print("Erro ao adicionar email:", e)

def fazer_feedback(usuario):

    feed = Feedback()
    cod_ext = input("Digite o código da extensão que deseja avaliar: ").strip()
    comentario = input("Digite seu comentário: ").strip()
    data = Data()
    d = input("Digite a data no formato DD-MM-YYYY: ")
    data.set(d)
    if data.get() is None:
        print("Data invalida")
        return
    feed.setData(data)

    nota = float(input("Digite uma nota entre 0 e 5: "))
    feed.setNota(nota)
    if feed.get()[3] is None:
        print("Erro na Nota")
        return
    feed.setComentario(comentario)

    try:
        # Insere na TB_Feedback
        dt = feed.get()[1]
        cm = feed.get()[2]
        nt = feed.get()[3]
        db.comandoSQL(f"INSERT INTO tb_feedback (codExt, dataFeedback, comentario, nota) VALUES ('{cod_ext}', '{dt}', '{cm}', {nt})")

        # Recupera o último codFeedback inserido
        resultado = db.comandoSQL("SELECT MAX(codfeedback) AS cod FROM tb_feedback")
        cod_feedback = resultado[0]["cod"]

        # Insere na tabela de relação específica
        if isinstance(usuario, user.Aluno):
            chave = usuario.getAll()[0]
            db.comandoSQL(f"INSERT INTO tb_feedbackaluno (codfeedback, codaluno) VALUES ('{cod_feedback}', '{chave}')")
        elif isinstance(usuario, user.Docente):
            chave = usuario.getAll()[0]
            db.comandoSQL(f"INSERT INTO tb_feedbackdocente (codfeedback, coddocente) VALUES ('{cod_feedback}', '{chave}')")
        elif isinstance(usuario, user.Pessoa):
            chave = usuario.getAll()[0]
            db.comandoSQL(f"INSERT INTO tb_feedbackpessoa (codfeedback, codpessoa) VALUES ('{cod_feedback}', '{chave}')")
        else:
            print("Tipo de usuario nao reconhecido.")
            return

        print("Feedback enviado com sucesso!")

    except Exception as e:
        print("Erro ao enviar feedback:", e)

def inscrever(usuario):
    print("\nExtensoes disponiveis:\n")

    try:
        extensoes = db.comandoSQL("SELECT codext, titulo, descricao FROM tb_extensao")

        if not extensoes:
            print("Nao ha nenhuma extensao cadastrada.")
            return

        for ext in extensoes:
            print(f"Codigo: {ext['codext']} | Titulo: {ext['titulo']} | Descricao: {ext['descricao']}")

        cod_ext = input("\nDigite o código da extensão que deseja se inscrever: ").strip()

        # Perguntar função desejada
        funcao = input("Qual funcao você deseja exercer (ex: Participante, Colaborador, Ministrante...)? ").strip().capitalize()

        if not funcao:
            print("Função invalida.")
            return

        # Determinar tabela e chave conforme tipo de usuário
        if isinstance(usuario, user.Aluno):
            cod_usuario = usuario.getAll()[0]
            tabela = "tb_funcaoaluno"
            chave = "codaluno"

        elif isinstance(usuario, user.Docente):
            cod_usuario = usuario.getAll()[0]
            tabela = "tb_funcaodocente"
            chave = "coddocente"

        elif isinstance(usuario, user.Pessoa):
            cod_usuario = usuario.getAll()[0]
            tabela = "tb_funcaopessoa"
            chave = "codpessoa"

        else:
            print("Tipo de usuario nao reconhecido.")
            return

        # Verificar se o usuario ja ta inscrito 
        ja_inscrito = db.comandoSQL(f"SELECT * FROM {tabela} WHERE {chave} = '{cod_usuario}' AND codExt = '{cod_ext}'")
        if ja_inscrito:
            print("Usuario ja esta inscrito ou com inscricao pendente nesta extensao.")
            return

        # Inserir inscrição com estado pendente
        db.comandoSQL(f"INSERT INTO {tabela} ({chave}, codext, funcao, estadoinscricao) VALUES ('{cod_usuario}', '{cod_ext}', '{funcao}', 'Pendente')")

        print(f"Inscricao realizada com sucesso na funcao : '{funcao}'! Aguarde aprovacao.")

    except Exception as e:
        print("Erro ao se inscrever na extensao:", e)

def ver_historico_academico(aluno):
    try:
        matricula = aluno.getAll()[0]

        resultado = db.comandoSQL(f"""
            SELECT 
                h.codMateria,
                m.nome AS nomeMateria,
                h.semestre,
                h.mencao
            FROM tb_historicoaluno h
            JOIN tb_materia m ON h.codmateria = m.codmateria
            WHERE h.codaluno = '{matricula}'
            ORDER BY h.semestre
        """)

        if  len(resultado) == 0:
            print("O aluno ainda nao cursou nenhuma materia.")
            return

        print(f"Historico academico do {aluno. __repr__()}:\n")
        for linha in resultado:
            print(f"Materia: {linha['codmateria']} - {linha['nomemateria']}")
            print(f"Semestre: {linha['semestre']}")
            print(f"Mencao: {linha['mencao']}\n")
            print()
            
    except Exception as e:
        print("Erro ao resgatar historico :", e)

def apagar_conta_pessoa(pessoa):
    cpf = pessoa.getAll()[0]

    confirm = input(f"\n Deseja apagar a conta vinculada ao CPF {cpf}? (s/n): ").strip().lower()
    if confirm != 's':
        print("Operacao cancelada.")
        return

    try:
        #Tira da tabela pessoa
        db.comandoSQL(f"DELETE FROM tb_pessoa WHERE cpf = '{cpf}'")
        print("Conta apagada.")

    except Exception as e:
        print("Erro ao apagar conta:", e)
