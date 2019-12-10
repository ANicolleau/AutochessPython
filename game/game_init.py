import pygame
import pygame.font
import sys
import time
import os
from pygame.locals import *
from database.db_manip import Database

pygame.init()

fps = 60
display_width = 900
display_height = 500
bg = [255, 255, 255]

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (200, 200, 0)
green = (34, 177, 76)

gameDisplay = pygame.display.set_mode((display_width, display_height), RESIZABLE)
pygame.display.set_caption('AUTO_CHESS')
clock = pygame.time.Clock()

button_play = pygame.Rect(150, 400, 100, 50)

pygame.display.flip()


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 115)
    text_surface, text_rect = text_objects(text, large_text)
    text_rect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(text_surface, text_rect)

    pygame.display.update()

    time.sleep(2)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                intro = False

        gameDisplay.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        text_surf, text_rect = text_objects("AUTO_CHESS", large_text)
        text_rect.center = (int(display_width / 2), int(display_height / 2))
        gameDisplay.blit(text_surf, text_rect)
        pygame.display.update()
        clock.tick(15)


def game_start_menu():
    intro = True
    character = pygame.image.load('%s/images/perso.png' % os.path.dirname(__file__)).convert_alpha()
    character = pygame.transform.scale(character, (50, 50))
    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # La position de l'image ressorti est enfaite la position de l'image.
                print('Image pos == %s' % character.get_rect())
                print('Mouse pos == %s' % event)
                if character.get_rect().collidepoint(x, y):
                    print('clicked on image')

        gameDisplay.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        text_surf, text_rect = text_objects("AUTO_CHESS", large_text)
        text_rect.center = (int(display_width / 2), int(display_height / 4))
        gameDisplay.blit(text_surf, text_rect)
        gameDisplay.blit(character, (350, 300))
        pygame.display.update()
        clock.tick(15)
        pygame.display.flip()


game_intro()
game_start_menu()
