# Domínios básicos do sistema (reutilizados em entidades)
# - Nome
# - Email
# - Cpf
# - Data
# - Senha

import datetime

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
        return f'{self.nome}'

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
            raise ValueError("Email no formato inválido")

    def __repr__(self):
        return f'{self.email}'

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
        return f'{self.cpf}'
    
class Data:
    def __init__(self, data = None):
        if str(data) == data:
            self.setData(data)
        else:
            self.data = data
    
    def getData(self):
        return self.data

    def setData(self, data):
        data2 = data.split('/')
        if (len(data2) != 3):
            raise ValueError("Formato da data inválido, coloque data no formato DD/MM/YYYY, incluindo o caracter '/' ")
        dd, mm, yyyy = data2
        if not dd.isdigit() or not mm.isdigit() or not yyyy.isdigit():
            raise ValueError("Formato da data inválido, coloque apenas caracteres numéricos intercalados com '/'. Exemplo, 24/07/2025")
        if len(dd) != 2 or len(mm) != 2 or len(yyyy) != 4:
            raise ValueError("Formato da data inválido, coloque o dia e o mês com dois dígitos e o ano com quatro dígitos. Exemplo: 03/07/1970")
        
        dd2 = int(dd)
        mm2 = int(mm)
        yyyy2 = int(yyyy)
        flag1 = (dd2 >= 1 and dd2 <= 31)
        flag2 = (mm2 >= 1 and mm2 <= 12)
        if not flag1 or not flag2:
            raise ValueError("Data inválida")
        
        if mm2 == 2:
            if yyyy2 % 4 == 0:
                if dd2 > 29: raise ValueError(f"Data inválida")
            elif dd2 > 28:
                raise ValueError(f"Data inválida")
            
        aux = [4,6,9,11]
        if (mm2 in aux) and dd2 == 31:
            raise ValueError("Data inválida")
        
        self.data = datetime.datetime(int(data[6:]), int(data[3:5]), int(data[:2]))
    
    def __repr__(self):
        return self.data.strftime("%d/%m/%Y")
    


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
        return f'{self.senha}'