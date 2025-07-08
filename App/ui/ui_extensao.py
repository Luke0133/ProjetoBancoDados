import os,shutil,math,textwrap

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pyfiglet import figlet_format
from colorama import init, Fore
init(autoreset=True)

from classes import extensao as ex
from classes import usuario as user
from controller import con_extensao as conEx
from controller import con_usuario as conUser
from ui import ui_extensao_helpers as uiExH
from ui import ui_extensao_prompt as uiExP

PERPAGE = 4
terminal_width = shutil.get_terminal_size().columns
banner = figlet_format("SGE - Extensoes").rstrip("\n")

# Funções relacionadas a extensoes e suas visualizações
# ui_extensoes
# criar_editar_dados_extensao
# ver_extensao
# inscrever_extensao


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
            case 2: titulo,msg = uiExP.prompt_basico(titulo, mode, 'titulo')
            case 3: tipo,msg = uiExP.prompt_basico(tipo,mode,'tipo')
            case 4: areaTematica,msg = uiExP.prompt_basico(areaTematica,mode,"areaTematica")
            case 5: inicioRealizacao,msg = uiExP.prompt_basico(inicioRealizacao,mode,"inicioRealizacao")
            case 6: fimRealizacao,msg = uiExP.prompt_basico(fimRealizacao,mode,"fimRealizacao")
            case 7: codLocal,msg = uiExP.prompt_local(codLocal,mode)
            case 8: descricao,msg = uiExP.prompt_basico(descricao,mode,"descricao")
            case 9: publicoInternoEstimado,publicoExternoEstimado,publicoInterno,publicoExterno,msg = uiExP.prompt_publico(publicoInternoEstimado,publicoExternoEstimado,publicoInterno,publicoExterno,mode)
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
        
        choices = [Choice(value=1, name="Descrição"), Choice(value=2, name="Público Alvo"), Choice(value=9, name="Ver Situações da Extensão"),Choice(value=11, name="Ver Participantes") , 
                   Choice(value=3, name="Ver Feedbacks"), Choice(value=4, name="Fazer Feedback"),Choice(value=10, name="Ver Fotos")]
        
        if (participacao := conEx.participacao(extensao,usuario))[0]:
            if participacao[1] == 'Coordenador(a)':
                choices.append(Choice(value=5, name="Ver Inscrições"))
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
            case 3: uiExH.ver_feedbacks(extensao)
            case 4: msg = uiExH.fazer_feedback(extensao, usuario)
            case 5: msg = participantes_extensao(extensao,mode='edição')
            case 11: participantes_extensao(extensao,mode='ver')
            case 6: # Editar/Apagar extensão
                existe_extensao, msg = editar_extensao(extensao,id)
                if not existe_extensao: return msg  # Se extensão não existir mais, retorna falso
                else: extensao = conEx.find_extensao(extensao.getCodExt())
            case 7: msg = inscrever_extensao(extensao,usuario)
            case 9: uiExH.situacao_extensao(extensao.getCodExt(), mode = 'ver') # Ver Situações da Extensão
            case 10: uiExH.fotos_extensao(extensao.getCodExt(), mode = 'ver') # Ver Fotos da Extensão
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

# Função para se inscrever em extensão
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


# Função para editar uma extensão
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
            case 2: uiExH.situacao_extensao(codExt,'adicionar')
            case 3: uiExH.fotos_extensao(codExt, 'adicionar') # Ver e Adicionar Fotos da Extensão
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


