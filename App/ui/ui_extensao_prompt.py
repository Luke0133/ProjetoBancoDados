import os,shutil,math,textwrap

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from pyfiglet import figlet_format
from colorama import init, Fore
init(autoreset=True)

from classes import extensao as ex
from classes import domains as dm
from controller import con_extensao as conEx

PERPAGE = 4
terminal_width = shutil.get_terminal_size().columns
banner = figlet_format("SGE - Extensoes").rstrip("\n")

# Funções relacionadas a pedidos (prompts) de usuário para a criação/edição da Extensão
# prompt_basico
# prompt_publico
# prompt_local
# gerar_local


# Prompts básicos para criação/edição de atributos da Extensão
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

# Prompt para a criação/edição de local
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



# Função para gerar local
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
