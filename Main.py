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
MERGE_SPRITES = False

ASSET_PAREDE = "bg.png"
ASSET_JOGADOR = "tite/sideD.png"
ASSET_SAIDA = "saida.png"
ASSET_EXT_MID = "wall_mid.png"
ASSET_EXT_LAT_MID_D = "wall_side_mid_left.png"
ASSET_EXT_LAT_MID_E = "wall_side_mid_right.png"
ASSET_EXT_LAT_INF_E = "wall_side_top_left.png"
ASSET_EXT_LAT_INF_D = "wall_side_top_right.png"


## Tela ##
LARGURA_TELA = 800
ALTURA_TELA = 690
TITULO_TELA = "Labirintite"
CAMPO_VISAO = 10

## Outros ##
# A velocidade de movimento é o tamnho do sprite
# para o personagem não "Empacar" em meio bloco
VELOCIDADE_MOVIMENTO = TAMANHO_SPRITE

## Deve ser um numero impar ##
ALTURA_LABIRINTO = 11
LARGURA_LABIRINTO = 11

# Tiles do mapa do jogo
TILE_VAZIO = 0
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
TILE_PREENCHIDO = 123
TILE_SAIDA = 99

# Faz uma "matriz" usando uma lista de lista
def criarGrade(largura, altura):
    grade = []
    for linha in range(altura):
        grade.append([])
        for coluna in range(largura):
            if ((coluna % 2) == 1) and ((linha % 2) == 1):
                grade[linha].append(TILE_VAZIO)
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
                grade[linha].append(TILE_PREENCHIDO)
            else:
                grade[linha].append(TILE_PREENCHIDO)
    # ult = copy.copy(grade[len(grade)-1])
    # ult = [TILE_EXT_MID for _ in ult]
    # gradeaux = []
    # gradeaux.append(ult)
    # gradeaux.append(x for x in grade)


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
                lab[max(y, yy) * 2][x * 2 + 1] = TILE_VAZIO
            if yy == y:
                lab[y * 2 + 1][max(x, xx) * 2] = TILE_VAZIO

            andarilho_bebado(xx, yy)

    andarilho_bebado(random.randrange(largura), random.randrange(altura))

    def definir_ponto_final():
        coordenada_maxima = len(lab) - 1
        lab[coordenada_maxima - 1][coordenada_maxima] = TILE_SAIDA
    definir_ponto_final()

    return lab


