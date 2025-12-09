# test_items.py
from character import Character
from item import Equipment, Consumable

def add_message(msg):
    """Simulate the in-game message function."""
    print(msg)

# -------------------------------
# Create a test character
# -------------------------------
hero = Character("Aria", race="Aasimar", char_class="Paladin", level=3)

# -------------------------------
# Define some equipment
# -------------------------------
helm = Equipment(name="Iron Helm", slot="helm", bonus_hp=5, bonus_attack=0, bonus_defense=2)
armor = Equipment(name="Steel Armor", slot="armor", bonus_hp=10, bonus_attack=0, bonus_defense=5)
sword = Equipment(name="Longsword", slot="main hand", bonus_hp=0, bonus_attack=4, bonus_defense=0)
shield = Equipment(name="Wooden Shield", slot="off hand", bonus_hp=0, bonus_attack=0, bonus_defense=3)
boots = Equipment(name="Leather Boots", slot="boots", bonus_hp=0, bonus_attack=0, bonus_defense=1)
ring = Equipment(name="Ring of Vitality", slot="trinket", bonus_hp=3, bonus_attack=0, bonus_defense=0)

# -------------------------------
# Equip items and show stat changes
# -------------------------------
for eq in [helm, armor, sword, shield, boots, ring]:
    hero.equip(eq)
    add_message(f"Equipped {eq.name}. Stats: HP={hero.max_hp}, Attack={hero.attack}, Defense={hero.defense}")

# -------------------------------
# Add consumables to inventory
# -------------------------------
potion_small = Consumable(name="Small Healing Potion", heal_amount=5)
potion_large = Consumable(name="Large Healing Potion", heal_amount=15)
hero.inventory.extend([potion_small, potion_large])

# -------------------------------
# Simulate damage and potion use
# -------------------------------
add_message("\n--- Taking Damage ---")
hero.take_damage(8)
add_message(f"Current HP: {hero.current_hp}/{hero.max_hp}")

add_message("\n--- Using Small Potion ---")
hero.use_consumable("Small Healing Potion", message_func=add_message)
add_message(f"Current HP: {hero.current_hp}/{hero.max_hp}")

add_message("\n--- Taking More Damage ---")
hero.take_damage(12)
add_message(f"Current HP: {hero.current_hp}/{hero.max_hp}")

add_message("\n--- Using Large Potion ---")
hero.use_consumable("Large Healing Potion", message_func=add_message)
add_message(f"Current HP: {hero.current_hp}/{hero.max_hp}")

# -------------------------------
# Simulate a battle
# -------------------------------
enemy = Character("Goblin", level=2)
add_message("\n--- Battle Start ---")
turn = 1
while hero.is_alive() and enemy.is_alive():
    add_message(f"\nTurn {turn}:")
    hero.deal_damage(enemy)
    if enemy.is_alive():
        enemy.deal_damage(hero)
    add_message(f"Hero HP: {hero.current_hp}/{hero.max_hp} | Enemy HP: {enemy.current_hp}/{enemy.max_hp}")
    turn += 1

if hero.is_alive():
    add_message("\nAria won the battle!")
else:
    add_message("\nAria was defeated!")
