import os,shutil,math,textwrap

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pyfiglet import figlet_format
from colorama import init, Fore
init(autoreset=True)

from classes import extensao as ex
from classes import usuario as user
from controller import con_extensao as conEx
from db import database as sql

PERPAGE = 4
terminal_width = shutil.get_terminal_size().columns
banner = figlet_format("SGE - Extensoes").rstrip("\n")

def ui_extensoes(usuario,mode='general'):
    mode_text = f"{Fore.YELLOW}(Ver Extensões)" if mode == 'general' else '(Minhas Extensões)'
    msg = None
    warning = "Ainda não existem extensões" if mode == 'general' else 'Você ainda não se inscreveu em nenhuma extensão'
    n = 0
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None

        extensoes = conEx.find_extensoes() if mode == 'general' else conEx.find_my_extensoes(usuario)
        if extensoes:
            nTotal = math.ceil(len(extensoes)/PERPAGE)
            msg_text = f"{Fore.YELLOW}Página {n+1}/{nTotal}"
            line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
        else:
            line = mode_text.rjust(terminal_width)

        print(line)

        choices = []
        if extensoes:
            show = PERPAGE if (n*PERPAGE + PERPAGE) < len(extensoes) else len(extensoes) - n*PERPAGE
            for i in range(show):
                info = conEx.get_info_ext(extensoes[i + n*PERPAGE], usuario, mode)

                if info:
                    if mode == 'general':
                        msg_extensao = f"{info['codext']} | {info['titulo']:<80} | {info['tipoacao']:^10} | Departamento: {info['departamento']}\n{18*' '}Coordenardor(a): {info['coordenador']}\n{16*' '}"
                    else:
                        msg_extensao = f"{info['codext']} | {info['titulo']:<80} | {info['tipoacao']:^10} | Departamento: {info['departamento']}\n  {f'({info['estadoinscricao']})':<16}Coordenardor(a): {info['coordenador']}\n{16*' '}"
                else:
                    return "Erro ao pegar informações das extensões"
                choices.append(Choice(value=i + n*PERPAGE + 4, name=f"{i + 1 + n*PERPAGE}. {msg_extensao}"))
        else:
            print(warning)

        if n > 0:
            choices.append(Choice(value=3, name="(<) PREV"))
        if (n*PERPAGE + PERPAGE) < len(extensoes):
            choices.append(Choice(value=2, name="NEXT (>)"))
        
        if isinstance(usuario, user.Docente):
            choices.append(Choice(value=1, name="Criar Extensão"))

        choices.append(Choice(value=0, name="Voltar"))

        choice = inquirer.select(
            message=f'Selecione uma extensão para ver seus detalhes ou uma das ações abaixo:',
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return None
            case 2: n+=1
            case 3: n-=1
            case 1: pass # criar extensao
            case _: ver_extensao(extensoes[choice - 4], usuario, mode)


        
def ver_extensao(extensao, usuario, mode = 'general'):

    mode_text = f"{Fore.YELLOW}(Visualização da Extensão)"
    msg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()}"
    line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
    msg = None
    warning = "Ainda não existem extensões" if mode == 'general' else 'Você ainda não se inscreveu em nenhuma extensão'
    n = 0
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        print(line)
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None
        local = conEx.find_local(extensao.getCodLocal())

        print(f'| Título: {extensao.getTitulo()}')
        print(f'| Tipo de Ação: {extensao.getTipoAcao()}')
        print(f'| Área temática: {extensao.getAreaTematica()}')
        print(f'| Data de realização: {extensao.getInicioRealizacao()} - {extensao.getFimRealizacao()}')
        print(f'| Local: {local.getNome()} -- {local.getEstado()} || {local.getMunicipio()} || {local.getBairro()}',end='')
        if local.getComplemento():
            print(f' || {local.getComplemento()}\n')
        else:
            print('\n')
        
        
        choices = [Choice(value=1, name="Descrição"), Choice(value=2, name="Público Alvo"), Choice(value=3, name="Ver Feedbacks"),
                   Choice(value=4, name="Fazer Feedback")]
        

        if (participacao := conEx.participacao(extensao,usuario))[0]:
            if participacao[1] == 'Coordenador(a)':
                choices.append(Choice(value=5, name="Ver Pedidos de Inscrição"))
                choices.append(Choice(value=6, name="Editar/Apagar Extensão"))
            else:
                choices.append(Choice(value=7, name="Sair da Extensão"))
        else:
            choices.append(Choice(value=8, name="Inscrever-se"))

        choices.append(Choice(value=0, name="Voltar"))

        choice = inquirer.select(
            message=f'Selecione uma ação:',
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return None
            case 3: ver_feedbacks(extensao)
            case 4: msg = fazer_feedback(extensao, usuario)
            case 5: pass # Ver pedidos de inscrição
            case 6: pass # Editar/Apagar extensão
            case 7: pass # Sair da extensão
            case 8: pass # Inscrever-se

            case 1: # Ver descrição da Extensão
                os.system('cls')
                print(Fore.CYAN + banner)
                print(Fore.CYAN + "=" * terminal_width)
                new_mode_text = f"{Fore.YELLOW}(Descrição da Extensão)".rjust(terminal_width)
                newline = msg_text + (" " * (terminal_width - 10 - len(new_mode_text) - len(msg_text))) + new_mode_text
                print(newline)
                print(textwrap.fill(f'| Descrição: {extensao.getDescricao()}', width=terminal_width))
                
                inquirer.select(
                    message=f'',
                    choices= [Choice(value=0, name="Voltar")],
                    qmark="",
                    pointer=">"
                ).execute()

            case 2: # Ver detalhes do público Alvo
                os.system('cls')
                print(Fore.CYAN + banner)
                print(Fore.CYAN + "=" * terminal_width)
                new_mode_text = f"{Fore.YELLOW}(Detalhes do Público Alvo)"
                newline = msg_text + (" " * (terminal_width - len(new_mode_text) - len(msg_text))) + new_mode_text
                print(newline)

                if extensao.getPublicoInterno():
                    print(f'| Público alvo interno: {extensao.getPublicoInterno()}')

                print(f'| Público interno estimado: {extensao.getPublicoInternoEst()}')

                if extensao.getPublicoExterno():
                    print(f'| Público alvo externo: {extensao.getPublicoExterno()}')

                print(f'| Público externo estimado: {extensao.getPublicoExternoEst()}')

                inquirer.select(
                    message=f'',
                    choices= [Choice(value=0, name="Voltar")],
                    qmark="",
                    pointer=">"
                ).execute()
            case _: pass


def ver_feedbacks(extensao):
    mode_text = f"{Fore.YELLOW}(Ver Feedbacks)"
    msg = None
    n = 0
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None

        feedbacks = conEx.find_feedbacks(extensao.getCodExt())
        if feedbacks:
            nTotal = math.ceil(len(feedbacks)/PERPAGE)
            msg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()} -- Página {n+1}/{nTotal}"
            line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
        else:
            line = mode_text.rjust(terminal_width)

        print(line)

        choices = []
        if feedbacks:
            show = PERPAGE if (n*PERPAGE + PERPAGE) < len(feedbacks) else len(feedbacks) - n*PERPAGE
            for i in range(show):
                choices.append(Choice(value=i + n*PERPAGE + 4, name=f"{i + 1 + n*PERPAGE}. {feedbacks[i + n*PERPAGE].getData()} - Nota {feedbacks[i + n*PERPAGE].getNota()} - {feedbacks[i + n*PERPAGE].getAutor()}"))
        else:
            print("Ainda não existem feedbacks para essa extensão")

        if n > 0:
            choices.append(Choice(value=3, name="(<) PREV"))
        if (n*PERPAGE + PERPAGE) < len(feedbacks):
            choices.append(Choice(value=2, name="NEXT (>)"))
        
        choices.append(Choice(value=0, name="Voltar"))

        choice = inquirer.select(
            message=f'Selecione um feedback para ler ou uma das ações abaixo:',
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return None
            case 2: n+=1
            case 3: n-=1
            case _: 
                os.system('cls')
                print(Fore.CYAN + banner)
                print(Fore.CYAN + "=" * terminal_width)
                new_mode_text = f"{Fore.YELLOW}(Ver Feedback)".rjust(terminal_width)
                new_msg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()}"
                newline = new_msg_text + (" " * (terminal_width - 10 - len(new_mode_text) - len(new_msg_text))) + new_mode_text
                print(newline)
                
                feedback = feedbacks[choice - 4]
                print(f'| Autor: {feedback.getAutor()}')
                print(f'| Nota: {feedback.getNota()}{26*' '}Função na Extensão: {feedback.getFunçao()}')
                print(f'| Data de Publicação: {feedback.getData()}')         
                print(textwrap.fill(f'| Comentário: {feedback.getComentario()}', width=terminal_width))
                
                inquirer.select(
                    message=f'',
                    choices= [Choice(value=0, name="Voltar")],
                    qmark="",
                    pointer=">"
                ).execute()
    
