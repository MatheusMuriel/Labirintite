from abc import ABC, abstractmethod
import Labirintite
import agentes

class RegrasJogo(ABC):
    """ Interface mínima para implementar um jogo interativo e modular. Não
    tente instanciar objetos dessa classe, ela deve ser herdada e seus métodos
    abstratos sobrecarregados.
    """

    @abstractmethod
    def registrarAgenteJogador(self, elemAgente):
        """ Cria ou recupera id de um elemento de jogo agente.
        """
        return
    
    @abstractmethod
    def isFim(self):
        """ Boolean indicando fim de jogo em True.
        """
        return

    @abstractmethod
    def gerarCampoVisao(self, idAgente):
        """ Retorna um EstadoJogoView para ser consumido por um agente
        específico. Objeto deve conter apenas descrição de elementos visíveis
        para este agente.

        EstadoJogoView é um objeto imutável ou uma cópia do jogo, de forma que
        sua manipulação direta não tem nenhum efeito no mundo de jogo real.
        """
        return

    @abstractmethod
    def registrarProximaAcao(self, id_jogador, acao):
        """ Informa ao jogo qual a ação de um jogador especificamente.
        Neste momento, o jogo ainda não é transformado em seu próximo estado,
        isso é feito no método de atualização do mundo.
        """
        return
    
    @abstractmethod
    def atualizarEstado(self, diferencial_tempo):
        """ Apenas neste momento o jogo é atualizado para seu próximo estado
        de acordo com as ações de cada jogador registradas anteriormente.
        """
        return

class Labirinto(RegrasJogo):
    JOGADOR_PADRAO = None
    
    def registrarAgenteJogador(self, lista_jogadores, jogo, elemAgente=JOGADOR_PADRAO):
        """ Cria ou recupera id de um elemento de jogo agente.
            Tem como retorno o ID do jogador
        """
        jogador = Labirintite.LabirintiteGame.cria_jogador(jogo, lista_jogadores)
        print("Teste")
        #jogador = jogo.cria_jogador(lista_jogadores)

        return int(jogador[1])
    
    def isFim(self, jogador, jogo):
        """ Boolean indicando fim de jogo em True.
        """
        fim = Labirintite.LabirintiteGame.verifica_fim(jogador, jogador.center_x, jogador.center_y)
        return fim

    def gerarCampoVisao(self, idAgente, jogo):
        """ Retorna um EstadoJogoView para ser consumido por um agente
        específico. Objeto deve conter apenas descrição de elementos visíveis
        para este agente.

        EstadoJogoView é um objeto imutável ou uma cópia do jogo, de forma que
        sua manipulação direta não tem nenhum efeito no mundo de jogo real.
        """

        estadoJogoView = Labirintite.campoDeVisao()

        return

    def registrarProximaAcao(self, id_jogador, acao):
        """ Informa ao jogo qual a ação de um jogador especificamente.
        Neste momento, o jogo ainda não é transformado em seu próximo estado,
        isso é feito no método de atualização do mundo.
        """
        return
    
    def atualizarEstado(self, diferencial_tempo):
        """ Apenas neste momento o jogo é atualizado para seu próximo estado
        de acordo com as ações de cada jogador registradas anteriormente.
        """
        return

    def iniciaJogo(self):
        jogo = Labirintite.construtor()
        #Labirintite.construtor()
        return jogo

def construir_jogo(*args,**kwargs):
    """ Método factory para uma instância Jogavel arbitrária, de acordo com os
    paraâmetros. Pode-se mudar à vontade a assinatura do método.
    """

    return Labirinto()