import re

CUBE_PRINT_LETTERS_TEMPLATE = """\
          +---------+
          | %(U1)s  %(U2)s  %(U3)s |
          | %(U4)s  %(U5)s  %(U6)s |
          | %(U7)s  %(U8)s  %(U9)s |
+---------+---------+---------+---------+
| %(L1)s  %(L2)s  %(L3)s | %(F1)s  %(F2)s  %(F3)s | %(R1)s  %(R2)s  %(R3)s | %(B1)s  %(B2)s  %(B3)s |
| %(L4)s  %(L5)s  %(L6)s | %(F4)s  %(F5)s  %(F6)s | %(R4)s  %(R5)s  %(R6)s | %(B4)s  %(B5)s  %(B6)s |
| %(L7)s  %(L8)s  %(L9)s | %(F7)s  %(F8)s  %(F9)s | %(R7)s  %(R8)s  %(R9)s | %(B7)s  %(B8)s  %(B9)s |
+---------+---------+---------+---------+
          | %(D1)s  %(D2)s  %(D3)s |
          | %(D4)s  %(D5)s  %(D6)s |
          | %(D7)s  %(D8)s  %(D9)s |
          +---------+\
"""

CUBE_PRINT_COLORS_TEMPLATE = """\
      %(U1)s%(U2)s%(U3)s
      %(U4)s%(U5)s%(U6)s
      %(U7)s%(U8)s%(U9)s
%(L1)s%(L2)s%(L3)s%(F1)s%(F2)s%(F3)s%(R1)s%(R2)s%(R3)s%(B1)s%(B2)s%(B3)s
%(L4)s%(L5)s%(L6)s%(F4)s%(F5)s%(F6)s%(R4)s%(R5)s%(R6)s%(B4)s%(B5)s%(B6)s
%(L7)s%(L8)s%(L9)s%(F7)s%(F8)s%(F9)s%(R7)s%(R8)s%(R9)s%(B7)s%(B8)s%(B9)s
      %(D1)s%(D2)s%(D3)s
      %(D4)s%(D5)s%(D6)s
      %(D7)s%(D8)s%(D9)s
"""


