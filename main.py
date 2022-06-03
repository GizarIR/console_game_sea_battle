# Морской бой
#   | 1 | 2 | 3 | 4 | 5 | 6 |
# 1 | X | X | X | О | О | О |
# 2 | О | О | О | О | X | X |
# 3 | О | T | О | О | О | О |
# 4 | ■ | О | ■ | О | ■ | О |
# 5 | О | О | О | О | ■ | О |
# 6 | ■ | О | ■ | О | О | О |

class BoardOutException(Exception):
    """Обработка исключения: Вышли за пределы поля"""
    pass


class BoardDotOccupied(Exception):
    """Обработка исключения: Поле на доске занято"""
    pass


class TypeCoordException(Exception):
    """Обработка исключения: Координата должна быть целое число"""
    pass


class TypeDotException(Exception):
    """Обработка исключения: Объект не является типом Dot"""
    pass


class Dot:
    """Базовый класс: Точка на доске"""
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


class Ship:
    """Базовый класс: Ship - Корабль на доске"""
    __positions = ('vert', 'horiz')

    def __init__(self, length, dot_top, position):
        self.__length = length
        self.__dot_top = dot_top
        self.__position = position
        self.__health = self.dots()

    # возвращает список всех точек корабля
    def dots(self):
        if self.__position == 'horiz':
            return [Dot(self.__dot_top.get_coord()[0], x) for x in range(1, self.__length+1)]
        else:
            return [Dot(x, self.__dot_top.get_coord()[0]) for x in range(1, self.__length + 1)]

    # возвращает кортеж с описанием корабля
    def get_ship(self):
        return self.__length, self.__dot_top.get_coord(), self.__position, [x.get_coord() for x in self.__health]

    # удаляет точку из списка здоровья корабля
    def set_health(self, dot_):
        try:
            if isinstance(dot_, Dot):
                if dot_ in self.__health:
                    self.__health.remove(dot_)
                else:
                    print(f'Точка {dot_.get_coord()} не принадлежит кораблю')
            else:
                raise TypeDotException
        except TypeDotException:
            print(f'Не верный тип данных в переменной {dot_}. Требуется Dot')





dot_1 = Dot(1, 2)
# print(dot_1.get_coord()[0])

ship_1 = Ship(4, Dot(1, 1), "horiz")

print(ship_1.get_ship())

ship_1.set_health(dot_1)

print(ship_1.get_ship())
