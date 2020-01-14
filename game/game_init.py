import pygame, pygame.font, sys, time, os
from pygame.locals import *
from database.object import *
from database.db_manip import get_all_champions

# from database.object.database import Database


pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Grobold", 20)
display_width = 900
display_height = 500
bg = [255, 255, 255]

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (200, 200, 0)
green = (34, 177, 76)

NEW_GAME = "new game"
CONTINUE = "continue"
OPTIONS = "options"

def terminate():
    pygame.quit()
    sys.exit()

def text_objects(text, style, object_color):
    text_surface = style.render(text, True, object_color)
    return text_surface, text_surface.get_rect()


def game_intro():
    intro = True

    game_display = pygame.display.set_mode((display_width, display_height), RESIZABLE)
    pygame.display.set_caption('Python Auto Battler')
    clock = pygame.time.Clock()

    button_play = pygame.Rect(150, 400, 100, 50)

    pygame.display.flip()

    while intro:
        if pygame.time.get_ticks() > 2000:
            intro = False
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                terminate()

        game_display.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 40)
        text_surf, text_rect = text_objects("Python Auto Battler", large_text, black)
        text_rect.center = ((display_width / 2), (display_height / 2))
        game_display.blit(text_surf, text_rect)
        pygame.display.update()
        clock.tick(40)


def create_button(text, rectangle, screen):
    new_game_text = font.render(text, False, (0, 0, 0))
    new_game_rect = new_game_text.get_rect(center=rectangle.center)
    return screen.blit(new_game_text, new_game_rect)


def game_menu():
    choose_menu = ""
    menu = True
    game_display = pygame.display.set_mode((display_width, display_height), RESIZABLE)
    pygame.display.set_caption('Python Auto Battler')
    clock = pygame.time.Clock()

    pygame.display.flip()

    while menu:
        game_display.fill(white)

        rect_new_game = pygame.draw.rect(game_display, red, ((display_width / 5), (display_height / 1.8), 100, 50))
        rect_start_game = pygame.draw.rect(game_display, red, ((display_width / 2.5), (display_height / 1.8), 100, 50))
        rect_options = pygame.draw.rect(game_display, red, ((display_width / 1.65), (display_height / 1.8), 100, 50))

        button_start_new_game = create_button("New Game", rect_new_game, game_display)
        button_start_game = create_button("Continue", rect_start_game, game_display)
        button_options = create_button("Personnages", rect_options, game_display)

        large_text = pygame.font.Font('freesansbold.ttf', 40)
        text_surf, text_rect = text_objects("Python Auto Battler", large_text, black)
        text_rect.center = ((display_width / 2), (display_height / 4))
        game_display.blit(text_surf, text_rect)
        pygame.display.update()
        clock.tick(15)

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if rect_new_game.collidepoint(pos):
                    choose_menu = NEW_GAME
                    menu = False
                elif rect_start_game.collidepoint(pos):
                    choose_menu = CONTINUE
                    menu = False
                elif rect_options.collidepoint(pos):
                    choose_menu = OPTIONS
                    menu = False
    if choose_menu == NEW_GAME:
        in_game()
    elif choose_menu == CONTINUE:
        in_game()  # Devrait reprendre la partie en cours.
    elif choose_menu == OPTIONS:
        show_characters()


def in_game():
    game = True
    while game:
        game_display = pygame.display.set_mode((display_width, display_height), RESIZABLE)
        clock = pygame.time.Clock()
        rect_return = pygame.draw.rect(game_display, red, ((display_width / 1.2), (display_height / 1.2), 100, 50))
        create_button("Retour", rect_return, game_display)

        pygame.display.flip()

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if rect_return.collidepoint(pos):
                    game = False

        pygame.display.update()
        clock.tick(15)
    game_menu()


def show_characters():
    game = True
    all_champions = get_all_champions()

    game_display = pygame.display.set_mode((display_width, display_height), RESIZABLE)

    rect_champ_width = display_width
    rect_champ_height = display_height
    dict_champ_length = len(all_champions)
    button_list = []
    temp_rect_champ_width = rect_champ_width
    temp_rect_champ_height = rect_champ_height
    for champion in all_champions:
        rect_champ = pygame.draw.rect(game_display, red,
                                      (temp_rect_champ_width / 1.2, temp_rect_champ_height / 1.2, 100, 50))
        button_list.append(rect_champ)
        create_button(champion, rect_champ, game_display)
        temp_rect_champ_width -= 150
        if temp_rect_champ_width <= 100:
            temp_rect_champ_width = rect_champ_width
            temp_rect_champ_height -= 150
        print(button_list)
        # print(champion)
        print(rect_champ_width)

    clock = pygame.time.Clock()
    rect_return = pygame.draw.rect(game_display, red, ((display_width / 1.2), (display_height / 1.2), 100, 50))
    print(rect_return)
    create_button("Retour", rect_return, game_display)

    # large_text = pygame.font.Font('freesansbold.ttf', 80)
    # text_surf, text_rect = text_objects("Personnages", large_text, white)
    # text_rect.center = ((display_width / 2), (display_height / 4))

    # game_display.blit(text_surf, text_rect)
    pygame.display.update()
    clock.tick(40)
    while game:

        pygame.display.flip()

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if rect_return.collidepoint(pos):
                    game = False
                for rect in button_list:
                    if rect.collidepoint(pos):
                        game = False

    game_menu()


game_intro()
game_menu()
