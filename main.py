# Морской бой
#   | 1 | 2 | 3 | 4 | 5 | 6 |
# 1 | X | X | X | О | О | О |
# 2 | О | О | О | О | X | X |
# 3 | О | T | О | О | О | О |
# 4 | ■ | О | ■ | О | ■ | О |
# 5 | О | О | О | О | ■ | О |
# 6 | ■ | О | ■ | О | О | О |
from random import *

import time


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

    # __positions = ('vert', 'horiz')

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
        self.ships = []  # список объектов типа Ship
        self.__hid = False  # должно быть bool
        self.num_live_ship = 0  # количество живых кораблей

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
        self.ships.append(ship_)

    # обводим контур кораблю на игровой доске - получаем список точек Dot куда нельзя ставить корабль
    @staticmethod
    def contour(ship_):
        contour_ = []
        min_x, min_y, max_x, max_y = None, None, None, None
        for desk in ship_.get_ship()[3]:
            max_x = desk[0] + 1 if desk[0] + 1 < 6 else 6
            max_y = desk[1] + 1 if desk[1] + 1 < 6 else 6
            min_x = desk[0] - 1 if desk[0] - 1 > 1 else 1
            min_y = desk[1] - 1 if desk[1] - 1 > 1 else 1
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
        except BoardDotOccupied:
            print(f'Точка с координатами ({x}, {y}) за пределами поля')
            return False, player_need_shot

        try:
            if self.__b_status[x - 1][y - 1] in ["T", "X"]:
                raise BoardDotOccupied
        except BoardDotOccupied:
            print(f'Точка с координатами ({x}, {y}) уже использована')
            return False, player_need_shot

        if self.__b_status[x - 1][y - 1] == "■":
            self.__b_status[x - 1][y - 1] = "X"
            for ship_ in self.ships:
                # s_1 = ship_.get_ship()[3]
                if (x, y) in ship_.get_ship()[3]:
                    ship_.set_health(Dot(x, y))
                    # s_2 = ship_.get_ship()[3]
                    if ship_.get_ship()[3] == []:
                        print(f'>>>>>>>  {ship_.get_ship()[0]}-х палубный корабль подбит!  <<<<<<<<')
                        self.num_live_ship -= 1
                        if self.num_live_ship == 0:
                            player_need_shot = False
                            return True, player_need_shot
                    else:
                        print('\n ***** >> Есть попадание! << ***** \n')
            player_need_shot = True
            return True, player_need_shot
        else:
            self.__b_status[x - 1][y - 1] = "T"
            print('\n ***** << Промахнулся >> ***** \n')
            player_need_shot = False
            return True, player_need_shot


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
        need_shot = False  # переменная которая отвечает на вопрос нужно ли делать ход после попадания
        right_shot = False  # переменная для понимания результат выстрела с исключениями или нет
        while not right_shot:
            dot_shot = self.ask()
            result_shot = self.__enemy_board.shot(dot_shot)
            right_shot, need_shot = result_shot[0], result_shot[1]
        return need_shot


class Ai(Player):
    """Класс потомок от Player: Игрок компьютер, вводим данные по генератору случайных чисел"""
    def ask(self):
        x = randint(1, 6)
        y = randint(1, 6)
        print(f'Искусственный интеллект делает выстрел по координатам ({x}, {y})... \n')
        time.sleep(3)
        return Dot(x, y)

class User(Player):
    """Класс потомок от Player: Игрок человек, вводим данные с консоли"""
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
        shot_str = ""
        right_shot = False
        while not right_shot:
            shot_str = input("Введите координаты выстрела через пробел (пример: 1 2): ")
            right_shot = User.right_enter(shot_str)
        shot_ = shot_str.split(" ")
        return Dot(int(shot_[0]), int(shot_[1]))





