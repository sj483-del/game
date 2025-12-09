import pygame
import random
import sys

from src.party_member import PartyMember
from src.player import Player
from src.monster import Monster
from src.room import Room

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Game")

clock = pygame.time.Clock()
FPS = 60

# Tile grid
ROWS, COLS = 10, 10
TILE_SIZE = 40
MAP_OFFSET_X = 200
MAP_OFFSET_Y = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
RED = (255, 70, 70)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont("consolas", 18)
msg_font = pygame.font.SysFont("consolas", 20)

# Game objects
player = Player("Hero", max_hp=20)
party = [
    PartyMember("Warrior", 20, 4),
    PartyMember("Archer", 14, 3),
    PartyMember("Cleric", 16, 2)
]

player_pos = [0, 0]
dungeon_map = [[None for _ in range(COLS)] for _ in range(ROWS)]

# Combat state
in_combat = False
current_monster = None
combat_buttons = []

# Messages
messages = []


# ===============================
# MAP GENERATION
# ===============================
def generate_room():
    """Create a random room with a small chance of containing a monster."""
    has_monster = random.random() < 0.2
    monster = None

    if has_monster:
        monster = Monster("Goblin", 8, 3)

    return Room(has_monster, monster)


for r in range(ROWS):
    for c in range(COLS):
        dungeon_map[r][c] = generate_room()


# ===============================
# MESSAGE HANDLING
# ===============================
def add_message(text):
    messages.append(text)
    if len(messages) > 6:
        messages.pop(0)


# ===============================
# DRAWING FUNCTIONS
# ===============================
def draw_hp_text():
    """Draw player HP."""
    hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, WHITE)
    screen.blit(hp_text, (10, 10))


def draw_party():
    """Draw party member HPs."""
    y = 40
    for member in party:
        text = font.render(f"{member.name}: {member.hp}/{member.max_hp} HP", True, WHITE)
        screen.blit(text, (10, y))
        y += 20


def draw_map():
    """Draw grid map and markers."""
    for row in range(ROWS):
        for col in range(COLS):
            x = MAP_OFFSET_X + col * TILE_SIZE
            y = MAP_OFFSET_Y + row * TILE_SIZE

            pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE))

            room = dungeon_map[row][col]

            # Monster indicator
            if room.has_monster:
                pygame.draw.circle(screen, GREEN, (x + 20, y + 20), 6)

            # Player indicator
            if [row, col] == player_pos:
                pygame.draw.rect(screen, RED, (x + 5, y + 5, 30, 30))


def draw_message_box():
    """Draw text message log at bottom."""
    pygame.draw.rect(screen, (30, 30, 30), (0, 450, WIDTH, 150))
    y = 460
    for msg in messages:
        screen.blit(msg_font.render(msg, True, WHITE), (10, y))
        y += 22


# ===============================
# COMBAT BUTTON CLASS & UI
# ===============================
class CombatButton:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 140, 40)
        self.color = (50, 50, 50)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        txt = msg_font.render(self.text, True, WHITE)
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 8))


def setup_combat_buttons():
    return [
        CombatButton("Attack", 600, 200),
        CombatButton("Flee", 600, 260)
    ]


def draw_combat_ui():
    if current_monster:
        screen.blit(
            msg_font.render(f"Combat: {current_monster.name}", True, WHITE),
            (560, 120)
        )
        screen.blit(
            msg_font.render(f"Monster HP: {current_monster.hp}/{current_monster.max_hp}", True, WHITE),
            (560, 150)
        )

    for b in combat_buttons:
        b.draw()


# ===============================
# ROOM ENTRY CHECK
# ===============================
def check_room_activate_combat():
    global in_combat, current_monster, combat_buttons
    room = dungeon_map[player_pos[0]][player_pos[1]]

    if room.has_monster:
        current_monster = room.monster
        in_combat = True
        combat_buttons = setup_combat_buttons()
        add_message(f"A {current_monster.name} appears!")


# ===============================
# MAIN GAME LOOP
# ===============================
running = True
while running:
    clock.tick(FPS)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # Movement - one tile per press
        if not in_combat and event.type == pygame.KEYDOWN:
            r, c = player_pos
            if event.key == pygame.K_LEFT and c > 0:
                player_pos[1] -= 1
            elif event.key == pygame.K_RIGHT and c < COLS - 1:
                player_pos[1] += 1
            elif event.key == pygame.K_UP and r > 0:
                player_pos[0] -= 1
            elif event.key == pygame.K_DOWN and r < ROWS - 1:
                player_pos[0] += 1

            check_room_activate_combat()

        # Combat clicks
        if in_combat and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Attack
            if combat_buttons[0].rect.collidepoint(mx, my):
                # Player attack
                player.deal_damage(current_monster)

                # Party attack
                for member in party:
                    if member.is_alive():
                        member.deal_damage(current_monster)
                        add_message(f"{member.name} hits the {current_monster.name}!")

                # Monster retaliates
                if current_monster.is_alive():
                    alive_members = [m for m in party if m.is_alive()]
                    if alive_members:
                        target = random.choice(alive_members)
                        current_monster.deal_damage(target)
                        add_message(f"{current_monster.name} strikes {target.name}!")
                else:
                    # Monster defeated - SAFE VERSION
                    name = current_monster.name
                    room = dungeon_map[player_pos[0]][player_pos[1]]
                    room.has_monster = False
                    room.monster = None

                    in_combat = False
                    current_monster = None
                    combat_buttons = []
                    add_message(f"You defeated the {name}!")

            # Flee
            elif combat_buttons[1].rect.collidepoint(mx, my):
                if random.random() < 0.5:
                    add_message("You escaped!")
                    in_combat = False
                    current_monster = None
                    combat_buttons = []
                else:
                    add_message("Failed to flee!")
                    current_monster.deal_damage(player)

    # Player defeated?
    if not player.is_alive():
        add_message("You died! Game over.")
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # DRAW EVERYTHING
    screen.fill(BLACK)
    draw_hp_text()
    draw_party()
    draw_map()

    if in_combat:
        draw_combat_ui()

    draw_message_box()

    pygame.display.flip()

pygame.quit()
sys.exit()
