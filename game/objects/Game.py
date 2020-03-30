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

        self.player_champion_battle = []

        self.player_shop = []  # type: List
        self.ia_shop = []  # type: List

    def clear_champ_battle(self):
        self.player_champion_battle.clear()

    def remove_champ_in_list(self, shop):
        # type: (List) -> None
        for champion in shop:
            self.available_champions.remove(champion)

    def fill_player_shop(self):
        # type: () -> None
        self.player_shop = random.sample(self.available_champions, 5)
        self.remove_champ_in_list(self.player_shop)

    def fill_ia_shop(self):
        # type: () -> None
        self.ia_shop = random.sample(self.available_champions, 5)
        self.remove_champ_in_list(self.ia_shop)

    def refresh_player_shop(self):
        # type: () -> None
        self.add_champ_shop_to_available_champions(self.player_shop)
        self.player_shop.clear()
        self.fill_player_shop()

    def add_champ_shop_to_available_champions(self, shop):
        # type: (List) -> None
        for champion in shop:
            self.available_champions.append(champion)

    def add_champ_by_id_to_available_champions(self, champion_id, board):
        # type: (Champion, List) -> None
        for champion in board:
            self.get_champion_by_id_in_shop(champion.id)
            self.get_champion_by_id_in_shop(champion_id)
            if champion.id == champion_id:
                self.player_board.champions.remove(champion)
                self.available_champions.append(champion)

    @staticmethod
    def add_champ_to_board(player, money, shop, champion_id):
        # type: (Board, Heroes, List, Champion)->None
        if not player.champions:
            player.champions = []
        for champion in shop:
            if champion.id == champion_id and money.money >= champion.price:
                player.champions.append(champion)
                money.money -= champion.price

    def buy_champion(self, shop, champion_bought, board):
        # type: (List, Champion, Board) -> None
        if not board.champions:
            board.champions = []
        board.champions.append(champion_bought)
        shop.remove(champion_bought)
        self.available_champions.remove(champion_bought)

    def get_champion_by_id_in_shop(self, champion_id):
        for champion in self.player_shop:
            if champion.id == champion_id:
                print(champion.name)
                return champion
        return

    def remove_champ_shop(self, board, champion_id):
        for champion in board:
            if champion.id == champion_id:
                self.player_shop.remove(champion)

    def get_players_health(self):
        return self.player.health

    def get_players_money(self):
        return self.player.money

    def end_turn(self, tour_number):
        if tour_number <= 2:
            self.player.money += 3
        elif 2 < tour_number <= 5:
            self.player.money += 5
        else:
            self.player.money += 7

    def set_ia_champion(self):
        if not self.ia_board.champions:
            self.ia_board.champions = []

    def select_champion(self, champion):
        self.player_champion_battle.append(champion)

    def lost_life(self, ia_champions):
        damage = 0
        for champion in ia_champions:
            if champion.health > 0:
                damage += 1
        self.player.health -= damage

    @staticmethod
    def check_champ_hp(champions):
        dead_champ = 0
        if len(champions) == 0:
            return 3
        for champion in champions:
            if champion.health <= 0:
                dead_champ += 1
        return dead_champ