def participantes_extensao(extensao,mode = 'ver'):
    mode_text = f"{Fore.YELLOW}(Ver Participantes)" if mode == 'ver' else f"{Fore.YELLOW}(Ver Inscrições)"
    err, msg = None, None
    n = 0
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
            

        if mode == 'ver':
            participantes = {'docente' : conEx.find_participacoes_deferido(extensao,user.Docente())}
            participantes['aluno'] = conEx.find_participacoes_deferido(extensao,user.Aluno())
            participantes['pessoa'] = conEx.find_participacoes_deferido(extensao,user.Pessoa())
        else: 
            participantes = {'docente' : conEx.find_participacoes_espera(extensao,user.Docente())}
            participantes['aluno'] = conEx.find_participacoes_espera(extensao,user.Aluno())
            participantes['pessoa'] = conEx.find_participacoes_espera(extensao,user.Pessoa())

        n_aluno = len(participantes['aluno'])
        n_docente = len(participantes['docente'])
        n_pessoa = len(participantes['pessoa'])
        n_participantes = n_aluno + n_docente + n_pessoa
        ok = True if not n_participantes == 0 else False


        if ok:
            nTotal = math.ceil(n_participantes/PERPAGE)
            msg_text = f"{Fore.YELLOW}Extensão {extensao.getCodExt()} -- Página {n+1}/{nTotal}"
            line = msg_text + (" " * (terminal_width - len(mode_text) - len(msg_text))) + mode_text
        else:
            line = mode_text.rjust(terminal_width)

        print(line)

        choices = []
        if ok:
            show = PERPAGE if (n*PERPAGE + PERPAGE) < n_participantes else n_participantes - n*PERPAGE
            if not mode == 'ver':
                for i in range(show):
                    value = i + n*PERPAGE
                    if value < n_docente:
                        participante = participantes['docente'][value]
                        choices.append(Choice(value= value + 4, name=f"{value + 1}. {conUser.get_usuario(participante['coddocente']).getNome():<60}  ||  Docente"))
                    elif value >= n_docente and i < n_docente+ n_aluno:
                        participante = participantes['aluno'][value - n_docente]
                        choices.append(Choice(value=value + 4, name=f"{value + 1}. {conUser.get_usuario(participante['codaluno']).getNome():<60}  ||  Aluno(a)"))
                    elif value >= n_docente+ n_aluno:
                        participante = participantes['pessoa'][value - n_docente - n_aluno]
                        if i == show - 1:    
                            choices.append(Choice(value=value + 4, name=f"{value + 1}. {conUser.get_usuario(participante['codpessoa']).getNome():<60}  ||  Pessoa Externa\n"))
                        else:    
                            choices.append(Choice(value=value + 4, name=f"{value + 1}. {conUser.get_usuario(participante['codpessoa']).getNome():<60}  ||  Pessoa Externa"))
            else:
                for i in range(show):
                    value = i + n*PERPAGE
                    if value < n_docente:
                        participante = participantes['docente'][value]
                        print(f"{value + 1}. {conUser.get_usuario(participante['coddocente']).getNome():<60}  ||  {participante['funcao']}")
                    elif i >= n_docente and i < n_docente+ n_aluno:
                        participante = participantes['aluno'][value - n_docente + n*PERPAGE]
                        print(f"{value + 1}. {conUser.get_usuario(participante['codaluno']).getNome():<60}  ||  {participante['funcao']}")
                    elif i >= n_docente+ n_aluno:
                        participante = participantes['pessoa'][value - n_docente - n_aluno]
                        print(f"{value + 1}. {conUser.get_usuario(participante['codpessoa']).getNome():<60}  ||  {participante['funcao']}")
        else:
            if mode == 'ver': print("Não há ninguém nessa extensão")
            else: print("Não há pedidos de inscrição para essa extensão")

        if n > 0:
            choices.append(Choice(value=3, name="(<) PREV"))
        if (n*PERPAGE + PERPAGE) < n_participantes:
            choices.append(Choice(value=2, name="NEXT (>)"))

        choices.append(Choice(value=0, name="Voltar"))

        query = "Selecione uma ação" if mode == 'ver' else "Escolha alguém para incluir no projeto ou selecione uma ação"
        choice = inquirer.select(
            message= query,
            choices= choices,
            qmark="",
            pointer=">"
        ).execute()

        match choice:
            case 0: return None
            case 2: n+=1
            case 3: n-=1
            case _:
                value = choice - 4
                if value < n_docente:
                    participante = participantes['docente'][value]
                    docente = conUser.get_usuario(participante['coddocente'])
                    try: 
                        conEx.atualizar_participacao(extensao,docente,'Docente Auxiliar','Deferido')
                        return 'Docente aceito na extensão!'
                    except (ValueError,Exception) as e: err = e
                elif value >= n_docente and i < n_docente+ n_aluno:
                    participante = participantes['aluno'][value - n_docente]
                    aluno = conUser.get_usuario(participante['codaluno'])
                    try: 
                        conEx.atualizar_participacao(extensao,aluno,'Aluno(a) Voluntário(a)','Deferido')
                        return 'Aluno(a) aceito(a) na extensão!'
                    except (ValueError,Exception) as e: err = e
                elif value >= n_docente+ n_aluno:
                    participante = participantes['pessoa'][value - n_docente - n_aluno]
                    pessoa = conUser.get_usuario(participante['codpessoa'])
                    try: 
                        conEx.atualizar_participacao(extensao,pessoa,'Pessoa Externa','Deferido')
                        return 'Pessoa aceita na extensão!'
                    except (ValueError,Exception) as e: err = e
