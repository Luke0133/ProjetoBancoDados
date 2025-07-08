import os,shutil,math,textwrap,psycopg2,tempfile,platform

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pyfiglet import figlet_format
from colorama import init, Fore
init(autoreset=True)

from controller import con_extensao as conEx

PERPAGE = 4
terminal_width = shutil.get_terminal_size().columns
banner = figlet_format("SGE - Extensoes").rstrip("\n")

# Funções auxiliares para a visualização/edição de extensões
# ver_feedbacks
# fazer_feedback
# situacao_extensao
# fotos_extensao


# Função para ver feedbacks da extensão
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

# Função para fazer um feedback na extensão
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

# Função para editar situação da extensão
def situacao_extensao(codExt, mode = 'ver'):
    mode_text = f"{Fore.YELLOW}(Situação da Extensao)" if mode == 'ver' else f"{Fore.YELLOW}(Adicionar Situação da Extensao)"
    msg = None
    n = 0
    extensao = conEx.find_extensao(codExt)
    err = None
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None
        if err:
            print(f'{Fore.RED}{err}')
            err = None

        situacoes = conEx.find_situacoes(extensao.getCodExt())
        if situacoes:
            nTotal = math.ceil(len(situacoes)/PERPAGE)
            msg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()} -- Página {n+1}/{nTotal}"
            line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
        else:
            line = mode_text.rjust(terminal_width)

        print(line)


        if situacoes:
            show = PERPAGE if (n*PERPAGE + PERPAGE) < len(situacoes) else len(situacoes) - n*PERPAGE
            for i in range(show):
                print(f"{i + 1 + n*PERPAGE}. {situacoes[i + n*PERPAGE].getDataSit()} {situacoes[i + n*PERPAGE].getHorarioSit().strftime("%H:%M:%S")} || {situacoes[i + n*PERPAGE].getSituacao()}")
        else:
            print("Ainda não foram inseridas situações para essa extensão")
        
        choices = []
        if n > 0:
            choices.append(Choice(value=3, name="(<) PREV"))
        if (n*PERPAGE + PERPAGE) < len(situacoes):
            choices.append(Choice(value=2, name="NEXT (>)"))
        
        if not mode == 'ver':
            choices.append(Choice(value=1, name="Adicionar Situação para essa Extensão"))
        choices.append(Choice(value=0, name="Voltar"))

        choice = inquirer.select(
            message=f'\nEscolha uma ação:',
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return
            case 2: n+=1
            case 3: n-=1
            case 1:
                while(True):
                    os.system('cls')
                    print(Fore.CYAN + banner)
                    print(Fore.CYAN + "=" * terminal_width)
                    print(line)
                    if err:
                        print(f'{Fore.RED}{err}')
                        err = None

                    sit = input("Digite a situação: ")            
                    if sit == 'cancelar': 
                        msg = "Situação NÃO foi adicionada"
                        break
                    if len(sit) > 100: err = "Situação ter até 100 caracteres"
                    elif not len(sit) == 0:
                        try:
                            conEx.adicionar_situacao(codExt,sit)
                            msg = "Situação adicionada com sucesso! Mudança salva!"
                            break
                        except (ValueError,Exception) as e: err = e

# Função para manejar fotos da extensão
def fotos_extensao(codExt, mode = 'ver'):
    mode_text = f"{Fore.YELLOW}(Fotos da Extensao)" if mode == 'ver' else f"{Fore.YELLOW}(Adicionar Fotos da Extensao)"
    msg = None
    n = 0
    extensao = conEx.find_extensao(codExt)
    err = None
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None
        if err:
            print(f'{Fore.RED}{err}')
            err = None

        find_fotos = conEx.find_fotos(extensao.getCodExt())
        if find_fotos:
            nTotal = math.ceil(len(find_fotos)/PERPAGE)
            msg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()} -- Página {n+1}/{nTotal}"
            line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
        else:
            line = mode_text.rjust(terminal_width)

        print(line)

        choices = []
        if find_fotos:
            show = PERPAGE if (n*PERPAGE + PERPAGE) < len(find_fotos) else len(find_fotos) - n*PERPAGE

            if mode == 'ver':
                for i in range(show):
                    choices.append(Choice(value=i + n*PERPAGE + 4, name=f"{i + 1 + n*PERPAGE}. {find_fotos[i + n*PERPAGE]['descricao']}"))
            else:
                for i in range(show):
                    print(f"{i + 1 + n*PERPAGE}. {find_fotos[i + n*PERPAGE]['descricao']}")
        else:
            print("Ainda não foram inseridas fotos para essa extensão")
        
        if n > 0:
            choices.append(Choice(value=3, name="(<) PREV"))
        if (n*PERPAGE + PERPAGE) < len(find_fotos):
            choices.append(Choice(value=2, name="NEXT (>)"))
        
        if not mode == 'ver':
            choices.append(Choice(value=1, name="Adicionar Foto para essa Extensão"))
        choices.append(Choice(value=0, name="Voltar"))

        choice = inquirer.select(
            message=f'\nEscolha uma ação:',
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return
            case 2: n+=1
            case 3: n-=1
            case 1:
                while(True):
                    os.system('cls')
                    print(Fore.CYAN + banner)
                    print(Fore.CYAN + "=" * terminal_width)
                    print(line)
                    if err:
                        print(f'{Fore.RED}{err}')
                        err = None

                    desc = input("Digite uma descrição da foto: ")            
                    if desc == 'cancelar': 
                        msg = "Foto NÃO foi adicionada"
                        break
                    if len(desc) > 100: err = "Situação ter até 100 caracteres"
                    elif not len(desc) == 0:
                        break
                while(True):
                    os.system('cls')
                    print(Fore.CYAN + banner)
                    print(Fore.CYAN + "=" * terminal_width)
                    print(line)
                    if err:
                        print(f'{Fore.RED}{err}')
                        err = None

                    print(f"Digite uma descrição da foto: {desc}")            
                    fotopath = input("Digite o caminho do arquivo da sua foto: ").strip()
                    if fotopath == 'cancelar': break
                    if not os.path.isfile(fotopath): err = "Arquivo não encontrado. Verifique o caminho e tente novamente."
                    else:
                        try:
                            with open(fotopath, 'rb') as f:
                                fotobin = f.read()
                            conEx.criar_foto(psycopg2.Binary(fotobin),codExt,desc)
                            msg = "Foto adicionada com sucesso!"
                            break
                        except (ValueError,Exception) as e: err = e
            case _:
                try:
                    dados_imagem = find_fotos[choice - 4][3]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(codExt)[1]) as tmp_file:
                        tmp_file.write(dados_imagem)
                        caminho_temp = tmp_file.name

                    msg = f"Imagem salva temporariamente em: {caminho_temp}"
                    sistema = platform.system()
                    if sistema == "Windows":
                        os.startfile(caminho_temp)

                except Exception as e: err = e
