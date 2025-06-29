import sys
import os

# Caminho para a pasta 'classes'
classes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'classes'))
if classes_path not in sys.path:
    sys.path.append(classes_path)

# Caminho para a pasta 'domains'
domains_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'domains'))
if domains_path not in sys.path:
    sys.path.append(domains_path)

database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db'))
if database_path not in sys.path:
    sys.path.append(database_path)

import usuario as user
import database as db

x = user.Aluno()

def loginProcess():
    os.system('cls')
    print("Selecione seu perfil:\n1 - Docente\n2 - Aluno\n3 - Colaborador\n4 - Admin\n0 - Sair")
    while True:
        select = input()
        if select in "01234":
            break
        else:
            print("Valor de seleção errado")
    
    if select == "0":
        print("Programa encerrado") 

    elif select == "1":
        os.system('cls')
        print("Entrando como Docente")
        print("Digite 'sair' no campo 'matricula' para encerrar o programa")
        while True:
            matricula = input("Matricula: ")
            if matricula == "sair":
                print("Programa encerrado")
                break
            cpf = input("CPF: ")
            senha = input("Senha: ")
            aux = db.comandoSQL(f"SELECT * FROM tb_docente where matricula = '{matricula}' or cpf = '{cpf}' or senha = '{senha}'")
            if aux == []:
                print("Usuário não registrado")
            elif [aux[0]["matricula"],aux[0]["cpf"],aux[0]["senha"]] == [matricula,cpf,senha]:
                print("Login efetuado")
                docente = user.Docente(aux[0]["matricula"],aux[0]["nome"],aux[0]["senha"],aux[0]["cpf"],aux[0]["coddep"])
                print(docente.getAll())
                break
            else:
                print("Erro em algum dos campos")

    elif select == "2":
        os.system('cls')
        print("Entrando como Aluno")
        print("Digite 'sair' no campo 'matricula' para encerrar o programa")
        while True:
            matricula = input("Matricula: ")
            if matricula == "sair":
                print("Programa encerrado")
                break
            cpf = input("CPF: ")
            senha = input("Senha: ")
            aux = db.comandoSQL(f"SELECT * FROM tb_aluno where matricula = '{matricula}' or cpf = '{cpf}' or senha = '{senha}'")
            if aux == []:
                print("Usuário não registrado")
            elif [aux[0]["matricula"],aux[0]["cpf"],aux[0]["senha"]] == [matricula,cpf,senha]:
                print("Login efetuado")
                aluno = user.Aluno(aux[0]["matricula"],aux[0]["nome"],aux[0]["senha"],aux[0]["cpf"],aux[0]["ira"],aux[0]["dataingresso"],aux[0]["semestreatual"])
                print(aluno.getAll())
                break
            else:
                print("Erro em algum dos campos")

    elif select == "3":
        os.system('cls')
        print("Entrando como Colaborador")
        print("Digite 'sair' no campo 'cpf' para encerrar o programa")
        while True:
            cpf = input("CPF: ")
            if cpf == "sair":
                print("Programa encerrado")
                break
            senha = input("Senha: ")
            aux = db.comandoSQL(f"SELECT * FROM tb_pessoa where cpf = '{cpf}' or senha = '{senha}'")
            if aux == []:
                print("Usuário não registrado")
            elif [aux[0]["cpf"],aux[0]["senha"]] == [cpf,senha]:
                print("Login efetuado")
                pessoa = user.Pessoa(aux[0]["cpf"],aux[0]["nome"],aux[0]["senha"])
                break
            else:
                print("Erro em algum dos campos")

    elif select == "4":
        os.system('cls')
        print("Digite a senha de admin")
        print("Digite 'sair' para encerrar o programa")
        while True:
            senha = input()
            if senha == "adminext":
                break
            elif senha == "sair":
                print("Programa encerrado")
                break
            else:
                print("senha incorreta")
