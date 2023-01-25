from .tile import LevelTile
from .access_flags import ACCESS_FLAGS

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
# # # # # # . # # O . . # - - - - - - # . # # . # # . . . . . # #
# # # # # # . O # . # . # - - - - - - # . # # . # # # # # . # # #
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
# . # # # . # # . . . . # # # . # # # # . # . . # O . # . . . # #
# . . . . . . . . . . . # # # . . . . . . . . . # . . # . # . # #
# . # # . # # # . . . . # # # . # # # # . # . . . . . . . # O # #
# . # # . # # # # . # # # # # . # # # # . # # # # # & # # # . # #
# . . O . . . . . . . . . . . . . O . . . . . . . . . . . . . # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""


def parse_map_file():
    linked: list[tuple[int, int],] = []
    tiles: list[list[LevelTile]] = []
    size: list[int, int] = [0, 0]
    gameobjects = []
    lines = layout.replace(' ', '').splitlines(False)

    for y in range(len(lines)):
        size[0] = max(len(lines), size[0])
        size[1] += 1
        tiles.append([])
        line = lines[y]
        for x in range(len(line)):
            access = ACCESS_FLAGS.NONE

            match line[x]:
                case '-':
                    access = ACCESS_FLAGS.ALL
                case 'G':
                    access = ACCESS_FLAGS.AI
                case '#':
                    access = ACCESS_FLAGS.NONE
                case '+':
                    access = ACCESS_FLAGS.ALL
                    linked.append((x, y))
                case 'O':
                    access = ACCESS_FLAGS.ALL
                case '&':
                    access = ACCESS_FLAGS.PLAYER
                case '.':
                    access = ACCESS_FLAGS.ALL


            # Construct the tile
            tiles[y].append(LevelTile((x, y), access))

    return size, tiles, linked, gameobjects

