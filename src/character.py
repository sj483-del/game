# character.py
from item import Equipment, Consumable

class Character:
    def __init__(self, name, race=None, char_class=None, level=1):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level

        # Core stats
        self.max_hp = 10 + level * 2
        self.current_hp = self.max_hp
        self.attack = 1 + level
        self.defense = 1 + level
        self.speed = 1 + level
        self.magic = 0

        # Inventory, abilities, equipment slots
        self.inventory = []
        self.abilities = []
        self.equipment = {
            "helm": None,
            "armor": None,
            "main hand": None,
            "off hand": None,
            "boots": None,
            "trinket": None
        }

    # -------------------------------
    # EQUIPMENT
    # -------------------------------
    def equip(self, item: Equipment):
        if item.slot not in self.equipment:
            raise ValueError(f"Invalid equipment slot: {item.slot}")
        self.equipment[item.slot] = item
        self.recalculate_stats()

    def recalculate_stats(self):
        """Update stats based on equipped items."""
        self.max_hp = 10 + self.level * 2
        self.attack = 1 + self.level
        self.defense = 1 + self.level

        for eq in self.equipment.values():
            if eq:
                self.max_hp += eq.bonus_hp
                self.attack += eq.bonus_attack
                self.defense += eq.bonus_defense

        # Ensure current HP doesn’t exceed max
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp  

    # -------------------------------
    # CONSUMABLES
    # -------------------------------
    def use_consumable(self, item_name, message_func=print):
        """
        Use a consumable from inventory. Pass a messaging function to display messages.
        """
        for i, item in enumerate(self.inventory):
            if isinstance(item, Consumable) and item.name == item_name:
                self.current_hp += item.heal_amount
                if self.current_hp > self.max_hp:
                    self.current_hp = self.max_hp
                message_func(f"{self.name} uses {item.name} (+{item.heal_amount} HP)")
                del self.inventory[i]  # remove used item
                return True
        message_func(f"{self.name} has no {item_name}!")
        return False

    # -------------------------------
    # COMBAT
    # -------------------------------
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
