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
        start_x = self.__dot_top.get_coord()[0]
        start_y = self.__dot_top.get_coord()[1]
        if self.__position == 'horiz':
            return [Dot(self.__dot_top.get_coord()[0], x) for x in range(start_x, start_x + self.__length)]
        else:
            return [Dot(x, self.__dot_top.get_coord()[0]) for x in range(start_y, start_y + self.__length)]

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

class Board:
    """Базовый класс: Board - Доска для игры в морской бой"""
    def __init__(self):
        self.__b_status = [["0" for y in range(6)] for x in range(6)]
        self.__ships = []  # список объектов типа Ship
        self.__hid = True  # должно быть bool
        self.__num_live_ship = 0  # количество живых кораблей

    # добавляем корабль на доску
    def add_ship(self, ship_):
        # ship_ = Ship(4, Dot(1, 1), "horiz")
        for desk in ship_.get_ship()[3]:
            self.__b_status[desk[0] - 1][desk[1] - 1] = "■"

    # обводим контур кораблю на игровой доске - получаем список точек Dot куда нельзя ставить
    @staticmethod
    def contour(ship_):
        contour_ = []
        max_x_ = None
        max_y = None
        for desk in ship_.get_ship()[3]:
            max_x = desk[0] + 2 if desk[0] + 2 < 6 else 6
            max_y = desk[1] + 2 if desk[1] + 2 < 6 else 6
            x = desk[0]
            y = desk[1]
            for i in range(x - 1, max_x + 1):
                for j in range(y - 1, max_y + 1):
                    if Dot(i, j) not in contour_:
                        contour_.append(Dot(i, j))
                    else:
                        continue
        return contour_

    # отрисовываем поле боя
    def show(self):
        board_show = ""
        count = 1
        board_show = "    " + " | ".join([str(x) for x in range(1, 6 + 1)]) + "\n"
        for i in self.__b_status:
            board_show += str(count) + " | " + " | ".join(i) + " \n"
            count += 1
        return board_show


dot_1 = Dot(1, 1)
# print(dot_1.get_coord()[0])
# проверить добавление корабля!!!
ship_1 = Ship(1, Dot(3, 4), "horiz")

print(ship_1.get_ship())

board_1 = Board()
print(board_1.show())

board_1.add_ship(ship_1)
print(board_1.show())
print([x.get_coord() for x in board_1.contour(ship_1)])
