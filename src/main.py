# main.py
from party_member import PartyMember

# Example party
party = [
    PartyMember("Aria", race="Aasimar", char_class="Paladin", level=1),
    PartyMember("Milly", race="Woodland Elf", char_class="Druid", level=1),
    PartyMember("Daisy", race="Rock Gnome", char_class="Ranger", level=1)
]

# Test printing stats
for member in party:
    print(f"{member.name} ({member.race} {member.char_class}) - HP: {member.current_hp}/{member.max_hp}")
