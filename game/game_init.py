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
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        text_surf, text_rect = text_objects("AUTO_CHESS", large_text)
        text_rect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(text_surf, text_rect)
        pygame.display.update()
        clock.tick(15)

game_intro()
