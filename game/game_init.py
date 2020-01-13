import pygame
import pygame.font
import sys
import time
import os
from pygame.locals import *
from database.db_manip import Database

db = Database()

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Grobold", 20)
#
# fps = 60
display_width = 900
display_height = 500
bg = [255, 255, 255]
rect = pygame.Rect(10, 20, 30, 30)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (200, 200, 0)
green = (34, 177, 76)


#
# def things_dodged(count):
#     font = pygame.font.SysFont(None, 25)
#     text = font.render("Dodged: " + str(count), True, black)
#     gameDisplay.blit(text, (0, 0))
#
#
# def things(thingx, thingy, thingw, thingh, color):
#     pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
#
#
def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


#
# def message_display(text):
#     largeText = pygame.font.Font('freesansbold.ttf', 115)
#     TextSurf, TextRect = text_objects(text, largeText)
#     TextRect.center = ((display_width / 2), (display_height / 2))
#     gameDisplay.blit(TextSurf, TextRect)
#
#     pygame.display.update()
#
#     time.sleep(2)
#

def game_intro():
    intro = True

    game_display = pygame.display.set_mode((display_width, display_height), RESIZABLE)
    pygame.display.set_caption('AUTO_CHESS')
    clock = pygame.time.Clock()

    button_play = pygame.Rect(150, 400, 100, 50)

    pygame.display.flip()

    while intro:
        if pygame.time.get_ticks() > 2000:
            intro = False
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                print("wsh")
                pygame.quit()
                quit()


        game_display.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        text_surf, text_rect = text_objects("AUTO_CHESS", large_text)
        text_rect.center = ((display_width / 2), (display_height / 2))
        game_display.blit(text_surf, text_rect)
        pygame.display.update()
        clock.tick(15)


def game_menu():
    menu = True
    game_display = pygame.display.set_mode((display_width, display_height), RESIZABLE)
    pygame.display.set_caption('AUTO_CHESS')
    clock = pygame.time.Clock()

    pygame.display.flip()

    while menu:
        game_display.fill(white)

        rect1 = pygame.draw.rect(game_display, red, ((display_width / 5), (display_height / 1.8), 100, 50))
        new_game_text = font.render("New Game", False, (0, 0, 0))
        new_game_rect = new_game_text.get_rect(center=rect1.center)
        button = game_display.blit(new_game_text, new_game_rect)

        large_text = pygame.font.Font('freesansbold.ttf', 115)
        text_surf, text_rect = text_objects("AUTO_CHESS", large_text)
        text_rect.center = ((display_width / 2), (display_height / 4))
        game_display.blit(text_surf, text_rect)
        pygame.display.update()
        clock.tick(15)

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                print('Le click est appuyé')
                if button.collidepoint(pos):
                    menu = False
                    print('Le click est dans le button')

    in_game()


def in_game():
    menu = True
    game_display = pygame.display.set_mode((display_width, display_height), RESIZABLE)
    clock = pygame.time.Clock()

    pygame.display.flip()

    while menu:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(white)

        pygame.display.update()
        clock.tick(15)


game_intro()
game_menu()
