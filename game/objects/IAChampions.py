from game.objects.Game import Game, List
from typing import Dict
import random


class IAChampions(object):
    def __init__(self, available_champions):
        # type: (List) -> None
        self.available_champions = available_champions
        self.champions = self.set_champions()

    def set_champions(self):
        champions = {}
        for i in range(10):
            champions[i] = []
            champions[i] = random.sample(self.available_champions, 3)
        return champions
