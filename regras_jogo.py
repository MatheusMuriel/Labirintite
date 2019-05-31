from abc import ABC, abstractmethod
import Labirintite
import agentes

"""Interface com metodos abstratos. Deve ser herdada e sobrecarregada."""
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

"""Implementação da interface *RegrasJogo*, aqui os metodos são sobrecarregados."""
class Labirinto(RegrasJogo):

    def __init__(self):
        self.jogavel = None #É um objeto LabirintiteGame
        self.jogador = None
        #Lista com [jogador, direção]
        self.historico_estados = []
    
    def registrarAgenteJogador(self, elemAgente):
        """ Cria ou recupera id de um elemento de jogo agente.
            Tem como retorno o ID do jogador
        """
        
        id_agente_registrado = elemAgente.get_id()
        self.jogador = elemAgente

        return id_agente_registrado
    
    def isFim(self):
        """ Boolean indicando fim de jogo em True.
        """
        fim = self.jogavel.verifica_fim()
        return fim

    def gerarCampoVisao(self):
        """ Retorna um EstadoJogoView para ser consumido por um agente
        específico. Objeto deve conter apenas descrição de elementos visíveis
        para este agente.

        EstadoJogoView é um objeto imutável ou uma cópia do jogo, de forma que
        sua manipulação direta não tem nenhum efeito no mundo de jogo real.
        """
        tipo_jogador = self.jogador.tipo_agente

        if tipo_jogador == 'HUMANO':
            # Basta o humano olhar para a tela
            return self.jogavel.labirinto
        elif tipo_jogador == 'ROBO':
            return self.jogavel.labirinto
        else:
            raise print("Não foi possivel gerar o campo de visão, tipo de agente desconhecido.")

        return jogo_view

    def registrarProximaAcao(self, id_jogador, acao):
        """ Informa ao jogo qual a ação de um jogador especificamente.
        Neste momento, o jogo ainda não é transformado em seu próximo estado,
        isso é feito no método de atualização do mundo.
        """
        registro_acao = [id_jogador, acao]
        self.historico_estados.append(registro_acao)
        print("Registrado", registro_acao)
        return
    
    def atualizarEstado(self, diferencial_tempo):
        """ Apenas neste momento o jogo é atualizado para seu próximo estado
        de acordo com as ações de cada jogador registradas anteriormente.
        """
        #Objeto que contém [Jogador, Movimento]
        ultima_acao = self.historico_estados[ len(self.historico_estados) - 1 ]

        #Passa somente a direção
        self.jogavel.atualiza_estado( ultima_acao[1], diferencial_tempo )

        return
    
    def iniciaJogo(self):
        #Decidir qual metodo vai usar
        jogavel = Labirintite.construtor()
        #jogavel = Labirintite.main()
        self.jogavel = jogavel

def construir_jogo(*args,**kwargs):
    """ Método factory para uma instância Jogavel arbitrária, de acordo com os
    paraâmetros. Pode-se mudar à vontade a assinatura do método.
    """

    return Labirinto()