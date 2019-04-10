"""
Projeto de Inteligencia Artificial

"""

import random
import arcade
import timeit
import os

# Variaveis Globais

## Sprites ##
TAMANHO_NATIVO_SPRITE = 128
ESCALA_SPRITE = 0.25
TAMANHO_SPRITE = TAMANHO_NATIVO_SPRITE * ESCALA_SPRITE
MERGE_SPRITES = True

ASSET_PAREDE = "bg.png"
ASSET_JOGADOR = "hero.png"

## Tela ##
LARGURA_TELA = 800
ALTURA_TELA = 690
TITULO_TELA = "Labirintite"
CAMPO_VISAO = 100

## Outros ##
# A velocidade de movimento é o tamnho do sprite
# para o personagem não "Empacar" em meio bloco
VELOCIDADE_MOVIMENTO = TAMANHO_SPRITE

## Deve ser um numero impar ##
ALTURA_LABIRINTO = 31
LARGURA_LABIRINTO = 31

TILE_VAZIO = 0
TILE_PREENCHIDO = 1


def criarGrade(largura, altura):
    grade = []
    for linha in range(altura):
        grade.append([])
        for coluna in range(largura):
            if ((coluna % 2) == 1) and ((linha % 2) == 1):
                grade[linha].append(TILE_VAZIO)
            elif (coluna == 0) or (linha == 0) or (coluna == largura - 1) or (linha == altura - 1):
                grade[linha].append(TILE_PREENCHIDO)
            else:
                grade[linha].append(TILE_PREENCHIDO)
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

    return lab


class LabirintiteGame(arcade.Window):

    def __init__(self, largura, altura, titulo):
        # Inicializador
        super().__init__(largura, altura, titulo)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.player_list = None
        self.wall_list = None

        # Player info
        self.score = 0
        self.player_sprite = None

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
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.score = 0

        # Create the maze
        maze = criaLabirinto(LARGURA_LABIRINTO, ALTURA_LABIRINTO)

        # Create sprites based on 2D grid
        if not MERGE_SPRITES:
            # This is the simple-to-understand method. Each grid location
            # is a sprite.
            for row in range(ALTURA_LABIRINTO):
                for column in range(LARGURA_LABIRINTO):
                    if maze[row][column] == 1:
                        wall = arcade.Sprite(ASSET_PAREDE, ESCALA_SPRITE)
                        wall.center_x = column * TAMANHO_SPRITE + TAMANHO_SPRITE / 2
                        wall.center_y = row * TAMANHO_SPRITE + TAMANHO_SPRITE / 2
                        self.wall_list.append(wall)
        else:
            # This uses new Arcade 1.3.1 features, that allow me to create a
            # larger sprite with a repeating texture. So if there are multiple
            # cells in a row with a wall, we merge them into one sprite, with a
            # repeating texture for each cell. This reduces our sprite count.
            for row in range(ALTURA_LABIRINTO):
                column = 0
                while column < len(maze):
                    while column < len(maze) and maze[row][column] == 0:
                        column += 1
                    start_column = column
                    while column < len(maze) and maze[row][column] == 1:
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

        # Set up the player
        self.player_sprite = arcade.Sprite(ASSET_JOGADOR, ESCALA_SPRITE)
        self.player_list.append(self.player_sprite)

        # Laço para definir o ponto de inicio do jogador
        placed = False
        iterador = 0
        while not placed:

            # Randomly position
            self.player_sprite.center_x = iterador
            self.player_sprite.center_y = iterador

            # Are we in a wall?
            walls_hit = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
            if len(walls_hit) == 0:
                # Not in a wall! Success!
                placed = True
            else:
                iterador += 1

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

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
        self.player_list.draw()

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
            self.player_sprite.change_y = VELOCIDADE_MOVIMENTO

        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -(VELOCIDADE_MOVIMENTO)

        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -(VELOCIDADE_MOVIMENTO)

        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = VELOCIDADE_MOVIMENTO



    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """

        start_time = timeit.default_timer()

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_bndry = self.view_left + CAMPO_VISAO
        if self.player_sprite.left <= left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + LARGURA_TELA - CAMPO_VISAO
        if self.player_sprite.right >= right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + ALTURA_TELA - CAMPO_VISAO
        if self.player_sprite.top >= top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + CAMPO_VISAO
        if self.player_sprite.bottom <= bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
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
