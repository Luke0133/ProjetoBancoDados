from domains import *

# Entidades relacionadas a matérias
# - Materia
# - Curso
# - Departamento

class Materia:
    def __init__(self, codMateria = None, nome = None):
        self.nome = Nome(nome)
        self.codMateria = codMateria
    
    def getAll(self):
        return [self.codMateria, self.nome]
    
    def setNome(self, nome):
        self.nome.set(nome)
    
    def setCodMateria(self, cod):
        if int(cod) == cod and cod > 0:
            self.codMateria = cod
        else:
            print("Codigo deve ser um inteiro positivo")
        
    def __repr__(self):
        return f"{self.codMateria} - {self.nome}"
    

class Curso:
    def __init__(self, codCurso=None, nome=None):
        self.codCurso = codCurso
        self.nome = Nome(nome)

    def get(self):
        return [self.codCurso, self.nome]
    
    def setNome(self,aux):
        self.nome.set(aux)

    def setCod(self,cod):
        if int(cod) == cod and cod > 0:
            self.codCurso = cod
        else:
            print("Codigo deve ser um inteiro positivo")

    def __repr__(self):
        return f"{self.codCurso} - {self.nome}"
    
class Departamento:
    def __init__(self, codDep=None, nome=None):
        self.codDep = codDep
        self.nome = Nome(nome)

    def get(self):
        return [self.codDep, self.nome]
    
    def setNome(self,aux):
        self.nome.set(aux)

    def setCod(self,cod):
        if int(cod) == cod and cod > 0:
            self.codDep = cod
        else:
            print("Codigo deve ser um inteiro positivo")

    def __repr__(self):
        return f"{self.codDep} - {self.nome}"