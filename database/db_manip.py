from .object import *


# Mettre ça dans le game_init pour essayer de voir comment récupérer tous les objets champions.
def get_all_champions():
    all_champions_object = get_all()
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
            'img_dos': champion.img_dos
        }
    print(all_champion_dict)
    # for id, name, health, price, description, rarity, level in champion:
    #     print(id, name, health, price, description, rarity, level)
    print('############################################################################################')
    return all_champion_dict
