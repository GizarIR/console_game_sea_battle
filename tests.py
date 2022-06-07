class Player:
    def ask(self):
        pass

    def move(self):
        self.ask()

class User(Player):
    def ask(self):
        print('Печать из User')

class Ai(Player):
    def ask(self):
        print('Печать из Ai')

a_ = User()

b_ = Ai()

a_.ask()
b_.ask()



