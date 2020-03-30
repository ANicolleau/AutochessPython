import pygame.font
import time

import pygame.font

from game.game_manip import *
from game.objects.Game import Game
from game.objects.IAChampions import IAChampions
from game.objects.combat import Combat
from game.utils import BoardPos
import sys
bg = [255, 255, 255]

if getattr(sys, 'frozen', False):
    # frozen
    path = os.path.dirname(sys.executable)
else:
    # unfrozen
    path = os.path.dirname(os.path.dirname(__file__))
# path = os.path.dirname(os.path.dirname(__file__))
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Boo", 20)
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
                sys.exit()

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
                sys.exit()
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
    number_turn = 1
    list_pos_rect = []
    board_rectangles = []
    game_display.fill(Colors.BEIGE)
    game_continue = True
    init_party()
    all_champions = get_all_champions()
    clock = pygame.time.Clock()

    rect_return = pygame.draw.rect(game_display, Colors.RED,
                                   ((Width.display_width / 1.1), (Height.display_height / 50), 100, 50))
    create_button("Retour", rect_return, game_display)

    game = Game()

    fill_shop(game)
    champ_pos_x = Width.board_purchase_width + 27
    draw_player_shop_board()
    refresh_button = draw_refresh_button(15, 583, 100, Height.display_height)
    end_turn_button = draw_button(1300, 625, 100, Height.display_height, text="Terminer tour")
    button_list = create_store_champ_view(game.player_shop, champ_pos_x, Height.board_purchase_height)
    change_page_back()
    group_rect(button_list, list_pos_rect)
    large_text = pygame.font.Font('freesansbold.ttf', 40)
    while game_continue:
        game_display.blit(render("Phase d'achat et de selection", large_text),
                          ((Width.display_width / 3.8), (Height.display_height / 6)))
        health_player_rect = pygame.draw.rect(game_display, Colors.RED,
                                              ((Width.display_width / 1.05), (Height.display_height / 1.2), 100, 50))
        money_player_rect = pygame.draw.rect(game_display, Colors.RED,
                                             ((Width.display_width / 1.05), (Height.display_height / 1.35), 100, 50))
        turn_number_rect = pygame.draw.rect(game_display, Colors.RED,
                                            ((Width.display_width / 50), (Height.display_height / 50), 100, 50))
        create_button("HP : %s" % game.get_players_health(), health_player_rect, game_display)
        create_button("OR : %s" % game.get_players_money(), money_player_rect, game_display)
        create_button("TOUR : %s" % number_turn, turn_number_rect, game_display)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drop_board()
                drop_database()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if len(game.player_board.champions) >= 1 and len(game.player_champion_battle) < 3:
                        print('Poeutte')
                        if game.player_board.champions[0] not in game.player_champion_battle:
                            game.select_champion(game.player_board.champions[0])
                            print('game.player_board.champions[1] : %s' % game.player_board.champions[0])
                if event.key == pygame.K_2:
                    if len(game.player_board.champions) >= 2 and len(game.player_champion_battle) < 3:
                        if game.player_board.champions[1] not in game.player_champion_battle:
                            game.select_champion(game.player_board.champions[1])
                            print('game.player_board.champions[2] : %s' % game.player_board.champions[1])
                if event.key == pygame.K_3:
                    if len(game.player_board.champions) >= 3 and len(game.player_champion_battle) < 3:
                        if game.player_board.champions[2] not in game.player_champion_battle:
                            game.select_champion(game.player_board.champions[2])
                            print('game.player_board.champions[3] : %s' % game.player_board.champions[2])
                if event.key == pygame.K_4:
                    if len(game.player_board.champions) >= 4 and len(game.player_champion_battle) < 3:
                        if game.player_board.champions[3] not in game.player_champion_battle:
                            game.select_champion(game.player_board.champions[3])
                            print('game.player_board.champions[4] : %s' % game.player_board.champions[3])
                if event.key == pygame.K_5:
                    if len(game.player_board.champions) >= 5 and len(game.player_champion_battle) < 3:
                        if game.player_board.champions[4] not in game.player_champion_battle:
                            game.select_champion(game.player_board.champions[4])
                            print('game.player_board.champions[5] : %s' % game.player_board.champions[4])
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if rect_return.collidepoint(pos):
                    drop_board()
                    game_continue = False
                if refresh_button.collidepoint(pos):
                    champ_pos_x = Width.board_purchase_width + 27
                    button_list = refresh_shop(button_list, game, champ_pos_x,
                                               Height.board_purchase_height)
                champ_pos_x = Width.board_purchase_width + 27
                if end_turn_button.collidepoint(pos):
                    battle(number_turn, game)
                    number_turn += 1
                    game.end_turn(number_turn)
                    champ_pos_x = Width.board_purchase_width + 27
                    button_list = refresh_shop(button_list, game, champ_pos_x,
                                               Height.board_purchase_height)
                    champ_pos_x = Width.board_purchase_width + 27
                    continue
                sprites = []
                for champion_id, list_of_rect in button_list.items():
                    for rect in list_of_rect:
                        for board_rect in board_rectangles:
                            if board_rect.collidepoint(pos):
                                game.add_champ_by_id_to_available_champions(champion_id,
                                                                            game.player_board.champions)
                                counter = 0
                                if list_pos_rect and sprites:
                                    for sprite_id, sprite in sprites.items():
                                        if counter <= len(game.player_board.champions):
                                            game_display.blit(sprite, (list_pos_rect[counter].x, 450))
                                            counter += 1
                                pos = (0, 0)
                        if rect.collidepoint(pos):
                            champion = game.get_champion_by_id_in_shop(champion_id)
                            if len(
                                    game.player_board.champions) >= 5 or not champion or champion.price > game.player.money:
                                continue
                            game.add_champ_to_board(game.player_board, game.player, game.player_shop, champion_id)
                            game.remove_champ_shop(game.player_board.champions, champion_id)
                            sprites, champ_pos_x, board_rectangles = create_player_board_view(
                                game.player_board.champions,
                                champ_pos_x,
                                Height.board_player_height)
                            game_display.blit(background, (rect.x, rect.y), rect)
                            counter = 0
                            if list_pos_rect and sprites:
                                for sprite_id, sprite in sprites.items():
                                    if counter <= len(game.player_board.champions):
                                        game_display.blit(sprite, (list_pos_rect[counter].x, 450))
                                        counter += 1
        pygame.display.update()
        clock.tick(15)
    game_menu()


