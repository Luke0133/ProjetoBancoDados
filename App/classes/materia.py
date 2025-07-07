from classes.domains import *

# Entidades relacionadas a matérias
# - Materia
# - Curso
# - Departamento

class Materia:
    def __init__(self, codMateria = None, nome = None, sigla = None):
        self.nome = nome
        self.codMateria = codMateria
        self.sigla = sigla
    
    def getAll(self):
        return [self.codMateria, self.nome,self.sigla]
    def getNome(self):
        return self.nome
    def getCodMateria(self):
        return self.codMateria
    def getSigla(self):
        return self.sigla
    
    def setNome(self, nome):
        self.nome = nome
    
    def setCodMateria(self, cod):
        if int(cod) == cod and cod > 0:
            self.codMateria = cod
        else:
            print("Codigo deve ser um inteiro positivo")
            
    def setSigla(self,aux):
        self.sigla = aux
        
    def __repr__(self):
        return f"{self.codMateria} - {self.nome}"
    

class Curso:
    def __init__(self, codCurso=None, nome=None):
        self.codCurso = codCurso
        self.nome = nome

    def get(self):
        return [self.codCurso, self.nome]
    def getCodCurso(self):
        return self.codCurso
    def getNome(self):
        return self.nome

    def setNome(self,aux):
        self.nome = aux

    def setCodCurso(self,cod):
        if int(cod) == cod and cod > 0:
            self.codCurso = cod
        else:
            print("Codigo deve ser um inteiro positivo")

    def __repr__(self):
        return f"{self.codCurso} - {self.nome}"
    
class Departamento:
    def __init__(self, codDep=None, nome=None, sigla = None):
        self.codDep = codDep
        self.nome = nome
        self.sigla = sigla

    def get(self):
        return [self.codDep, self.nome, self.sigla]
    def getCodDep(self):
        return self.codCurso
    def getNome(self):
        return self.nome
    def getSigla(self):
        return self.sigla
    
    def setNome(self,aux):
        self.nome.set(aux)

    def setCodDep(self,cod):
        if int(cod) == cod and cod > 0:
            self.codDep = cod
        else:
            print("Codigo deve ser um inteiro positivo")
    def setSigla(self,aux):
        self.sigla = aux
    
    def __repr__(self):
        return f"{self.codDep} - {self.nome}"