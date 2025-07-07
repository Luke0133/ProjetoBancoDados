from classes.domains import *

# Entidades relacionadas aos usuários
# - Aluno
# - Professor
# - Pessoa

class Aluno:
    def __init__(self, matricula=None, codCurso=None, nome=None, cpf=None, senha=None,  ira=None, dataIngresso=None, semestre=None):
        self.matricula = matricula
        self.codCurso = codCurso
        self.nome = nome
        self.cpf = Cpf(cpf)
        self.senha = senha
        self.ira = ira
        self.dataIngresso = Data(dataIngresso)
        self.semestreAtual = semestre
        
        
    def getAll(self):
        return [self.matricula,self.codCurso,self.nome,self.cpf,self.senha,self.ira,self.dataIngresso,self.semestreAtual]
    def getMatricula(self):
        return self.matricula
    def getCodCurso(self):
        return self.codCurso
    def getNome(self):
        return self.nome
    def getSenha(self):
        return self.senha
    def getCpf(self):
        return self.cpf
    def getIra(self):
        return self.ira
    def getDataIngresso(self):
        return self.dataIngresso
    def getSemestreAtual(self):
        return self.semestreAtual
    
    def setMatricula(self,aux):
        aux = str(aux)
        if (aux.isnumeric() and len(aux) == 9):
            self.matricula = aux
        else:
            print("Matricula no formato errado")

    def setNome(self,aux):
        self.nome = aux

    def setSenha(self,aux):
        self.senha.set(aux)

    def setCpf(self,aux):
        self.cpf.set(aux)

    def setIra(self,aux):
        if aux <= 5 or aux >= 0:
            self.ira = aux
        else:
            print("IRA deve ser entre 0 e 5")
    
    def setDataIngresso(self,aux):
        self.dataIngresso.set(aux)
    
    def setSemestreAtual(self,aux):
        if int(aux) == aux and aux > 0:
            self.semestreAtual = aux
        else:
            print("Semestre deve ser um inteiro positivo")

    def __repr__(self):
        return f"Aluno {self.matricula} - {self.nome}"
    
class Docente:
    def __init__(self, matricula=None, codDep=None, nome=None, senha=None, cpf=None):
        self.matricula = matricula
        self.codDep = codDep
        self.nome = nome
        self.senha = Senha(senha)
        self.cpf = Cpf(cpf)
    
    def getAll(self):
        return [self.matricula,self.codDep,self.nome,self.senha,self.cpf]
    def getMatricula(self):
        return self.matricula
    def getCodDep(self):
        return self.codDep
    def getNome(self):
        return self.nome
    def getSenha(self):
        return self.senha
    def getCpf(self):
        return self.cpf
    
    def setMatricula(self,aux):
        aux = str(aux)
        if (aux.isnumeric() and len(aux) == 11):
            self.matricula = aux
        else:
            print("Matricula no formato errado")

    def setNome(self,aux):
        self.nome = aux

    def setSenha(self,aux):
        self.senha = aux

    def setCpf(self,aux):
        self.cpf.set(aux)

    def setCodDep(self,aux):
        self.codDep = aux
    

    def __repr__(self):
        return f"Docente {self.matricula} - {self.nome}"
    
class Pessoa:
    def __init__(self, cpf = None, nome = None, senha = None):
        self.cpf = Cpf(cpf)
        self.nome = nome
        self.senha = senha
    
    
    def getAll(self):
        return [self.cpf, self.nome, self.senha]
    def getCpf(self):
        return self.cpf
    def getNome(self):
        return self.nome
    def getSenha(self):
        return self.senha
    
    def setCpf(self, cpf):
        self.cpf.set(cpf)
        
    def setNome(self,aux):
        self.nome = aux
        
    def setSenha(self, senha):
        self.senha = senha
        
    def __repr__(self):
        return f"Pessoa {self.cpf} - {self.nome}"