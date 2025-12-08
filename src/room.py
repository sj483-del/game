from src.monster import sample_goblin

class Room:
    def __init__(self, has_monster=False):
        self.has_monster = has_monster
        self.monster = sample_goblin() if has_monster else None

    def enter(self, player):
        print("\nYou enter a room...")

        if self.has_monster:
            print(f"A {self.monster.name} appears!")
            self.combat(player, self.monster)
        else:
            print("The room is empty.")

    def combat(self, player, monster):
        print("\n=== Combat Start ===")

        while player.is_alive() and monster.is_alive():
            player.deal_damage(monster)
            if monster.is_alive():
                monster.deal_damage(player)

        if player.is_alive():
            print(f"\nYou defeated the {monster.name}!")
            self.has_monster = False
        else:
            print("\nYou have been defeated...")
# room system
