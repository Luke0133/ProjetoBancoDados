from domains import *

# Entidades relacionadas à extensão
# - Extensao
# - Situacao
# - Local
# - Feedback

class Extensao:
    def __init__(self, codExt=None, codLocal=None, titulo=None, tipo=None, 
                 area=None, desc=None, pubIntEst=None,pubExtEst=None,pubInt=None,
                 pubExt=None, dataInicio=None, dataFim=None):
        self.codExt = codExt
        self.codLocal = codLocal
        self.titulo = titulo
        self.tipo = tipo
        self.area = area
        self.desc = desc
        self.pubIntEst = pubIntEst
        self.pubExtEst = pubExtEst
        self.pubInt = pubInt
        self.pubExt = pubExt
        self.dataInicio = Data(dataInicio)
        self.dataFim = Data(dataFim)       

    def get(self):
        return [self.codExt, self.codLocal, self.titulo,
                self.tipo, self.area, self.desc, self.pubIntEst,
                self.pubExtEst, self.pubInt, self.pubExt,
                self.dataInicio, self.dataFim]
    
    def setCodExt(self,aux):
        self.codExt = aux
        
    def setCodLocal(self,aux):
        self.codLocal = aux

    def setTitulo(self,aux):
        self.titulo = aux
    
    def setTipo(self,aux):
        self.tipo = aux
    
    def setArea(self,aux):
        self.area = aux
    
    def setDesc(self,aux):
        self.desc = aux
    
    def setPubIntEst(self,aux):
        if int(aux) == aux and aux > 0:
            self.pubIntEst = aux
        else:
            print("Publico deve ser um inteiro positivo")

    def setPubExtEst(self,aux):
        if int(aux) == aux and aux > 0:
            self.pubExtEst = aux
        else:
            print("Publico deve ser um inteiro positivo")

    def setPubInt(self,aux):
        if int(aux) == aux and aux > 0:
            self.pubInt = aux
        else:
            print("Publico deve ser um inteiro positivo")

    def setPubExt(self,aux):
        if int(aux) == aux and aux > 0:
            self.pubExt = aux
        else:
            print("Publico deve ser um inteiro positivo")
    
    def setDataInicio(self,aux):
        self.dataInicio.set(aux)
        
    def setDataFim(self,aux):
        self.dataFim.set(aux)

    def __repr__(self):
        return f"{self.codExt}"
    

class SituacaoExt:
    def __init__(self, codExt=None, dataSit=None, situacao=None):
        self.codExt = codExt
        self.dataSit = Data(dataSit)
        self.situacao = situacao

    def get(self):
        return [self.codExt, self.dataSit, self.situacao]
    
    def getSit(self):
        return self.situacao
    
    def setCodExt(self,aux):
        self.codExt = aux

    def setData(self,aux):
        self.dataSit.set(aux)

    def __repr__(self):
        return f"Situação {self.situacao} - {self.dataSit}"
    
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
        return f"{self.nome}"

class Feedback:
    def __init__(self, codFeedback=None, data=None, comentario=None, nota=None):
        self.codFeedback = codFeedback
        self.data = Data(data)
        self.comentario = comentario
        self.nota = nota

    def get(self):
        return [self.codFeedback, self.data, self.comentario, self.nota]
    
    
    def setCod(self,aux):
        self.codFeedback = aux

    def setData(self,aux):
        self.data.set(aux)

    def setComentario(self,aux):
        self.comentario = aux

    def setNota(self,aux):
        if aux <= 5 or aux >= 0:
            self.nota = aux
        else:
            print("Nota deve ser entre 0 e 5")

    def __repr__(self):
        return f"Feedback: {self.nota}/5 - {self.comentario}"