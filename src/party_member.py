class PartyMember:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def deal_damage(self, target):
        target.hp -= self.attack
