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
        end_y = start_y + self.__length
        end_x = start_x + self.__length
        if self.__position == 'horiz':
            return [Dot(self.__dot_top.get_coord()[0], y) for y in range(start_y, end_y)]
        else:
            return [Dot(x, self.__dot_top.get_coord()[1]) for x in range(start_x, end_x)]

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
        self.__b_status = [["O" for y in range(6)] for x in range(6)]
        self.__ships = []  # список объектов типа Ship
        self.__hid = False  # должно быть bool
        self.__num_live_ship = 0  # количество живых кораблей

    # сеттер для защищенного атрибута __hid
    def set_hid(self, value):
        try:
            if isinstance(value, bool):
                self.__hid = value
            else:
                raise TypeError
        except TypeError as e:
            print('Функции set_hid требуется значение типа Bool')


    # добавляем корабль на доску
    def add_ship(self, ship_):
        # ship_ = Ship(4, Dot(1, 1), "horiz")
        for desk in ship_.get_ship()[3]:
            self.__b_status[desk[0] - 1][desk[1] - 1] = "■"

    # обводим контур кораблю на игровой доске - получаем список точек Dot куда нельзя ставить
    @staticmethod
    def contour(ship_):
        contour_ = []
        min_x, min_y, max_x, max_y = None, None, None, None
        for desk in ship_.get_ship()[3]:
            max_x = desk[0] + 1 if desk[0] + 1 < 6 else 6
            max_y = desk[1] + 1 if desk[1] + 1 < 6 else 6
            min_x = desk[0] - 1 if desk[0] - 1 > 1 else 1
            min_y = desk[0] - 1 if desk[0] - 1 > 1 else 1
            for i in range(min_x, max_x + 1):
                for j in range(min_y, max_y + 1):
                    if Dot(i, j) not in contour_:
                        contour_.append(Dot(i, j))
                    else:
                        continue
        return contour_

    # отрисовываем поле боя в зависимости от значения __hid
    def show(self):
        board_show = ""
        line_in_board = []
        count = 1
        board_show = "    " + " | ".join([str(x) for x in range(1, 6 + 1)]) + "\n"
        for line in self.__b_status:
            line_in_board = []
            if not self.__hid:
                board_show += str(count) + " | " + " | ".join(line) + " \n"
                count += 1
            else:
                line_in_board = ["O" if x == "■" else x for x in line]
                board_show += str(count) + " | " + " | ".join(line_in_board) + " \n"
                count += 1
        return board_show


dot_1 = Dot(1, 1)

ship_1 = Ship(2, Dot(1, 1), "vert")

print(ship_1.get_ship())

board_1 = Board()
# print(board_1.show())

board_1.add_ship(ship_1)
ship_2 = Ship(4, Dot(3, 3), "horiz")
board_1.add_ship(ship_2)
print(board_1.show())
print([x.get_coord() for x in board_1.contour(ship_1)])

