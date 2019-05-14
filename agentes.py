# Código com definição de agentes abstratos a serem utilizados em nossas aulas.

from abc import ABC, abstractmethod



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

# Implemente seu jogador humano nessa classe, sobrescrevendo os métodos
# abstratos de Agente. Em construir_agente, retorne uma instância dessa classe.
class AgenteHumano(Agente):

    sequencia = 0
    agentes = []
    
    def __init__(self):
        
        #Define aqui o ID do agente
        self.__class__.sequencia += 1
        self.id = self.__class__.sequencia

        #Define aqui o tipo do agente
        self.tipo_agente = 'HUMANO'
        
        #Adiciona esse agente na lista de agentes
        self.__class__.agentes.append(self)

    def __str__(self):
        return self.tipo_agente

    def __repr__(self):
        return '<{}: {} - {}\n'.format(self.__class__.__name__, self.id, self.tipo_agente)

    @classmethod
    def all(cls):
        return cls.agentes

    def adquirirPercepcao(self, percepcao_mundo):
        # Utilize percepcao de mundo para atualizar tela (terminal ou blit),
        # tocar sons, dispositivos hápticos, etc, todo e qualquer dispositivo
        # de saída para interface humana.
        
        print("Admire a tela")
    
    def escolherProximaAcao(self):
        # Receba entrada humana apenas neste momento, seja com prompt (terminal)
        # ou polling (jogos interativos).
        
        return input('Proxima ação: ')

class AgenteRobo(Agente):
    sequencia = 0
    agentes = []
    
    def __init__(self):
        
        #Define aqui o ID do agente
        self.__class__.sequencia += 1
        self.id = self.__class__.sequencia

        #Define aqui o tipo do agente
        self.tipo_agente = 'ROBO'
        
        #Adiciona esse agente na lista de agentes
        self.__class__.agentes.append(self)

    def __str__(self):
        return self.tipo_agente

    def __repr__(self):
        return '<{}: {} - {}\n'.format(self.__class__.__name__, self.id, self.tipo_agente)

    @classmethod
    def all(cls):
        return cls.agentes

    def adquirirPercepcao(self, percepcao_mundo):
        # Utilize percepcao de mundo para atualizar tela (terminal ou blit),
        # tocar sons, dispositivos hápticos, etc, todo e qualquer dispositivo
        # de saída para interface humana.
        
        print("Ainda não implementado")
    
    def escolherProximaAcao(self):
        # Receba entrada humana apenas neste momento, seja com prompt (terminal)
        # ou polling (jogos interativos).
        
        print("Ainda não implementado")


def construir_agente(*args,**kwargs):
    """ Método factory para uma instância Agente arbitrária, de acordo com os
    paraâmetros. Pode-se mudar à vontade a assinatura do método.
    """
    return AgenteHumano()