# enemy.py
from character import Character

class Enemy(Character):
    def __init__(self, name, level=1):
        super().__init__(name, race=None, char_class=None, level=level)
        # Add AI behavior or enemy-specific attributes here
