from src.player import Player
from src.room import Room
import random

class Dungeon:
    def __init__(self):
        # For now: 3 rooms, random monster chance
        self.rooms = [
            Room(has_monster=random.choice([True, False]))
            for _ in range(3)
        ]
        self.player = Player()

    def start(self):
        print("\nEntering the dungeon...\n")

        for index, room in enumerate(self.rooms, start=1):
            print(f"--- Room {index}/{len(self.rooms)} ---")
            room.enter(self.player)

            if not self.player.is_alive():
                print("Game Over.")
                return

        print("\n🎉 You cleared the dungeon! 🎉")
# dungeon generation
