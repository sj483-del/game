import random
from monster import Monster, sample_goblin

class Room:
    def __init__(self, has_monster=False, monster=None):
        """
        has_monster: True if room contains a monster
        monster: a Monster instance (optional)
        """
        self.has_monster = has_monster
        self.monster = monster if monster else (sample_goblin() if has_monster else None)

    def enter(self, party_member):
        """
        party_member: a single party member entering the room (for text-based combat)
        """
        print("\nYou enter a room...")

        if self.has_monster:
            print(f"A {self.monster.name} appears!")
            self.combat(party_member, self.monster)
        else:
            print("The room is empty.")

    def combat(self, party_member, monster):
        """Simple turn-based combat for a single party member."""
        print("\n=== Combat Start ===")

        while party_member.is_alive() and monster.is_alive():
            print(f"\n{party_member.name} HP: {party_member.current_hp} | {monster.name} HP: {monster.current_hp}")
            print("Choose your action:")
            print("1. Attack")
            print("2. Flee")

            choice = input("> ")

            if choice == "1":
                party_member.deal_damage(monster)
                if monster.is_alive():
                    monster.deal_damage(party_member)
            elif choice == "2":
                print("You attempt to flee...")
                if random.random() < 0.5:  # 50% chance to escape
                    print("You successfully escaped!")
                    return
                else:
                    print("Failed to escape!")
                    monster.deal_damage(party_member)
            else:
                print("Invalid choice, try again.")

        if party_member.is_alive():
            print(f"\nYou defeated the {monster.name}!")
            self.has_monster = False
            self.monster = None
        else:
            print("\nYou have been defeated...")
