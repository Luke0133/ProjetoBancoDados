class Nome:
    def __init__(self, nome=None):
        self.nome = nome

    def get(self):
        return self.nome
    
    def set(self,nome):
        nome = str(nome)
        if ((nome.replace(" ", "")).isalpha() and len(nome) <= 100):
            self.nome = nome
        else:
            print("Nome possui caracteres nao permitidos ou e maior do que 100 caracteres")

    def __repr__(self):
        return self.nome

class Email:
    def __init__(self, email=None):
        self.email = email

    def get(self):
        return self.email
    
    def set(self,email):
        email = str(email)
        if (("@" in email) and len(email) <= 100):
            self.email = email
        else:
            print("Nao e um email valido ou e maior do que 100 caracteres")

    def __repr__(self):
        return self.email

class Docente:
    def __init__(self, matricula=None, nome=None, senha=None, cpf=None, codDep=None):
        self.matricula = matricula
        self.nome = Nome(nome)

        self.senha = senha
        self.cpf = cpf
        self.codDep = codDep
    
    def getAll(self):
        return [self.matricula,self.nome,self.senha,self.cpf,self.codDep]
    
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

    def __repr__(self):
        return [self.matricula, self.nome]

class Curso:
    def __init__(self, codCurso=None, nome=None):
        self.codCurso = codCurso
        self.nome = Nome(nome)

    def get(self):
        return [self.codCurso, self.nome]
    
    def setNome(self,aux):
        self.nome.set(aux)

    def setCod(self,cod):
        cod = str(cod)
        if (cod.isnumeric()):
            self.codCurso = cod

    def __repr__(self):
        return [self.codCurso, self.nome]

class SituacaoExt:
    def __init__(self, codExt=None, dataSit=None, situacao=None):
        self.codExt = codExt
        self.dataSit = dataSit
        self.situacao = situacao

    def get(self):
        return [self.codExt, self.dataSit]
    
    def getSit(self):
        return self.situacao
    
    def setCodExt(self,aux):
        self.codExt = aux

    def setData(self,aux):
        self.dataSit = aux

    def __repr__(self):
        return [self.codExt, self.dataSit]