def draw_sprite(champions_in_battle, champions_sprites, sprites, X, Y, Z):
    for champion in champions_in_battle:
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load('%s%s' % (path, champion.img))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.topleft = (X, Y)

        champions_sprites.add(sprite)
        sprites.append(sprite)
        X += Z
        Y += Z


def draw_sprite_back(champions_in_battle, champions_sprites, sprites, X, Y, Z):
    for champion in champions_in_battle:
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load('%s%s' % (path, champion.img_dos))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.topleft = (X, Y)

        champions_sprites.add(sprite)
        sprites.append(sprite)
        X += Z
        Y += Z


def battle(turn, game):
    # type: (int, Game) -> None
    sprites = []
    ia_champions_sprites = pygame.sprite.Group()
    X, Y, Z = 900, 50, 40
    player_X, player_Y, player_Z = 600, 150, 40
    ia = IAChampions(game.available_champions)

    ia_champions = ia.champions.get(turn, [])
    player_champions = game.player_champion_battle

    fight = Combat(ia_champions, player_champions)
    fight_pair = fight.set_battle()
    print('fight_pair : %s' % fight_pair)
    draw_sprite(ia_champions, ia_champions_sprites, sprites, X, Y, Z)
    draw_sprite_back(player_champions, ia_champions_sprites, sprites, player_X, player_Y,
                     player_Z)
    game_continue = True

    while game_continue:
        pygame.display.flip()
        fight.battle()
        show_health(ia_champions)
        show_health_player(player_champions)
        ia_dead_champion = game.check_champ_hp(ia_champions)
        player_dead_champion = game.check_champ_hp(player_champions)
        if ia_dead_champion == 3:
            pygame.draw.rect(game_display, Colors.BEIGE, (500, 50, 700, 300))
            remove_sprites(ia_champions_sprites)
            game.clear_champ_battle()
            fight.reset_health(player_champions)
            game_continue = False
        elif player_dead_champion == 3:
            time.sleep(2)
            pygame.draw.rect(game_display, Colors.BEIGE, (500, 50, 700, 300))
            remove_sprites(ia_champions_sprites)
            game.lost_life(ia_champions)
            game.clear_champ_battle()
            fight.reset_health(player_champions)
            game_continue = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        ia_champions_sprites.draw(game_display)
        ia_champions_sprites.update()
        time.sleep(2)


