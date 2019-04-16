"""
Projeto de Inteligencia Artificial

"""
import copy
import random
import arcade
import timeit
import os

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
LARGURA_TELA = 800
ALTURA_TELA = 690
TITULO_TELA = "Labirintite"
CAMPO_VISAO = 10

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
    vencedor = False
    tempo_final = 0
    def __init__(self, largura, altura, titulo):
        # Inicializador.
        super().__init__(largura, altura, titulo)

        # Sprite lists
        self.jogador_list = None
        self.parede_list = None
        self.saida_list = None
        self.chao_list = None
        largura, altura = self.get_size()
        self.set_viewport(0, largura, 0, altura)

        # Player info
        self.score = 0
        self.jogador = None

        # Engine de Fisica
        self.physics_engine = None

        # Usado para mover o campo de visao
        self.visao_inferior = 0
        self.visao_esquerda = 0

        # Tempo de processamento
        self.total_time = 0.0
        self.processing_time = 0
        self.tempo_render = 0

    """ Setup e inicialização de variaveis. """
    def setup(self):
        # Lista de Sprites
        self.jogador_list = arcade.SpriteList()
        self.parede_list = arcade.SpriteList()
        self.saida_list = arcade.SpriteList()
        self.chao_list = arcade.SpriteList()
        self.score = 0
        self.total_time = 0.0

        # Cria o labirinto
        labirinto = criaLabirinto(LARGURA_LABIRINTO, ALTURA_LABIRINTO)

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

        # Define os Sprites com base no grid
        # Usa tecnica de Tilemap
        for linha in range(ALTURA_LABIRINTO):
            for coluna in range(LARGURA_LABIRINTO):
                localizacao = labirinto[linha][coluna]
                lateralEsq = labirinto[linha][coluna - 1]
                lateralDir = labirinto[linha][coluna + 1] if coluna < LARGURA_LABIRINTO-1 else -100
                superior = labirinto[linha + 1][coluna] if linha < ALTURA_LABIRINTO-1 else -100
                inferior = labirinto[linha - 1][coluna]

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
        self.jogador = arcade.Sprite(ASSET_JOGADOR, ESCALA_SPRITE)
        self.jogador.append_texture(arcade.load_texture("tite/up.png", scale=ESCALA_SPRITE))
        self.jogador.append_texture(arcade.load_texture("tite/down.png", scale=ESCALA_SPRITE))
        self.jogador.append_texture(arcade.load_texture("tite/sideE.png", scale=ESCALA_SPRITE))
        self.jogador.append_texture(arcade.load_texture("tite/sideD.png", scale=ESCALA_SPRITE))
        self.jogador_list.append(self.jogador)

        # Metodo que define o ponto de inicio do jogador
        # Ele define usando o ponto mais baixo do mapa (inferior esquerdo)
        # em que não seja uma parede
        def definir_ponto_inicio():
            coordenada_maxima = int(LARGURA_LABIRINTO * TAMANHO_SPRITE)

            for i in range(0, coordenada_maxima):
                self.jogador.center_x = i
                self.jogador.center_y = i

                # Verifica se esta em uma parede
                hits_parede = arcade.check_for_collision_with_list(self.jogador, self.parede_list)
                if len(hits_parede) == 0:
                    break

        definir_ponto_inicio()

        # Define a fisica para o jogo.
        self.physics_engine = arcade.PhysicsEngineSimple(self.jogador, self.parede_list)

        # Define a cor de fundo.
        arcade.set_background_color((34, 34, 34, 255))

        # Define os limites do campo de visao
        self.visao_esquerda = 0
        self.visao_inferior = 0

        print(f"Total wall blocks: {len(self.parede_list)}")

    """Metodo que renderiza a tela. """
    def on_draw(self):

        # Comando obrigatorio antes de começar a printar os graficos na tela
        arcade.start_render()

        minutes = int(self.total_time)//60
        seconds = int(self.total_time) % 60
        output = f"Time: {minutes:02d}:{seconds:02d}"

        # Cronometro para conferir o tempo de renderezição.
        tempo_inicio_render = timeit.default_timer()
        # Printa todos os itens da lista de sprites.
        # A ordem deles faz diferença.
        self.chao_list.draw()
        self.parede_list.draw()
        self.saida_list.draw()
        self.jogador_list.draw()

        # Draw info on the screen
        # Printa informações na tela
        sprite_count = len(self.parede_list)


        output = f"Numero de Sprites: {sprite_count}"
        arcade.draw_text(output,
                         self.visao_esquerda + 20,
                         ALTURA_LABIRINTO - 20 + self.visao_inferior,
                         arcade.color.WHITE, 16)

        output = f"Tempo de Renderização: {self.tempo_render:.3f}"
        arcade.draw_text(output,
                         self.visao_esquerda + 20,
                         ALTURA_TELA - 40 + self.visao_inferior,
                         arcade.color.WHITE, 16)

        output = f"Tempo de processamento: {self.processing_time:.3f}"
        arcade.draw_text(output,
                         self.visao_esquerda + 20,
                         ALTURA_TELA - 60 + self.visao_inferior,
                         arcade.color.WHITE, 16)

        output = f"Tempo de jogo: {self.total_time:.2f}"
        arcade.draw_text(output,
                         self.visao_esquerda + 20,
                         ALTURA_TELA - 80 + self.visao_inferior,
                         arcade.color.WHITE, 16)

        if self.vencedor == True:
            output = f"Você ganhou, seu tempo foi de: {self.tempo_final:.2f}"
            arcade.draw_text(output,
                             self.visao_esquerda + 60,
                             ALTURA_TELA // 2 - 20,
                             arcade.color.RED, 32)
            output = f"click para frente para sair:"
            arcade.draw_text(output,
                             self.visao_esquerda + 60,
                             ALTURA_TELA // 2 - 60,
                             arcade.color.RED, 32)

        self.tempo_render = timeit.default_timer() - tempo_inicio_render

    """Metodo chamado quando qualquer tecla é pressionada. """
    def on_key_press(self, tecla, modifiers):

        if tecla == arcade.key.UP or tecla == arcade.key.W:
            self.jogador.change_y = VELOCIDADE_MOVIMENTO
            self.jogador.set_texture(1)

        elif tecla == arcade.key.DOWN or tecla == arcade.key.S:
            self.jogador.change_y = -(VELOCIDADE_MOVIMENTO)
            self.jogador.set_texture(2)

        elif tecla == arcade.key.LEFT or tecla == arcade.key.D:
            self.jogador.change_x = -(VELOCIDADE_MOVIMENTO)
            self.jogador.set_texture(3)

        elif tecla == arcade.key.RIGHT or tecla == arcade.key.A:
            self.jogador.change_x = VELOCIDADE_MOVIMENTO
            self.jogador.set_texture(4)

    """Metodo chamado quando o usuario solta a tecla. """
    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.jogador.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.jogador.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """

        start_time = timeit.default_timer()

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        jogador_X = self.jogador.center_x
        jogador_Y = self.jogador.center_y

        '''print("Jogador X", jogador_X)
        print("Jogador Y", jogador_Y)

        print("Saida x", SAIDA_X)
        print("Saida y", SAIDA_Y)
        print("--")'''

        if jogador_X == SAIDA_X and jogador_Y == SAIDA_Y and self.vencedor == False:
            self.vencedor = True
            print("Achoooo")
            self.tempo_final = self.total_time
            print("Seu tempo foi de: "'%6.2f' % self.tempo_final)

        if jogador_X == SAIDA_X + 32 and jogador_Y == SAIDA_Y:
            arcade.close_window()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_bndry = self.visao_esquerda + CAMPO_VISAO
        if self.jogador.left <= left_bndry:
            self.visao_esquerda -= left_bndry - self.jogador.left
            changed = True

        # Scroll right
        right_bndry = self.visao_esquerda + LARGURA_TELA - CAMPO_VISAO
        if self.jogador.right >= right_bndry:
            self.visao_esquerda += self.jogador.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.visao_inferior + ALTURA_TELA - CAMPO_VISAO
        if self.jogador.top >= top_bndry:
            self.visao_inferior += self.jogador.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.visao_inferior + CAMPO_VISAO
        if self.jogador.bottom <= bottom_bndry:
            self.visao_inferior -= bottom_bndry - self.jogador.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.visao_esquerda,
                                LARGURA_TELA + self.visao_esquerda,
                                self.visao_inferior,
                                LARGURA_TELA + self.visao_inferior)

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time
        arcade.pause(0.05)
        self.total_time += delta_time


def main():
    """ Main method """
    window = LabirintiteGame(LARGURA_TELA, ALTURA_TELA, TITULO_TELA)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
