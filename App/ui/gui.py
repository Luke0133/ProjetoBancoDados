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
    print("Selecione seu perfil:\n1 - Docente\n2 - Aluno\n3 - Colaborador\n0 - Sair")
    while True:
        select = input()
        if select in "0123":
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

#Foto e local
def verifLocal(nome,tipo,estado,municipio,bairro,complemento = None):
    auxlocal = db.comandoSQL(f"SELECT * FROM tb_local WHERE nome = '{nome}' or nome = '{tipo}' or estado = '{estado}' or municipio = '{municipio}' or bairro = '{bairro}'")
    if auxlocal == []:
        print("Nenhum local encontrado")
        sn = input("Deseja adicionar um local? (S para sim, N para não): ")
        if sn.lower() == 's':
            while True:
                print("Digite 'sair' no campo 'Nome' para cancelar")
                while True:
                    nome = input("Nome: ")
                    if nome == "sair":
                        break
                    elif len(nome) > 100:
                        print("Erro: Nome com mais de 100 caracteres")
                        continue
                    else:
                        break
                if nome == "sair":
                        break
                while True:
                    tipo = input("Tipo ('Campus','Escola','Outro'): ")
                    if tipo not in ["Campus","Escola","Outro"]:
                        print("Erro: 'tipo' deve ser um dos três: Campus, Escola, Outro")
                        continue
                    else:
                        break
                while True:
                    estado = input("Estado (sigla): ")
                    if len(estado) != 2:
                        print("Erro: Sigla de estado do formato errado")
                        continue
                    else:
                        break
                while True:
                    municipio = input("Municipio: ")
                    if len(municipio) > 50:
                        print("Erro: Nome de municipio com mais de 50 caracteres")
                        continue
                    else:
                        break
                while True:
                    bairro = input("Bairro: ")
                    if len(bairro) > 50:
                        print("Erro: Nome de bairro com mais de 50 caracteres")
                        continue
                    else:
                        break
                while True:
                    complemento = input("Complemento (digite 'sem' se não quiser adicionar complemento): ")
                    if complemento == "sem":
                        complemento = None
                        break
                    elif len(complemento) > 100:
                        print("Erro: Complemento com mais de 100 caracteres")
                        continue
                    else:
                        break
                break
            if complemento != None:
                db.comandoSQL(f'''INSERT INTO tb_local (nome, tipo, estado, municipio, bairro, complemento) 
                              values ('{nome}','{tipo}','{estado}','{municipio}','{bairro}','{complemento}')
                              ''')
            else:
                db.comandoSQL(f'''INSERT INTO tb_local (nome, tipo, estado, municipio, bairro)
                               values ('{nome}','{tipo}','{estado}','{municipio}','{bairro}')
                               ''')    
    else:
        tam = len(auxlocal)
        if tam == 1:
            return auxlocal
        else:
            count = 0
            for i in auxlocal:
                count += 1
                print(f"{count} - {i["nome"]} | {i["tipo"]} | {i["estado"]} | {i["municipio"]} | {i["bairro"]}")
                if i["complemento"] != None:
                    print(f"Complemento: {i["complemento"]}")
            print("Escolha um local")
            while True:
                sel = input("Digite: ")
                if (sel.isdigit() == False or int(sel) > count or int(sel) == 0):
                    print("Valor de seleção errado")
                else:
                    return auxlocal[sel-1]
