import random
from typing import List
from database.models.heroes import Heroes
from database.models.board import Board
from database.models.champions import Champion
from database.db_manip import get_db_champions, get_db_heroes


class Game(object):
    def __init__(self):
        self.player = get_db_heroes()[0]  # type: Heroes
        self.ia = get_db_heroes()[1]  # type: Heroes
        self.available_champions = get_db_champions()  # type: List

        self.player_board = self.player.child  # type: Board
        self.ia_board = self.ia.child  # type: Board

        self.player_shop = []  # type: List
        self.ia_shop = []  # type: List

    def remove_champ_in_list(self, shop):
        # type: (List) -> None
        for champion in shop:
            self.available_champions.remove(champion)

    def fill_player_shop(self):
        self.player_shop = random.sample(self.available_champions, 5)
        self.remove_champ_in_list(self.player_shop)

    def fill_ia_shop(self):
        self.ia_shop = random.sample(self.available_champions, 5)
        self.remove_champ_in_list(self.ia_shop)

    def refresh_player_shop(self):
        self.add_champ_to_available_champions(self.player_shop)
        self.player_shop.clear()
        self.fill_player_shop()

    def add_champ_to_available_champions(self, shop):
        # type: (List) -> None
        for champion in shop:
            self.available_champions.append(champion)

    @staticmethod
    def add_champ_to_board(player, shop, champion_id):
        # type: (Board, List, Champion)->None
        print('player : %s'%player)
        if not player.champions:
            player.champions = []
        for champion in shop:
            print('champion.id : %s' % champion.id)
            print('champion_id : %s' % champion_id)
            if champion.id == champion_id:
                print('WHUEUUEUEUEU')
                player.champions.append(champion)
        print('player : %s'%player.champions)

    def buy_champion(self, shop, champion_bought, board):
        # type: (List, Champion, Board) -> None
        if not board.champions:
            board.champions = []
        board.champions.append(champion_bought)
        shop.remove(champion_bought)
        self.available_champions.remove(champion_bought)

    def remove_champ_shop(self, shop):
        pass
