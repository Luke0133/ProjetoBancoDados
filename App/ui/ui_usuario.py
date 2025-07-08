import os, shutil, platform, tempfile, math

import psycopg2

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pyfiglet import figlet_format
from colorama import init, Fore
init(autoreset=True)

from classes import usuario as user
from db import database as db
from classes import domains as dm
from classes import extensao as ex
from controller import con_usuario as conUser
from controller import con_materia as conMt
from ui import ui_extensao as uiEx

# Funções relacionadas à interface do usuário:
# user_ui
# user_detalhes_ui
# ui_alterar_senha
# apagar_conta
# email_detalhes_ui
# historico_aluno_ui
# curriculo_ui(id):
# adicionar_Curriculo(cpf):
# verCurriculo(cpf):

PERPAGE = 4
terminal_width = shutil.get_terminal_size().columns
banner = figlet_format("SGE - Extensoes").rstrip("\n")
def ui_usuario(id):
    mode_text = f"{Fore.YELLOW}(Página Inicial)"
    err = None
        
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        print(mode_text.rjust(terminal_width))
        if err:
            print(f'{Fore.RED}{err}')
            err = None
            
        try:
            usuario = conUser.get_usuario(id)
        except ValueError:
            return
        
        choices= [Choice(value=1, name="Detalhes da conta"),
                  Choice(value=2, name="Ver/Adicionar e-mails")]
        
        if isinstance(usuario, user.Aluno):
            choices.extend([Choice(value=5, name="Ver Histórico")])

        elif isinstance(usuario, user.Pessoa):
            choices.extend([Choice(value=6, name="Ver/Adicionar currículo")])  

        
        choices.extend([Choice(value=3, name="Ver Extensões"),Choice(value=4, name="Minhas Extensões"),Choice(value=0, name="Voltar e encerrar sessão")])

        choice = inquirer.select(
            message=f"Olá, {usuario.getNome()}! Escolha uma ação:",
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return
            case 1: 
                if user_detalhes_ui(id):
                    return "Usuário deletado com sucesso!"    
            case 2: email_detalhes_ui(id)
            case 3: err = uiEx.ui_extensoes(usuario,mode='general')
            case 4: err = uiEx.ui_extensoes(usuario,mode='usuario')
            case 5: historico_aluno_ui(usuario.getMatricula())
            case 6: curriculo_ui(id)
            case _: pass

# Mostra detalhes do usuário
def user_detalhes_ui(id):
    mode_text = f"{Fore.YELLOW}(Detalhes da Conta)"
    msg = None
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        print(mode_text.rjust(terminal_width))
        
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None

        try:
            usuario = conUser.get_usuario(id)
        except ValueError:
            return NotImplementedError
        
        choices = [Choice(value=1, name="Alterar Senha")]
        if isinstance(usuario, user.Aluno):
            print(f"Nome: {usuario.getNome()}")
            print(f"Matrícula: {usuario.getMatricula():<40} Cpf: {usuario.getCpf().get()} ")
            print(f"Curso:     {conMt.find_curso(usuario.getCodCurso()).getNome():<40} Ira: {usuario.getIra()}")  
            print(f"Data ingresso: {usuario.getDataIngresso()}{26*' '} Semestre atual: {usuario.getSemestreAtual()}")
            
        elif isinstance(usuario, user.Docente):
            print(f"Nome: {usuario.getNome()}")
            print(f"Matrícula: {usuario.getMatricula():<40} Cpf: {usuario.getCpf().get()} ")
            print(f"Departamento: {conMt.find_dep(usuario.getCodDep()).getNome()}")  

        elif isinstance(usuario, user.Pessoa):
            print(f"Nome: {usuario.getNome()}")
            print(f"Cpf: {usuario.getCpf().get()}")
            choices.append(Choice(value=2, name=f"Apagar Conta"))
            usuario = None

        choices.append(Choice(value=0, name="Voltar"))
        choice = inquirer.select(
            message=f"",
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return
            case 1: msg = ui_alterar_senha(id)
            case 2: return apagar_conta(id) # Se conseuiu apagar a conta, retornará True
            case _: pass


# Altera a senha do usuário
def ui_alterar_senha(id):
    mode_text = f"{Fore.YELLOW}(Alterar Senha do Usuário)"
    msg_text = f"{Fore.YELLOW}Digite cancelar para voltar"
    line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text

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

            senha = input("Insira sua senha atual: ")
            if senha == 'cancelar': return None
            if not len(senha) == 0:
                try:
                    conUser.con_login(id,senha)
                    break
                except ValueError as e:
                    err = "Senha incorreta"
        
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            print(f'Insira sua senha atual: {senha}')
            
            nova_senha1 = input("Insira sua nova senha: ")
            if nova_senha1 == 'cancelar': return None
            if not len(senha) == 0:
                break

        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            if err:
                print(f'{Fore.RED}{err}')
                err = None
            print(f'Insira sua senha atual: {senha}')
            print(f'Insira sua nova senha: {nova_senha1}')
            
            nova_senha2 = input("Insira novamente sua nova senha: ")
            if nova_senha2 == 'cancelar': return None
            if not len(nova_senha2) == 0:
                if nova_senha1 == nova_senha2:
                    try:
                        conUser.update_senha(id,nova_senha2)
                        return 'Senha alterada com Sucesso!'
                    except (Exception,ValueError) as e:
                        print(f'\nNão foi possível atualizar sua senha. Erro: {Fore.RED}{e}')
                        input("Pressione ENTER para voltar ao menu de Detalhes de Conta")
                        return None
                else:
                    err = 'Senhas novas estão diferentes'

# Apaga a conta da Pessoa
def apagar_conta(id):
    mode_text = f"{Fore.YELLOW}(Apagar Conta)"
    msg_text = f"{Fore.YELLOW}Digite cancelar para voltar"
    line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text

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

            senha = input("Insira sua senha: ")
            if senha == 'cancelar': return None
            if not len(senha) == 0:
                try:
                    conUser.con_login(id,senha)
                    break
                except ValueError as e:
                    err = "Senha incorreta"
        
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            print(f'Insira sua senha atual: {senha}\n\n{Fore.RED}{'Sua conta, feedbacks e tudo relacionado a ela serão deletados!!'}')
            
            choice = inquirer.select(
                message=f"Você realmente deseja deletar sua conta?",
                choices= [
                Choice(value=2, name="Não"),
                Choice(value=1, name="Sim")],
                qmark="",
                pointer=">"
            ).execute()
            
            match choice:
                case 1: 
                    try:
                        conUser.deletar_usuario(id)
                        return True
                    except (Exception,ValueError) as e:
                        print(f'\nNão foi possível deletar sua conta. Erro: {Fore.RED}{e}')
                        input("Pressione ENTER para voltar ao menu de Detalhes de Conta")
                        return False
                case 2:
                    print(f'\nSua conta NÃO foi deletada. Processo cancelado')
                    input("Pressione ENTER para voltar ao menu de Detalhes de Conta") 
                    return False
                case _: pass


# Mostra detalhes sobre os emails do usuário
def email_detalhes_ui(id):
    try:
        usuario = conUser.get_usuario(id)
    except ValueError:
        return
    mode_text = f"{Fore.YELLOW}(Ver Emails)"
    msg = None
    n = 0
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None

        emails = conUser.find_emails(usuario)
        if emails:
            nTotal = math.ceil(len(emails)/PERPAGE)
            msg_text = f"{Fore.YELLOW}Página {n+1}/{nTotal}"
            line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
        else:
            line = mode_text.rjust(terminal_width)

        print(line)

        choices = []
        if emails:
            show = PERPAGE if (n*PERPAGE + PERPAGE) < len(emails) else len(emails) - n*PERPAGE
            for i in range(show):
                choices.append(Choice(value=i + n*PERPAGE + 4, name=f"{i + 1 + n*PERPAGE}. {emails[i + n*PERPAGE]}"))
        else:
            print("Você ainda não possui emails registrados nessa conta")

        if n > 0:
            choices.append(Choice(value=3, name="(<) PREV"))
        if (n*PERPAGE + PERPAGE) < len(emails):
            choices.append(Choice(value=2, name="NEXT (>)"))
        
        choices.extend([Choice(value=1, name="Adicionar email"),Choice(value=0, name="Voltar")])

        choice = inquirer.select(
            message=f"Escolha uma ação (selecione um email para deletá-lo, caso exista)",
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return
            case 2: n+=1
            case 3: n-=1
            case 1: 
                err = None  
                mode_text1 = f"{Fore.YELLOW}(Adicionar Email Emails)"
                msg_text1 = f"{Fore.YELLOW}Digite cancelar para voltar"
                line1 = msg_text1 + (" " * (terminal_width - len(mode_text1) - len(msg_text1))) + mode_text1
                while(True):
                    os.system('cls')
                    print(Fore.CYAN + banner)
                    print(Fore.CYAN + "=" * terminal_width)
                    print(line1)
                    if err:
                        print(f'{Fore.RED}{err}')
                        err = None

                    novo_email = dm.Email()
                    s = input("Digite o seu novo email: ").strip()
                    if s == 'cancelar': break
                    try:
                        novo_email.set(s)
                        try:
                            conUser.adicionar_email(usuario, novo_email)
                            msg = 'Email cadastrado com sucesso'
                            break
                        except (Exception) as e:
                            err = e
                    except ValueError as e:
                        err = e 

            case _:
                while(True):
                    os.system('cls')
                    print(Fore.CYAN + banner)
                    print(Fore.CYAN + "=" * terminal_width)
                    print(line)

                    new_choice = inquirer.select(
                        message=f"Você realmente deseja deletar o email {emails[choice - 4]}?",
                        choices= [
                        Choice(value=2, name="Não"),
                        Choice(value=1, name="Sim")],
                        qmark="",
                        pointer=">"
                    ).execute()
                    
                    match new_choice:
                        case 1: 
                            try:
                                conUser.deletar_email(usuario, emails[choice - 4])
                                msg = "Email deletado com sucesso!"
                            except (Exception,ValueError) as e:
                                print(f'\nNão foi possível deletar esse email. Erro: {Fore.RED}{e}')
                                input("Pressione ENTER para voltar ao menu de Ver Emails")
                            break
                        case 2:
                            msg = 'Seu email NÃO foi deletado. Processo cancelado'
                            break
                        case _: pass


def historico_aluno_ui(matricula):
    mode_text = f"{Fore.YELLOW}(Ver Histórico)"
    historico = conUser.find_historico(matricula)
    nTotal = math.ceil(len(historico)/PERPAGE)

    n = 0
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        
        msg_text = f"{Fore.YELLOW}Página {n+1}/{nTotal}"
        line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
        print(line)

        choices = []
        if historico:
            show = PERPAGE if (n*PERPAGE + PERPAGE) < len(historico) else len(historico) - n*PERPAGE
            for i in range(show):
                materia = conMt.find_materia(historico[i + n*PERPAGE]['codmateria'])
                print(f"{i + 1 + n*PERPAGE}. {materia.getSigla()} - {materia.getNome():<70}| Semestre: {historico[i + n*PERPAGE]['semestre']} | Menção: {historico[i + n*PERPAGE]['mencao']}")
        else:
            print("Seu histórico está vazio")

        if n > 0:
            choices.append(Choice(value=3, name="(<) PREV"))
        if (n*PERPAGE + PERPAGE) < len(historico):
            choices.append(Choice(value=2, name="NEXT (>)"))
        
        choices.extend([Choice(value=0, name="Voltar")])

        choice = inquirer.select(
            message=f"",
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return
            case 2: n+=1
            case 3: n-=1

def curriculo_ui(id):
    mode_text = f"{Fore.YELLOW}(Currículo)"
    err = None
    msg = None
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        print(mode_text.rjust(terminal_width))
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None
        if err:
            print(f'{Fore.RED}{err}')
            err = None
            
        try:
            usuario = conUser.get_usuario(id)
        except ValueError:
            return
        
        if conUser.curriculo_usuario(id):
            choices= [Choice(value=1, name="Ver Currículo"),
                    Choice(value=2, name="Trocar Currículo")]
        else:
            print("Você ainda não possui um currículo!")
            choices= [Choice(value=2, name="Adicionar Currículo")]
        
        choices.append(Choice(value=0, name="Voltar"))

        choice = inquirer.select(
            message=f"Escolha uma ação:",
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return
            case 1: msg, err = verCurriculo(id)
            case 2: msg = adicionar_Curriculo(id) 
            case _: pass

def adicionar_Curriculo(cpf):
    err = None  
    mode_text = f"{Fore.YELLOW}(Adicionar Currículo)"
    msg_text = f"{Fore.YELLOW}Digite cancelar para voltar"
    line1 = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        print(line1)
        if err:
            print(f'{Fore.RED}{err}')
            err = None


        pdfpath = input("Digite o caminho do arquivo do seu currículo: ").strip()
        if pdfpath == 'cancelar': return None
        if not os.path.isfile(pdfpath): err = "Arquivo não encontrado. Verifique o caminho e tente novamente."
        else:
            try:
                with open(pdfpath, 'rb') as f:
                    pdfbin = f.read()
                conUser.criar_curriculo(psycopg2.Binary(pdfbin),cpf)  
                return "Currículo Adicionado com sucesso!"
            except Exception as e: err = e

def verCurriculo(cpf):
    try:
        dados_curriculo = conUser.curriculo_usuario(cpf)

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(cpf)[1]) as tmp_file:
            tmp_file.write(dados_curriculo)
            caminho_temp = tmp_file.name
        
        sistema = platform.system()
        if sistema == "Windows":
            os.startfile(caminho_temp)

        return (f"Imagem salva temporariamente em: {caminho_temp}",None)
    
    except (ValueError,Exception) as e:
        return (None,e)