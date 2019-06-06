# Código com definição de agentes abstratos a serem utilizados em nossas aulas.

from abc import ABC

class Agente(ABC):
    '''
    Classe abstrata de agentes artificiais racionais.
    '''

    @abstractmethod
    def adquirirPercepcao(self, percepcao_mundo):
        ''' Forma uma percepcao interna por meio de seus sensores, a partir das
        informacoes de um objeto de visao de mundo.
        '''
        return
    
    @abstractmethod
    def escolherProximaAcao(self):
        ''' Escolhe proxima acao, com base em seu entendimento do mundo, a partir
        das percepções anteriores.
        '''
        return


class AgenteReflexivo(Agente):
    def __init__(self, regras):
        ''' Inicializa o agente e suas regras de atuação
        
        :param regras: dicionário de condição-ação, no formato modelo -> ação
        '''
        self.regras = regras

    def adquirirPercepcao(self, percepcao_mundo):
        ''' Forma uma percepcao interna por meio de seus sensores, a partir das
        informacoes de um objeto de visao de mundo.
        '''
        self.ultima_percepcao = percepcao_mundo

    def escolherProximaAcao(self):
        modelo_imediato = self.ultima_percepcao
        acao = self.regras[modelo_imediato]
        return acao


class AgenteComModelo(Agente):
    def __init__(self, modelo, regras):
        self.modelo = modelo
        self.regras = regras
        
        # Ultima acao realizada, inicialmente nenhuma
        self.acao = None
    
    def adquirirPercepcao(self, percepcao_mundo):
        ''' Atualiza o estado de acordo com os atributos internos (estado,
            acao, modelo) e a nova percepcao do ambiente
        '''
        pass

    def escolherProximaAcao(self):
        acao = self.regras[modelo]
        return acao


class AgenteComObjetivo(Agente):
    def __init__(self):
        # Uma sequencia de acoes, inicialmente vazia
        self.seq = []
        # Um objetivo, inicialmente nulo
        self.objetivo = None
    
    def escolherProximaAcao(self):
        # Se seq estiver vazia
        if not self.seq:
            self.formularProblema()
            self.busca()
            if not self.seq:
                return None
        acao = self.seq.pop(0)
        return acao
    
    def formularEstadoAtual(self):
        ''' Instancia objeto com base em AbstractEstado representando o estado
        atual e as corretas funções de navegação pelo estado, bem como o teste
        de objetivo e a função de custo.
        
        Ao final, self.estado deve estar preenchido.
        '''
        pass
    
    def busca(self):
        ''' Monta uma nova sequencia de acoes para resolver o problema atual.
        
            Ao final, self.seq deve conter uma lista de acoes.
        '''
        pass