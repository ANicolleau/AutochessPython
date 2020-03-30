import os
import sys
import pygame
import pygame.font
from pygame.locals import *

from database.db_manip import *
from .colors import Colors
from .objects.Game import Game
from .utils import Icons, Height, Width

pygame.font.init()
if getattr(sys, 'frozen', False):
    # frozen
    path = os.path.dirname(sys.executable)
else:
    # unfrozen
    path = os.path.dirname(os.path.dirname(__file__))
font = pygame.font.SysFont("Boo", 20)
background = pygame.Surface((1400, 700))

game_display = pygame.display.set_mode((Width.display_width, Height.display_height), RESIZABLE)


def create_button(text, rectangle, screen):
    new_game_text = font.render(text, True, (0, 0, 0))
    new_game_rect = new_game_text.get_rect(center=rectangle.center)
    return screen.blit(new_game_text, new_game_rect)


def add_champion_in_game(pokemons):
    available_pokemons = []
    print('PRINT POKEMONS')
    print('######################################################')
    print(pokemons)
    print('######################################################')
    for pokemon, stats in pokemons.items():
        print(pokemon, stats.get('number_on_game', ''))
        number_on_game = stats.get('number_on_game', '')
        for i in range(number_on_game):
            available_pokemons.append(pokemon)

    print(available_pokemons)
    return available_pokemons


#
# def remove_element_on_list(list_of_char, pokemon):
#     list_of_char.remove(pokemon)


def add_champ_to_player_board(champ_to_buy):
    champion_sprite_dos = pygame.image.load('%s%s' % (path, champ_to_buy['img']))
    champion_sprite_dos = pygame.transform.rotozoom(champion_sprite_dos, 0, 2)


def create_store_champ_view(player_shop, pos_x, pos_y):
    button_list = {}
    for champ in player_shop:
        board_champ = pygame.draw.rect(game_display, Colors.WHITE, (
            pos_x, pos_y, 200, Height.display_height))
        if champ not in button_list:
            button_list[champ.id] = []
        button_list[champ.id].append(board_champ)
        champion_sprite = pygame.image.load('%s%s' % (path, champ.img))
        champion_sprite = pygame.transform.rotozoom(champion_sprite, 0, 2)
        create_button("", board_champ, game_display)
        game_display.blit(champion_sprite, (pos_x + 30, pos_y))
        pos_x += 227
    return button_list


def create_player_board_view(player_shop, pos_x, pos_y):
    sprites = {}
    game_rectangles = []
    for champ in player_shop:
        board_champ = pygame.draw.rect(game_display, Colors.WHITE, (
            pos_x, pos_y, 200, 146))
        game_rectangles.append(board_champ)
        champion_sprite_dos = pygame.image.load('%s%s' % (path, champ.img_dos))
        champion_sprite_dos = pygame.transform.rotozoom(champion_sprite_dos, 0, 2)
        sprites[champ.id] = champion_sprite_dos
        create_button("", board_champ, game_display)
        pos_x += 227
    return sprites, pos_x, game_rectangles


def change_page_back():
    # 1056
    back_arrow = pygame.image.load('%s%s' % (path, '\\img\\arrow_back.png'))
    champion_sprite_dos = pygame.transform.rotozoom(back_arrow, 0, 2)


def draw_player_shop_board():
    board_player = pygame.draw.rect(game_display, Colors.BLACK, (
        Width.board_player_width, Height.board_player_height, (Width.display_width / 1.2), Height.display_height))

    board_purchase = pygame.draw.rect(game_display, Colors.BEIGE, (
        Width.board_purchase_width, Height.board_purchase_height, (Width.display_width / 1.2), Height.display_height))
    create_button("", board_purchase, game_display)
    create_button("", board_player, game_display)


# def fill_shop(all_champions):
#     available_pokemon = add_champion_in_game(all_champions)
#     available_to_buy = random.sample(available_pokemon, 5)
#     return available_to_buy, available_pokemon

def fill_shop(game):
    # type: (Game) -> None
    game.fill_player_shop()
    game.fill_ia_shop()


def refill_shop(available_pokemon):
    available_to_buy = random.sample(available_pokemon, 5)
    return available_to_buy


def draw_refresh_button(pos_x, pos_y, width, height):
    refresh_button = pygame.draw.rect(game_display, Colors.BEIGE, (
        pos_x, pos_y, width, height))
    create_button("", refresh_button, game_display)
    refresh = pygame.image.load('%s%s' % (path, Icons.REFRESH))
    refresh = pygame.transform.rotozoom(refresh, 0, 2)
    game_display.blit(refresh, (pos_x, pos_y))
    return refresh_button


def draw_button(pos_x, pos_y, width, height, icon="", text=""):
    refresh_button = pygame.draw.rect(game_display, Colors.BEIGE, (
        pos_x, pos_y, width, height))
    create_button(text, refresh_button, game_display)
    if icon:
        refresh = pygame.image.load('%s%s' % (path, icon))
        refresh = pygame.transform.rotozoom(refresh, 0, 2)
        game_display.blit(refresh, (pos_x, pos_y))
    return refresh_button


def refresh_shop(button_list, game, pos_x, pos_y):
    for name, list_of_rect in button_list.items():
        for rect in list_of_rect:
            game_display.blit(background, (rect.x, rect.y), rect)
    game.refresh_player_shop()
    button_list = create_store_champ_view(game.player_shop, pos_x, pos_y)
    return button_list


def group_rect(button_list, list_pos_rect):
    for name, list_of_rect in button_list.items():
        for rect in list_of_rect:
            if rect not in list_pos_rect:
                list_pos_rect.append(rect)
    list_pos_rect = sorted(list_pos_rect)
