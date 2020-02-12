import os
import random
import pygame
import pygame.font
from pygame.locals import *

from database.db_manip import *
from game.colors import Colors

display_width = 1400
display_height = 700

bg = [255, 255, 255]

path = os.path.dirname(os.path.dirname(__file__))
pygame.init()
pygame.font.init()
game_display = pygame.display.set_mode((display_width, display_height), RESIZABLE)
game_display.fill(Colors.BEIGE)
font = pygame.font.SysFont("Grobold", 20)

NEW_GAME = "new_game"
CONTINUE = "continue"
OPTIONS = "options"

_circle_cache = {}


def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render(text, font, gfcolor=pygame.Color('yellow'), ocolor=(0, 0, 0), opx=5):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


def text_objects(text, style, object_color):
    text_surface = style.render(text, True, object_color)
    return text_surface, text_surface.get_rect()


def game_intro():
    game_display.fill(Colors.BEIGE)
    intro = True
    pygame.display.set_caption('AUTO_CHESS')
    clock = pygame.time.Clock()

    pygame.Rect(150, 400, 100, 50)

    pygame.display.flip()

    while intro:
        if pygame.time.get_ticks() > 2000:
            intro = False
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                drop_database()
                pygame.quit()
                quit()

        game_display.fill(Colors.BEIGE)
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        game_display.blit(render('Pokéchess', large_text),
                          ((display_width / 3.8), (display_height / 3)))
        pygame.display.update()
        clock.tick(15)


def create_button(text, rectangle, screen):
    new_game_text = font.render(text, False, (0, 0, 0))
    new_game_rect = new_game_text.get_rect(center=rectangle.center)
    return screen.blit(new_game_text, new_game_rect)


def game_menu():
    game_display.fill(Colors.BEIGE)
    choose_menu = ""
    menu = True
    pygame.display.set_caption('AUTO_CHESS')
    clock = pygame.time.Clock()

    pygame.display.flip()

    rect_new_game = pygame.draw.rect(game_display, Colors.RED, ((display_width / 5), (display_height / 1.8), 100, 50))
    rect_start_game = pygame.draw.rect(game_display, Colors.RED,
                                       ((display_width / 2.5), (display_height / 1.8), 100, 50))
    rect_character = pygame.draw.rect(game_display, Colors.RED,
                                      ((display_width / 1.65), (display_height / 1.8), 100, 50))

    create_button("New Game", rect_new_game, game_display)
    create_button("Continue", rect_start_game, game_display)
    create_button("Personnages", rect_character, game_display)

    large_text = pygame.font.Font('freesansbold.ttf', 115)

    game_display.blit(render('Pokéchess', large_text),
                      ((display_width / 3.8), (display_height / 6)))
    pygame.display.update()
    clock.tick(15)
    while menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drop_database()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if rect_new_game.collidepoint(pos):
                    choose_menu = NEW_GAME
                    menu = False
                elif rect_start_game.collidepoint(pos):
                    choose_menu = CONTINUE
                    menu = False
                elif rect_character.collidepoint(pos):
                    choose_menu = OPTIONS
                    menu = False
    if choose_menu == NEW_GAME:
        in_game()
    elif choose_menu == CONTINUE:
        in_game()  # Devrait reprendre la partie en cours.
    elif choose_menu == OPTIONS:
        show_all_characters()


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
    # rect_champ = pygame.draw.rect(game_display, Colors.RED,
    #                               (temp_rect_champ_width / 1.2, temp_rect_champ_height / 1.8, 100, 50))
    # button_list[champion] = rect_champ
    # create_button(champion, rect_champ, game_display)
    # temp_rect_champ_width -= 150
    # if temp_rect_champ_width <= 100:
    #     temp_rect_champ_width = rect_champ_width
    #     temp_rect_champ_height -= 150


def remove_element_on_list(list_of_char, list_to_removed):
    for pokemon in list_to_removed:
        list_of_char.remove(pokemon)


def in_game():
    game_display.fill(Colors.BEIGE)
    game = True
    init_party()
    all_champions = get_all_champions()
    clock = pygame.time.Clock()
    rect_return = pygame.draw.rect(game_display, Colors.RED, ((display_width / 1.2), (display_height / 12), 100, 50))
    create_button("Retour", rect_return, game_display)

    board_purchase = pygame.draw.rect(game_display, Colors.BLACK, (
        (display_width / 11.5), (display_height / 1.6), (display_width / 1.2), display_height))

    board_player = pygame.draw.rect(game_display, Colors.RED, (
        (display_width / 11.5), (display_height / 1.2), (display_width / 1.2), display_height))
    create_button("", board_purchase, game_display)
    create_button("", board_player, game_display)

    available_pokemon = add_champion_in_game(all_champions)
    available_to_buy = random.sample(available_pokemon, 5)
    remove_element_on_list(available_pokemon, available_to_buy)
    print('available_pokemon : %s' % available_pokemon)
    while game:

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drop_board()
                drop_database()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if rect_return.collidepoint(pos):
                    drop_board()
                    game = False

        pygame.display.update()
        clock.tick(15)
    game_menu()