class Game:
    """Базовый класс Game: Описывает логику игры"""
    __positions = ['vert', 'horiz']

    def __init__(self):
        self.user_board = Board()
        self.ai_board = Board()
        # self.user = User(self.user_board, self.ai_board )
        # self.ai = Ai(self.ai_board, self.user_board)
        self.user = User(Board, Board)
        self.ai = Ai(Board, Board)

    @staticmethod
    def __check_ship(board_, candidate):
        if candidate == []:
            return False
        else:
            if candidate[3] == "horiz" and candidate[2] + candidate[0] <= 6:
                temp_ship = Ship(candidate[0], Dot(candidate[1], candidate[2]), candidate[3])
                for ship_ in board_.ships:
                    temp_contour = Board.contour(ship_)
                    t_l_ = [x.get_coord() for x in temp_contour]
                    for dot_ in temp_contour:
                        t_d_ = dot_.get_coord()
                        t_s_ = [x.get_coord() for x in temp_ship.dots()]
                        if dot_ in temp_ship.dots():
                            del temp_ship
                            return False
                return True
            elif candidate[3] == "vert" and candidate[1] + candidate[0] <= 6:
                temp_ship = Ship(candidate[0], Dot(candidate[1], candidate[2]), candidate[3])
                for ship_ in board_.ships:
                    temp_contour = Board.contour(ship_)
                    for dot_ in temp_contour:
                        if dot_ in temp_ship.dots():
                            del temp_ship
                            return False
                return True
            else:
                return False

    # генератор случайных досок. 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку.
    def random_board(self):
        print("Пожалуйста, подoждите минутку. Генерируем доски...")
        num_ship = [0, 4, 2, 1, 0]  # количество кораблей (значение элемента) в зависимости от количества палуб (индекс)
        # num_ship = [0, 0, 0, 1, 0] # чтобы не играть всю игру на период тестирования
        # создадим доску для человека
        count = 0
        num_gen = 1
        candidate_ship = []
        break_point = False
        board_created = False
        while not break_point and not board_created:
            for i in range(4, 0, -1):
                for j in range(1, num_ship[i] + 1):
                    # подбор кандидата
                    while not Game.__check_ship(self.user_board, candidate_ship) and count <= 1000:
                        candidate_ship = [i, randint(1, 6), randint(1, 6), choice(self.__positions)]
                        count += 1
                    # размещение на доске корабля
                    if count <= 1000:
                        ship_temp = Ship(i, Dot(candidate_ship[1], candidate_ship[2]), candidate_ship[3])
                        # str_ = ship_temp.get_ship()
                        self.user_board.add_ship(ship_temp)
                        # t_s_ = [x.get_ship() for x in self.user_board.ships]
                        self.user_board.num_live_ship += 1
                        # print(self.user_board.show())
                        count = 0
                        candidate_ship = []
                        del ship_temp
                    else:
                        del self.user_board
                        self.user_board = Board()
                        print(f'Еще одна попытка ({num_gen}) генерации доски для Вас')
                        # print(self.user_board.show())
                        num_gen += 1
                        count = 0
                        candidate_ship = []
                        break_point = True
                        break
            if break_point:
                break_point = False
                board_created = False
            else:
                board_created = True
        num_gen = 1
        print("Доска для Вас сгенерирована.")
        print("Генерируем доску для ИИ...")
        # print(self.user_board.show())

        # создадим доску для AI (компьютера)
        count = 0
        candidate_ship = []
        break_point = False
        board_created = False
        while not break_point and not board_created:
            for i in range(4, 0, -1):
                for j in range(1, num_ship[i] + 1):
                    # подбор кандидата
                    while not Game.__check_ship(self.ai_board, candidate_ship) and count <= 1000:
                        candidate_ship = [i, randint(1, 6), randint(1, 6), choice(self.__positions)]
                        count += 1
                    # размещение на доске корабля
                    if count <= 1000:
                        ship_temp = Ship(i, Dot(candidate_ship[1], candidate_ship[2]), candidate_ship[3])
                        # str_ = ship_temp.get_ship()
                        self.ai_board.add_ship(ship_temp)
                        # t_s_ = [x.get_ship() for x in self.ai_board.ships]
                        self.ai_board.num_live_ship += 1

                        # print(self.ai_board.show())
                        count = 0
                        candidate_ship = []
                        del ship_temp
                    else:
                        del self.ai_board
                        self.ai_board = Board()
                        print(f'Еще одна попытка ({num_gen}) генерации доски для ИИ')
                        num_gen += 1
                        # print(self.ai_board.show())
                        count = 0
                        candidate_ship = []
                        break_point = True
                        break
            if break_point:
                break_point = False
                board_created = False
            else:
                board_created = True

        self.user = User(self.user_board, self.ai_board)
        self.ai = Ai(self.ai_board, self.user_board)

        print("-----------------Ваша доска с кораблям----------------")
        print(self.user_board.show())
        print('--------Доска ИИ (корабли противника скрыты)-----------')
        self.ai_board.set_hid(True)
        # self.ai_board.set_hid(False)  # на время тестирования
        print(self.ai_board.show())

    # приветствие
    def greet(self):
        print('|----------------------Добро пожаловать в игру Морской бой с ИИ!-----------------------|')
        print('| Правила:                                                                             |')
        print('| 1. Сейчас ИИ (искусственный интеллект) сгенерирует 2 поля боя - доски размером 6 х 6 |')
        print('| 2. На каждой доске (у ИИ и у Вас) будет находиться следующее количество кораблей:    |')
        print('|    -1 корабль на 3 клетки,                                                           |')
        print('|    -2 корабля на 2 клетки,                                                           |')
        print('|    -4 корабля на одну клетку.                                                        |')
        print('| 3. Для осуществления выстрела необходимо ввести координаты точки в формате: 1 2      |')
        print('| 4. В случае попадания, корабль противника будет отмечен знаком: Х                    |')
        print('| 5. В случае промаха, точка на поле будет отмечена знаком: Т                          |')
        input('|--------------Теперь Вы все знаете:) Удачи, для начала игры нажмите Enter-------------|\n')

    # рисуем пару досок для диалога в игровом цикле loop
    def boards_show(self):
        print("-----------------Ваша доска с кораблям-----------------")
        print(self.user_board.show())
        print('--------Доска ИИ (корабли противника скрыты)-----------')
        print(self.ai_board.show())

    # игровой цикл в результате которого определим победителя
    def loop(self):
        self.random_board()
        # self.boards_show()
        while self.user_board.num_live_ship != 0 and self.ai_board.num_live_ship != 0:
            got_ = True
            while got_ and self.user_board.num_live_ship != 0:
                got_ = self.user.move()
                self.boards_show()
            got_ = True
            while got_ and self.ai_board.num_live_ship != 0:
                got_ = self.ai.move()
                self.boards_show()

        if self.user_board.num_live_ship > 0 and self.ai_board.num_live_ship == 0:
            print('|---------------------------------------------|')
            print("| Поздравляем Вас с победой!!! Вы выиграли!!! |")
            print('|---------------------------------------------|')
        elif self.user_board.num_live_ship == 0 and self.ai_board.num_live_ship > 0:
            print('|-----------------------------------------------------------------------------|')
            print("|На этот раз Искусственный интеллект выиграл. Можно попробовать взять реванш;)|")
            print('|-----------------------------------------------------------------------------|')
        else:
            print('|---------------------------------------------|')
            print('| Возможно у вас с ИИ ничья или он сломался:) |')
            print('|---------------------------------------------|')

    # метод запускающий игру
    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()

