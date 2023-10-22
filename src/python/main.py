class Human:
    def __init__(self, name):
        self.name = name

    def sayh_hello(self):
        print(f"hello, my name is {self.name}")

class Player:
    def __init__(self, name, xp):
        super().__init__(name)
        self.xp = xp

class Fan(Human):
    def __init__(self, name,  fav_team):
        super().__init__(name)
        self.fav_team = fav_team

hyungyu = Player("hyungyu", 100)
hyungyu.say_hello()