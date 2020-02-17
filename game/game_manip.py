import os
import random
import pygame
import pygame.font
from pygame.locals import *
from database.db_manip import *
from game.colors import Colors
from game.utils import Icons, Height, Width

pygame.font.init()
path = os.path.dirname(os.path.dirname(__file__))
font = pygame.font.SysFont("Grobold", 20)
background = pygame.Surface((1400, 700))

game_display = pygame.display.set_mode((Width.display_width, Height.display_height), RESIZABLE)


def create_button(text, rectangle, screen):
    new_game_text = font.render(text, False, (0, 0, 0))
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


def remove_element_on_list(list_of_char, pokemon):
    list_of_char.remove(pokemon)


def add_champ_to_player_board(champ_to_buy):
    champion_sprite_dos = pygame.image.load('%s%s' % (path, champ_to_buy['img']))
    champion_sprite_dos = pygame.transform.rotozoom(champion_sprite_dos, 0, 2)


def create_store_champ_view(available_to_buy, pos_x, pos_y):
    button_list = {}
    all_champions = get_all_champions()
    for champ in available_to_buy:
        champ_to_buy = all_champions.get(champ)
        board_champ = pygame.draw.rect(game_display, Colors.WHITE, (
            pos_x, pos_y, 200, Height.display_height))
        print('board_champ : %s' % board_champ)
        if champ not in button_list:
            button_list[champ] = []
        button_list[champ].append(board_champ)
        champion_sprite = pygame.image.load('%s%s' % (path, champ_to_buy['img']))
        champion_sprite = pygame.transform.rotozoom(champion_sprite, 0, 2)
        create_button("", board_champ, game_display)
        game_display.blit(champion_sprite, (pos_x + 30, pos_y))
        pos_x += 227
    return button_list


def create_player_champ_view(available_to_buy, pos_x, pos_y):
    list_of_sprites = {}
    all_champions = get_all_champions()
    for champ in available_to_buy:
        champ_to_buy = all_champions.get(champ)
        board_champ = pygame.draw.rect(game_display, Colors.GREEN, (
            pos_x, pos_y, 200, 146))
        champion_sprite_dos = pygame.image.load('%s%s' % (path, champ_to_buy['img_dos']))
        champion_sprite_dos = pygame.transform.rotozoom(champion_sprite_dos, 0, 2)
        list_of_sprites[champ] = champion_sprite_dos
        create_button("", board_champ, game_display)
        pos_x += 227
    return list_of_sprites, pos_x


def change_page_back():
    # 1056
    back_arrow = pygame.image.load('%s%s' % (path, '\\img\\arrow_back.png'))
    champion_sprite_dos = pygame.transform.rotozoom(back_arrow, 0, 2)


def draw_player_shop_board():
    board_player = pygame.draw.rect(game_display, Colors.BLACK, (
        Width.board_player_width, Height.board_player_height, (Width.display_width / 1.2), Height.display_height))

    board_purchase = pygame.draw.rect(game_display, Colors.RED, (
        Width.board_purchase_width, Height.board_purchase_height, (Width.display_width / 1.2), Height.display_height))
    create_button("", board_purchase, game_display)
    create_button("", board_player, game_display)


def fill_shop(all_champions):
    available_pokemon = add_champion_in_game(all_champions)
    available_to_buy = random.sample(available_pokemon, 5)
    return available_to_buy, available_pokemon


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


def refresh_shop(button_list, available_pokemon, pos_x, pos_y):
    for name, list_of_rect in button_list.items():
        for rect in list_of_rect:
            game_display.blit(background, (rect.x, rect.y), rect)
    available_to_buy = refill_shop(available_pokemon)
    # draw_player_shop_board()
    button_list = create_store_champ_view(available_to_buy, pos_x, pos_y)
    return button_list, available_to_buy


def group_rect(button_list, list_pos_rect):
    for name, list_of_rect in button_list.items():
        for rect in list_of_rect:
            if rect not in list_pos_rect:
                list_pos_rect.append(rect)
    list_pos_rect = sorted(list_pos_rect)
