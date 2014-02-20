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

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

    def interact(self, player):
        for item in player.inventory:
            if type(item) == Gem and (self.x == 2 and self.y == 3):
                GAME_BOARD.del_el(2, 3)

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
        GAME_BOARD.draw_msg("Oh no! Ryan Reynolds is trying to step in for Ryan Gosling's photoshoot! Use the gem's super strength. Use your new strength to crush a boulder, and defeat Ryan Reynolds!")

class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = True

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True

    def interact(self, player): 
        for item in player.inventory:
            if type(item) == Key:
                player.inventory.append(self)
                GAME_BOARD.draw_msg('There\'s a message in the chest! "Use wood from a tree to cross the river."')
                GAME_BOARD.del_el(8, 8)
                openchest = ChestOpen()
                GAME_BOARD.register(openchest)
                GAME_BOARD.set_el(8, 8, openchest)

class ChestOpen(GameElement):
    IMAGE = "ChestOpen"
    SOLID = True

class ShortTree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True

class TallTree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

class SpecialTallTree(GameElement):
    IMAGE = "SpecialTallTree"
    SOLID = True

    def interact(self, player):
        for item in player.inventory:
            if type(item) == Chest:
                player.inventory.append(self)
                GAME_BOARD.del_el(5,6)
                GAME_BOARD.draw_msg("You built a canoe! Hey, remember that canoe scene from the Notebook? Cross the river and find the Blue Gem.")
                boat = Boat()
                GAME_BOARD.register(boat)
                GAME_BOARD.set_el(6, 5, boat)

class UglyTree(GameElement):
    IMAGE = "UglyTree"
    SOLID = True

    def interact(self, player):
        for item in player.inventory:
            if type(item) == Girl:
                GAME_BOARD.draw_msg("You have found the key!")
                GAME_BOARD.del_el(0, 6)
                keys = Key()
                GAME_BOARD.register(keys)
                GAME_BOARD.set_el(5, 7, keys)

class Boat(GameElement):
    IMAGE = "Boat"
    SOLID = False

class Water(GameElement):
    IMAGE = "WaterBlock"
    SOLID = True

    def interact(self, player):
        for item in player.inventory:
            if type(item) == SpecialTallTree and (self.x == 6 and self.y == 5):
                self.SOLID = False

# class SpecialWaterBlock(GameElement):
#     IMAGE = "WaterBlock"
#     def interact(self, player):
#         for item in player.inventory:
#             if type(item) == SpecialTallTree:
#                 self.SOLID = False

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a key! Now go use it to unlock the chest!")

class Stone(GameElement):
    IMAGE = "StoneBlock"
    SOLID = True

    def interact(self, player):
        for item in player.inventory:
            if type(item) == Ava and (self.x == 7 and self.y == 0):
                GAME_BOARD.del_el(7, 0)
                player.inventory.append(self)
        
        for item in player.inventory:
            if type(item) == Stone and (self.x == 8 and self.y == 0):
                GAME_BOARD.del_el(8, 0)

class Boy(GameElement):
    IMAGE = "Boy"
    SOLID = True

    def interact(self, player):
        GAME_BOARD.draw_msg("Hey girl, fork my heart because I'm ready to commit.")
        GAME_BOARD.del_el(8, 1)
        heart = Heart()
        GAME_BOARD.register(heart)
        GAME_BOARD.set_el(8, 1, heart)

class Girl(GameElement):
    IMAGE = "Girl"
    SOLID = True

    def interact(self, player):
        GAME_BOARD.draw_msg("To help Ryan, search for a key to unlock the chest.")
        speech_bubble = SpeechBubble()
        GAME_BOARD.register(speech_bubble)
        GAME_BOARD.set_el(3, 7, speech_bubble)
        player.inventory.append(self)

class SpeechBubble(GameElement):
    IMAGE = "SpeechBubble"
    SOLID = False

class Ava(GameElement):
    IMAGE = "Princess"
    SOLID = False

    def interact(self, player):
        GAME_BOARD.draw_msg("You have defeated me! Now you can go save Ryan from the tower I locked him in.")
        player.inventory.append(self)


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    # ROCKS
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

    for rock in rocks:
        print rock

    # PLAYER
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 9, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("Help Ryan Gosling! He's trapped and can't get to his Sexiest Man Alive photoshoot!")

    # GEM
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(0, 1, gem)

    # CHEST
    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(8, 8, chest)

    # SHORT TREES
    short_tree_positions = [
            (9, 8),
            (9, 9),
            (9, 7),
            (8, 7),
            (7, 7),
            (7, 8),
            (7, 9),
            (8, 9)
        ]

    short_trees = []

    for pos in short_tree_positions:
        short_tree = ShortTree()
        GAME_BOARD.register(short_tree)
        GAME_BOARD.set_el(pos[0], pos[1], short_tree)
        short_trees.append(short_tree)

    for short_tree in short_trees:
        print short_tree

    short_trees[-1].SOLID = False
    short_trees[-2].SOLID = False
    

    # TALL TREES
    tall_tree_positions = [
            (3, 6),
            (4, 6),
            (1, 8),
            (4, 8),
            (3, 9),
        ]

    tall_trees = []

    for pos in tall_tree_positions:
        tall_tree = TallTree()
        GAME_BOARD.register(tall_tree)
        GAME_BOARD.set_el(pos[0], pos[1], tall_tree)
        tall_trees.append(tall_tree)

    # SPECIAL TALL TREE
    special_tall_tree = SpecialTallTree()
    GAME_BOARD.register(special_tall_tree)
    GAME_BOARD.set_el(5, 6, special_tall_tree)

    # UGLY TREE
    ugly_tree = UglyTree()
    GAME_BOARD.register(ugly_tree)
    GAME_BOARD.set_el(0, 6, ugly_tree)

    # STONE BLOCKS
    stone_positions = [
            (9, 0),
            (7, 1),
            (7, 2),
            (9, 1),
            (9, 2),
            (8, 2),
            (7, 0),
            (8, 0),
        ]

    stones = []

    for pos in stone_positions:
        stone_wall = Stone()
        GAME_BOARD.register(stone_wall)
        GAME_BOARD.set_el(pos[0], pos[1], stone_wall)
        stones.append(stone_wall)

    for stone_wall in stones:
        print stone_wall


    # WATER BLOCKS
    water_positions = [
            (0, 5),
            (1, 5),
            (2, 5),
            (3, 5),
            (4, 5),
            (5, 5),
            (6, 5),
            (7, 5),
            (8, 5),
            (9, 5)
        ]

    water_blocks = []

    for pos in water_positions:
        water = Water()
        GAME_BOARD.register(water)
        GAME_BOARD.set_el(pos[0], pos[1], water)
        water_blocks.append(water)

    for water in water_blocks:
        print water

    # BOY
    boy = Boy()
    GAME_BOARD.register(boy)
    GAME_BOARD.set_el(8, 1, boy)

    # HELPER GIRL
    girl = Girl()
    GAME_BOARD.register(girl)
    GAME_BOARD.set_el(2, 8, girl)

    # Ava Enemy
    ava = Ava()
    GAME_BOARD.register(ava)
    GAME_BOARD.set_el(2, 2, ava)


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