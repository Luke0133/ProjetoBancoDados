
import os, platform, tempfile, shutil

import psycopg2

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pyfiglet import figlet_format
from colorama import init, Fore
init(autoreset=True)

from classes import usuario as user
from db import database as db
from classes import extensao as ex
from controller import con_usuario as conUser
from ui import ui_usuario as ui_user

terminal_width = shutil.get_terminal_size().columns
banner = figlet_format("SGE - Extensoes").rstrip("\n")
def main_ui():
    msg = None
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None

        choice = inquirer.select(
            message="Olá! Escolha uma ação:",
            choices=[
                Choice(value=1, name="Entrar"),
                Choice(value=2, name="Registrar (Público Externo)"),
                Choice(value=0, name="Sair do SGE"),
            ],
            default="Entra",
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 1: 
                id = loginProcess()
                if id: msg = ui_user.ui_usuario(id)
            case 2: msg = registerProcess()
            case _: 
                os.system('cls')
                return



def loginProcess():
    login_text = f"{Fore.YELLOW}(LOGIN)"
    msg_text = f"{Fore.YELLOW}Digite cancelar para voltar"
    line = msg_text + (" " * (terminal_width - len(login_text) - len(msg_text))) + login_text
    
    err = None
    while(True):
        # Espera matricula/cpf correto e checa se é aluno, docente ou pessoa externa
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            if err:
                print(f'{Fore.RED}{err}')
                err = None

            id = input("Insira matrícula ou CPF: ")
            len_id = len(id)
            if id.isdigit() and (len_id == 9 or len_id == 11):
                break
            elif id == 'cancelar': return None
            else:
                err = "Matrícula/CPF deve ser de 9 ou 11 caracteres"
        
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            print(f'Insira matrícula ou CPF: {id}')

            senha = input("Insira sua senha: ")
            if senha == 'cancelar': return None
            
            if not len(senha) == 0:
                try:
                    return conUser.con_login(id,senha)
                except ValueError as e:
                    err = e
                    break

def registerProcess():
    login_text = f"{Fore.YELLOW}(REGISTRO DE CONTA PÚBLICA)"
    msg_text = f"{Fore.YELLOW}Digite cancelar para voltar"
    line = msg_text + (" " * (terminal_width - len(login_text) - len(msg_text))) + login_text
    
    err = None
    while(True):
        # Espera matricula/cpf correto e checa se é aluno, docente ou pessoa externa
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            if err:
                print(f'{Fore.RED}{err}')
                err = None

            id = input("Insira seu CPF: ")
            len_id = len(id)
            if id.isdigit() and (len_id == 11):
                try:
                    conUser.get_usuario(id)
                    err = "Usuário já está cadastrado"
                except ValueError:
                    break # Se usuário não foi encontrado, continua
            elif id == 'cancelar': return None
            else:
                err = "CPF deve ser de 11 caracteres"
        
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            print(f'Insira seu CPF: {id}')
            
            nome = input("Insira seu nome: ")
            if nome == 'cancelar': return None
            if not len(nome) == 0:
                break

        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            print(f'Insira seu CPF: {id}')
            print(f'Insira seu nome: {nome}')

            senha = input("Insira sua senha: ")
            if senha == 'cancelar': return None
            
            if not len(senha) == 0:
                try:
                    conUser.criar_usuario(user.Pessoa(id,nome,senha))
                    return 'Registro do usuário feito com sucesso! Agora é possível Entrar com sua conta'
                except (Exception,ValueError) as e:
                    print(f'\nNão foi possível criar um usuário. Erro: {Fore.RED}{e}')
                    input("Pressione ENTER para voltar ao menu principal")
                    return None


#Foto e local
def verifLocal(nome,tipo,estado,municipio,bairro,complemento = None):
    auxlocal = db.comandoSQL(f'''SELECT * FROM tb_local 
                             WHERE nome = '{nome}' or nome = '{tipo}' or estado = '{estado}' 
                             or municipio = '{municipio}' or bairro = '{bairro}'
                             ''')
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
            local = ex.Local(auxlocal[0]["codlocal"],auxlocal[0]["nome"],auxlocal[0]["tipo"],[auxlocal[0]["estado"],auxlocal[0]["municipio"],auxlocal[0]["bairro"],auxlocal[0]["complemento"]],auxlocal[0]["estado"],auxlocal[0]["municipio"],auxlocal[0]["bairro"],auxlocal[0]["complemento"])
            return local
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
                    aux = sel-1
                    local = ex.Local(auxlocal[aux]["codlocal"],auxlocal[aux]["nome"],auxlocal[aux]["tipo"],[auxlocal[aux]["estado"],auxlocal[aux]["municipio"],auxlocal[aux]["bairro"],auxlocal[aux]["complemento"]],auxlocal[aux]["estado"],auxlocal[aux]["municipio"],auxlocal[aux]["bairro"],auxlocal[aux]["complemento"])
                    return local

def addFoto(codext):
    ext = db.comandoSQL(f"SELECT * FROM tb_extensao WHERE codext = '{codext}'")
    if not ext:
        print("Erro: Extensao nao existente")
    else:
        print("Descriçao da foto: ")
        desc = input()
        print("Digite o caminho da imagem: ")
        fotopath = input().strip()
        if not os.path.isfile(fotopath):
            print("Erro: Arquivo não encontrado. Verifique o caminho e tente novamente.")
            return
        try:
            with open(fotopath, 'rb') as f:
                fotobin = f.read()
            print(psycopg2.Binary(fotobin))
            db.comandoSQL(f"INSERT INTO tb_foto (codext, descricao, foto) VALUES ('{codext}', '{desc}', {psycopg2.Binary(fotobin)})")
        except Exception as e:
            print("Ocorreu um erro:", e)

def verImagem(codext):
    img = db.comandoSQL(f"SELECT * FROM tb_foto WHERE codext = '{codext}'")
    try:
        dados_imagem = img[0][3]

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(codext)[1]) as tmp_file:
            tmp_file.write(dados_imagem)
            caminho_temp = tmp_file.name

        print(f"Imagem salva temporariamente em: {caminho_temp}")

        sistema = platform.system()
        if sistema == "Windows":
            os.startfile(caminho_temp)

    except Exception as e:
        print("Erro:", e)
