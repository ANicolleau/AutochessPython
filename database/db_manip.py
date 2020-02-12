from .models import *
from .constants import DB_CONNECTION_STRING

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
    Champion.drop_table_champion()
    Board.drop_table_board()
    Type.drop_table_type()
    User.drop_table_user()
    Heroes.drop_table_heroes()
    print("TABLES DELETED")
