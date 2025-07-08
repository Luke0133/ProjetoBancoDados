from classes import usuario as user
from db import database as db
from classes import domains as dm



def con_login(id,senha):
    if (usuario := db.get_aluno(id)):
        senha_usuario =  usuario[0]['senha']

    elif (usuario := db.get_docente(id)):
        senha_usuario = usuario[0]['senha']
        
    elif (usuario := db.get_pessoa(id)):
        senha_usuario = usuario[0]['senha']
    else:
        raise ValueError("Usuário não encontrado")
    
    if not str(senha_usuario) == senha:
        raise ValueError("Usuário ou Senha incorretos")
    else:
        return id
    

def get_usuario(id):
    if (usuario := db.get_aluno(id)):
        usuario =  user.Aluno(usuario[0]['matricula'],usuario[0]['codcurso'],usuario[0]['nome'],usuario[0]['cpf'],
                              usuario[0]['senha'],usuario[0]['ira'],usuario[0]['dataingresso'],usuario[0]['semestreatual'])

    elif (usuario := db.get_docente(id)):
         usuario = user.Docente(usuario[0]['matricula'],usuario[0]['coddep'],usuario[0]['nome'],usuario[0]['senha'],usuario[0]['cpf'])
        
    elif (usuario := db.get_pessoa(id)):
        usuario = user.Pessoa(usuario[0]['cpf'],usuario[0]['nome'],usuario[0]['senha'])
    else:
        raise ValueError("Usuário não encontrado")
    
    return usuario

def criar_usuario(pessoa:user.Pessoa):
    db.create_pessoa(pessoa.getCpf(),pessoa.getNome(),pessoa.getSenha())
    return

def deletar_usuario(id):
    db.delete_pessoa(id)
    return

def update_senha(id,newPass):
    if db.get_aluno(id):
        db.update_senha_aluno(id,newPass)

    elif db.get_docente(id):
        db.update_senha_docente(id,newPass)
        
    elif db.get_pessoa(id):
        db.update_senha_pessoa(id,newPass)
    else:
        raise ValueError("Usuário não encontrado")
    
    return

# Retorna todos os emails de uma determinada conta
def find_emails(usuario):
    # Verifica qual é o tipo do usuário para inseri-lo na respectiva tabela
    if isinstance(usuario, user.Aluno):
        emailsExistentes = db.get_emails_aluno(usuario.getMatricula())
    elif isinstance(usuario, user.Docente):
        emailsExistentes = db.get_emails_docente(usuario.getMatricula())
    elif isinstance(usuario, user.Pessoa):
        emailsExistentes = db.get_emails_pessoa(usuario.getCpf())
    
    for i in range(len(emailsExistentes)):
        emailsExistentes[i] = dm.Email(emailsExistentes[i]['email'])  

    return emailsExistentes

#Função para adicionar um novo email para um usuário do tipo Aluno, Docente ou Pessoa
def adicionar_email(usuario, email): 
    # Verifica qual é o tipo do usuário para inseri-lo na respectiva tabela
    if isinstance(usuario, user.Aluno):
        db.criar_email_aluno(usuario.getMatricula(),email)
    elif isinstance(usuario, user.Docente):
        db.criar_email_docente(usuario.getMatricula(),email)
    elif isinstance(usuario, user.Pessoa):
        db.criar_email_pessoa(usuario.getCpf(),email)
    return


def deletar_email(usuario, email):
    # Verifica qual é o tipo do usuário para inseri-lo na respectiva tabela
    if isinstance(usuario, user.Aluno):
        db.deletar_email_aluno(usuario.getMatricula(),email)
    elif isinstance(usuario, user.Docente):
        db.deletar_email_docente(usuario.getMatricula(),email)
    elif isinstance(usuario, user.Pessoa):
        db.deletar_email_pessoa(usuario.getCpf(),email)
    return

def find_historico(matricula):
    return db.get_historico(matricula)

def criar_curriculo(pdf,cpf):
    db.update_curriculo(pdf,cpf) 

def curriculo_usuario(cpf):
    return db.get_curriculo(cpf)[0][3]

