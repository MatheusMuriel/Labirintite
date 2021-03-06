"""
Projeto de Inteligencia Artificial
"""
import copy
import random
import time
import arcade
import timeit
import os
import engine_zepelim

# Variaveis Globais

## Sprites ##
TAMANHO_NATIVO_SPRITE = 128
ESCALA_SPRITE = 0.25
TAMANHO_SPRITE = TAMANHO_NATIVO_SPRITE * ESCALA_SPRITE

ASSET_PAREDE = "cenario/paredeinterna.png"
ASSET_CHAO = "cenario/bg.png"
ASSET_JOGADOR = "tite/sideD.png"
ASSET_SAIDA = "cenario/saida.png"
ASSET_EXT_MID = "cenario/wall_mid.png"
ASSET_EXT_LAT_MID_D = "cenario/lateral_externo_esquerdo.png"
ASSET_EXT_LAT_MID_E = "cenario/lateral_externo_direito.png"
ASSET_EXT_LAT_INF_E = "cenario/wall_side_top_left.png"
ASSET_EXT_LAT_INF_D = "cenario/wall_side_top_right.png"
ASSET_INT_SUP = "cenario/quina3.png"
ASSET_INT_CANTO = "cenario/wall_mid.png"
ASSET_INT_CANTO_DIR = "cenario/internacantodireito.png"
ASSET_INT_CANTO_ESQ = "cenario/internacantoesquerdo.png"
ASSET_QUINA1 = "cenario/quina1.png"
ASSET_QUINA1esp = "cenario/quina1ESP.png"
ASSET_QUINA2 = "cenario/quina2.png"
ASSET_QUINA2ESP = "cenario/quina2esp.png"
ASSET_CRUZAMENTO = "cenario/cruzamento.png"


## Tela ##
LARGURA_TELA = 500
ALTURA_TELA = 500
TITULO_TELA = "Labirintite"
CAMPO_VISAO = 150

## Outros ##
# A velocidade de movimento é o tamnho do sprite
# para o personagem não "Empacar" em meio bloco
VELOCIDADE_MOVIMENTO = TAMANHO_SPRITE

# Deve ser um numero impar.
ALTURA_LABIRINTO = 21
LARGURA_LABIRINTO = 21

# Tiles do mapa do jogo
TILE_CHAO = 0
VIEWPORT_MARGIN = 40

# Parede externa
TILE_EXT_MID = 1
TILE_EXT_LAT_MID_D = 2
TILE_EXT_LAT_MID_E = 3
TILE_EXT_CNT_INF_E = 4
TILE_EXT_CNT_INF_D = 5
TILE_EXT_CNT_SUP_E = 6
TILE_EXT_CNT_SUP_D = 7
TILE_EXT_LAT_INF_E = 8
TILE_EXT_LAT_INF_D = 9

# Parede interna
TILE_PAREDE_INTERNA = 123
TILE_SAIDA = 99

SAIDA_X = 0
SAIDA_Y = 0

# Faz uma "matriz" usando uma lista de lista
def criarGrade(largura, altura):
    grade = []
    for linha in range(altura):
        grade.append([])
        for coluna in range(largura):
            if ((coluna % 2) == 1) and ((linha % 2) == 1):
                grade[linha].append(TILE_CHAO)
            elif (coluna == 0 ):
                # Condição verdadeira se for a primeira coluna
                if linha == 0:
                    grade[linha].append(TILE_EXT_LAT_INF_E)
                else:
                    grade[linha].append(TILE_EXT_LAT_MID_D)
            elif (coluna.__index__() == (largura - 1)):
                # Condição verdadeira se for a ultima coluna
                if linha == 0:
                    grade[linha].append(TILE_EXT_LAT_INF_D)
                else:
                    grade[linha].append(TILE_EXT_LAT_MID_E)
            elif (linha == 0):
                # Condição verdadeira se for a primeira linha
                if len(grade[linha]) > 0:
                    grade[linha].append(TILE_EXT_MID)
            elif (linha.__index__() == (altura-1)):
                # Ultima linha
                if len(grade[linha]) > 0:
                    grade[linha].append(TILE_EXT_MID)

            elif (coluna == largura - 1) or (linha == altura - 1):
                grade[linha].append(TILE_PAREDE_INTERNA)
            else:
                grade[linha].append(TILE_PAREDE_INTERNA)

    return grade

