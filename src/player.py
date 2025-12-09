class Player:
    def __init__(self, name, max_hp=20, attack=3):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def deal_damage(self, target):
        target.hp -= self.attack

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

# player class
