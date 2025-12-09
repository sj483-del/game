import random
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
            print(f"\nYour HP: {player.hp} | {monster.name} HP: {monster.hp}")
            print("Choose your action:")
            print("1. Attack")
            print("2. Flee")

            choice = input("> ")

            if choice == "1":
                player.deal_damage(monster)
                if monster.is_alive():
                    monster.deal_damage(player)
            elif choice == "2":
                print("You attempt to flee...")
                if random.random() < 0.5:  # 50% chance to escape
                    print("You successfully escaped!")
                    return
                else:
                    print("Failed to escape!")
                    monster.deal_damage(player)
            else:
                print("Invalid choice, try again.")

        if player.is_alive():
            print(f"\nYou defeated the {monster.name}!")
            self.has_monster = False
        else:
            print("\nYou have been defeated...")
