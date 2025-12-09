# item.py

# ===============================
# BASE CLASSES
# ===============================
class Equipment:
    def __init__(self, name, slot, bonus_hp=0, bonus_attack=0, bonus_defense=0):
        self.name = name
        self.slot = slot  # "helm", "armor", "main hand", "off hand", "boots", "trinket"
        self.bonus_hp = bonus_hp
        self.bonus_attack = bonus_attack
        self.bonus_defense = bonus_defense

class Consumable:
    def __init__(self, name, heal_amount=0):
        self.name = name
        self.heal_amount = heal_amount

# ===============================
# EQUIPMENT EXAMPLES
# ===============================

# Helm
iron_helm = Equipment("Iron Helm", "helm", bonus_hp=5, bonus_defense=2)
leather_cap = Equipment("Leather Cap", "helm", bonus_hp=2, bonus_defense=1)

# Armor
chainmail_armor = Equipment("Chainmail Armor", "armor", bonus_hp=15, bonus_defense=5)
leather_armor = Equipment("Leather Armor", "armor", bonus_hp=8, bonus_defense=2)

# Main hand
iron_sword = Equipment("Iron Sword", "main hand", bonus_attack=3)
dagger = Equipment("Dagger", "main hand", bonus_attack=1)

# Off hand
wooden_shield = Equipment("Wooden Shield", "off hand", bonus_defense=3)
buckler = Equipment("Buckler", "off hand", bonus_defense=1)

# Boots
leather_boots = Equipment("Leather Boots", "boots", bonus_hp=2, bonus_defense=1)
iron_boots = Equipment("Iron Boots", "boots", bonus_hp=5, bonus_defense=2)

# Trinkets
silver_ring = Equipment("Silver Ring", "trinket", bonus_hp=3)
amulet_of_strength = Equipment("Amulet of Strength", "trinket", bonus_attack=2)

# ===============================
# CONSUMABLE EXAMPLES
# ===============================

small_healing_potion = Consumable("Small Healing Potion", heal_amount=5)
large_healing_potion = Consumable("Large Healing Potion", heal_amount=15)
elixir_of_health = Consumable("Elixir of Health", heal_amount=25)

# ===============================
# ITEM COLLECTIONS FOR EASY ACCESS
# ===============================
all_equipment = [
    iron_helm, leather_cap,
    chainmail_armor, leather_armor,
    iron_sword, dagger,
    wooden_shield, buckler,
    leather_boots, iron_boots,
    silver_ring, amulet_of_strength
]

all_consumables = [
    small_healing_potion,
    large_healing_potion,
    elixir_of_health
]
