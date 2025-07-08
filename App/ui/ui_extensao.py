import os,shutil,math,textwrap,psycopg2,tempfile,platform

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pyfiglet import figlet_format
from colorama import init, Fore
init(autoreset=True)

from classes import extensao as ex
from classes import usuario as user
from classes import domains as dm
from controller import con_extensao as conEx
from controller import con_usuario as conUser
from db import database as sql

PERPAGE = 4
terminal_width = shutil.get_terminal_size().columns
banner = figlet_format("SGE - Extensoes").rstrip("\n")

# Funções relacionadas a extensoes e suas visualizações
# ui_extensoes
# criar_editar_dados_extensao
# ver_extensao

# prompt_basico
# prompt_publico


# Interface principal
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
            case 1: criar_editar_dados_extensao(codDocente = usuario.getMatricula(),mode = 'criar')
            case _: msg = ver_extensao(extensoes[choice - 4], usuario, mode)

# Função chamada para criar uma extensão ou editar seus dados
def criar_editar_dados_extensao(codDocente = None,codExt = None,mode = 'criar'):
    
    mode_text = f"{Fore.YELLOW}(Criação de Extensão)" if mode == 'criar' else f"{Fore.YELLOW}(Edição da Extensão)"
    err, msg = None, None
    
    if mode == 'criar':
        titulo,codLocal,tipo,descricao,areaTematica,publicoInternoEstimado, = None, None, None, None, None, None
        publicoExternoEstimado,publicoInterno,publicoExterno,inicioRealizacao,fimRealizacao = None, None, None, None, None
    else:
        extensao = conEx.find_extensao(codExt)
        titulo = extensao.getTitulo()
        codLocal = extensao.getCodLocal()
        tipo = extensao.getTipoAcao()
        descricao = extensao.getDescricao()
        areaTematica = extensao.getAreaTematica()
        publicoInternoEstimado = extensao.getPublicoInternoEst()
        publicoExternoEstimado = extensao.getPublicoExternoEst()
        publicoInterno = extensao.getPublicoInterno()
        publicoExterno = extensao.getPublicoExterno()
        inicioRealizacao = extensao.getInicioRealizacao() 
        fimRealizacao = extensao.getFimRealizacao()
    
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        print(mode_text.rjust(terminal_width))
        if err:
            print(f'{Fore.RED}{err}')
            err = None
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None

        if codLocal:
            local = conEx.find_local(codLocal)
            complemento_inquirer = f' || {local.getComplemento()}' if local.getComplemento() else ''
            local_inquirer = f"Local: {local.getNome()} ({local.getTipo()}) -- {local.getEstado()} || {local.getMunicipio()} || {local.getBairro()}" + complemento_inquirer
        else:
            local_inquirer = "NÃO FORNECIDO [CAMPO OBRIGATÓRIO]"

        choices = [Choice(value=2, name=f"Título: {titulo if titulo else 'NÃO FORNECIDO [CAMPO OBRIGATÓRIO]'}")]
        if mode == 'criar':
            choices.append(Choice(value=3, name=f"Tipo de Ação: {tipo if tipo else 'NÃO FORNECIDO [CAMPO OBRIGATÓRIO]'}"))
        choices.extend([Choice(value=4, name=f"Área temática: {areaTematica if areaTematica else 'NÃO FORNECIDA [CAMPO OBRIGATÓRIO]'}"),
                      Choice(value=5, name=f"Data de Início da realização: {inicioRealizacao if inicioRealizacao else 'NÃO FORNECIDA [CAMPO OBRIGATÓRIO]'}"),
                      Choice(value=6, name=f"Data de Fim da realização: {fimRealizacao if fimRealizacao else 'NÃO FORNECIDO [CAMPO OBRIGATÓRIO]'}"),
                      Choice(value=7, name=f"Local: {local_inquirer}"),
                      Choice(value=8, name=f"Descrição: {'SELECIONE PARA VER/ALTERAR' if descricao else 'NÃO FORNECIDA [CAMPO OBRIGATÓRIO]'}"),
                      Choice(value=9, name=f"Público Alvo: {'SELECIONE PARA VER/ALTERAR' if publicoExternoEstimado and publicoInternoEstimado else 'INCOMPLETO [CAMPO OBRIGATÓRIO]' if publicoExternoEstimado or publicoInternoEstimado else 'NÃO FORNECIDO [CAMPO OBRIGATÓRIO]'}\n"),
                      Choice(value=1, name=f"Salvar {'criação' if mode == 'criar' else 'edições'} e voltar"),
                      Choice(value=0, name=f"Voltar (cancelar processo de {mode})")])
        
        choice = inquirer.select(
            message=f'Selecione um campo para escrever ou uma ação:',
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return f"Processo de {'criação' if mode == 'criar' else 'edição'} cancelado"
            case 2: titulo,msg = prompt_basico(titulo, mode, 'titulo')
            case 3: tipo,msg = prompt_basico(tipo,mode,'tipo')
            case 4: areaTematica,msg = prompt_basico(areaTematica,mode,"areaTematica")
            case 5: inicioRealizacao,msg = prompt_basico(inicioRealizacao,mode,"inicioRealizacao")
            case 6: fimRealizacao,msg = prompt_basico(fimRealizacao,mode,"fimRealizacao")
            case 7: codLocal,msg = prompt_local(codLocal,mode)
            case 8: descricao,msg = prompt_basico(descricao,mode,"descricao")
            case 9: publicoInternoEstimado,publicoExternoEstimado,publicoInterno,publicoExterno,msg = prompt_publico(publicoInternoEstimado,publicoExternoEstimado,publicoInterno,publicoExterno,mode)
            case 1:
                if titulo and tipo and areaTematica and inicioRealizacao and fimRealizacao and codLocal and descricao and publicoInternoEstimado and publicoExternoEstimado:
                    extensao = ex.Extensao(codExt,codLocal, titulo, tipo, descricao, areaTematica, publicoInternoEstimado,
                                           publicoExternoEstimado,publicoInterno, publicoExterno, inicioRealizacao, fimRealizacao)
                    try: 
                        codExt = conEx.criar_atualizar_extensao(extensao, mode)
                        if mode == 'criar':
                            conEx.criar_coordenador(codDocente,codExt)
                        return f"Extensão {'criada' if mode == 'criar' else 'editada'} com sucesso!"
                    except (ValueError,Exception) as e: err = e
                else: err = "Nem todos os campos obrigatórios foram fornecidos!"

# Função para visualizar extensao
def ver_extensao(extensao, usuario, mode = 'general'):
    if isinstance(usuario, user.Aluno):
        id = usuario.getMatricula()
    elif isinstance(usuario, user.Docente):
        id = usuario.getMatricula()
    elif isinstance(usuario, user.Pessoa):
        id = usuario.getCpf().get()

    mode_text = f"{Fore.YELLOW}(Visualização da Extensão)"
    msg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()}"
    line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
    msg = None
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
        print(f'| Data da realização: {extensao.getInicioRealizacao()} - {extensao.getFimRealizacao()}')
        print(f'| Local: {local.getNome()} ({local.getTipo()}) -- {local.getEstado()} || {local.getMunicipio()} || {local.getBairro()}',end='')
        if local.getComplemento():
            print(f' || {local.getComplemento()}\n')
        else:
            print('\n')
        
        choices = [Choice(value=1, name="Descrição"), Choice(value=2, name="Público Alvo"), Choice(value=9, name="Ver Situações da Extensão"), Choice(value=3, name="Ver Feedbacks"),
                   Choice(value=4, name="Fazer Feedback"),Choice(value=10, name="Ver Fotos")]
        
        if (participacao := conEx.participacao(extensao,usuario))[0]:
            if participacao[1] == 'Coordenador(a)':
                choices.append(Choice(value=6, name="Editar/Apagar Extensão"))
            elif participacao[1]:
                choices.append(Choice(value=8, name="Sair da Extensão"))
            else: choices.append(Choice(value=7, name="Inscrever-se"))
        else:
            choices.append(Choice(value=7, name="Inscrever-se"))

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
            case 6: # Editar/Apagar extensão
                existe_extensao, msg = editar_extensao(extensao,id)
                if not existe_extensao: return msg  # Se extensão não existir mais, retorna falso
                else: extensao = conEx.find_extensao(extensao.getCodExt())
            case 7: msg = inscrever_extensao(extensao,usuario)
            case 9: situacao_extensao(extensao.getCodExt(), mode = 'ver') # Ver Situações da Extensão
            case 10: fotos_extensao(extensao.getCodExt(), mode = 'ver') # Ver Fotos da Extensão
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
            
            case 8: 
                newmode_text = f"{Fore.YELLOW}(Sair da Extensão)"
                newmsg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()} -- Digite cancelar para voltar"
                newline = newmsg_text + (" " * (terminal_width - len(newmode_text) - len(newmsg_text))) + newmode_text

                err = None
                while(True):
                    while(True):
                        os.system('cls')
                        print(Fore.CYAN + banner)
                        print(Fore.CYAN + "=" * terminal_width)
                        print(newline)
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
                        print(f'Insira sua senha atual: {senha}\n\n{Fore.RED}{'Você irá sair desta Extensão e não constará mais como participante!'}')
                        
                        choice = inquirer.select(
                            message=f"Você realmente deseja sair desta extensão?",
                            choices= [
                            Choice(value=2, name="Não"),
                            Choice(value=1, name="Sim")],
                            qmark="",
                            pointer=">"
                        ).execute()
                        
                        match choice:
                            case 1: 
                                try: 
                                    conEx.deletar_participacao(extensao,usuario)
                                    return 'Inscrição cancelada com sucesso!'
                                except (ValueError,Exception) as e:
                                    print(f'\nNão foi possível sair da extensão. Erro: {Fore.RED}{e}')
                                    input("Pressione ENTER para voltar ao menu de Visualização da Extensão")
                                    return False
                            case 2:
                                print(f'\nVocê não saiu da extensão. Processo cancelado')
                                input("Pressione ENTER para voltar ao menu de Visualização da Extensão") 
                                return False
                            case _: pass
         
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


            