def create_stats_area(champion_stats):
    stats = []
    health = "Points de vie : %s" % champion_stats.get("health", "")
    price = "Prix : %s" % champion_stats.get("price", "")
    rarity = "Rareté : %s" % champion_stats.get("rarity", "")
    level = "Niveau : %s" % champion_stats.get("level", "")
    description = "Description : %s" % champion_stats.get("description", "")

    stats.append(health)
    stats.append(price)
    stats.append(rarity)
    stats.append(level)
    stats.append(description)
    return stats


def show_all_characters():
    game_display.fill(Colors.BEIGE)
    game = True
    selected_champion = ""
    all_champions = get_all_champions()
    large_text = pygame.font.Font('freesansbold.ttf', 80)

    game_display.blit(render('Pokémon disponibles', large_text),
                      ((display_width / 5), (display_height / 6)))
    rect_champ_width = display_width
    rect_champ_height = display_height
    button_list = {}
    temp_rect_champ_width = rect_champ_width
    temp_rect_champ_height = rect_champ_height
    for champion in all_champions:
        rect_champ = pygame.draw.rect(game_display, Colors.RED,
                                      (temp_rect_champ_width / 1.2, temp_rect_champ_height / 1.8, 100, 50))
        button_list[champion] = rect_champ
        create_button(champion, rect_champ, game_display)
        temp_rect_champ_width -= 150
        if temp_rect_champ_width <= 100:
            temp_rect_champ_width = rect_champ_width
            temp_rect_champ_height -= 150

    clock = pygame.time.Clock()
    rect_return = pygame.draw.rect(game_display, Colors.RED, ((display_width / 1.2), (display_height / 1.2), 100, 50))
    create_button("Retour", rect_return, game_display)

    pygame.display.update()
    clock.tick(15)
    while game:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drop_database()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if rect_return.collidepoint(pos):
                    game = False
                for name, rect in button_list.items():
                    if rect.collidepoint(pos):
                        selected_champion = name
                        game = False
    if selected_champion:
        for champion_name, stats in all_champions.items():
            if selected_champion == champion_name:
                print('(champion_name : stats) [%s : %s]' % (champion_name, stats))
                show_stats_champions(selected_champion, stats)
    game_menu()


def show_stats_champions(champion_name, stats):
    game_display.fill(Colors.BEIGE)
    game = True
    clock = pygame.time.Clock()

    champ_stats = create_stats_area(stats)

    rect_stats_key_width = display_width
    rect_stats_key_height = display_height

    temp_rect_champ_width = rect_stats_key_width
    temp_rect_champ_height = rect_stats_key_height
    for stat in champ_stats:
        print('stat : %s' % stat)
        stat_name = stat.split(':')[0].title() + ' :'
        stat_value = stat.split(':')[1].title()
        new_height = temp_rect_champ_height / 5
        new_width = temp_rect_champ_width / 3

        new_height2 = temp_rect_champ_height / 5
        new_width2 = temp_rect_champ_width / 11
        rect_champ_property_name = pygame.draw.rect(game_display, Colors.RED,
                                                    (new_width, new_height, 100, 50))

        rect_champ_property_value = pygame.draw.rect(game_display, Colors.RED,
                                                     (new_width2, new_height2, 100, 50))

        create_button(stat_value, rect_champ_property_name, game_display)
        create_button(stat_name, rect_champ_property_value, game_display)
        print('new_width : %s' % new_width)
        print('new_height : %s' % new_height)

        temp_rect_champ_height += 300

    rect_return = pygame.draw.rect(game_display, Colors.RED, ((display_width / 1.2), (display_height / 1.2), 100, 50))
    create_button("Retour", rect_return, game_display)
    large_text = pygame.font.Font('freesansbold.ttf', 50)
    text_surf, text_rect = text_objects(champion_name.title(), large_text, Colors.RED)
    text_rect.center = ((display_width / 2), (display_height / 10))
    game_display.blit(text_surf, text_rect)

    champion_sprite = pygame.image.load('%s%s' % (path, stats['img']))
    champion_sprite_dos = pygame.image.load('%s%s' % (path, stats['img_dos']))
    champion_sprite = pygame.transform.rotozoom(champion_sprite, 0, 2)
    champion_sprite_dos = pygame.transform.rotozoom(champion_sprite_dos, 0, 2)

    game_display.blit(champion_sprite, (600, 150))
    game_display.blit(champion_sprite_dos, (600, 300))
    pygame.display.flip()

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drop_database()
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if rect_return.collidepoint(pos):
                    game = False

        pygame.display.update()
        clock.tick(15)
    show_all_characters()


def init_party():
    create_board()


game_intro()
game_menu()