# код для тестирования классов, методов и атрибутов
if __name__ == "__main__":
    print()
    # ship_1 = Ship(2, Dot(1, 1), "vert")
    # print(ship_1.get_ship())
    # board_2 = Board()
    # print(board_1.show())
    # board_1.add_ship(ship_1)
    # board_1 = Board()
    # ship_2 = Ship(2, Dot(1, 1), "horiz")
    # board_1.add_ship(ship_2)
    # print(board_1.show())
    # print([x.get_coord() for x in board_1.contour(ship_2)])
    # dot_1 = Dot(1, 1)
    # ship_3 = Ship(4, Dot(6, 3), "horiz")
    # board_2.add_ship(ship_3)
    # # player_1 = User(board_2, board_1)
    # player_1 = Ai(board_2, board_1)
    # f_1 = player_1.move()
    # print(board_1.shot(dot_1))
    # print(board_1.show())
    # game_1 = Game()
    # game_1.greet()
    # game_1.random_board()
    # game_1.ai_board.set_hid(False)
    # game_1.ai.move()
    # game_1.user.move()
    # print("-----------------Ваша доска с кораблям----------")
    # print(game_1.user_board.show())
    # print('--------Доска ИИ (корабли противника скрыты)-----------')
    # print(game_1.ai_board.show())
    # game_1.loop()
