from random import randint
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы стреляете за пределы игрового поля!"

class BoardShotException(BoardException):
    def __str__(self):
        return "В эту клетку вы уже стреляли!"

class BoardShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ships:
    def __init__(self, bow, size, rotation):
        self.size = size
        self.hp = size
        self.bow = bow
        self.rotation = rotation

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.size):
            new_x = self.bow.x
            new_y = self.bow.y

            if self.rotation == 0:
                new_x += i
            elif self.rotation == 1:
                new_y += i

            ship_dots.append(Dot(new_x, new_y))

        return ship_dots


class Field:
    def __init__(self, skip = False, size = 6):
        self.skip = skip
        self.size = size
        self.field = [["○"] * size for _ in range(size)]
        self.busy = []
        self.ships = []
        self.count = 0


    def add_ships(self, ships):
        for i in ships.dots:
            if self.out(i) or i in self.busy:
                raise BoardShipException()
        for i in ships.dots:
            self.field[i.x][i.y] = "■"
            self.busy.append(i)

        self.ships.append(ships)
        self.contour(ships)


    def contour(self, ships, verb = False):
        near = [(0, -1), (0, 0), (0, 1),
                (-1, -1), (-1, 0), (-1, 1),
                (1, -1), (1, 0), (1, 1)
                ]
        for i in ships.dots:
            for ix, iy in near:
                new = Dot(i.x + ix, i.y + iy)
                if not(self.out(new)) and new not in self.busy:
                    if verb:
                        self.field[new.x][new.y] = "."
                    self.busy.append(new)

    def __str__(self):
        res = ""
        res += " |1|2|3|4|5|6|"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1}|" + "|".join(row) + "|"

        if self.skip:
            res = res.replace("■", "○")
        return res


    def out(self, i):
        return not((0 <= i.x < self.size) and (0 <= i.y < self.size))


    def shoot(self, shot):
        if self.out(shot):
            raise BoardOutException()
        if shot in self.busy:
            raise BoardShotException()

        self.busy.append(shot)

        for i in self.ships:
            if shot in i.dots:
                i.hp -= 1
                self.field[shot.x][shot.y] = "x"
                if i.hp == 0:
                    self.count += 1
                    self.contour(i, verb=True)
                    print("Убит!")
                    return True
                else:
                    print("Ранен!")
                    return True

        self.field[shot.x][shot.y] = "."
        print("Мимо!")
        return False


    def start(self):
        self.busy = []
