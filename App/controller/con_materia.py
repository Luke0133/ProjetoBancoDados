from db import database as db
from classes import materia as mt


def find_curso(id):
    curso = db.get_curso(id)
    if curso:
        return mt.Curso(curso[0]['codcurso'],curso[0]['nome'])
    else:
        raise ValueError("Curso não encontrado")

def find_dep(id):
    dep = db.get_dep(id)
    if dep:
        return mt.Departamento(dep[0]['coddep'],dep[0]['nome'],dep[0]['sigla'])
    else:
        raise ValueError("Departamento não encontrado")

def find_materia(id):
    mat = db.get_materia(id)
    if mat:
        return mt.Materia(mat[0]['codmateria'],mat[0]['nome'],mat[0]['sigla'])
    else:
        raise ValueError("Matéria não encontrada")