def fazer_feedback(extensao,usuario):
    mode_text = f"{Fore.YELLOW}(Fazer Feedback)"
    msg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()}  -- Digite cancelar para voltar"
    line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
    err = None
    while(True):
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            if err:
                print(f'{Fore.RED}{err}')
                err = None

            nota = input("Dê a sua nota de 1 a 5: ")
            if nota == 'cancelar': return None
            if not len(nota) == 0 and nota.isdigit():
                nota = int(nota)
                if nota <=5 and nota >= 1:
                    break
                else:
                    err = "Nota deve ser entre 1 e 5"
        
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            print(f'Dê a sua nota de 1 a 5: {nota}')
            
            comentario = input("Digite o seu comentário: ")
            if comentario == 'cancelar': return None
            if not len(comentario) == 0:
                try:
                    conEx.criar_feedback(extensao, nota, comentario, usuario)
                    return 'Comentário registrado com sucesso'
                except (Exception,ValueError) as e:
                    err = e 





def criar_extensao(codDocente):
    extensao = ex.Extensao()
    os.system('cls')
    print("CRIAR EXTENSÃO\n")

    print(f'| Título: {extensao.getTitulo()}')
    print(f'| Tipo de Ação: {extensao.getTipoAcao()}')
    print(f'| Área temática: {extensao.getAreaTematica()}')
    print(f'| Data de realização: {extensao.getInicioRealizacao()} - {extensao.getFimRealizacao()}')
    #print(f'| Local: {local.getNome()} -- {local.getEstado()} || {local.getMunicipio()} || {local.getBairro()}',end='')

