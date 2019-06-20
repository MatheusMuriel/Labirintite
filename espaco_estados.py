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

        #Estado inicial é padrão
        self.estadoInicial = estado_teste('B',2)
        self.estadoAtual = self.estadoInicial

        #Lista de todos os estados possiveis
        self.todosEstadosPossiveis = None
    
    def estado_atual(self, jogo):
        x = jogo.jogavel.jogador_x
        y = jogo.jogavel.jogador_y
        print(x,y)
        pass

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
                    estado_aux = estado_teste(alfabeto[cod_letra], cod_num)
                    lista_estados.append(estado_aux)
                elif (bit == 99):
                    estado_saida = estado_teste(alfabeto[cod_letra], cod_num, True)
                    lista_estados.append(estado_saida)
                cod_letra += 1
            cod_num += 1
        return lista_estados


class estado_teste():
    #Modelagem para entender conceitos
    #Baseado na wiki do jogo

    def __init__(self, cod_letra, cod_numero, isObjetivo=False):
        
        #Cod ex A1, B2, Zn...
        self.CodigoObjeto = cod_letra + str(cod_numero)
        self.letra = cod_letra
        self.numero = cod_numero

        #Variavel que diz se é o objetivo(Saida do labirinto)
        self.isObjetivo = isObjetivo

        #Uma transição é representada por: T = (EA, <DIREÇAO>). 
        self.Transicao = None

    def __repr__(self):
        return '<E = ({})>'.format(self.CodigoObjeto)

    def getLetra(self):
        return self.letra

    def getNumero(self):
        return self.numero

    def preencher(self, mapa_matriz):
        letra = self.CodigoObjeto[0]
        numero = self.CodigoObjeto[1]

        nLetra = converteLetra(letra)
        #Bater com a matriz do mapa 
        pontoNoMapa = mapa_matriz[nLetra-1, numero-1]
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
        return '<T = ({}, {})'.format(self.EstadoAtual, self.Direcao)
    