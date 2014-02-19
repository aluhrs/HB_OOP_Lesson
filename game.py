import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Horns"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))

class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a heart! You have %d items!"%(len(player.inventory)))

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True

    def interact(self, player):
        for item in player.inventory:
            if type(item) == Key:
                GAME_BOARD.draw_msg("You have unlocked the chest!")
                # self.IMAGE = "ChestOpen"
                
# open_chest = Chest("OpenChest", True)

class ChestOpen(GameElement):
    IMAGE = "ChestOpen"
    SOLID = True

class ShortTree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True

class TallTree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a key! You have %d items!" % (len(player.inventory)))

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
            (2, 1),
            (1, 2),
            (3, 2),
            (2, 3)
        ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    for rock in rocks:
        print rock

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("Jona and Ashley's Excellent Adventure")

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    heart = Heart()
    GAME_BOARD.register(heart)
    GAME_BOARD.set_el(6, 6, heart)

    openchest = ChestOpen()
    GAME_BOARD.register(openchest)
    GAME_BOARD.set_el(5, 6, openchest)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(5, 6, chest)

    keys = Key()
    GAME_BOARD.register(keys)
    GAME_BOARD.set_el(7,7, keys)

    short_tree_positions = [
            (1, 7),
            (6, 2)
        ]

    short_trees = []

    for pos in short_tree_positions:
        short_tree = ShortTree()
        GAME_BOARD.register(short_tree)
        GAME_BOARD.set_el(pos[0], pos[1], short_tree)
        short_trees.append(short_tree)

    for short_tree in short_trees:
        print short_tree

    tall_tree = TallTree()
    GAME_BOARD.register(tall_tree)
    GAME_BOARD.set_el(3,5, tall_tree)

def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"
    
    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if (-1 < next_x < GAME_WIDTH) and (-1 < next_y < GAME_HEIGHT):
            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el:
                existing_el.interact(PLAYER)

            if existing_el is None or not existing_el.SOLID:
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
