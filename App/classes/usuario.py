from domains import *

# Entidades relacionadas aos usuários
# - Aluno
# - Professor
# - Pessoa

class Aluno:
    def __init__(self, matricula=None, nome=None, senha=None, cpf=None, ira=None, dataIngresso=None, semestre=None, emails=[]):
        self.matricula = matricula
        self.nome = Nome(nome)
        self.senha = Senha(senha)
        self.cpf = Cpf(cpf)
        self.ira = ira
        self.dataIngresso = Data(dataIngresso)
        self.semestre = semestre
        self.emails = emails
    
    def getAll(self):
        return [self.matricula,self.nome,self.senha,self.cpf,self.ira,self.dataIngresso,self.semestre,self.emails]
    
    def setMatricula(self,aux):
        aux = str(aux)
        if (aux.isnumeric() and len(aux) == 9):
            self.matricula = aux
        else:
            print("Matricula no formato errado")

    def setNome(self,aux):
        self.nome.set(aux)

    def setSenha(self,aux):
        self.senha.set(aux)

    def setCpf(self,aux):
        self.cpf.set(aux)

    def setIra(self,aux):
        if aux <= 5 or aux >= 0:
            self.ira = aux
        else:
            print("IRA deve ser entre 0 e 5")
    
    def setData(self,aux):
        self.data.set(aux)
    
    def setSemestre(self,aux):
        if int(aux) == aux and aux > 0:
            self.semestre = aux
        else:
            print("Semestre deve ser um inteiro positivo")
    
    def setEmails(self,aux):
        self.emails = aux

    def addEmail(self, aux):
        if isinstance(aux, Email):
            email = aux
        else:
            email = Email()
            email.set(aux)
            
        if not self.emails:
            self.emails = [email]
        else:
            self.emails.append(email)

    def __repr__(self):
        return f"Aluno {self.matricula} - {self.nome}"
    
class Docente:
    def __init__(self, matricula=None, nome=None, senha=None, cpf=None, codDep=None, emails = []):
        self.matricula = matricula
        self.nome = Nome(nome)
        self.senha = Senha(senha)
        self.cpf = Cpf(cpf)
        self.codDep = codDep
        self.emails = emails
    
    def getAll(self):
        return [self.matricula,self.nome,self.senha,self.cpf,self.codDep,self.emails]
    
    def setMatricula(self,aux):
        aux = str(aux)
        if (aux.isnumeric() and len(aux) == 11):
            self.matricula = aux
        else:
            print("Matricula no formato errado")

    def setNome(self,aux):
        self.nome.set(aux)

    def setSenha(self,aux):
        self.senha.set(aux)

    def setCpf(self,aux):
        self.cpf.set(aux)

    def setCodDep(self,aux):
        self.codDep = aux
    
    def setEmails(self,aux):
        self.emails = aux

    def addEmail(self, aux):
        if isinstance(aux, Email):
            email = aux
        else:
            email = Email()
            email.set(aux)
            
        if not self.emails:
            self.emails = [email]
        else:
            self.emails.append(email)

    def __repr__(self):
        return f"Docente {self.matricula} - {self.nome}"
    
class Pessoa:
    def __init__(self, cpf = None, nome = None, senha = None, emails = []):
        self.cpf = Cpf(cpf)
        self.nome = Nome(nome)
        self.senha = Senha(senha)
        self.emails = emails
    
    def getAll(self):
        return [self.cpf, self.nome, self.senha, self.emails]
    
    def setCpf(self, cpf):
        self.cpf.set(cpf)
        
    def setNome(self, nome):
        self.nome.set(nome)
        
    def setSenha(self, senha):
        self.senha.set(senha)
    
    def setEmails(self,aux):
        self.emails = aux

    def addEmail(self, aux):
        if isinstance(aux, Email):
            email = aux
        else:
            email = Email()
            email.set(aux)
            
        if not self.emails:
            self.emails = [email]
        else:
            self.emails.append(email)
        
    def __repr__(self):
        return f"Pessoa {self.cpf} - {self.nome}"