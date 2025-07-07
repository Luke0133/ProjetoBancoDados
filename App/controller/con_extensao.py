from classes import usuario as user
from db import database as db
from classes import extensao as ex

import datetime

def find_extensoes():
    extensoesExistentes = db.get_extensoes()
    for i in range(len(extensoesExistentes)):
        extensoesExistentes[i] = ex.Extensao(extensoesExistentes[i]['codext'], extensoesExistentes[i]['codlocal'], extensoesExistentes[i]['titulo'],
                                             extensoesExistentes[i]['tipoacao'], extensoesExistentes[i]['descricao'], extensoesExistentes[i]['areatematica'],
                                             extensoesExistentes[i]['publicointernoest'], extensoesExistentes[i]['publicoexternoest'], extensoesExistentes[i]['publicointerno'],
                                             extensoesExistentes[i]['publicoexterno'], extensoesExistentes[i]['iniciorealizacao'], extensoesExistentes[i]['fimrealizacao'])   
    return extensoesExistentes

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

def participacao(extensao,usuario):
    if isinstance(usuario, user.Aluno):
        participacao = db.get_funcao_aluno(extensao.getCodExt(),usuario.getMatricula())
    elif isinstance(usuario, user.Docente):
        participacao = db.get_funcao_docente(extensao.getCodExt(),usuario.getMatricula())
    elif isinstance(usuario, user.Pessoa):
        participacao = db.get_funcao_pessoa(extensao.getCodExt(),usuario.getCpf())

    if participacao:
        return (True,participacao[0]['funcao'])
    else:
        return (False,None)

def find_local(codLocal):
    local = db.get_local(codLocal)
    if local:
        local = ex.Local(local[0]['codlocal'], local[0]['nome'],local[0]['tipo'],local[0]['estado'],local[0]['municipio'],local[0]['bairro'],local[0]['complemento'])
    return local

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