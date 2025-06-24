from joao import Nome, Email

class Cpf: 
    def __init__(self, cpf = None):
        self.cpf = cpf
        
    def get(self):
        return self.cpf

    def set(self, cpf):
        if len(cpf) != 11 or not cpf.isdigit():
            print("Formato de CPF inválido, coloque apenas números")
        else:
            self.cpf = cpf

    def __repr__(self):
        return self.cpf
    
class Pessoa:
    #como colocar curriculo ?
    def __init__(self, cpf = None, nome = None, senha = None, curriculo = None, email = None):
        self.cpf = Cpf(cpf)
        self.nome = Nome(nome)
        self.senha = senha
        self.curriculo = curriculo 
        self.email = Email(email)
    
    def getAll(self):
        return [self.cpf, self.nome, self.senha, self.email, self.curriculo]
    
    def setCpf(self, cpf):
        self.cpf.set(cpf)
        
    def setNome(self, nome):
        self.nome.set(nome)
        
    def setSenha(self, senha):
        self.senha.set(senha)
    
    def setCurriculo(self, curriculo):
        self.curriculo = curriculo
    
    def setEmail(self, email):
        self.email.set(email)
        
    def __repr__(self):
        return [self.cpf, self.nome]

class Materia:
    def __init__(self, nome = None, codMateria = None):
        self.nome = Nome(nome)
        self.codMateria = codMateria
    
    def getAll(self):
        return [self.nome, self.codMateria]
    
    def setNome(self, nome):
        self.nome.set(nome)
    
    def setCodMateria(self, codMateria):
        self.codMateria = codMateria
        
    def __repr__(self):
        return [self.codMateria, self.nome]

class Local:
    def __init__(self, codLocal = None, nome = None, tipo = None, endereco = None, estado = None, municipio = None, bairro = None, complemento = None):
        self.codLocal = codLocal
        self.nome = Nome(nome)
        self.tipo = tipo
        self.endereco = endereco
        self.estado = estado
        self.municipio = municipio
        self.bairro = bairro
        self.complemento = complemento
    
    def getAll(self):
        return [self.codLocal,
        self.nome,
        self.tipo,
        self.endereco,
        self.estado,
        self.municipio,
        self.bairro,
        self.complemento]
    
    def setCodLocal(self, cod):
        self.codLocal = cod
    def setNome(self, nome):
        self.nome.set(nome)
    def setTipo(self, tipo):
        self.tipo = tipo
    def setEndereco(self, endereco):
        self.endereco = endereco
    def setEstado(self, estado):
        self.estado = estado
    def setMunicipio(self, municipio):
        self.municipio = municipio
    def setBairro(self, bairro):
        self.bairro = bairro
    def setComplemento(self, comp):
        self.complemento = comp

    def __repr__(self):
        return self.nome

class Data:
    def __init__(self, data = None):
        self.data = data
    
    def getData(self):
        return self.data

    def setData(self, data):
        data2 = data.split('-')
        if (len(data2) != 3):
            print("Formato invalido, coloque no formato DD-MM-YYYY, incluindo o caracter '-' ")
            return
        dd, mm, yyyy = data2
        if not dd.isdigit() or not mm.isdigit() or not yyyy.isdigit():
            print("Coloque apenas caracteres numericos intercalados com '-', por exemplo, 24-07-2025")
            return
        if len(dd) != 2 or len(mm) != 2 or len(yyyy) != 4:
            print("Formato invalido, coloque o dia e o mes com dois digitos e o ano com quatro digitos, exemplo: 03-07-1970")
            return
        
        dd2 = int(dd)
        mm2 = int(mm)
        yyyy2 = int(yyyy)
        flag1 = (dd2 >= 1 and dd2 <= 31)
        flag2 = (mm2 >= 1 and mm2 <= 12)
        if not flag1 or not flag2:
            print("Data invalida")
            return
        
        if mm2 == 2:
            if yyyy2 % 4 == 0 and dd2 > 29:
                print("Data invalida")
                return
            elif dd2 > 28:
                print("Data invalida")
                return
        aux = [4,6,9,11]
        if (mm2 in aux) and dd2 == 31:
            print("Data invalida")
            return
        
        self.data = data
    
    def __repr__(self):
        return self.data