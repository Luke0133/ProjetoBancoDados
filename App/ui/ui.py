
import os, shutil

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