class Cube:
    COLOR_LETTERS = ["W", "R", "G", "Y", "O", "B"]
    COLOR_ASCII_CODES = ["48;5;15", "48;5;1", "48;5;2", "48;5;11", "48;5;9", "48;5;4"]
    FACES = ["U", "R", "F", "D", "L", "B"]

    NUM_FACELETS = 54
    FACE_SIZE = 9

    ORIENTATIONS = {
        "up": 0,
        "right": 1,
        "front": 2,
        "down": 3,
        "left": 4,
        "back": 5,
    }

    VALID_MOVES = {
        move + variation
        for move in FACES + ["y", "x", "z"]
        for variation in ["", "'", "2"]
    }

    # fmt: off
    TRANSFORMATIONS = {
        "U":  [ 6,  3,  0,  7,  4,  1,  8,  5,  2,
               45, 46, 47, 12, 13, 14, 15, 16, 17,
                9, 10, 11, 21, 22, 23, 24, 25, 26,
               27, 28, 29, 30, 31, 32, 33, 34, 35,
               18, 19, 20, 39, 40, 41, 42, 43, 44,
               36, 37, 38, 48, 49, 50, 51, 52, 53],
        "U'": [ 2,  5,  8,  1,  4,  7,  0,  3,  6,
               18, 19, 20, 12, 13, 14, 15, 16, 17,
               36, 37, 38, 21, 22, 23, 24, 25, 26,
               27, 28, 29, 30, 31, 32, 33, 34, 35,
               45, 46, 47, 39, 40, 41, 42, 43, 44,
                9, 10, 11, 48, 49, 50, 51, 52, 53],

        "R":  [ 0,  1, 20,  3,  4, 23,  6,  7, 26,
               15, 12,  9, 16, 13, 10, 17, 14, 11,
               18, 19, 29, 21, 22, 32, 24, 25, 35,
               27, 28, 51, 30, 31, 48, 33, 34, 45,
               36, 37, 38, 39, 40, 41, 42, 43, 44,
                8, 46, 47,  5, 49, 50,  2, 52, 53],
        "R'": [ 0,  1, 51,  3,  4, 48,  6,  7, 45,
               11, 14, 17, 10, 13, 16,  9, 12, 15,
               18, 19,  2, 21, 22,  5, 24, 25,  8,
               27, 28, 20, 30, 31, 23, 33, 34, 26,
               36, 37, 38, 39, 40, 41, 42, 43, 44,
               35, 46, 47, 32, 49, 50, 29, 52, 53],

        "F":  [ 0,  1,  2,  3,  4,  5, 44, 41, 38,
                6, 10, 11,  7, 13, 14,  8, 16, 17,
               24, 21, 18, 25, 22, 19, 26, 23, 20,
               15, 12,  9, 30, 31, 32, 33, 34, 35,
               36, 37, 27, 39, 40, 28, 42, 43, 29,
               45, 46, 47, 48, 49, 50, 51, 52, 53],
        "F'": [ 0,  1,  2,  3,  4,  5,  9, 12, 15,
               29, 10, 11, 28, 13, 14, 27, 16, 17,
               20, 23, 26, 19, 22, 25, 18, 21, 24,
               38, 41, 44, 30, 31, 32, 33, 34, 35,
               36, 37,  8, 39, 40,  7, 42, 43,  6,
               45, 46, 47, 48, 49, 50, 51, 52, 53],

        "D":  [ 0,  1,  2,  3,  4,  5,  6,  7,  8,
                9, 10, 11, 12, 13, 14, 24, 25, 26,
               18, 19, 20, 21, 22, 23, 42, 43, 44,
               33, 30, 27, 34, 31, 28, 35, 32, 29,
               36, 37, 38, 39, 40, 41, 51, 52, 53,
               45, 46, 47, 48, 49, 50, 15, 16, 17],
        "D'": [ 0,  1,  2,  3,  4,  5,  6,  7,  8,
                9, 10, 11, 12, 13, 14, 51, 52, 53,
               18, 19, 20, 21, 22, 23, 15, 16, 17,
               29, 32, 35, 28, 31, 34, 27, 30, 33,
               36, 37, 38, 39, 40, 41, 24, 25, 26,
               45, 46, 47, 48, 49, 50, 42, 43, 44],

        "L":  [53,  1,  2, 50,  4,  5, 47,  7,  8,
                9, 10, 11, 12, 13, 14, 15, 16, 17,
                0, 19, 20,  3, 22, 23,  6, 25, 26,
               18, 28, 29, 21, 31, 32, 24, 34, 35,
               42, 39, 36, 43, 40, 37, 44, 41, 38,
               45, 46, 33, 48, 49, 30, 51, 52, 27],
        "L'": [18,  1,  2, 21,  4,  5, 24,  7,  8,
                9, 10, 11, 12, 13, 14, 15, 16, 17,
               27, 19, 20, 30, 22, 23, 33, 25, 26,
               53, 28, 29, 50, 31, 32, 47, 34, 35,
               38, 41, 44, 37, 40, 43, 36, 39, 42,
               45, 46,  6, 48, 49,  3, 51, 52,  0],

        "B":  [11, 14, 17,  3,  4,  5,  6,  7,  8,
                9, 10, 35, 12, 13, 34, 15, 16, 33,
               18, 19, 20, 21, 22, 23, 24, 25, 26,
               27, 28, 29, 30, 31, 32, 36, 39, 42,
                2, 37, 38,  1, 40, 41,  0, 43, 44,
               51, 48, 45, 52, 49, 46, 53, 50, 47],
        "B'": [42, 39, 36,  3,  4,  5,  6,  7,  8,
                9, 10,  0, 12, 13,  1, 15, 16,  2,
               18, 19, 20, 21, 22, 23, 24, 25, 26,
               27, 28, 29, 30, 31, 32, 17, 14, 11,
               33, 37, 38, 34, 40, 41, 35, 43, 44,
               47, 50, 53, 46, 49, 52, 45, 48, 51],

        "y":  [ 6,  3,  0,  7,  4,  1,  8,  5,  2,
               45, 46, 47, 48, 49, 50, 51, 52, 53,
                9, 10, 11, 12, 13, 14, 15, 16, 17,
               29, 32, 35, 28, 31, 34, 27, 30, 33,
               18, 19, 20, 21, 22, 23, 24, 25, 26,
               36, 37, 38, 39, 40, 41, 42, 43, 44],
        "y'": [ 2,  5,  8,  1,  4,  7,  0,  3,  6,
               18, 19, 20, 21, 22, 23, 24, 25, 26,
               36, 37, 38, 39, 40, 41, 42, 43, 44,
               33, 30, 27, 34, 31, 28, 35, 32, 29,
               45, 46, 47, 48, 49, 50, 51, 52, 53,
                9, 10, 11, 12, 13, 14, 15, 16, 17],

        "x":  [18, 19, 20, 21, 22, 23, 24, 25, 26,
               15, 12,  9, 16, 13, 10, 17, 14, 11,
               27, 28, 29, 30, 31, 32, 33, 34, 35,
               53, 52, 51, 50, 49, 48, 47, 46, 45,
               38, 41, 44, 37, 40, 43, 36, 39, 42,
                8,  7,  6,  5,  4,  3,  2,  1,  0],
        "x'": [53, 52, 51, 50, 49, 48, 47, 46, 45,
               11, 14, 17, 10, 13, 16,  9, 12, 15,
                0,  1,  2,  3,  4,  5,  6,  7,  8,
               18, 19, 20, 21, 22, 23, 24, 25, 26,
               42, 39, 36, 43, 40, 37, 44, 41, 38,
               35, 34, 33, 32, 31, 30, 29, 28, 27],

        "z":  [42, 39, 36, 43, 40, 37, 44, 41, 38,
                6,  3,  0,  7,  4,  1,  8,  5,  2,
               24, 21, 18, 25, 22, 19, 26, 23, 20,
               15, 12,  9, 16, 13, 10, 17, 14, 11,
               33, 30, 27, 34, 31, 28, 35, 32, 29,
               47, 50, 53, 46, 49, 52, 45, 48, 51],
        "z'": [11, 14, 17, 10, 13, 16,  9, 12, 15,
               29, 32, 35, 28, 31, 34, 27, 30, 33,
               20, 23, 26, 19, 22, 25, 18, 21, 24,
               38, 41, 44, 37, 40, 43, 36, 39, 42,
                2,  5,  8,  1,  4,  7,  0,  3,  6,
               51, 48, 45, 52, 49, 46, 53, 50, 47],
    }

    ORIENTATION_TRANSFORMATIONS = {
        "y":  [0, 5, 1, 3, 2, 4],
        "y'": [0, 2, 4, 3, 5, 1],
        "x":  [2, 1, 3, 5, 4, 0],
        "x'": [5, 1, 0, 2, 4, 3],
        "z":  [4, 0, 2, 1, 3, 5],
        "z'": [1, 3, 2, 4, 0, 5],
    }
    # fmt: on

    def __init__(self, init_conf=None):
        if init_conf:
            self.cube = [
                Cube.FACES.index(init_conf[i]) if i < len(init_conf) else None
                for i in range(0, Cube.NUM_FACELETS)
            ]
        else:
            self.cube = [
                f for f in range(0, len(Cube.FACES)) for _ in range(0, Cube.FACE_SIZE)
            ]
        self.faces = list(Cube.FACES)

    def _apply_one_transformation(self, transformation):
        if transformation not in Cube.TRANSFORMATIONS:
            raise ValueError("Invalid transformation '%s'" % transformation)
        t = Cube.TRANSFORMATIONS[transformation]
        new_conf = [self.cube[t[i]] for i in range(0, Cube.NUM_FACELETS)]
        self.cube = new_conf
        if transformation in Cube.ORIENTATION_TRANSFORMATIONS:
            ot = Cube.ORIENTATION_TRANSFORMATIONS[transformation]
            new_faces = [self.faces[ot[i]] for i in range(0, len(self.faces))]
            self.faces = new_faces

    def apply(self, moves):
        for m in moves.strip().split():
            if m not in Cube.VALID_MOVES:
                raise ValueError("Invalid move '%s'" % m)
        mvs = re.sub(r"([URFDLBxyz])2", r"\1 \1", moves).strip().split()
        for move in mvs:
            self._apply_one_transformation(move)

    def get_oriented_face(self, direction):
        if direction not in Cube.ORIENTATIONS:
            raise ValueError("Invalid direction '%s'" % direction)
        return self.faces[Cube.ORIENTATIONS[direction]]

    def assign_colors_top_face(self, colors):
        for i, c in enumerate(colors):
            self.cube[i] = Cube.COLOR_LETTERS.index(c)

    def reset_orientation(self):
        omap = {Cube.FACES.index(self.faces[i]): i for i in range(len(Cube.FACES))}
        new_cube = [omap[self.cube[i]] for i in range(0, Cube.NUM_FACELETS)]
        self.cube = new_cube
        self.faces = list(Cube.FACES)

    def __str__(self):
        return "".join([Cube.FACES[self.cube[i]] for i in range(0, Cube.NUM_FACELETS)])

    def print(self, mode="colors"):
        if mode == "colors":
            print(
                CUBE_PRINT_COLORS_TEMPLATE
                % dict(
                    [
                        (
                            "%s%d" % (f, i + 1),
                            "\x1b[%sm  \x1b[0m"
                            % Cube.COLOR_ASCII_CODES[
                                self.cube[f_ind * Cube.FACE_SIZE + i]
                            ],
                        )
                        for (f_ind, f) in enumerate(Cube.FACES)
                        for i in range(0, Cube.FACE_SIZE)
                    ]
                )
            )
        else:
            print(
                CUBE_PRINT_LETTERS_TEMPLATE
                % dict(
                    [
                        (
                            "%s%d" % (f, i + 1),
                            Cube.COLOR_LETTERS[self.cube[f_ind * Cube.FACE_SIZE + i]],
                        )
                        for (f_ind, f) in enumerate(Cube.FACES)
                        for i in range(0, Cube.FACE_SIZE)
                    ]
                )
            )
