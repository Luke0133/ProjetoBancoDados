from classes import usuario as user
from db import database as db
from classes import extensao as ex

import datetime

# Cria ou atualiza uma extensão
def criar_atualizar_extensao(extensao, mode = 'criar'):
    if mode == 'criar':
        return db.criar_extensao(extensao.getCodLocal(), extensao.getTitulo(), extensao.getTipoAcao(), extensao.getDescricao(), extensao.getAreaTematica(), 
                          extensao.getPublicoInternoEst(),extensao.getPublicoExternoEst(),extensao.getPublicoInterno(), extensao.getPublicoExterno(),
                          extensao.getInicioRealizacao().getData(), extensao.getFimRealizacao().getData())[0]['codext']
    else:
        db.atualizar_extensao(extensao.getCodExt(), extensao.getCodLocal(), extensao.getTitulo(), extensao.getTipoAcao(), extensao.getDescricao(), extensao.getAreaTematica(), 
                          extensao.getPublicoInternoEst(),extensao.getPublicoExternoEst(),extensao.getPublicoInterno(), extensao.getPublicoExterno(),
                          extensao.getInicioRealizacao().getData(), extensao.getFimRealizacao().getData())
        
# Retorna todas as extensões do sistema
def find_extensoes():
    extensoesExistentes = db.get_extensoes()
    for i in range(len(extensoesExistentes)):
        extensoesExistentes[i] = ex.Extensao(extensoesExistentes[i]['codext'], extensoesExistentes[i]['codlocal'], extensoesExistentes[i]['titulo'],
                                             extensoesExistentes[i]['tipoacao'], extensoesExistentes[i]['descricao'], extensoesExistentes[i]['areatematica'],
                                             extensoesExistentes[i]['publicointernoest'], extensoesExistentes[i]['publicoexternoest'], extensoesExistentes[i]['publicointerno'],
                                             extensoesExistentes[i]['publicoexterno'], extensoesExistentes[i]['iniciorealizacao'], extensoesExistentes[i]['fimrealizacao'])   
    return extensoesExistentes

# Retorna uma extensão
def find_extensao(codext):
    extensao = db.get_extensao(codext)
    if extensao:
        extensao = ex.Extensao(extensao[0]['codext'], extensao[0]['codlocal'], extensao[0]['titulo'],
                                             extensao[0]['tipoacao'], extensao[0]['descricao'], extensao[0]['areatematica'],
                                             extensao[0]['publicointernoest'], extensao[0]['publicoexternoest'], extensao[0]['publicointerno'],
                                             extensao[0]['publicoexterno'], extensao[0]['iniciorealizacao'], extensao[0]['fimrealizacao'])   
    return extensao

# Retorna extensões de um usuário
def find_my_extensoes(usuario):
    # Verifica qual é o tipo do usuário para inseri-lo na respectiva tabela
    if isinstance(usuario, user.Aluno):
        extensoesExistentes = db.get_extensoes_aluno(usuario.getMatricula())
    elif isinstance(usuario, user.Docente):
        extensoesExistentes = db.get_extensoes_docente(usuario.getMatricula())
    elif isinstance(usuario, user.Pessoa):
        extensoesExistentes = db.get_extensoes_pessoa(usuario.getCpf())
    
    for i in range(len(extensoesExistentes)):
        extensoesExistentes[i] = ex.Extensao(extensoesExistentes[i]['codext'], extensoesExistentes[i]['codlocal'], extensoesExistentes[i]['titulo'],
                                             extensoesExistentes[i]['tipoacao'], extensoesExistentes[i]['descricao'], extensoesExistentes[i]['areatematica'],
                                             extensoesExistentes[i]['publicointernoest'], extensoesExistentes[i]['publicoexternoest'], extensoesExistentes[i]['publicointerno'],
                                             extensoesExistentes[i]['publicoexterno'], extensoesExistentes[i]['iniciorealizacao'], extensoesExistentes[i]['fimrealizacao'])   
    return extensoesExistentes

# Retorna informações sobre extensão
def get_info_ext(extensao, usuario = None, mode = 'general'):
    info = db.get_infoextensao(extensao.getCodExt())
    info = {'codext':info[0]['codext'], 'titulo':info[0]['titulo'],'tipoacao':info[0]['tipoacao'],'departamento':info[0]['departamento'], 'coordenador':info[0]['coordenador']}
    
    if not mode == 'general':
        if isinstance(usuario, user.Aluno):
            info['estadoinscricao'] = db.get_funcao_aluno(extensao.getCodExt(),usuario.getMatricula())
        elif isinstance(usuario, user.Docente):
            info['estadoinscricao'] = db.get_funcao_docente(extensao.getCodExt(),usuario.getMatricula())
        elif isinstance(usuario, user.Pessoa):
            info['estadoinscricao'] = db.get_funcao_pessoa(extensao.getCodExt(),usuario.getCpf())
        
        if info['estadoinscricao']:
            info['estadoinscricao'] = info['estadoinscricao'][0]['estadoinscricao']
            
    return info

# Retorna todas as situações de uma extensao
def find_situacoes(codExt):
    situacoes = db.get_situacoes(codExt)
    for i in range(len(situacoes)):
        situacoes[i] = ex.SituacaoExt(situacoes[i]['codext'], situacoes[i]['datasit'], situacoes[i]['horariosit'],situacoes[i]['situacao']) 
    return situacoes

def adicionar_situacao(codExt,situacao):
    db.set_situacao(codExt,situacao)