# Pede para o usuário um título, tipo
def prompt_basico(valor = None, mode = 'criar', prompt = 'titulo'):
    mode_text = f"{Fore.YELLOW}(Criação da Extensão)" if mode == 'criar' else f"{Fore.YELLOW}(Edição da Extensão)"
    msg_text = f"{Fore.YELLOW}Digite cancelar para voltar"
    line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
    err = None
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        print(line)
        if err:
            print(f'{Fore.RED}{err}')
            err = None

        match prompt:
            case 'titulo':
                if (valor):
                    print(f"Titulo {'fornecido' if mode == 'criar' else 'atual'}: {valor}\n")
                else:
                    print(f"Você ainda não definiu um título\n")

                input_text = input(f"Digite um {'novo' if valor else ''} título: ")
                if input_text == 'cancelar': return (valor, 'Nenhum valor alterado')
                if len(input_text) == 0: err = 'Forneça um título'
                else: return (input_text, f'Título {'alterado' if valor else 'fornecido'} com sucesso!')
            
            case 'tipo':
                if (valor):
                    print(f"Tipo de Ação {'fornecido' if mode == 'criar' else 'atual'}: {valor}\n")
                else:
                    print(f"Você ainda não definiu um tipo de ação\n")

                choice = inquirer.select(
                    message=f'Selecione qual é o tipo de ação da sua extensão:',
                    choices= [Choice(value=1, name=f"Curso"),
                              Choice(value=2, name=f"Evento"),
                              Choice(value=3, name=f"Projeto"),
                              Choice(value=0, name=f"Voltar (cancelar processo de {mode})")],
                    qmark="",
                    pointer=">"
                ).execute()
                
                match choice:
                    case 0: return (valor, 'Nenhum valor alterado')
                    case 1: return ("Curso", f'Tipo de Ação {'alterado' if valor else 'fornecido'} com sucesso!')
                    case 2: return ("Evento", f'Tipo de Ação {'alterado' if valor else 'fornecido'} com sucesso!')
                    case 3: return ("Projeto", f'Tipo de Ação {'alterado' if valor else 'fornecido'} com sucesso!')
                    case _: err = "Nenhum tipo foi selecionado"
            
            case 'areaTematica':
                if (valor):
                    print(f"Área temática {'fornecida' if mode == 'criar' else 'atual'}: {valor}\n")
                else:
                    print(f"Você ainda não definiu uma área temática\n")

                input_text = input(f"Digite uma {'nova' if valor else ''} área temática para a sua extensão: ")
                if input_text == 'cancelar': return (valor, 'Nenhum valor alterado')
                if len(input_text) == 0: err = 'Forneça uma área temática'
                else: return (input_text,f'Área temática {'alterada' if valor else 'fornecida'} com sucesso!')
            
            case 'inicioRealizacao' | 'fimRealizacao':
                label = 'início' if prompt == 'inicioRealizacao' else 'fim'
                if (valor):
                    print(f"Data de {label} da realização {'fornecida' if mode == 'criar' else 'atual'}: {valor}\n")
                else:
                    print(f"Você ainda não definiu uma data de {label} da realização\n")

                input_text = input(f"Digite uma {'nova' if valor else ''} data de {label} da realização para a sua extensão: ")
                if input_text == 'cancelar': return (valor, 'Nenhum valor alterado')
                if len(input_text) == 0: err = 'Forneça uma data'
                else: 
                    try: 
                        data = dm.Data()
                        data.setData(input_text)
                        return (data,f'Data de {label} da realização {'alterada' if valor else 'fornecida'} com sucesso!')
                    except ValueError as e:
                        err = e
                
            case 'descricao':
                if (valor):
                    print(textwrap.fill(f"Descrição {'fornecida' if mode == 'criar' else 'atual'}: {valor}", width=terminal_width))
                else:
                    print(f"Você ainda não definiu uma descrição\n")

                input_text = input(f"\nDigite uma {'nova' if valor else ''} descrição para a sua extensão: ")
                if input_text == 'cancelar': return (valor, 'Nenhum valor alterado')
                if len(input_text) == 0: err = 'Forneça uma descrição'
                else: return (input_text,f'Descrição {'alterada' if valor else 'fornecida'} com sucesso!')

            case "paInt" | "paExt": 
                label = 'interno' if prompt == 'paInt' else 'externo'
                if (valor):
                    print(f"Público-Alvo {label} {'fornecido' if mode == 'criar' else 'atual'}: {valor}\n")
                else:
                    print(f"Você ainda não definiu um público-alvo {label}\n")

                input_text = input(f"Digite um {'novo' if valor else ''} público-alvo {label} para a sua extensão: ")
                if input_text == 'cancelar': return (valor, 'Nenhum valor alterado')
                if len(input_text) == 0: err = 'Forneça um público-alvo'
                else: return (input_text,f'Público-Alvo {label} {'alterado' if valor else 'fornecido'} com sucesso!')

            case "peInt" | "peExt": 
                label = 'interno' if prompt == 'peInt' else 'externo'
                if (valor):
                    print(f"Público-Alvo {label} estimado {'fornecido' if mode == 'criar' else 'atual'}: {valor}\n")
                else:
                    print(f"Você ainda não definiu um público-alvo {label} estimado\n")

                input_text = input(f"Digite um {'novo' if valor else ''} público-alvo {label} estimado para a sua extensão: ")
                if input_text == 'cancelar': return (valor, 'Nenhum valor alterado')
                if len(input_text) == 0: err = "Forneça um valor numérico para o público-alvo"
                else:
                    if input_text.isdigit(): return (int(input_text),f'Público-Alvo {label} estimado {'alterado' if valor else 'fornecido'} com sucesso!')
                    else: err = "Forneça um valor numérico para o público-alvo"


