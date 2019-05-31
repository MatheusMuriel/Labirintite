import time
from regras_jogo import construir_jogo
from agentes import construir_agente

def ler_tempo(em_turnos=False):
    """ Se o jogo for em turnos, passe 1 (rodada), senão se o jogo for
    continuo ou estratégico, precisa.
    """
    return 1 if em_turnos else time.time()


def iniciar_jogo():
    
        # Inicializar e configurar jogo
        jogo = construir_jogo()

        jogador = construir_agente('HUMANO')
        id_jogador = jogo.registrarAgenteJogador(jogador)

        tempo_de_jogo = 0

        jogo.iniciaJogo()

        """Game loop principal."""
        while not jogo.isFim():

                # Mostrar mundo ao jogador
                ambiente_perceptivel = jogo.gerarCampoVisao()
                jogador.adquirirPercepcao(ambiente_perceptivel, jogo)

                # Decidir jogada e apresentar ao jogo
                acao = jogador.escolherProximaAcao(jogo)
                jogo.registrarProximaAcao(id_jogador, acao)

                # Atualizar jogo
                tempo_corrente = ler_tempo()
                jogo.atualizarEstado(tempo_corrente - tempo_de_jogo)
                tempo_de_jogo += tempo_corrente
        
if __name__ == '__main__':
    iniciar_jogo()