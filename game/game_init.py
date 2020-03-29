import os
import random
import pygame
import pygame.font

from pygame.locals import *
from database.db_manip import *
from game.colors import Colors
from game.utils import Icons, Height, Width, BoardPos
from game.game_manip import *
from game.objects.Game import Game

bg = [255, 255, 255]
path = os.path.dirname(os.path.dirname(__file__))
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Grobold", 20)
game_display = pygame.display.set_mode((Width.display_width, Height.display_height), RESIZABLE)
game_display.fill(Colors.BEIGE)

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
                          ((Width.display_width / 3.8), (Height.display_height / 3)))
        pygame.display.update()
        clock.tick(15)


def game_menu():
    game_display.fill(Colors.BEIGE)
    choose_menu = ""
    menu = True
    pygame.display.set_caption('AUTO_CHESS')
    clock = pygame.time.Clock()

    pygame.display.flip()

    rect_new_game = pygame.draw.rect(game_display, Colors.RED,
                                     ((Width.display_width / 5), (Height.display_height / 1.8), 100, 50))
    rect_start_game = pygame.draw.rect(game_display, Colors.RED,
                                       ((Width.display_width / 2.5), (Height.display_height / 1.8), 100, 50))
    rect_character = pygame.draw.rect(game_display, Colors.RED,
                                      ((Width.display_width / 1.65), (Height.display_height / 1.8), 100, 50))

    create_button("New Game", rect_new_game, game_display)
    create_button("Continue", rect_start_game, game_display)
    create_button("Personnages", rect_character, game_display)

    large_text = pygame.font.Font('freesansbold.ttf', 115)

    game_display.blit(render('Pokéchess', large_text),
                      ((Width.display_width / 3.8), (Height.display_height / 6)))
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


def in_game():
    possible_pos_x = BoardPos.possible_pos_x
    list_pos_rect = []
    game_display.fill(Colors.BEIGE)
    game_continue = True
    init_party()
    all_champions = get_all_champions()
    clock = pygame.time.Clock()

    rect_return = pygame.draw.rect(game_display, Colors.RED,
                                   ((Width.display_width / 1.2), (Height.display_height / 12), 100, 50))
    create_button("Retour", rect_return, game_display)

    game = Game()

    fill_shop(game)
    champ_pos_x = Width.board_purchase_width + 27
    draw_player_shop_board()
    refresh_button = draw_refresh_button(15, 583, 100, Height.display_height)
    button_list = create_store_champ_view(game.player_shop, champ_pos_x, Height.board_purchase_height)
    change_page_back()
    group_rect(button_list, list_pos_rect)
    while game_continue:
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
                    game_continue = False
                if refresh_button.collidepoint(pos):
                    champ_pos_x = Width.board_purchase_width + 27
                    button_list = refresh_shop(button_list, game, champ_pos_x,
                                               Height.board_purchase_height)
                for champion_id, list_of_rect in button_list.items():
                    for rect in list_of_rect:
                        if rect.collidepoint(pos):
                            if len(game.player_board.champions) >= 5:
                                continue
                            print('len(game.player_board.champions) : %s' % len(game.player_board.champions))
                            game.add_champ_to_board(game.player_board, game.player_shop, champion_id)
                            list_of_sprites, champ_pos_x = create_player_board_view(game.player_board.champions,
                                                                                    champ_pos_x,
                                                                                    Height.board_player_height)
                            champion_sprite_dos = list_of_sprites.get(champion_id, '')
                            game_display.blit(background, (rect.x, rect.y), rect)
                            counter = 0
                            if list_pos_rect and list_of_sprites:
                                for sprite_id, sprite in list_of_sprites.items():
                                    print('len(game.player_board.champions) : %s' % len(game.player_board.champions))
                                    if counter <= len(game.player_board.champions):
                                        print('HERE')
                                        # pos_in_list = len(game.player_board.champions) - 1
                                        # print('pos_in_list : %s'%pos_in_list)
                                        # game_display.blit(sprite, (list_pos_rect[pos_in_list].x, 450))
                                        game_display.blit(sprite, (list_pos_rect[counter].x, 450))
                                        counter += 1

                                    # list_pos_rect.pop(pos_in_list)
                                # print('list_pos_rect[0].x : %s' % list_pos_rect[0].x)
                                # print('champion_sprite_dos : %s' % champion_sprite_dos)
                                # game_display.blit(champion_sprite_dos, (list_pos_rect[0].x, 450))
                                # list_pos_rect.pop(0)

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
                      ((Width.display_width / 5), (Height.display_height / 6)))
    rect_champ_width = Width.display_width
    rect_champ_height = Height.display_height
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
    rect_return = pygame.draw.rect(game_display, Colors.RED,
                                   ((Width.display_width / 1.2), (Height.display_height / 1.2), 100, 50))
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

    rect_stats_key_width = Width.display_width
    rect_stats_key_height = Height.display_height

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
        rect_champ_property_name = pygame.draw.rect(game_display, Colors.BEIGE,
                                                    (new_width, new_height, 100, 50))

        rect_champ_property_value = pygame.draw.rect(game_display, Colors.BEIGE,
                                                     (new_width2, new_height2, 100, 50))

        create_button(stat_value, rect_champ_property_name, game_display)
        create_button(stat_name, rect_champ_property_value, game_display)
        print('new_width : %s' % new_width)
        print('new_height : %s' % new_height)

        temp_rect_champ_height += 300

    rect_return = pygame.draw.rect(game_display, Colors.RED,
                                   ((Width.display_width / 1.2), (Height.display_height / 1.2), 100, 50))
    create_button("Retour", rect_return, game_display)
    large_text = pygame.font.Font('freesansbold.ttf', 50)
    text_surf, text_rect = text_objects(champion_name.title(), large_text, Colors.RED)
    text_rect.center = ((Width.display_width / 2), (Height.display_height / 10))
    game_display.blit(text_surf, text_rect)

    champion_sprite = pygame.image.load('%s%s' % (path, stats['img']))
    champion_sprite_dos = pygame.image.load('%s%s' % (path, stats['img_dos']))
    champion_sprite = pygame.transform.rotozoom(champion_sprite, 0, 2)
    champion_sprite_dos = pygame.transform.rotozoom(champion_sprite_dos, 0, 2)

    game_display.blit(champion_sprite, (900, 150))
    game_display.blit(champion_sprite_dos, (900, 300))
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
    create_champion_board_collection()
    create_board()
    create_party()


game_intro()
game_menu()
