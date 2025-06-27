# Domínios básicos do sistema (reutilizados em entidades)
# - Nome
# - Email
# - Cpf
# - Data
# - Senha

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
        return f"{self.data}"
    


class Senha: 
    def __init__(self, senha = None):
        self.senha = senha
        
    def get(self):
        return self.senha

    def set(self, senha):
        if len(senha) > 30:
            print("Senha deve ter menos de 30 dígitos")
        else:
            self.senha = senha

    def __repr__(self):
        return self.senha