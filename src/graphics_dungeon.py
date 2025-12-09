import pygame
import random
import sys

from party_member import PartyMember
from monster import Monster
from room import Room

pygame.init()

# ===============================
# WINDOW SETUP
# ===============================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Game")

clock = pygame.time.Clock()
FPS = 60

# ===============================
# TILE GRID
# ===============================
ROWS, COLS = 10, 10
TILE_SIZE = 40
MAP_OFFSET_X = 200
MAP_OFFSET_Y = 60

# ===============================
# COLORS & FONTS
# ===============================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
RED = (255, 70, 70)
GREEN = (0, 255, 0)

font = pygame.font.SysFont("consolas", 18)
msg_font = pygame.font.SysFont("consolas", 20)

# ===============================
# GAME STATE
# ===============================
party = [
    PartyMember("Aria", race="Aasimar", char_class="Paladin", level=1),
    PartyMember("Milly", race="Woodland Elf", char_class="Druid", level=1),
    PartyMember("Daisy", race="Rock Gnome", char_class="Ranger", level=1)
]

combat_turn_index = 0  # Track whose turn it is in combat
active_member_index = 0  # For movement highlighting
player_pos = [0, 0]

dungeon_map = [[None for _ in range(COLS)] for _ in range(ROWS)]
messages = []

in_combat = False
current_monster = None
combat_buttons = []

# ===============================
# MAP GENERATION
# ===============================
def generate_room():
    has_monster = random.random() < 0.2
    monster = Monster("Goblin", 8, 3) if has_monster else None
    return Room(has_monster, monster)

for r in range(ROWS):
    for c in range(COLS):
        dungeon_map[r][c] = generate_room()

# ===============================
# MESSAGE LOG
# ===============================
def add_message(text):
    messages.append(text)
    if len(messages) > 6:
        messages.pop(0)

# ===============================
# DRAW FUNCTIONS
# ===============================
def draw_party():
    y = 10
    for i, member in enumerate(party):
        hp_text = f"{member.name}: {member.current_hp}/{member.max_hp} HP"
        if i == active_member_index:
            hp_text = "> " + hp_text
        text = font.render(hp_text, True, WHITE)
        screen.blit(text, (10, y))
        y += 20

def draw_map():
    for row in range(ROWS):
        for col in range(COLS):
            x = MAP_OFFSET_X + col * TILE_SIZE
            y = MAP_OFFSET_Y + row * TILE_SIZE
            pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE))
            room = dungeon_map[row][col]
            if room.has_monster:
                pygame.draw.circle(screen, GREEN, (x + TILE_SIZE//2, y + TILE_SIZE//2), 6)
            if [row, col] == player_pos:
                pygame.draw.rect(screen, RED, (x + 5, y + 5, TILE_SIZE-10, TILE_SIZE-10))

def draw_message_box():
    pygame.draw.rect(screen, (30, 30, 30), (0, 450, WIDTH, 150))
    y = 460
    for msg in messages:
        screen.blit(msg_font.render(msg, True, WHITE), (10, y))
        y += 22

# ===============================
# COMBAT BUTTONS
# ===============================
class CombatButton:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 140, 40)
        self.color = (50, 50, 50)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        screen.blit(msg_font.render(self.text, True, WHITE), (self.rect.x + 10, self.rect.y + 8))

def setup_combat_buttons():
    return [
        CombatButton("Attack", 600, 200),
        CombatButton("Flee", 600, 260)
    ]

def draw_combat_ui():
    if current_monster:
        screen.blit(msg_font.render(f"Combat: {current_monster.name}", True, WHITE), (560, 120))
        screen.blit(msg_font.render(f"Monster HP: {current_monster.current_hp}/{current_monster.max_hp}", True, WHITE), (560, 150))
    for b in combat_buttons:
        b.draw()

# ===============================
# ROOM CHECK
# ===============================
def check_room_activate_combat():
    global in_combat, current_monster, combat_buttons, combat_turn_index
    room = dungeon_map[player_pos[0]][player_pos[1]]
    if room.has_monster:
        current_monster = room.monster
        in_combat = True
        combat_buttons = setup_combat_buttons()
        combat_turn_index = 0
        add_message(f"A {current_monster.name} appears!")

# ===============================
# MAIN LOOP
# ===============================
running = True
while running:
    clock.tick(FPS)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # Movement
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

        # Combat clicks - turn-based party system
        if in_combat and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Skip dead members
            while combat_turn_index < len(party) and not party[combat_turn_index].is_alive():
                combat_turn_index += 1

            if combat_turn_index >= len(party):
                # All members acted, monster retaliates
                alive_members = [m for m in party if m.is_alive()]
                if alive_members and current_monster.is_alive():
                    target = random.choice(alive_members)
                    current_monster.deal_damage(target)
                    add_message(f"{current_monster.name} strikes {target.name}!")
                combat_turn_index = 0

            else:
                current_member = party[combat_turn_index]

                # Attack button
                if combat_buttons[0].rect.collidepoint(mx, my):
                    if current_member.is_alive() and current_monster.is_alive():
                        current_member.deal_damage(current_monster)
                        add_message(f"{current_member.name} hits the {current_monster.name}!")

                    # Next member
                    combat_turn_index += 1

                    # Check monster defeat
                    if not current_monster.is_alive():
                        name = current_monster.name
                        room = dungeon_map[player_pos[0]][player_pos[1]]
                        room.has_monster = False
                        room.monster = None
                        in_combat = False
                        current_monster = None
                        combat_buttons = []
                        add_message(f"You defeated the {name}!")

                # Flee button
                elif combat_buttons[1].rect.collidepoint(mx, my):
                    if random.random() < 0.5:
                        add_message("You escaped!")
                        in_combat = False
                        current_monster = None
                        combat_buttons = []
                        combat_turn_index = 0
                    else:
                        add_message("Failed to flee!")
                        alive_members = [m for m in party if m.is_alive()]
                        if alive_members and current_monster.is_alive():
                            target = random.choice(alive_members)
                            current_monster.deal_damage(target)
                            add_message(f"{current_monster.name} strikes {target.name}!")

    # Game over check
    if not any(m.is_alive() for m in party):
        add_message("All party members died! Game over.")
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # DRAW EVERYTHING
    screen.fill(BLACK)
    draw_party()
    draw_map()
    draw_message_box()
    if in_combat:
        draw_combat_ui()

    pygame.display.flip()

pygame.quit()
sys.exit()