def show_health(battle_champions):
    rect_champion_1 = pygame.draw.rect(game_display, Colors.BEIGE, (970, 70, 20, 30))
    rect_champion_2 = pygame.draw.rect(game_display, Colors.BEIGE, (1010, 110, 20, 30))
    rect_champion_3 = pygame.draw.rect(game_display, Colors.BEIGE, (1050, 150, 20, 30))

    if len(battle_champions) > 0:
        champ_1_health = battle_champions[0].health if battle_champions[0].health >= 0 else 0
        create_button("%s" % champ_1_health, rect_champion_1, game_display)
        if len(battle_champions) > 1:
            champ_2_health = battle_champions[1].health if battle_champions[1].health >= 0 else 0
            create_button("%s" % champ_2_health, rect_champion_2, game_display)
            if len(battle_champions) > 2:
                champ_3_health = battle_champions[2].health if battle_champions[2].health >= 0 else 0
                create_button("%s" % champ_3_health, rect_champion_3, game_display)


def show_health_player(battle_champions):
    rect_champion_1 = pygame.draw.rect(game_display, Colors.BEIGE, (580, 180, 20, 30))
    rect_champion_2 = pygame.draw.rect(game_display, Colors.BEIGE, (620, 220, 20, 30))
    rect_champion_3 = pygame.draw.rect(game_display, Colors.BEIGE, (660, 260, 20, 30))

    if len(battle_champions) > 0:
        champ_1_health = battle_champions[0].health if battle_champions[0].health >= 0 else 0
        create_button("%s" % champ_1_health, rect_champion_1, game_display)
        if len(battle_champions) > 1:
            champ_2_health = battle_champions[1].health if battle_champions[1].health >= 0 else 0
            create_button("%s" % champ_2_health, rect_champion_2, game_display)
            if len(battle_champions) > 2:
                champ_3_health = battle_champions[2].health if battle_champions[2].health >= 0 else 0
                create_button("%s" % champ_3_health, rect_champion_3, game_display)


def remove_sprites(ia_champions_sprites):
    ia_champions_sprites.remove(sprite for sprite in ia_champions_sprites)
    ia_champions_sprites.draw(game_display)
    ia_champions_sprites.update()


def create_stats_area(champion_stats):
    stats = []
    print('champion_stats : %s'%champion_stats)
    health = "Points de vie : %s" % champion_stats.get("health", "")
    price = "Prix : %s" % champion_stats.get("price", "")
    rarity = "Rareté : %s" % champion_stats.get("rarity", "")
    attack = "Attaque : %s" % champion_stats.get('attack', '')
    level = "Niveau : %s" % champion_stats.get("level", "")
    description = "Description : %s" % champion_stats.get("description", "")
    nb = "Nombre en jeu : %s" % champion_stats.get('number_on_game', '')

    stats.append(health)
    stats.append(price)
    stats.append(rarity)
    stats.append(level)
    stats.append(description)
    stats.append(attack)
    stats.append(nb)
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
        rect_champ = pygame.draw.rect(game_display, Colors.BEIGE,
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
                sys.exit()
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
                sys.exit()
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
