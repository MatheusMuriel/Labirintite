from abc import ABC
import Labirintite
import string

class AbstractEstado(ABC):
    def __init__(self, is_objetivo, custo_transicao=lambda s,a,st: 1):
        self.isObjetivo = is_objetivo
        self.custoTransicao = custo_transicao
    
    #@abstractmethod
    def acoesPossiveis(self):
        """ AbstractEstado -> (AbstractAcao)
        Cria um generator de ações válidas para self.
        """
        return
    
    #@abstractmethod
    def transicaoPor(self, acao):
        """ AbstractEstado, AbstractAcao -> AbstractEstado
        Computa o estado adjacente a self ao aplicar uma acao válida.
        """
        return
    
    def adjacentes(self):
        """ AbstractEstado -> (AbstractEstado)
        Cria um generator de estados adjacentes a self, o estado atual.
        """
        return (self.transicaoPor(acao) for acao in self.acoesPossiveis())

class EstadosLabirintite(AbstractEstado):
    """
    Com base em seu design, implemente uma classe que corresponda à interface de `AbstractEstado` 
    (ver `espaco_estado.py` no GitLab), e que seja capaz de gerar o espaço de estados de seu jogo.
    """
    def __init__(self, is_objetivo, custo_transicao=lambda s,a,st: 1):
        self.isObjetivo = is_objetivo
        self.custoTransicao = custo_transicao
    
    def estado_atual(jogavel:Labirintite.LabirintiteGame):
        mapa = jogavel.labirinto
        print(mapa)

    def acoesPossiveis(self):
        """ AbstractEstado -> (AbstractAcao)
        Cria um generator de ações válidas para self.
        """
        def generator():
            
            yield
            #
        return
    
    def transicaoPor(self, acao):
        """ AbstractEstado, AbstractAcao -> AbstractEstado
        Computa o estado adjacente a self ao aplicar uma acao válida.
        """
        return
    
    def adjacentes(self):
        """ AbstractEstado -> (AbstractEstado)
        Cria um generator de estados adjacentes a self, o estado atual.
        """
        return (self.transicaoPor(acao) for acao in self.acoesPossiveis())

class estado_teste():
    #Modelagem para entender conceitos
    #Baseado na wiki do jogo

    def __init__(self, cod_letra, cod_numero):
        
        #Cod ex A1, B2, Zn...
        self.CodigoObjeto = [cod_letra,cod_numero]
        
        #Os elementos que são paredes tem código mas não são representados no espaço de estados.
        self.IsParede = None

        #Um estado é representado por: EA = <CÓDIGO DA LOCALIZAÇÃO ATUAL>.
        self.EstadoAtual = None

        #Uma transição é representada por: T = (EA, <DIREÇAO>). 
        self.Transicao = None

        return super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<E = ({})\n'.format(self.CodigoObjeto)
    
    def preencher(self, mapa_matriz):
        letra = self.CodigoObjeto[0]
        numero = self.CodigoObjeto[1]

        #Bater com a matriz do mapa 
        pontoNoMapa = mapa_matriz[]
        pass

    def converteLetra(letra):
        alfabeto = list(string.ascii_uppercase)
        letra = letra.upper()
        numeroSaida = 1
        for iLetra in alfabeto:
            if iLetra == letra:
                return numeroSaida
            else:
                numeroSaida += 1
        raise "Letra invalida"

    def definirEstado(self, CodigoObjeto, isParede, EstadoAtual, Transicao):
        self.CodigoObjeto = CodigoObjeto
        self.isParede = isParede
        self.EstadoAtual = EstadoAtual
        self.Transicao = Transicao

class transicao_teste():

    def __init__(self, EstadoAtual, Direcao):
        self.EstadoAtual = EstadoAtual
        self.Direcao = Direcao

    def __repr__(self):
        return '<T = ({}, {})\n'.format(self.EstadoAtual, self.Direcao)
    