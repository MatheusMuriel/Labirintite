""" 
EnGeni de Fisica

Sobrescreve o - PhysicsEngineSimple - do arcade 
para resolver o bug de movimentação na parede

"""
import arcade.physics_engines
import copy
from arcade.geometry import check_for_collision_with_list
from arcade.geometry import check_for_collision
from arcade.sprite import Sprite
from arcade.sprite_list import SpriteList


class Zepelim(arcade.physics_engines.PhysicsEngineSimple):
    """
    Essa classe move tudo e cuidar das colisões.
    """

    def __init__(self, player_sprite: Sprite, walls: SpriteList):
        """
        Constructor.
        """
        assert(isinstance(player_sprite, Sprite))
        assert(isinstance(walls, SpriteList))
        self.player_sprite = player_sprite
        self.walls = walls

    def update(self):
        """
        Move os objetos, verifica e resolve as colisões.
        """
        player_aux = copy.deepcopy(self.player_sprite)

        """
        Movimentação do eixo X
        """
        player_aux.center_x += player_aux.change_x

        # Check for wall hit
        hit_list = \
            check_for_collision_with_list(player_aux,
                                          self.walls)
        # If we hit a wall, move so the edges are at the same point
        if len(hit_list) > 0:
            self.player_sprite.change_x = 0
        else:
            self.player_sprite.center_x += self.player_sprite.change_x

        """
        Movimentação do eixo Y
        """
        player_aux.center_y += player_aux.change_y

        # Check for wall hit
        hit_list = \
            check_for_collision_with_list(player_aux,
                                          self.walls)

        # If we hit a wall, move so the edges are at the same point
        if len(hit_list) > 0:
            self.player_sprite.change_y = 0
        else:
            self.player_sprite.center_y += self.player_sprite.change_y

        #Limpeza de variaveis
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0