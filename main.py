import time
from regras_jogo import construir_jogo
from agentes import construir_agente

def ler_tempo(em_turnos=False):
    """ Se o jogo for em turnos, passe 1 (rodada), senão se o jogo for
    continuo ou estratégico, precisa.
    """
    return 1 if em_turnos else time.time()

tipos_agentes = ['Agente_Humano',
                'Agente_Amplitude',
                'Agente_Profundidade',
                'Agente_Aprofundamento_Iterativo']
def ler_tipo_agente():
    print("Escolha um dos tipos de agente: ")
    for i in range(0,len(tipos_agentes)):
        print("{}. {}.".format(i, tipos_agentes[i]))

    input_tipo_agente = int(input("Codigo: "))

    return tipos_agentes[input_tipo_agente]

def iniciar_jogo():
    
        # Inicializar e configurar jogo
        jogo = construir_jogo()

        # Escolher o agente
        ###tipo_agente = ler_tipo_agente()
        tipo_agente = 'Agente_Amplitude'
        ###print("Vc escolheu o", tipo_agente)

        jogador = construir_agente(tipo_agente.upper())
        id_jogador = jogo.registrarAgenteJogador(jogador)

        tempo_de_jogo = 0

        jogo.iniciaJogo()

        """Game loop principal."""
        while not jogo.isFim():
                # Mostrar mundo ao jogador
                ambiente_perceptivel = jogo.gerarCampoVisao() #Matriz aqui
                jogador.adquirirPercepcao(ambiente_perceptivel, jogo) #Gera estados aqui

                # Decidir jogada e apresentar ao jogo
                acao = jogador.escolherProximaAcao(jogo, ambiente_perceptivel)
                jogo.registrarProximaAcao(id_jogador, acao)

                # Atualizar jogo
                tempo_corrente = ler_tempo()
                jogo.atualizarEstado(tempo_corrente - tempo_de_jogo)
                tempo_de_jogo += tempo_corrente
        
if __name__ == '__main__':
    iniciar_jogo()