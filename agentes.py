# Código com definição de agentes abstratos a serem utilizados em nossas aulas.

from abc import ABC, abstractmethod
import espaco_estados

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

    def get_id(self):
        return self.id

    @classmethod
    def all(cls):
        return cls.agentes

    def adquirirPercepcao(self, percepcao_mundo, jogo):
        # Utilize percepcao de mundo para atualizar tela (terminal ou blit),
        # tocar sons, dispositivos hápticos, etc, todo e qualquer dispositivo
        # de saída para interface humana.

        #No caso de um humano ele deve olhar a tela
        jogo.jogavel.on_draw()
        return
    
    def escolherProximaAcao(self, jogo):
        # Receba entrada humana apenas neste momento, seja com prompt (terminal)
        # ou polling (jogos interativos).

        direcao = input("Proxima direção? ")
        direcao = direcao.upper()

        if direcao == 'W' or direcao == 'CIMA':
            direcao = 'CIMA'
        elif direcao == 'S' or direcao == 'BAIXO':
            direcao = 'BAIXO'
        elif direcao == 'A' or direcao == 'ESQUERDA':
            direcao = 'ESQUERDA'
        elif direcao == 'D' or direcao == 'DIREITA':
            direcao = 'DIREITA'
        else:
            print("Direção invalida.")
            return 'invalid'

        print("Direção escolhida foi: ", direcao)
        return direcao

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
    
    def get_id(self):
        return self.id

    @classmethod
    def all(cls):
        return cls.agentes

    def adquirirPercepcao(self, percepcao_mundo):
        # Utilize percepcao de mundo para atualizar tela (terminal ou blit),
        # tocar sons, dispositivos hápticos, etc, todo e qualquer dispositivo
        # de saída para interface robotica.
        
        print("Ainda não implementado")
    
    def escolherProximaAcao(self):
        # Receba entrada humana apenas neste momento, seja com prompt (terminal)
        # ou polling (jogos interativos).
        
        print("Ainda não implementado")

class AgenteAmplitude(Agente):
    """
    Para seu jogo, sua equipe está interessada em implementar um *agente com objetivos*.
    Para tal, veja a implementação de `AgenteComObjetivo` (`agentes-por-capacidades.py`) 
    e combine-o com a implementação de busca em amplitude (`buscas-cegas.py`), 
    implementando a classe `AgenteAmplitude` para seu jogo.
    """
    sequencia = 0
    
    def __init__(self):
        # Uma sequencia de acoes, inicialmente vazia
        self.seq = []
        # Um objetivo, inicialmente nulo
        self.objetivo = None
        self.estado = None
        self.tipo_agente = 'AGENTE_AMPLITUDE'
        self.__class__.sequencia += 1
        self.id = self.__class__.sequencia

    def get_id(self):
        return self.id

    def escolherProximaAcao(self):
        # Se seq estiver vazia
        if not self.seq:
            self.formularEstadoAtual()
            self.busca()
            if not self.seq:
                return None
        acao = self.seq.pop(0)
        return acao
    
    def formularEstadoAtual(self, jogavel):
        ''' Instancia objeto com base em AbstractEstado representando o estado
        atual e as corretas funções de navegação pelo estado, bem como o teste
        de objetivo e a função de custo.
        
        Ao final, self.estado deve estar preenchido.
        '''
        #self.estado = espaco_estados.EstadosLabirintite.estado_atual(jogavel)

        pass
    
    def busca(self):
        ''' Monta uma nova sequencia de acoes para resolver o problema atual.
        
            Ao final, self.seq deve conter uma lista de acoes.
        '''
        pass

    #@abstractmethod
    def adquirirPercepcao(self, ambiente_perceptivel, jogo):
        ''' Forma uma percepcao interna por meio de seus sensores, a partir das
        informacoes de um objeto de visao de mundo.

        Pega espaço de estados
        '''
        #Diferente de um humano, o robo não olha a tela
        #Ele deve analisar a matriz e gerar o espaço de estados

        objetivo = jogo.objetivo
        novo_espaco_estados = espaco_estados.EstadosLabirintite()
        
        jogo.espaco_estados = novo_espaco_estados
        

        return
    
    #@abstractmethod
    def escolherProximaAcao(self):
        ''' Escolhe proxima acao, com base em seu entendimento do mundo, a partir
        das percepções anteriores.
        '''
        return
    

class AgenteProfundidade(Agente):
    
    
    #@abstractmethod
    def adquirirPercepcao(self, percepcao_mundo):
        ''' Forma uma percepcao interna por meio de seus sensores, a partir das
        informacoes de um objeto de visao de mundo.
        '''
        return
    
    #@abstractmethod
    def escolherProximaAcao(self):
        ''' Escolhe proxima acao, com base em seu entendimento do mundo, a partir
        das percepções anteriores.
        '''
        return 

class AgenteAprofundamentoIterativo(Agente):

    def adquirirPercepcao(ambiente_perceptivel, jogo):
        ''' Forma uma percepcao interna por meio de seus sensores, a partir das
        informacoes de um objeto de visao de mundo.

        Pega espaço de estados
        '''
        #Diferente de um humano, o robo não olha a tela
        #Ele deve analisar a matriz e gerar o espaço de estados

        objetivo = jogo.objetivo
        novo_espaco_estados = espaco_estados.EstadosLabirintite()
        
        jogo.espaco_estados = novo_espaco_estados
        

        return
    
    #@abstractmethod
    def escolherProximaAcao(self):
        ''' Escolhe proxima acao, com base em seu entendimento do mundo, a partir
        das percepções anteriores.
        '''
        return
    
def construir_agente(tipo_agente):
    """ Método factory para uma instância Agente arbitrária, de acordo com os
    paraâmetros. Pode-se mudar à vontade a assinatura do método.
    """
    
    if tipo_agente == 'AGENTE_HUMANO':
        agente = AgenteHumano()

    elif tipo_agente == 'AGENTE_AMPLITUDE':
        agente = AgenteAmplitude()

    elif tipo_agente == 'AGENTE_PROFUNDIDADE':
        agente = AgenteProfundidade()

    elif tipo_agente == 'AGENTE_APROFUNDAMENTO_ITERATIVO':
        agente = AgenteAprofundamentoIterativo()

    else:
        raise print("Tipo de agente desconhecido. Por favor escolha HUMANO ou ROBO.")
    
    return agente