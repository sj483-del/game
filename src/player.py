class Player:
    def __init__(self, name="Hero", hp=20, attack=4):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.inventory = []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp -= amount
        print(f"{self.name} takes {amount} damage! (HP: {self.hp})")

    def deal_damage(self, target):
        print(f"{self.name} attacks {target.name} for {self.attack} damage!")
        target.take_damage(self.attack)
# player class
