from classes.domains import *

# Entidades relacionadas à extensão
# - Extensao
# - Situacao
# - Local
# - Feedback

class Extensao:
    def __init__(self, codExt=None, codLocal=None, titulo=None, tipo=None, 
                 descricao=None, areaTematica=None, publicoInternoEstimado=None,publicoExternoEstimado=None,publicoInterno=None,
                 publicoExterno=None, inicioRealizacao=None, fimRealizacao=None):
        self.codExt = codExt
        self.codLocal = codLocal
        self.titulo = titulo
        self.tipo = tipo
        self.descricao = descricao
        self.areaTematica = areaTematica
        self.publicoInternoEstimado = publicoInternoEstimado
        self.publicoExternoEstimado = publicoExternoEstimado
        self.publicoInterno = publicoInterno
        self.publicoExterno = publicoExterno
        self.inicioRealizacao = Data(inicioRealizacao)
        self.fimRealizacao = Data(fimRealizacao)       

    def get(self):
        return [self.codExt, self.codLocal, self.titulo,
                self.tipo, self.descricao, self.areaTematica, self.publicoInternoEstimado,
                self.publicoExternoEstimado, self.publicoInterno, self.publicoExterno,
                self.inicioRealizacao, self.fimRealizacao]
    
    def getCodExt(self): 
        return self.codExt
    def getCodLocal(self): 
        return self.codLocal
    def getTitulo(self):
        return self.titulo
    def getTipoAcao(self):
        return self.tipo
    def getDescricao(self):
        return self.descricao
    def getAreaTematica(self):
        return self.areaTematica
    def getPublicoInternoEst(self):
        return self.publicoInternoEstimado
    def getPublicoExternoEst(self):
        return self.publicoExternoEstimado
    def getPublicoInterno(self):
        return self.publicoInterno
    def getPublicoExterno(self):
        return self.publicoExterno
    def getInicioRealizacao(self):
        return self.inicioRealizacao
    def getFimRealizacao(self):
        return self.fimRealizacao

    def setCodExt(self,aux):
        self.codExt = aux
        
    def setCodLocal(self,aux):
        self.codLocal = aux

    def setTitulo(self,aux):
        self.titulo = aux
    
    def setTipo(self,aux):
        self.tipo = aux
    
    def setArea(self,aux):
        self.areaTematica = aux
    
    def setDesc(self,aux):
        self.descricao = aux
    
    def setPubIntEst(self,aux):
        if int(aux) == aux and aux > 0:
            self.publicoInternoEstimado = aux
        else:
            print("Publico deve ser um inteiro positivo")

    def setPubExtEst(self,aux):
        if int(aux) == aux and aux > 0:
            self.publicoExternoEstimado = aux
        else:
            print("Publico deve ser um inteiro positivo")

    def setPubInt(self,aux):
        if int(aux) == aux and aux > 0:
            self.publicoInterno = aux
        else:
            print("Publico deve ser um inteiro positivo")

    def setPubExt(self,aux):
        if int(aux) == aux and aux > 0:
            self.publicoExterno = aux
        else:
            print("Publico deve ser um inteiro positivo")
    
    def setDataInicio(self,aux):
        self.inicioRealizacao.set(aux)
        
    def setDataFim(self,aux):
        self.fimRealizacao.set(aux)

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
    def __init__(self, codLocal = None, nome = None, tipo = None, estado = None, municipio = None, bairro = None, complemento = None):
        self.codLocal = codLocal
        self.nome = Nome(nome)
        self.tipo = tipo
        self.estado = estado
        self.municipio = municipio
        self.bairro = bairro
        self.complemento = complemento
    
    
    def getAll(self):
        return [self.codLocal,
        self.nome,
        self.tipo,
        self.estado,
        self.municipio,
        self.bairro,
        self.complemento]
    
    def getCodLocal(self):
        return self.codLocal
    def getNome(self):
        return self.nome
    def getTipo(self):
        return self.tipo
    def getEstado(self):
        return self.estado
    def getMunicipio(self):
        return self.municipio
    def getBairro(self):
        return self.bairro
    def getComplemento(self):
        return self.complemento
    
    def setCodLocal(self, cod):
        self.codLocal = cod
    def setNome(self, nome):
        self.nome.set(nome)
    def setTipo(self, tipo):
        self.tipo = tipo
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
    def __init__(self, codFeedback=None, data=None, comentario=None, nota=None, autor=None, funcao=None):
        self.codFeedback = codFeedback
        self.data = Data(data)
        self.comentario = comentario
        self.nota = nota
        self.autor = autor
        self.funcao = funcao

    def get(self):
        return [self.codFeedback, self.data, self.comentario, self.nota, self.autor, self.funcao]
    def getCod(self):
        self.codFeedback
    def getData(self):
        return self.data
    def getComentario(self):
        return self.comentario
    def getAutor(self):
        return self.autor
    def getFunçao(self):
        return self.funcao

    def getNota(self):
        return self.nota

    
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