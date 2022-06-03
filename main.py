# Морской бой
#   | 1 | 2 | 3 | 4 | 5 | 6 |
# 1 | X | X | X | О | О | О |
# 2 | О | О | О | О | X | X |
# 3 | О | T | О | О | О | О |
# 4 | ■ | О | ■ | О | ■ | О |
# 5 | О | О | О | О | ■ | О |
# 6 | ■ | О | ■ | О | О | О |

# Обработка исключения: Вышли за пределы поля
class BoardOutException(Exception):
    pass


# Обработка исключения: Поле на доске занято
class BoardDotOccupied(Exception):
    pass


# Обработка исключения: Координата должна быть целое число
class TypeCoordException(Exception):
    pass

# Описание класса Точка на доске
class Dot:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_coord(self):
        return self.__x, self.__y

    @classmethod
    def __check_value(cls, x):
        return (type(x) == int) and (1 <= x <= 6)

    def set_coord(self, value_x, value_y):
        try:
            if self.__check_value(value_x) and self.__check_value(value_y):
                self.__x = value_x
                self.__y = value_y
            else:
                raise BoardOutException
        except BoardOutException or TypeCoordException:
            print('Координаты должны быть целыми числами от 1 до 6')

    def __eq__(self, other):
        return True if self.__x == other.__x and self.__y == other.__y else False

# Описание класса Ship - Корабль на доске
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