# Prompt para receber informações sobre o público
def prompt_publico(publicoInternoEstimado,publicoExternoEstimado,publicoInterno,publicoExterno,mode = 'criar'):
    mode_text = f"{Fore.YELLOW}(Criação de Extensão)" if mode == 'criar' else f"{Fore.YELLOW}(Edição da Extensão)"
    err, msg = None, None
    n_publicoInternoEstimado,n_publicoInterno = publicoInternoEstimado, publicoInterno
    n_publicoExternoEstimado,n_publicoExterno = publicoExternoEstimado, publicoExterno
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        print(mode_text.rjust(terminal_width))
        if err:
            print(f'{Fore.RED}{err}')
            err = None
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None

        choice = inquirer.select(
            message=f'Selecione um campo para escrever ou uma ação (se não houver indicação, não é obrigatório o preenchimento):',
            choices= [Choice(value=2, name=f"Público Interno Estimado: {n_publicoInternoEstimado if n_publicoInternoEstimado else 'NÃO FORNECIDO [CAMPO OBRIGATÓRIO]'}"),
                      Choice(value=3, name=f"Público-Alvo Interno: {n_publicoInterno if n_publicoInterno else ''}"),
                      Choice(value=4, name=f"Público Externo Estimado: {n_publicoExternoEstimado if n_publicoExternoEstimado else 'NÃO FORNECIDO [CAMPO OBRIGATÓRIO]'}"),
                      Choice(value=5, name=f"Público-Alvo Externo: {n_publicoExterno if n_publicoExterno else ''}\n"),
                      Choice(value=1, name=f"Salvar alterações"),
                      Choice(value=0, name=f"Voltar (cancelar alterações)")],
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return (publicoInternoEstimado,publicoExternoEstimado,publicoInterno,publicoExterno,'Nenhum valor alterado')
            case 1: return (n_publicoInternoEstimado,n_publicoExternoEstimado,n_publicoInterno,n_publicoExterno,'Valores alterados com sucesso')
            case 2: n_publicoInternoEstimado,msg = prompt_basico(n_publicoInternoEstimado, mode, 'peInt')
            case 3: n_publicoInterno,msg = prompt_basico(n_publicoInterno,mode,'paInt')
            case 4: n_publicoExternoEstimado,msg = prompt_basico(n_publicoExternoEstimado,mode,"peExt")
            case 5: n_publicoExterno,msg = prompt_basico(n_publicoExterno,mode,"paExt")

def prompt_local(codLocal,mode='criar'):
    mode_text = f"{Fore.YELLOW}(Criação de Extensão - Locais)" if mode == 'criar' else f"{Fore.YELLOW}(Edição da Extensão - Locais)"
    msg = None
    n = 0
    
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None

        locais = conEx.find_locais()
        if locais:
            nTotal = math.ceil(len(locais)/PERPAGE)
            msg_text = f"{Fore.YELLOW}Página {n+1}/{nTotal}"
            line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
        else:
            line = mode_text.rjust(terminal_width)
        print(line)
        
        if codLocal:
            local_fornecido = conEx.find_local(codLocal)
            complemento_atual = f' || {local_fornecido.getComplemento()}' if local_fornecido.getComplemento() else ''
            local_atual = f"Local: {local_fornecido.getNome()} ({local_fornecido.getTipo()}) -- {local_fornecido.getEstado()} || {local_fornecido.getMunicipio()} || {local_fornecido.getBairro()}" + complemento_atual
            print(f"Local {'fornecido' if mode == 'criar' else 'atual'}: {local_atual}")
        else:
            print(f"Você ainda não definiu um local\n")

        choices = []
        if locais:
            show = PERPAGE if (n*PERPAGE + PERPAGE) < len(locais) else len(locais) - n*PERPAGE
            for i in range(show):
                complemento_inquirer = f' || {locais[i + n*PERPAGE].getComplemento()}' if locais[i + n*PERPAGE].getComplemento() else ''
                local_inquirer = f"Local: {locais[i + n*PERPAGE].getNome()} ({locais[i + n*PERPAGE].getTipo()}) -- {locais[i + n*PERPAGE].getEstado()} || {locais[i + n*PERPAGE].getMunicipio()} || {locais[i + n*PERPAGE].getBairro()}" + complemento_inquirer
                if i == show - 1:
                    local_inquirer = local_inquirer + '\n'
                choices.append(Choice(value=i + n*PERPAGE + 4, name=f"{i + 1 + n*PERPAGE}. {local_inquirer}"))
        else:
            print("Ainda não existem locais. Crie algum para a sua extensão")

        if n > 0:
            choices.append(Choice(value=3, name="(<) PREV"))
        if (n*PERPAGE + PERPAGE) < len(locais):
            choices.append(Choice(value=2, name="NEXT (>)"))
        
        choices.extend([Choice(value=1, name="Criar Local Para Extensão"),Choice(value=0, name="Voltar")])

        choice = inquirer.select(
            message=f'Selecione um local para a sua extensão ou uma das ações abaixo:',
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return (None,None)
            case 2: n+=1
            case 3: n-=1
            case 1: 
                resultado, status = gerar_local(mode)
                if (status): return (resultado,"Local escolhido com sucesso!") 
            case _: return(locais[choice - 4].getCodLocal(),"Local escolhido com sucesso!")
    
def gerar_local(mode = 'criar'):
    mode_text = f"{Fore.YELLOW}(Criação de Extensão - Locais)" if mode == 'criar' else f"{Fore.YELLOW}(Edição da Extensão - Locais)"
    msg_text = f"{Fore.YELLOW}Digite cancelar para voltar"
    line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
    err = None
    while(True):
        local = ex.Local()
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            if err:
                print(f'{Fore.RED}{err}')
                err = None

            nome = input("Digite o nome do Local: ")            
            if nome == 'cancelar': return (None,False)
            if len(nome) > 100: err = "Nome do local deve ter até 100 caracteres"
            elif not len(nome) == 0:
                local.setNome(nome)
                break
        
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            if err:
                print(f'{Fore.RED}{err}')
                err = None

            print(f"Digite o nome do Local: {nome}")            
            choice = inquirer.select(
                    message=f'Selecione qual é o tipo do local da sua extensão:',
                    choices= [Choice(value=1, name=f"Campus"),
                              Choice(value=2, name=f"Escola"),
                              Choice(value=3, name=f"Outro"),
                              Choice(value=0, name=f"Cancelar")],
                    qmark="",
                    pointer=">"
                ).execute()
            tipo = None
            match choice:
                case 0: return (tipo,False)
                case 1: tipo = 'Campus'
                case 2: tipo = 'Escola'
                case 3: tipo = 'Outro'
                case _: err = "Nenhum tipo foi selecionado"
            
            if tipo: 
                local.setTipo(tipo)
                break
        
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            if err:
                print(f'{Fore.RED}{err}')
                err = None
            
            print(f"Digite o nome do Local: {nome}") 
            print(f"Selecione qual é o tipo do local da sua extensão: {tipo}") 
            estado = input("Digite o estado em que ocorrerá a extensão (sigla de 2 caracteres): ")            
            if estado == 'cancelar': return (None,False)
            if len(estado) != 2: err = "Estado é uma sigla de 2 caracteres"
            else:
                local.setEstado(estado)
                break
        
        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            if err:
                print(f'{Fore.RED}{err}')
                err = None
            
            print(f"Digite o nome do Local: {nome}") 
            print(f"Selecione qual é o tipo do local da sua extensão: {tipo}") 
            print(f"Digite o estado em que ocorrerá a extensão (sigla de 2 caracteres): {estado}")  

            municipio = input("Digite o municipio em que ocorrerá a extensão: ")           
            if municipio == 'cancelar': return (None,False)
            if len(municipio) > 50: err = "Município deve ter até 50 caracteres"
            elif not len(municipio) == 0:
                local.setMunicipio(municipio)
                break

        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            if err:
                print(f'{Fore.RED}{err}')
                err = None
            
            print(f"Digite o nome do Local: {nome}") 
            print(f"Selecione qual é o tipo do local da sua extensão: {tipo}") 
            print(f"Digite o estado em que ocorrerá a extensão (sigla de 2 caracteres): {estado}")  
            print(f"Digite o municipio em que ocorrerá a extensão: {municipio}")  

            bairro = input("Digite o bairro em que ocorrerá a extensão: ")           
            if bairro == 'cancelar': return (None,False)
            if len(bairro) > 50: err = "Bairro deve ter até 50 caracteres"
            elif not len(bairro) == 0:
                local.setBairro(bairro)
                break

        while(True):
            os.system('cls')
            print(Fore.CYAN + banner)
            print(Fore.CYAN + "=" * terminal_width)
            print(line)
            if err:
                print(f'{Fore.RED}{err}')
                err = None
            
            print(f"Digite o nome do Local: {nome}") 
            print(f"Selecione qual é o tipo do local da sua extensão: {tipo}") 
            print(f"Digite o estado em que ocorrerá a extensão (sigla de 2 caracteres): {estado}")  
            print(f"Digite o municipio em que ocorrerá a extensão: {municipio}")  
            print(f"Digite o bairro em que ocorrerá a extensão: {bairro}") 

            comp = input("Digite um complemento, caso necesário (pressione ENTER e deixe vazio caso não haja): ")           
            if comp == 'cancelar': return (None,False)
            if len(comp) > 100: err = "Complemento deve ter até 100 caracteres"
            else:
                if not len(comp) == 0:
                    local.setComplemento(comp)
                else:
                    local.setComplemento(None)
                try:
                    return (conEx.criar_local(local),True)
                except (Exception,ValueError) as e:
                    err = e 
                    break

def inscrever_extensao(extensao,usuario):
    mode_text = f"{Fore.YELLOW}(Realização de Inscrição)"
    msg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()}"
    line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
    err = None
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        print(line)
        if err:
            print(f'{Fore.RED}{err}')
            err = None
            
        choices = []
        participacao = conEx.participacao(extensao,usuario)
        if participacao[2] == 'Em Espera':
            print('Você já enviou um pedido de inscrição e este está em análise')
            choices.append(Choice(value=2, name="Cancelar Inscrição"))
        elif participacao[2] == 'Indeferido':
            print('Seu pedido foi INDEFERIDO!! Se achar necessário, inscreva-se novamente')
            choices.append(Choice(value=3, name="Re-enviar Inscrição"))
            choices.append(Choice(value=2, name="Cancelar Inscrição"))
        else:
            choices.append(Choice(value=4, name="Fazer Inscrição"))
        
        choices.append(Choice(value=0, name="Voltar"))

        choice = inquirer.select(
            message=f'Selecione uma ação:',
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return None
            case 2: 
                try: 
                    conEx.deletar_participacao(extensao,usuario)
                    return 'Inscrição cancelada com sucesso!'
                except (ValueError,Exception) as e: err = e
            case 3: 
                try: 
                    conEx.atualizar_participacao(extensao,usuario,None,'Em Espera')
                    return 'Inscrição re-enviada com sucesso!'
                except (ValueError,Exception) as e: err = e
            case 4: 
                try: 
                    conEx.criar_participacao(extensao,usuario,None,'Em Espera')
                    return 'Inscrição enviada com sucesso!'
                except (ValueError,Exception) as e: err = e
            case _: pass

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



def editar_extensao(extensao,id):
    mode_text = f"{Fore.YELLOW}(Editar Extensão)"
    msg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()}"
    line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
    msg = None
    while(True):
        os.system('cls')
        print(Fore.CYAN + banner)
        print(Fore.CYAN + "=" * terminal_width)
        print(line)
        if msg:
            print(f'{Fore.LIGHTGREEN_EX}{msg}')
            msg = None
            

        choice = inquirer.select(
            message=f'Selecione uma ação:',
            choices= [Choice(value=1, name="Editar Extensão"),
                      Choice(value=2, name="Adicionar Situação de Extensão"),
                      Choice(value=3, name="Adicionar Fotos da Extensão"),
                      Choice(value=4, name="Apagar Extensão"),
                        Choice(value=0, name="Voltar")],
            qmark="",
            pointer=">"
        ).execute()

        
        codExt = extensao.getCodExt()
        match choice:
            case 0: return (True,None)
            case 1:     
                criar_editar_dados_extensao(codExt = codExt,mode = 'editar') 
                extensao = conEx.find_extensao(codExt) 
            case 2: situacao_extensao(codExt,'adicionar')
            case 3: fotos_extensao(codExt, 'adicionar') # Ver e Adicionar Fotos da Extensão
            case 4: 
                newmode_text = f"{Fore.YELLOW}(Apagar da Extensão)"
                newmsg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()} -- Digite cancelar para voltar"
                newline = newmsg_text + (" " * (terminal_width - len(newmode_text) - len(newmsg_text))) + newmode_text

                err = None
                while(True):
                    while(True):
                        os.system('cls')
                        print(Fore.CYAN + banner)
                        print(Fore.CYAN + "=" * terminal_width)
                        print(newline)
                        if err:
                            print(f'{Fore.RED}{err}')
                            err = None
                        senha = input("Insira sua senha: ")
                        if senha == 'cancelar': break
                        if not len(senha) == 0:
                            try:
                                conUser.con_login(id,senha)
                                break
                            except ValueError as e:
                                err = "Senha incorreta"
                    if senha == 'cancelar': break
                    while(True):
                        os.system('cls')
                        print(Fore.CYAN + banner)
                        print(Fore.CYAN + "=" * terminal_width)
                        print(line)
                        print(f'Insira sua senha atual: {senha}\n\n{Fore.RED}{'Você deletar esta Extensão e todas as informações a ela relacionadas!'}')
                        
                        choice = inquirer.select(
                            message=f"Você realmente quer DELETAR esta extensão?",
                            choices= [
                            Choice(value=2, name="Não"),
                            Choice(value=1, name="Sim")],
                            qmark="",
                            pointer=">"
                        ).execute()
                        
                        match choice:
                            case 1: 
                                try: 
                                    conEx.apagar_extensao(codExt)
                                    return (False,'Extensão e todas as suas informações deletadas com sucesso!')
                                except (ValueError,Exception) as e:
                                    print(f'\nNão foi possível deletar extensão. Erro: {Fore.RED}{e}')
                                    input("Pressione ENTER para voltar ao menu de Edição da Extensão")
                                    break
                            case 2:
                                print(f'\nVocê NÃO deletou a extensão. Processo cancelado')
                                input("Pressione ENTER para voltar ao menu de Edição da Extensão") 
                                break
                            case _: pass
            case _: pass