class LabirintiteGame(arcade.Window):

    def __init__(self, largura, altura, titulo):
        # Inicializador
        super().__init__(largura, altura, titulo)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.jogador_list = None
        self.wall_list = None

        # Player info
        self.score = 0
        self.jogador = None

        # Physics engine
        self.physics_engine = None

        # Used to scroll
        self.view_bottom = 0
        self.view_left = 0

        # Time to process
        self.processing_time = 0
        self.draw_time = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.jogador_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.saida_list = arcade.SpriteList()

        self.score = 0

        # Cria o labirinto
        labirinto = criaLabirinto(LARGURA_LABIRINTO, ALTURA_LABIRINTO)

        def preenchedor(asset, asset_list, issaida=False):
            bit = arcade.Sprite(asset, ESCALA_SPRITE)
            bit.center_x = column * TAMANHO_SPRITE + TAMANHO_SPRITE / 2
            bit.center_y = row * TAMANHO_SPRITE + TAMANHO_SPRITE / 2
            asset_list.append(bit)
            if(issaida):
                global SAIDA_X
                SAIDA_X = bit.center_x
                global SAIDA_Y
                SAIDA_Y = bit.center_y

        # Create sprites based on 2D grid
        if not MERGE_SPRITES:
            # This is the simple-to-understand method. Each grid location
            # is a sprite.
            for row in range(ALTURA_LABIRINTO):
                for column in range(LARGURA_LABIRINTO):
                    localizacao = labirinto[row][column]
                    if localizacao == TILE_PREENCHIDO:
                        preenchedor(ASSET_PAREDE, self.wall_list)
                    if localizacao == TILE_SAIDA:
                        preenchedor(ASSET_SAIDA, self.saida_list, True)
                    if localizacao == TILE_EXT_MID:
                        preenchedor(ASSET_EXT_MID, self.wall_list)
                    if localizacao == TILE_EXT_LAT_MID_D:
                        preenchedor(ASSET_EXT_LAT_MID_D, self.wall_list)
                    if localizacao == TILE_EXT_LAT_MID_E:
                        preenchedor(ASSET_EXT_LAT_MID_E, self.wall_list)
                    if localizacao == TILE_EXT_LAT_INF_E:
                        preenchedor(ASSET_EXT_LAT_INF_E, self.wall_list)
                    if localizacao == TILE_EXT_LAT_INF_D:
                        preenchedor(ASSET_EXT_LAT_INF_D, self.wall_list)
        else:
            # This uses new Arcade 1.3.1 features, that allow me to create a
            # larger sprite with a repeating texture. So if there are multiple
            # cells in a row with a wall, we merge them into one sprite, with a
            # repeating texture for each cell. This reduces our sprite count.
            for row in range(ALTURA_LABIRINTO):
                column = 0
                while column < len(labirinto):
                    while column < len(labirinto) and labirinto[row][column] == 0:
                        column += 1
                    start_column = column
                    while column < len(labirinto) and labirinto[row][column] == 1:
                        column += 1
                    end_column = column - 1

                    column_count = end_column - start_column + 1
                    column_mid = (start_column + end_column) / 2

                    wall = arcade.Sprite(ASSET_PAREDE, ESCALA_SPRITE,
                                         repeat_count_x=column_count)
                    wall.center_x = column_mid * TAMANHO_SPRITE + TAMANHO_SPRITE / 2
                    wall.center_y = row * TAMANHO_SPRITE + TAMANHO_SPRITE / 2
                    wall.width = TAMANHO_SPRITE * column_count
                    self.wall_list.append(wall)

                    #saida = arcade.Sprite(ASSET_SAIDA, ESCALA_SPRITE, re)

        # Definições do objeto jogador
        self.jogador = arcade.Sprite(ASSET_JOGADOR, ESCALA_SPRITE)
        self.jogador.append_texture(arcade.load_texture("tite/up.png", scale=ESCALA_SPRITE))
        self.jogador.append_texture(arcade.load_texture("tite/down.png", scale=ESCALA_SPRITE))
        self.jogador.append_texture(arcade.load_texture("tite/sideE.png", scale=ESCALA_SPRITE))
        self.jogador.append_texture(arcade.load_texture("tite/sideD.png", scale=ESCALA_SPRITE))
        self.jogador_list.append(self.jogador)

        def definir_ponto_inicio():
            # Laço para definir o ponto de inicio do jogador
            coordenada_maxima = int(LARGURA_LABIRINTO * TAMANHO_SPRITE)
            for i in range(0, coordenada_maxima):
                self.jogador.center_x = i
                self.jogador.center_y = i

                # Verifica se esta em uma parede
                hits_parede = arcade.check_for_collision_with_list(self.jogador, self.wall_list)
                if len(hits_parede) == 0:
                    break
        definir_ponto_inicio()
        self.color = arcade.color
        self.physics_engine = arcade.PhysicsEngineSimple(self.jogador, self.wall_list)

        # Set the background color
        #cor_fundo = self.color(34,34,34,255)
        arcade.set_background_color((34,34,34,255))

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0
        print(f"Total wall blocks: {len(self.wall_list)}")

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        # Draw all the sprites.
        self.wall_list.draw()
        self.jogador_list.draw()
        self.saida_list.draw()

        # Draw info on the screen
        sprite_count = len(self.wall_list)

        output = f"Sprite Count: {sprite_count}"
        arcade.draw_text(output,
                         self.view_left + 20,
                         ALTURA_LABIRINTO - 20 + self.view_bottom,
                         arcade.color.WHITE, 16)

        output = f"Drawing time: {self.draw_time:.3f}"
        arcade.draw_text(output,
                         self.view_left + 20,
                         ALTURA_TELA - 40 + self.view_bottom,
                         arcade.color.WHITE, 16)

        output = f"Processing time: {self.processing_time:.3f}"
        arcade.draw_text(output,
                         self.view_left + 20,
                         ALTURA_TELA - 60 + self.view_bottom,
                         arcade.color.WHITE, 16)

        self.draw_time = timeit.default_timer() - draw_start_time

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP:
            self.jogador.change_y = VELOCIDADE_MOVIMENTO
            self.jogador.set_texture(1)

        elif key == arcade.key.DOWN:
            self.jogador.change_y = -(VELOCIDADE_MOVIMENTO)
            self.jogador.set_texture(2)

        elif key == arcade.key.LEFT:
            self.jogador.change_x = -(VELOCIDADE_MOVIMENTO)
            self.jogador.set_texture(3)

        elif key == arcade.key.RIGHT:
            self.jogador.change_x = VELOCIDADE_MOVIMENTO
            self.jogador.set_texture(4)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

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

        print("Jogador X", jogador_X)
        print("Jogador Y", jogador_Y)

        print("Saida x", SAIDA_X)
        print("Saida y", SAIDA_Y)
        print("--")

        if (jogador_X == SAIDA_X) and (jogador_Y == SAIDA_Y):
            print("Achoooo")

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_bndry = self.view_left + CAMPO_VISAO
        if self.jogador.left <= left_bndry:
            self.view_left -= left_bndry - self.jogador.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + LARGURA_TELA - CAMPO_VISAO
        if self.jogador.right >= right_bndry:
            self.view_left += self.jogador.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + ALTURA_TELA - CAMPO_VISAO
        if self.jogador.top >= top_bndry:
            self.view_bottom += self.jogador.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + CAMPO_VISAO
        if self.jogador.bottom <= bottom_bndry:
            self.view_bottom -= bottom_bndry - self.jogador.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                LARGURA_TELA + self.view_left,
                                self.view_bottom,
                                LARGURA_TELA + self.view_bottom)

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time
        arcade.pause(0.05)


def main():
    """ Main method """
    window = LabirintiteGame(LARGURA_TELA, ALTURA_TELA, TITULO_TELA)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
