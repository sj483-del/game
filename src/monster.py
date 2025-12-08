class Monster:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp -= amount
        print(f"{self.name} takes {amount} damage! (HP: {self.hp})")

    def deal_damage(self, target):
        print(f"{self.name} attacks {target.name} for {self.attack} damage!")
        target.take_damage(self.attack)


def sample_goblin():
    return Monster("Goblin", hp=8, attack=2)
# monster class