def apagar_extensao(codExt):
    db.deletar_extensao(codExt)

def criar_foto(foto,codExt,desc):
    db.inserir_foto(codExt,desc,foto)
def find_fotos(codExt):
    return db.get_fotos(codExt)


def participacao(extensao,usuario):
    if isinstance(usuario, user.Aluno):
        participacao = db.get_funcao_aluno(extensao.getCodExt(),usuario.getMatricula())
    elif isinstance(usuario, user.Docente):
        participacao = db.get_funcao_docente(extensao.getCodExt(),usuario.getMatricula())
    elif isinstance(usuario, user.Pessoa):
        participacao = db.get_funcao_pessoa(extensao.getCodExt(),usuario.getCpf())

    if participacao:
        return (True,participacao[0]['funcao'],participacao[0]['estadoinscricao'])
    else:
        return (False,None,None)

def deletar_participacao(extensao,usuario):
    if isinstance(usuario, user.Aluno):
        db.deletar_funcao_aluno(extensao.getCodExt(),usuario.getMatricula())
    elif isinstance(usuario, user.Docente):
        db.deletar_funcao_docente(extensao.getCodExt(),usuario.getMatricula())
    elif isinstance(usuario, user.Pessoa):
        db.deletar_funcao_pessoa(extensao.getCodExt(),usuario.getCpf())
    return

def criar_participacao(extensao,usuario,funcao,situacao):
    if isinstance(usuario, user.Aluno):
        db.set_funcao_aluno(extensao.getCodExt(),usuario.getMatricula(),funcao,situacao)
    elif isinstance(usuario, user.Docente):
        db.set_funcao_docente(extensao.getCodExt(),usuario.getMatricula(),funcao,situacao)
    elif isinstance(usuario, user.Pessoa):
        db.set_funcao_pessoa(extensao.getCodExt(),usuario.getCpf(),funcao,situacao)
    return

def atualizar_participacao(extensao,usuario,funcao,situacao):
    if isinstance(usuario, user.Aluno):
        db.update_funcao_aluno(extensao.getCodExt(),usuario.getMatricula(),funcao,situacao)
    elif isinstance(usuario, user.Docente):
        db.update_funcao_docente(extensao.getCodExt(),usuario.getMatricula(),funcao,situacao)
    elif isinstance(usuario, user.Pessoa):
        db.update_funcao_pessoa(extensao.getCodExt(),usuario.getCpf(),funcao,situacao)
    return

def find_participacoes_deferido(extensao,usuario):
    codExt = extensao.getCodExt()
    if isinstance(usuario, user.Aluno):
        return db.get_funcoes_aluno_deferido(codExt)
    elif isinstance(usuario, user.Docente):
        return db.get_funcoes_docente_deferido(codExt)
    elif isinstance(usuario, user.Pessoa):
        return db.get_funcoes_pessoa_deferido(codExt)
    return None

def find_participacoes_espera(extensao,usuario):
    codExt = extensao.getCodExt()
    if isinstance(usuario, user.Aluno):
        return db.get_funcoes_aluno_espera(codExt)
    elif isinstance(usuario, user.Docente):
        return db.get_funcoes_docente_espera(codExt)
    elif isinstance(usuario, user.Pessoa):
        return db.get_funcoes_pessoa_espera(codExt)
    return None

def find_local(codLocal):
    local = db.get_local(codLocal)
    if local:
        local = ex.Local(local[0]['codlocal'], local[0]['nome'],local[0]['tipo'],local[0]['estado'],local[0]['municipio'],local[0]['bairro'],local[0]['complemento'])
    return local

def find_locais():
    locais = db.get_locais()
    for i in range(len(locais)):
        locais[i] = ex.Local(locais[i]['codlocal'], locais[i]['nome'], locais[i]['tipo'],locais[i]['estado'], 
                             locais[i]['municipio'], locais[i]['bairro'],locais[i]['complemento'])
    return locais

def criar_local(local:ex.Local):
    if local.getComplemento():
        return db.create_local_complemento(local.getNome(),local.getTipo(),local.getEstado(),local.getMunicipio(),local.getBairro(),local.getComplemento())[0]
    else:
        return db.create_local(local.getNome(),local.getTipo(),local.getEstado(),local.getMunicipio(),local.getBairro())[0]

def find_feedbacks(codExt):
    feedbacks = db.get_feedbacks(codExt)
    for i in range(len(feedbacks)):
        funcao = feedbacks[i]['funcao'] if feedbacks[i]['funcao'] else "Não faz parte da extensão"
        feedbacks[i] = ex.Feedback(feedbacks[i]['codfeedback'], feedbacks[i]['datafeedback'], feedbacks[i]['comentario'], 
                                   feedbacks[i]['nota'], feedbacks[i]['nome'], funcao)        
    return feedbacks

def criar_feedback(extensao, nota, comentario, usuario):
    codFeedback = db.criar_feedback(extensao.getCodExt(),nota,comentario)[0]
    
    if isinstance(usuario, user.Aluno):
        db.conectar_feedback_aluno(codFeedback,usuario.getMatricula())
    elif isinstance(usuario, user.Docente):
        db.conectar_feedback_docente(codFeedback,usuario.getMatricula())
    elif isinstance(usuario, user.Pessoa):
        db.conectar_feedback_pessoa(codFeedback,usuario.getCpf())
    return


def criar_coordenador(codDocente,codExt):
    db.set_funcao_docente(codExt,codDocente,"Coordenador(a)","Deferido")