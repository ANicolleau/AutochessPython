from typing import Dict


class TYPE(object):
    FIRE = 'fire'
    GRASS = 'grass'
    WATER = 'water'
    PSYCHIC = 'psychic'
    DARK = 'dark'
    DRAGON = 'dragon'
    NORMAL = 'normal'
    ELECTRIC = 'electric'
    ALL = 'all'


class Combat(object):
    def __init__(self, ia_battle_champions, player_battle_champions):
        self.ia_battle_champions = ia_battle_champions
        self.player_battle_champions = player_battle_champions
        self.fight_pair = self.set_battle()
        self.health_point = {}

    @staticmethod
    def get_weakness(champion_type):
        if champion_type == TYPE.FIRE:
            return TYPE.WATER
        if champion_type == TYPE.GRASS:
            return TYPE.FIRE
        if champion_type == TYPE.WATER:
            return TYPE.ELECTRIC
        if champion_type == TYPE.PSYCHIC:
            return TYPE.DARK
        if champion_type == TYPE.DARK:
            return TYPE.NORMAL
        if champion_type == TYPE.DRAGON:
            return TYPE.PSYCHIC
        if champion_type == TYPE.NORMAL:
            return TYPE.GRASS

    @staticmethod
    def get_effectiveness(champion_type):
        if champion_type == TYPE.FIRE:
            return TYPE.GRASS
        if champion_type == TYPE.GRASS:
            return TYPE.WATER
        if champion_type == TYPE.WATER:
            return TYPE.FIRE
        if champion_type == TYPE.PSYCHIC:
            return TYPE.DRAGON
        if champion_type == TYPE.DARK:
            return TYPE.PSYCHIC
        if champion_type == TYPE.DRAGON:
            return TYPE.ALL
        if champion_type == TYPE.NORMAL:
            return TYPE.DARK

    def set_battle(self):
        # type: () -> Dict
        fight_pair = {champion: None for champion in self.player_battle_champions}
        for attacker_champion, other_champion in fight_pair.items():
            if attacker_champion.health <= 0:
                continue
            type_weak = self.get_effectiveness(attacker_champion.type)
            for attacked_champion in self.ia_battle_champions:
                if attacked_champion.health <= 0:
                    continue
                if attacked_champion.type == TYPE.DRAGON:
                    fight_pair[attacker_champion] = attacked_champion
                elif attacked_champion.type == type_weak:
                    fight_pair[attacker_champion] = attacked_champion
                else:
                    fight_pair[attacker_champion] = attacked_champion
        return fight_pair

    def battle(self):
        print('self.fight_pair : %s' % self.fight_pair)
        for attacker, attacked in self.fight_pair.items():
            if attacker not in self.health_point:
                self.health_point[attacker] = attacker.health
            if attacked:
                if attacked.health <= 0:
                    self.fight_pair = self.set_battle()
                attacked.health -= attacker.attack * 2 if self.get_weakness(
                    attacked.type) == attacker.type else attacker.attack
                print('attacked.name : %s' % attacked.name)
                print('attacked.health : %s' % attacked.health)
                if attacked.health > 0:
                    attacker.health -= attacked.attack * 2 if self.get_weakness(
                        attacker.type) == attacked.type else attacked.attack
                print('attacker.health : %s' % attacker.health)

    def reset_health(self, champions):
        for champion in champions:
            champion.health = self.health_point[champion]