# Usando algoritmo Depth First
def criaLabirinto(lab_largura, lab_altura):
    lab = criarGrade(lab_largura, lab_altura)

    largura = (len(lab[0]) - 1) // 2
    altura = (len(lab) - 1) // 2
    visita = [[0] * largura + [1] for _ in range(altura)] + [[1] * (largura + 1)]

    # Algoritmo para andar aleatoriamente no labirinto
    def andarilho_bebado(x, y):
        visita[y][x] = 1

        # Possibilidades
        a = (x - 1, y)
        b = (x + 1, y)
        c = (x, y + 1)
        d = (x, y - 1)
        possibilidades = [a, b, c, d]

        random.shuffle(possibilidades)  # Embaralha

        for (xx, yy) in possibilidades:
            if visita[yy][xx]:
                continue
            if xx == x:
                lab[max(y, yy) * 2][x * 2 + 1] = TILE_CHAO
            if yy == y:
                lab[y * 2 + 1][max(x, xx) * 2] = TILE_CHAO

            andarilho_bebado(xx, yy)

    andarilho_bebado(random.randrange(largura), random.randrange(altura))

    def definir_ponto_final():
        coordenada_maxima = len(lab) - 1
        lab[coordenada_maxima - 1][coordenada_maxima] = TILE_SAIDA
    definir_ponto_final()

    return lab

