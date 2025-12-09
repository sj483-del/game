# party_member.py
from character import Character

class PartyMember(Character):
    def __init__(self, name, race, char_class, level=1, is_player=True):
        super().__init__(name, race, char_class, level)
        self.is_player = is_player
