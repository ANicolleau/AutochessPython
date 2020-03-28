from .models import *
from .constants import DB_CONNECTION_STRING, PartyState
import random

Base = declarative_base()
engine = create_engine(DB_CONNECTION_STRING, echo=True)


# Mettre ça dans le game_init pour essayer de voir comment récupérer tous les objets champions.
def get_all_champions():
    all_champions_object = Champion.get_all()
    all_champion_dict = {}
    print('############################################################################################')
    for champion in all_champions_object:
        all_champion_dict[champion.name] = {
            'health': champion.health,
            'price': champion.price,
            'description': champion.description,
            'rarity': champion.rarity,
            'level': champion.level,
            'img': champion.img,
            'img_dos': champion.img_dos,
            'number_on_game': champion.number_on_game
        }
    print(all_champion_dict)
    # for id, name, health, price, description, rarity, level in champion:
    #     print(id, name, health, price, description, rarity, level)
    print('############################################################################################')
    return all_champion_dict


def get_db_champions():
    return Champion.get_all()


def create_champion_board_collection():
    all_champions = get_db_champions()
    player_shop = random.sample(all_champions, 5)
    ia_shop = random.sample(all_champions, 5)
    print('player_shop : %s' % player_shop)
    print('ia_shop : %s' % ia_shop)


def create_board():
    for i in range(1, 3):
        name = "player"
        spot = 0
        if i == 2:
            name = "IA"
            spot = 1
        game_board = Board(id=i, name=name, spot=spot)
        session.add(game_board)
    session.commit()
    get_all_boards()
    print("BOARD CREATED")


def drop_board():
    to_delete = [session.query(Board).get(1), session.query(Board).get(2)]
    for in_game_board in to_delete:
        session.delete(in_game_board)
    session.commit()
    print("BOARD DELETED")


def get_all_boards():
    all_boards_object = Board.get_all()
    print(all_boards_object)
    all_boards_dict = {}
    print('############################################################################################')
    for in_game_board in all_boards_object:
        all_boards_dict[in_game_board.name] = {
            'spot': in_game_board.spot
        }
    print(all_boards_dict)
    # for id, name, health, price, description, rarity, level in champion:
    #     print(id, name, health, price, description, rarity, level)
    print('############################################################################################')
    return all_boards_dict


def drop_database():
    Champion.drop_table()
    Board.drop_table()
    Type.drop_table()
    User.drop_table()
    Heroes.drop_table()
    Party.drop_table()
    print("TABLES DELETED")


def create_heroes():
    for i in range(1, 3):
        name = "player"
        is_ia = False
        if i == 2:
            name = "IA"
            is_ia = True
        hero = Heroes(id=i, name=name, health=15, money=0, level=1, ia=is_ia)
        session.add(hero)
    session.commit()
    print("HEROES CREATED")


def get_heroes():
    db_heroes = Heroes.get_all()
    print(db_heroes)
    heroes_dict = {}
    print('############################################################################################')
    for hero in db_heroes:
        heroes_dict[hero.name] = {
            'health': hero.health,
            'money': hero.money,
            'level': hero.level,
            'champions': hero.champions,
            'ia': hero.ia
        }
    print(heroes_dict)
    # for id, name, health, price, description, rarity, level in champion:
    #     print(id, name, health, price, description, rarity, level)
    print('############################################################################################')
    return heroes_dict


def get_db_heroes():
    return Heroes.get_all()


def create_party():
    create_heroes()
    # in_game_heroes = get_heroes()
    db_party = Party(id=1, players=get_db_heroes(), player_turn='', state=PartyState.IN_GAME)
    session.add(db_party)
    session.commit()
    print("PARTY CREATED")


def get_party():
    db_party = Party.get_all()
    # print(db_party)
    # party_dict = {}
    # print('############################################################################################')
    # for actual_party in db_party:
    #     party_dict['party'] = {
    #         'id': actual_party.id,
    #         'players': actual_party.players,
    #         'player_turn': actual_party.player_turn,
    #         'state': actual_party.state,
    #     }
    # print(party_dict)
    # # for id, name, health, price, description, rarity, level in champion:
    # #     print(id, name, health, price, description, rarity, level)
    # print('############################################################################################')
    # return party_dict
    return Party.get_all()
