from abc import ABC
import Labirintite
import string
from heuristica import HeuristicaLabirinto

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
    def __init__(self, custo_transicao=lambda s,a,st: 1):
        #self.isObjetivo = is_objetivo
        self.custoTransicao = custo_transicao

        #Estado inicial é padrão
        self.estadoInicial = estado('B',2)
        self.estadoAtual = None
        self.estadoFinal = None

        #Lista de todos os estados possiveis
        self.todosEstadosPossiveis = []

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

    def todos_estados(self, matriz):
        lista_estados = []
        alfabeto = list(string.ascii_uppercase)

        cod_num = 0
        for coluna in matriz:
            cod_letra = 0
            for linha in coluna:
                bit = matriz[cod_letra][cod_num]
                if bit == 0:
                    estado_aux = estado(alfabeto[cod_letra], cod_num)
                    lista_estados.append(estado_aux)
                elif (bit == 99):
                    estado_saida = estado(alfabeto[cod_letra], cod_num, True)
                    self.estadoFinal = estado_saida
                    lista_estados.append(estado_saida)
                cod_letra += 1
            cod_num += 1
        self.todosEstadosPossiveis = lista_estados

    def transicao(origem, destino):
        x, x_aux = origem.getLetra(), destino.getLetra()
        vx, vx_aux = origem.getValorLetra(), destino.getValorLetra()
        n, n_aux = origem.getNumero(), destino.getNumero()

        if (x == x_aux):
            if n_aux > n:
                #Para frente
                d = 'DIREITA'
            elif n_aux < n:
                #Para tras
                d = 'ESQUERDA'
        elif n == n_aux:
            if vx_aux > vx:
                #Para cima
                d = 'CIMA'
            elif vx_aux < vx:
                #Para baixo
                d = 'BAIXO'

        return transicao(origem,d, destino)

    def estados_adjacentes(self):
        estados = self.todosEstadosPossiveis

        for e in estados:
            for e_aux in estados:
                adjacente = False
                #Adjacentes a X n: X+1 n, X-1 n, X n+1, X n-1
                
                x, x_aux = e.getLetra(), e_aux.getLetra()
                vx, vx_aux = e.getValorLetra(), e_aux.getValorLetra()
                n, n_aux = e.getNumero(), e_aux.getNumero()

                if ( x == x_aux ):    
                    if ( n_aux + 1 == n ) or ( n_aux - 1 == n ):
                        adjacente = True
                elif ( n == n_aux ):
                    if ( vx_aux + 1 == vx ) or (vx_aux - 1 == vx):
                        adjacente = True

                if adjacente: e.estadosAdjacentes.append(e_aux)

    def estados_heuristica(self):
        estados = self.todosEstadosPossiveis

        for e in estados:
            h = HeuristicaLabirinto(e,self.estadoFinal)
            h.getValorH()
            e.heuristica = h
        
class estado():
    #Modelagem para entender conceitos
    #Baseado na wiki do jogo

    def __init__(self, cod_letra, cod_numero, isObjetivo=False, custo=1):
        
        #Cod ex A1, B2, Zn...
        self.CodigoObjeto = cod_letra + str(cod_numero)
        self.letra = cod_letra
        self.numero = cod_numero

        #Variavel que diz se é o objetivo(Saida do labirinto)
        self.isObjetivo = isObjetivo

        #Uma transição é representada por: T = (EA, <DIREÇAO>). 
        self.Transicao = None

        self.estadosAdjacentes = []

        self.heuristica = None

    def __repr__(self):
        return '<E = ({})>'.format(self.CodigoObjeto)

    def getCodigo(self):
        return self.CodigoObjeto

    def getLetra(self):
        return self.letra
    
    def getValorLetra(self):
        return self.converteLetra(self.letra)

    def getNumero(self):
        return self.numero

    def preencher(self, mapa_matriz):
        letra = self.CodigoObjeto[0]
        numero = self.CodigoObjeto[1]

        nLetra = converteLetra(letra)
        #Bater com a matriz do mapa 
        pontoNoMapa = mapa_matriz[nLetra-1, numero-1]
        pass

    def converteLetra(self, letra):
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

class transicao():

    def __init__(self, estadoAtual, direcao, destino):
        self.estadoAtual = estadoAtual
        self.direcao = direcao
        self.destino = destino

    def __repr__(self):
        return '<T = ({}, {})>'.format(self.estadoAtual, self.direcao)
    
    def getEstadoAtual(self):
        return self.estadoAtual

    def getDirecao(self):
        return self.direcao

    def getDestino(self):
        return self.destino
