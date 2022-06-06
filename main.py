# Морской бой
#   | 1 | 2 | 3 | 4 | 5 | 6 |
# 1 | X | X | X | О | О | О |
# 2 | О | О | О | О | X | X |
# 3 | О | T | О | О | О | О |
# 4 | ■ | О | ■ | О | ■ | О |
# 5 | О | О | О | О | ■ | О |
# 6 | ■ | О | ■ | О | О | О |
from random import *

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
    def __init__(self, x=None, y=None):
        self.__x = x if self.__check_value(x) else None
        self.__y = y if self.__check_value(y) else None

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
    __max_board_xy = 6

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
        except TypeError:
            print('Функции set_hid требуется значение типа Bool')

    # добавляем корабль на доску
    def add_ship(self, ship_):
        for desk in ship_.get_ship()[3]:
            self.__b_status[desk[0] - 1][desk[1] - 1] = "■"

    # обводим контур кораблю на игровой доске - получаем список точек Dot куда нельзя ставить корабль
    # @staticmethod
    def contour(self, ship_):
        contour_ = []
        min_x, min_y, max_x, max_y = None, None, None, None
        for desk in ship_.get_ship()[3]:
            max_x = desk[0] + 1 if desk[0] + 1 < self.__max_board_xy else self.__max_board_xy
            max_y = desk[1] + 1 if desk[1] + 1 < self.__max_board_xy else self.__max_board_xy
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
        result = ""
        line_in_board = []
        count = 1
        result = "    " + " | ".join([str(x) for x in range(1, 6 + 1)]) + "\n"
        for line in self.__b_status:
            line_in_board = []
            if not self.__hid:
                result += str(count) + " | " + " | ".join(line) + " \n"
                count += 1
            else:
                line_in_board = ["O" if x == "■" else x for x in line]
                result += str(count) + " | " + " | ".join(line_in_board) + " \n"
                count += 1
        return result

    # метод проверки принадлежности точки к данной доске
    def out(self, dot_):
        # dot_1 = Dot(1, 1)
        if 1 <= dot_.get_coord()[0] <= self.__max_board_xy and 1 <= dot_.get_coord()[1] <= self.__max_board_xy:
            return True
        else:
            return False

    # Метод shot, который делает выстрел по доске (если есть попытка выстрелить за пределы и в
    # использованную точку, нужно выбрасывать исключения).
    def shot(self, dot_):
        player_need_shot = False
        x = dot_.get_coord()[0]
        y = dot_.get_coord()[1]
        try:
            if not self.out(dot_):
                raise BoardOutException
            elif self.__b_status[x - 1][y - 1] in ["T", "X"]:
                raise BoardDotOccupied
            else:
                if self.__b_status[x - 1][y - 1] == "■":
                    self.__b_status[x - 1][y - 1] = "X"
                    player_need_shot = True
                    return True, player_need_shot
                else:
                    self.__b_status[x - 1][y - 1] = "T"
                    player_need_shot = False
                    return True, player_need_shot
        except BoardOutException or BoardDotOccupied:
            print(f'Точка с координатами ({x}, {y}) уже использована или за пределами поля')
            return False, player_need_shot

class Player:
    """Базовый класс: Player - Игрок или AI"""
    # __need_shot = False # атрибут хранит в себе статус необходимости повторного хода после попадания

    def __init__(self, my_board, enemy_board):
        self.__my_board = my_board
        self.__enemy_board = enemy_board

    # def set_need_shot(self, value):
    #     try:
    #         if type(value) == bool:
    #             self.__need_shot = value
    #         else:
    #             raise TypeError
    #     except TypeError:
    #         print("Переменна need_shot должна быть bool")

    # метод, который «спрашивает» игрока, в какую клетку он делает выстрел. переопределеяем в классах потомках
    def ask(self):
        pass

    # метод, который делает ход в игре. Тут мы вызываем метод ask, делаем выстрел по
    # вражеской доске (метод Board.shot), отлавливаем исключения, и если они есть, пытаемся
    # повторить ход. Метод должен возвращать True, если этому игроку нужен повторный ход
    # (например если он выстрелом подбил корабль)
    def move(self):
        result_shot = ()
        need_shot = False # переменная которая отвечает на вопрос нужно ли делать ход после попадания
        right_shot = False # переменная для понимания результат выстрела с исключениями или нет
        while not right_shot:
            dot_shot = self.ask()
            result_shot = self.__enemy_board.shot(dot_shot)
            right_shot, need_shot = result_shot[0], result_shot[1]
        return need_shot


class User(Player):
    """Класс потомок от Player: Игорок человек, вводим данные с консоли"""
    @classmethod
    def right_enter(cls, str_):
        if str_ is None:
            return False
        if len(str_) != 3:
            print('Координаты хода не соответствуют формату. Строка не из 3-х символов')
            return False
        elif not str_[0].isdigit() or not str_[2].isdigit():
            print('Координаты хода не соответствуют формату. Координаты не цифры')
            return False
        elif all([(1 <= int(str_[0]) <= 6),
                  (str_[1] == ' '),
                  (1 <= int(str_[2]) <= 6)]):
            return True
        else:
            print('Координаты хода не соответствуют формату. Формат ввода: Цифра Пробел Цифра. Цифра от 1 до 6')
            return False

    def ask(self):
        shot_str = " "
        right_shot = False
        while not right_shot:
            shot_str = input("Введите координаты выстрела через пробел (пример: 1 2): ")
            right_shot = User.right_enter(shot_str)
        shot_ = shot_str.split(" ")
        return Dot(int(shot_[0]), int(shot_[1]))

class Ai(Player):
    def ask(self):
        x = randint(1, 6)
        y = randint(1, 6)
        return Dot(x, y)


ship_1 = Ship(2, Dot(1, 1), "vert")

print(ship_1.get_ship())

board_1 = Board()
board_2 = Board()
# print(board_1.show())

board_1.add_ship(ship_1)
ship_2 = Ship(4, Dot(3, 3), "horiz")
board_1.add_ship(ship_2)
print(board_1.show())
print([x.get_coord() for x in board_1.contour(ship_1)])

dot_1 = Dot(1, 1)
ship_3 = Ship(4, Dot(6, 3), "horiz")
board_2.add_ship(ship_3)
# player_1 = User(board_2, board_1)
player_1 = Ai(board_2, board_1)
f_1 = player_1.move()
print(board_1.shot(dot_1))
print(board_1.show())
