class Monster:
    def __init__(self, name, hp, attack):
        self.name = name
        self.current_hp = hp
        self.max_hp = hp
        self.attack = attack

    def is_alive(self):
        return self.current_hp > 0

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0
        print(f"{self.name} takes {amount} damage! (HP: {self.current_hp}/{self.max_hp})")

    def deal_damage(self, target):
        print(f"{self.name} attacks {target.name} for {self.attack} damage!")
        target.take_damage(self.attack)


def sample_goblin():
    """Return a default goblin monster."""
    return Monster("Goblin", hp=8, attack=2)
