# Морской бой
#   | 1 | 2 | 3 | 4 | 5 | 6 |
# 1 | X | X | X | О | О | О |
# 2 | О | О | О | О | X | X |
# 3 | О | T | О | О | О | О |
# 4 | ■ | О | ■ | О | ■ | О |
# 5 | О | О | О | О | ■ | О |
# 6 | ■ | О | ■ | О | О | О |

class BoardOutException(Exception):
    pass

class Dot:
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x_y(self):
        return self.x, self.y

    def set_x_y(self, value_x, value_y):
        try:
            if 1 <= value_x <= 6 or 1 <= value_y <= 6:
                self.x = value_x
                self.y = value_y
            else:
                raise BoardOutException
        except BoardOutException:
            print('Выход за пределы поля')

    def __eq__(self, other):
        return True if self.x == other.x and self.y else False

class Ship:
    def __init__(self, length, dot_top, position, health):
        self.length = length
        self.dot_top = dot_top
        self.position = position
        self.health = health

    def get_length(self):
        return self.length

    # возвращает список не подбитых точек корабля
    def dots(self):
        pass



dot_1 = Dot(1, 1)
print(dot_1.x, dot_1.y)
dot_1.set_x_y(7, 6)
print(dot_1.x, dot_1.y)