class LabirintiteGame(arcade.Window):

    def __init__(self, largura, altura, titulo):
        # Inicializador.
        super().__init__(largura, altura, titulo) #Abre a janela

        # Sprite lists
        self.jogador_objeto = None
        self.parede_list = None
        self.saida_list = None
        self.saida = None
        self.chao_list = None
        self.jogador_x = None
        self.jogador_y = None

        largura, altura = self.get_size()
        self.set_viewport(0, largura, 0, altura)

        # Engine de Fisica
        self.physics_engine = None

        # Usado para mover o campo de visao
        self.visao_inferior = 0
        self.visao_esquerda = 0

    """ Setup e inicialização de variaveis. """
    def setup(self):
        # Lista de Sprites
        self.parede_list = arcade.SpriteList()
        self.saida_list = arcade.SpriteList()
        self.chao_list = arcade.SpriteList()
        self.score = 0
        self.total_time = 0.0
        self.saida = None

        # Cria o labirinto
        self.labirinto = criaLabirinto(ALTURA_LABIRINTO, ALTURA_LABIRINTO)

        # Metodo responsavel por definir o sprite e suas cordenadas
        # Grava tudo na lista de Sprites para dps o metodo on_draw renderizar
        # OBS: Ultimo parametro opcional, é um tratamento especial para o ponto
        # de saida do labirinto.
        def preenchedor(asset, asset_list, issaida=False):
            bit = arcade.Sprite(asset, ESCALA_SPRITE)
            bit.center_x = coluna * TAMANHO_SPRITE + TAMANHO_SPRITE / 2
            bit.center_y = linha * TAMANHO_SPRITE + TAMANHO_SPRITE / 2
            asset_list.append(bit)
            if(issaida):
                global SAIDA_X
                SAIDA_X = bit.center_x
                global SAIDA_Y
                SAIDA_Y = bit.center_y
                self.saida = [linha,coluna] # "LETRA" , NUMERO

        # Define os Sprites com base no grid
        # Usa tecnica de Tilemap
        for linha in range(ALTURA_LABIRINTO):
            for coluna in range(LARGURA_LABIRINTO):
                localizacao = self.labirinto[linha][coluna]
                lateralEsq = self.labirinto[linha][coluna - 1]
                lateralDir = self.labirinto[linha][coluna + 1] if coluna < LARGURA_LABIRINTO-1 else -100
                superior = self.labirinto[linha + 1][coluna] if linha < ALTURA_LABIRINTO-1 else -100
                inferior = self.labirinto[linha - 1][coluna]

                if localizacao == TILE_CHAO:
                    preenchedor(ASSET_CHAO, self.chao_list)

                if localizacao == TILE_PAREDE_INTERNA:
                    preenchedor(ASSET_CHAO, self.chao_list)

                    if lateralEsq == TILE_EXT_LAT_MID_D:
                        preenchedor(ASSET_EXT_MID, self.parede_list)

                    elif lateralDir == TILE_EXT_LAT_MID_E and superior == TILE_CHAO and inferior == TILE_CHAO:
                        preenchedor(ASSET_EXT_MID, self.parede_list)

                    elif superior == TILE_CHAO and inferior == TILE_CHAO and lateralEsq == TILE_PAREDE_INTERNA and lateralDir == TILE_PAREDE_INTERNA:
                        preenchedor(ASSET_EXT_MID, self.parede_list)

                    elif superior == TILE_PAREDE_INTERNA and inferior == TILE_CHAO and lateralDir == TILE_PAREDE_INTERNA and lateralEsq == TILE_PAREDE_INTERNA:
                        preenchedor(ASSET_INT_CANTO, self.parede_list)

                    elif superior == TILE_CHAO and inferior == TILE_CHAO and lateralEsq == TILE_PAREDE_INTERNA and lateralDir == TILE_CHAO:
                        preenchedor(ASSET_INT_CANTO_DIR, self.parede_list)

                    elif superior == TILE_CHAO and inferior == TILE_CHAO and lateralEsq == TILE_CHAO and lateralDir == TILE_PAREDE_INTERNA:
                        preenchedor(ASSET_INT_CANTO_ESQ, self.parede_list)

                    elif superior == TILE_PAREDE_INTERNA and inferior == TILE_PAREDE_INTERNA and lateralEsq == TILE_CHAO and lateralDir == TILE_PAREDE_INTERNA:
                        preenchedor(ASSET_QUINA1, self.parede_list)

                    elif superior == TILE_PAREDE_INTERNA and inferior == TILE_PAREDE_INTERNA and lateralEsq == TILE_PAREDE_INTERNA and lateralDir == TILE_CHAO:
                        preenchedor(ASSET_QUINA1esp, self.parede_list)

                    elif superior == TILE_PAREDE_INTERNA and inferior == TILE_CHAO and lateralEsq == TILE_PAREDE_INTERNA and lateralDir == TILE_CHAO:
                        preenchedor(ASSET_QUINA2, self.parede_list)

                    elif superior == TILE_PAREDE_INTERNA and inferior == TILE_CHAO and lateralEsq == TILE_CHAO and lateralDir == TILE_PAREDE_INTERNA:
                        preenchedor(ASSET_QUINA2ESP, self.parede_list)

                    elif superior == TILE_CHAO and lateralDir == TILE_CHAO and inferior == TILE_PAREDE_INTERNA and lateralEsq == TILE_PAREDE_INTERNA:
                        preenchedor(ASSET_QUINA1esp, self.parede_list)

                    elif superior == TILE_CHAO and lateralDir == TILE_PAREDE_INTERNA and inferior == TILE_PAREDE_INTERNA and lateralEsq == TILE_CHAO:
                        preenchedor(ASSET_QUINA1, self.parede_list)

                    elif superior == TILE_CHAO and lateralDir == TILE_PAREDE_INTERNA and inferior == TILE_PAREDE_INTERNA and lateralEsq == TILE_PAREDE_INTERNA:
                        preenchedor(ASSET_INT_SUP, self.parede_list)

                    elif superior == TILE_PAREDE_INTERNA and inferior == TILE_PAREDE_INTERNA and lateralEsq == TILE_PAREDE_INTERNA and lateralDir == TILE_PAREDE_INTERNA:
                        preenchedor(ASSET_CRUZAMENTO, self.parede_list)

                    else:
                        preenchedor(ASSET_PAREDE, self.parede_list)

                if localizacao == TILE_SAIDA:
                    preenchedor(ASSET_SAIDA, self.saida_list, True)

                if localizacao == TILE_EXT_MID:
                    if inferior == TILE_PAREDE_INTERNA:
                        preenchedor(ASSET_INT_SUP, self.parede_list)
                    else:
                        preenchedor(ASSET_EXT_MID, self.parede_list)

                if localizacao == TILE_EXT_LAT_MID_D:
                    preenchedor(ASSET_EXT_LAT_MID_D, self.parede_list)

                if localizacao == TILE_EXT_LAT_MID_E:
                    preenchedor(ASSET_EXT_LAT_MID_E, self.parede_list)

                if localizacao == TILE_EXT_LAT_INF_E:
                    preenchedor(ASSET_EXT_LAT_INF_E, self.parede_list)

                if localizacao == TILE_EXT_LAT_INF_D:
                    preenchedor(ASSET_EXT_LAT_INF_D, self.parede_list)

        # Definições do objeto jogador
        # Os append_texture carregam os sprites do jogador de frente, lado e costas
        self.jogador_objeto = arcade.Sprite(ASSET_JOGADOR, ESCALA_SPRITE)
        self.jogador_objeto.append_texture(arcade.load_texture("tite/up.png", scale=ESCALA_SPRITE))
        self.jogador_objeto.append_texture(arcade.load_texture("tite/down.png", scale=ESCALA_SPRITE))
        self.jogador_objeto.append_texture(arcade.load_texture("tite/sideE.png", scale=ESCALA_SPRITE))
        self.jogador_objeto.append_texture(arcade.load_texture("tite/sideD.png", scale=ESCALA_SPRITE))

        """
        Metodo que define o ponto de inicio do jogador
        Ele define usando o ponto mais baixo do mapa (inferior esquerdo)
        em que não seja uma parede
        """
        def definir_ponto_inicio():
            coordenada_maxima = int(LARGURA_LABIRINTO * TAMANHO_SPRITE)

            for i in range(0, coordenada_maxima):
                self.jogador_objeto.center_x = i
                self.jogador_objeto.center_y = i

                # Verifica se esta em uma parede
                hits_parede = arcade.check_for_collision_with_list(self.jogador_objeto, self.parede_list)
                if len(hits_parede) == 0:
                    break

        definir_ponto_inicio()

        # Define a fisica para o jogo.
        self.physics_engine = engine_zepelim.Zepelim(self.jogador_objeto, self.parede_list)

        # Define a cor de fundo.
        arcade.set_background_color((34, 34, 34, 255))

        # Define os limites do campo de visao
        self.visao_esquerda = 0
        self.visao_inferior = 0

        return

    """Metodo que renderiza a tela. """
    def on_draw(self):

        # Comando obrigatorio antes de começar a printar os sprites na tela
        arcade.start_render()

        # Printa todos os itens da lista de sprites.
        # A ordem deles faz diferença.
        self.chao_list.draw()
        self.parede_list.draw()
        self.saida_list.draw()
        self.jogador_objeto.draw()

        arcade.finish_render()
        return

    """Metodo chamado quando qualquer tecla é pressionada. """
    def on_key_press(self, tecla, modifiers):
        pass

    """Metodo chamado quando o usuario solta a tecla. """
    def on_key_release(self, key, modifiers):
        pass

    """Metodo usado pelo FrameWork para atualizar o espaço do jogo"""
    def atualiza_estado(self, direcao, diferencial_tempo):
        direcao = direcao.upper()
        
        if direcao == 'CIMA':
            self.jogador_objeto.set_texture(1)
            self.jogador_objeto.change_y = TAMANHO_SPRITE
        elif direcao == 'BAIXO':
            self.jogador_objeto.set_texture(2)
            self.jogador_objeto.change_y = -(TAMANHO_SPRITE)
        elif direcao == 'ESQUERDA':
            self.jogador_objeto.set_texture(3)
            self.jogador_objeto.change_x = -(TAMANHO_SPRITE)
        elif direcao == 'DIREITA':
            self.jogador_objeto.set_texture(4)
            self.jogador_objeto.change_x = TAMANHO_SPRITE
        else:
            return

        self.update(diferencial_tempo)

        return
    
    """ Atualiza a fisica e a visao do jogo."""
    def update(self, delta_time):
        self.physics_engine.update()

        changed = False

        # Scroll left
        left_bndry = self.visao_esquerda + CAMPO_VISAO
        if self.jogador_objeto.left <= left_bndry:
            self.visao_esquerda -= left_bndry - self.jogador_objeto.left
            changed = True

        # Scroll right
        right_bndry = self.visao_esquerda + LARGURA_TELA - CAMPO_VISAO
        if self.jogador_objeto.right >= right_bndry:
            self.visao_esquerda += self.jogador_objeto.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.visao_inferior + ALTURA_TELA - CAMPO_VISAO
        if self.jogador_objeto.top >= top_bndry:
            self.visao_inferior += self.jogador_objeto.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.visao_inferior + CAMPO_VISAO
        if self.jogador_objeto.bottom <= bottom_bndry:
            self.visao_inferior -= bottom_bndry - self.jogador_objeto.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.visao_esquerda,
                                LARGURA_TELA + self.visao_esquerda,
                                self.visao_inferior,
                                LARGURA_TELA + self.visao_inferior)

        self.total_time += delta_time

        return

    def verifica_fim(self):
        jogador_x = self.jogador_objeto.center_x
        jogador_y = self.jogador_objeto.center_y

        if jogador_x == SAIDA_X and jogador_y == SAIDA_Y:
            arcade.start_render()
            output = f"Parabéns, você ganhou!"
            arcade.draw_text(output,
                             self.visao_esquerda + 70,
                             ALTURA_TELA // 2 - 20,
                             arcade.color.RED, 18)
            arcade.finish_render()
            input("Aperte Enter para sair.")
            return True
        else:
            return False

def construtor():
    """Metodo para subistituir o metodo main, na adaptação para o framework"""
    ret_labirinto = LabirintiteGame(LARGURA_TELA, ALTURA_TELA, TITULO_TELA)
    ret_labirinto.setup()
    ret_labirinto.on_draw()
    return ret_labirinto