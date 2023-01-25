# AI&P Final project [Create M6 2022-2023]
# level/level_layout.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# Imports
from level import ACCESS_FLAGS, LevelTile 

layout = """# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # O # # # #
# # . . . . . O . . . . . . . # # # # # # # # # # # # # . . & . #
# # . # # # # # # # # # # # . . . . . . . . . . . . . . . # # . #
# # . # # # # # # # # # # # . # # # # . # # # # # # # # . # # O #
# # . # # # . . . . . . . . . G . O . . # # # # # # # # . # # . #
# # . # # # . # # # # # # # . # # # # . # # # # # # # # . # # . #
# # . # # # . # . . . . # # . # # # # . # # # . . . . . . . G . #
# # . # # # . # # # # . # # . # # # # . # # # . # # # # # . # # #
# # . # # # . # # # # . . . . . . . . . . # # . # # . . . . . # #
# # . . . . . # # # # . # # # G G # # # . # # . . . . - - - . # #
# # # # # # . # # O . . # - 1 - - - - # . # # . # # . . . . . # #
# # # # # # . O # . # . # - 2 3 - - - # . # # . # # # # # . # # #
# # # # # # . . # . # . # # # # # # # # . . . . . # # # # . # # #
+ - - - - - . . . . # . . . . . . . . . . # # # . # . . . . - - +
# # # # # # . . . . # # # . . . . . # # # # # # O # . # # # # # #
# # # # # # . # # . # # # . # # # . # # # # # # . # . # # # # # #
# . . . . . . # # . # # # . - O - . # # . . . . . . . . . . . # #
# . # # # # . # # . . . . . . . . . # # . # # # # # . # # # . # #
# . # # # # . # # # G # # # # . # # # # . # # # # # O # # # . # #
# . # # # # . # # # G # # # # . # # # # . # # # # # # # # # . # #
# . . & . . . . . . . # # # # . # # # # . . . . . . . . . . . # #
# . # # # . # # # # . . . . & . G G G G . # # # # # . # # # . # #
# . # # # . # # # # . # # # # . # # # # . # . . . . . . . # . # #
# . # # # . # # . . . . # # # . # # # # . # P . # O . # . . . # #
# . . . . . . . . . . . # # # . . . . . . . . . # . . # . # . # #
# . # # . # # # . . . . # # # . # # # # . # . . . . . . . # O # #
# . # # . # # # # . # # # # # . # # # # . # # # # # & # # # . # #
# . . O . . . . . . . . . . . . . O . . . . . . . . . . . . . # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""


def parse_map_file():
    linked: list[tuple[int, int],] = []
    tiles: list[list[LevelTile]] = []
    size: list[int] = [-1, -1]
    gameobjects = []
    lines = layout.replace(' ', '').splitlines(False)

    for y in range(len(lines)):
        size[0] = max(len(lines[y]), size[0])
        size[1] += 1
        tiles.append([])
        line = lines[y]
        for x in range(len(line)):
            access = ACCESS_FLAGS.NONE

            match line[x]:
                case 'G':
                    access = ACCESS_FLAGS.AI
                case '#':
                    access = ACCESS_FLAGS.NONE
                case '+':
                    access = ACCESS_FLAGS.ALL
                    linked.append((x, y))
                case '&':
                    access = ACCESS_FLAGS.PLAYER
                case _: 
                    access = ACCESS_FLAGS.ALL 

            # Construct the tile
            tiles[y].append(LevelTile((x, y), access))
            # Store the type
            tiles[y][x].set_data(hash("MAIN"),"type",line[x])

    return size, tiles, linked, gameobjects

