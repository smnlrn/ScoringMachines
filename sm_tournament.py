# Tournament Scoring Machine
# By Simon Laurin simonlaurin@yahoo.com
# http://github.com/smnlrn
# Released under a tbd license

import random
import pygame
import sys
from pygame.locals import *

FPS = 30  # frames per second, the general speed of the program
WINDOWWIDTH = 800  # size of window's width in pixels
WINDOWHEIGHT = 480  # size of windows' height in pixels
#  Line 707 for full screen on Pi

JVT = .9  # Joystick Value Threshold
# the values for the following constants are not used themselves
START = "start"
SELECT = "select"
UP = "up"
RIGHT = "right"
DOWN = "down"
LEFT = "Left"
LEFTRIGHT = "lr"
UPDOWN = "ud"
STICK = "joystick"

#       R    G    B
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255, 5)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

# Player Info Page Variables
letterGap = 50
letterMarginLeft = 500
letterMarginTop = 180
squareSide = 40
squareAlignement = 5

switch = 0
letters = [["A", "B", "C", "D", "E", "F"], ["G", "H", "I", "J", "K", "L"], ["M", "N", "O", "P", "Q", "R"],
           ["S", "T", "U", "V", "W", "X"], ["Y", "Z", "-", ".", "<", ">"], [" ", "&", "!", "?", "BYE", ""]]
Players = ["        "] * 8
xmax = len(letters[0]) - 1

ymax = len(letters) - 1
rectposxmin = letterMarginLeft - squareAlignement
rectposxmax = letterMarginLeft + letterGap * xmax - squareAlignement
rectposymin = letterMarginTop - squareAlignement
rectposymax = letterMarginTop + letterGap * ymax - squareAlignement
rectposxstep = letterGap
rectposystep = letterGap

# Player Name, Score box center coordinates (add approx. 3px to vertical center for uppercase letters)
G1P1CXY = (95, 23)
G1P2CXY = (290, 23)
G1S1CXY = (173, 23)
G1S2CXY = (217, 23)

G2P1CXY = (510, 23)
G2P2CXY = (705, 23)
G2S1CXY = (588, 23)
G2S2CXY = (632, 23)

G3P1CXY = (95, 463)
G3P2CXY = (290, 463)
G3S1CXY = (173, 463)
G3S2CXY = (217, 463)

G4P1CXY = (510, 463)
G4P2CXY = (705, 463)
G4S1CXY = (588, 463)
G4S2CXY = (632, 463)

G5P1CXY = (192, 88)
G5P2CXY = (608, 88)
G5S1CXY = (270, 88)
G5S2CXY = (535, 88)

G6P1CXY = (192, 397)
G6P2CXY = (608, 397)
G6S1CXY = (270, 397)
G6S2CXY = (535, 397)

G7P1CXY = (400, 123)
G7P2CXY = (400, 363)
G7S1CXY = (478, 123)
G7S2CXY = (478, 363)

MGP1CXY = (192, 190)
MGP2CXY = (607, 190)
MGS1CXY = (300, 275)
MGS2CXY = (505, 275)
MGSET1CXY = (340, 235)
MGSET2CXY = (465, 235)

# ARGONNE POOL LEAGUE HANDICAP SYSTEM CONSTANTS AND CHARTS/FUNCTIONS
PLAYER_STATUS_EST = "EST."
PLAYER_STATUS_NEW = "NEW"


def match_games(h1, h2):
    maxh = max(h1, h2)
    diffh = abs(h1 - h2)
    if maxh < 40:  # CHART-4
        if diffh < 20:
            m1, m2 = 2, 2
        else:
            m1, m2 = 2, 1
    elif maxh < 50:  # CHART-6
        if diffh < 11:
            m1, m2 = 3, 3
        elif diffh < 27:
            m1, m2 = 3, 2
        elif diffh < 54:
            m1, m2 = 4, 2
        else:
            m1, m2 = 4, 1
    elif maxh < 70:  # CHART-8
        if diffh < 7:
            m1, m2 = 4, 4
        elif diffh < 19:
            m1, m2 = 4, 3
        elif diffh < 30:
            m1, m2 = 5, 3
        elif diffh < 40:
            m1, m2 = 4, 2
        elif diffh < 49:
            m1, m2 = 5, 2
        elif diffh < 69:
            m1, m2 = 6, 2
        else:
            m1, m2 = 5, 1
    elif maxh < 90:  # CHART-10
        if diffh < 6:
            m1, m2 = 5, 5
        elif diffh < 15:
            m1, m2 = 5, 4
        elif diffh < 22:
            m1, m2 = 6, 4
        elif diffh < 29:
            m1, m2 = 5, 3
        elif diffh < 37:
            m1, m2 = 6, 3
        elif diffh < 47:
            m1, m2 = 7, 3
        elif diffh < 57:
            m1, m2 = 6, 2
        elif diffh < 63:
            m1, m2 = 7, 2
        elif diffh < 83:
            m1, m2 = 8, 2
        elif diffh < 102:
            m1, m2 = 7, 1
        else:
            m1, m2 = 8, 1
    else:  # CHART-12
        if diffh < 5:
            m1, m2 = 6, 6
        elif diffh < 12:
            m1, m2 = 6, 5
        elif diffh < 18:
            m1, m2 = 7, 5
        elif diffh < 23:
            m1, m2 = 6, 4
        elif diffh < 29:
            m1, m2 = 7, 4
        elif diffh < 36:
            m1, m2 = 8, 4
        elif diffh < 43:
            m1, m2 = 7, 3
        elif diffh < 49:
            m1, m2 = 8, 3
        elif diffh < 59:
            m1, m2 = 9, 3
        elif diffh < 69:
            m1, m2 = 8, 2
        elif diffh < 75:
            m1, m2 = 9, 2
        elif diffh < 94:
            m1, m2 = 10, 2
        elif diffh < 113:
            m1, m2 = 9, 1
        else:
            m1, m2 = 10, 1

    if h1 == maxh:
        g1, g2 = m1, m2
    else:
        g1, g2 = m2, m1

    print("Handicaps:", h1, h2, "for Match Games:", g1, ":", g2)
    return g1, g2


def change_skill_rating(games, status, win):
    if status == PLAYER_STATUS_EST:
        if games < 3:
            delta = 3
        elif games < 14:
            delta = 2
        else:
            delta = 1
    else:
        if games < 2:
            delta = 6
        if games < 3:
            delta = 4
        if games < 6:
            delta = 3
        elif games < 17:
            delta = 2
        else:
            delta = 1
    if win:
        return delta
    else:
        return -delta


# FUNCTIONS
# def text_objects(text, font):
#     textsurface = font.render(text, True, BLACK)
#     return textsurface, textsurface.get_rect()


def check_button(event, test):
    if event.type == KEYUP:
        if test == START and event.key == K_SPACE:
            return True
        if test == SELECT and event.key == K_RETURN:
            return True
        if test == UP and event.key == K_UP:
            return True
        if test == RIGHT and event.key == K_RIGHT:
            return True
        if test == DOWN and event.key == K_DOWN:
            return True
        if test == LEFT and event.key == K_LEFT:
            return True
        if test == LEFTRIGHT and (event.key == K_LEFT or event.key == K_RIGHT):
            return True
        if test == UPDOWN and (event.key == K_UP or event.key == K_DOWN):
            return True
        if test == STICK and (event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT):
            return True
    if event.type == pygame.JOYBUTTONUP:  # USING A GEEEKPI JOYSTICK
        if test == START and event.button == 9:  # ST
            return True
        if test == SELECT and event.button == 8:  # SE
            return True
        if test == UP and event.button == 0:  # K1
            return True
        if test == RIGHT and event.button == 1:  # K2
            return True
        if test == DOWN and event.button == 2:  # K3
            return True
        if test == LEFT and event.button == 3:  # K4
            return True
        if test == LEFTRIGHT and (event.button == 1 or event.button == 3):  # K2 or K4
            return True
        if test == UPDOWN and (event.button == 0 or event.button == 2):  # K1 or K3
            return True
        if test == STICK and (event.button == 0 or event.button == 1 or event.button == 2 or event.button == 3):  #K1-3
            return True
    return False


def text_blit(text, font, clr, center):
    textrender = font.render(text, True, clr)
    return textrender, textrender.get_rect(center=center)


def select_section(event, index):
    # if event.type == pygame.KEYUP:
    #     if event.key == pygame.K_RIGHT:
    #         index += 1
    #         if index > 3:
    #             index = 1
    #     if event.key == pygame.K_LEFT:
    #         index -= 1
    #         if index < 1:
    #             index = 3
    # # axis tested to be 1
    # if event.type == pygame.JOYBUTTONUP:
    #     if event.button == 1:  # RIGHT / K2
    #         index += 1
    #         if index > 3:
    #             index = 1
    #     if event.axis == 0 and event.value < -JVT:  # LEFT
    #         index -= 1
    #         if index < 1:
    #             index = 3
    if check_button(event, RIGHT):
        index += 1
        if index > 3:
            index = 1
    if check_button(event, LEFT):
        index -= 1
        if index < 1:
            index = 3
    return index


def select_player(event, index):
    # if event.type == pygame.KEYUP:
    #     if event.key == pygame.K_DOWN:
    #         index += 1
    #         if index > 7:
    #             index = 0
    #     if event.key == pygame.K_UP:
    #         index -= 1
    #         if index < 0:
    #             index = 7
    # axis tested to be 1
    # if event.type == pygame.JOYAXISMOTION:
    #     if event.axis == 1 and event.value > JVT:
    #         index += 1
    #         if index > 7:
    #             index = 0
    #     if event.axis == 1 and event.value < -JVT:
    #         index -= 1
    #         if index < 0:
    #             index = 7
    if check_button(event, DOWN):
        index += 1
        if index > 7:
            index = 0
    if check_button(event, UP):
        index -= 1
        if index < 0:
            index = 7
    return index


def select_mode(event, index):
    # if event.type == pygame.KEYUP:
    #     if event.key == pygame.K_RIGHT:
    #         index += 1
    #         if index > 2:
    #             index = 0
    #     if event.key == pygame.K_LEFT:
    #         index -= 1
    #         if index < 0:
    #             index = 2
    # # axis tested to be 1
    # if event.type == pygame.JOYAXISMOTION:
    #     if event.axis == 0 and event.value > JVT:
    #         index += 1
    #         if index > 2:
    #             index = 0
    #     if event.axis == 0 and event.value < -JVT:
    #         index -= 1
    #         if index < 0:
    #             index = 2
    # return index
    if check_button(event, RIGHT):
        index += 1
        if index > 2:
            index = 0
    if check_button(event, LEFT):
        index -= 1
        if index < 0:
            index = 2
    return index


def letterpicker(event, rectposx, rectposy, x, y):
    if check_button(event, RIGHT):
        rectposx += rectposxstep
        x += 1
        if rectposx > rectposxmax:
            rectposx = rectposxmin
            x = 0
    if check_button(event, LEFT):
        rectposx -= rectposxstep
        x -= 1
        if rectposx < rectposxmin:
            rectposx = rectposxmax
            x = xmax
    if check_button(event, DOWN):
        rectposy += rectposystep
        y += 1
        if rectposy > rectposymax:
            rectposy = rectposymin
            y = 0
    if check_button(event, UP):
        rectposy -= rectposystep
        y -= 1
        if rectposy < rectposymin:
            rectposy = rectposymax
            y = ymax
    return rectposx, rectposy, x, y


def init_players():
    fontplayer = pygame.font.Font("OCRAStd.otf", 40)
    fontmode = pygame.font.Font("OCRAStd.otf", 10)
    fontinstructions = pygame.font.Font("OCRAStd.otf", 12)
    section_player = 1
    section_handicap = 2
    section_start = 3
    mode_toggle = 1  # 1:Tgggle, 2:Select, 3:Set Value
    mode_sets = True
    seed_toggle = True  # True for set seed
    start_confirmation = False
    setlist = [3] * 8 + [5] * 4 + [7] * 2
    rectposx = rectposxmin
    rectposy = rectposymin
    player_index = 0
    player_x = 10
    player_y = 50
    player_vgap = 50
    player_square = 30
    name_x = 40
    name_y = 45
    name_gap = 29
    name_square = 39
    mode_index = 0
    mode_x = 330
    mode_y = 50
    mode_vgap = 50
    mode_hgap = 42
    mode_square = 35
    x = 0
    # xmax = len(letters[0]) - 1
    y = 0
    # pygame.draw.rect(DISPLAYSURF, ORANGE, [rectposx, rectposy, squareSide, squareSide], 2)
    player_status = ["EST."] * 4 + ["NEW"] * 4 + [""] * 6
    player_games = [17] * 8 + [0] * 6
    player_handicap = [30] * 8 + [0] * 6
    initials = [" "] * 8
    ii = 0
    background_image_player = pygame.image.load("TournamentScorerBGPlayer.png").convert()
    init = True
    section_index = section_player
    while init:
        DISPLAYSURF.blit(background_image_player, (0, 0))
        if section_index == section_player:
            pygame.draw.rect(DISPLAYSURF, RED, [player_x, player_y + player_vgap * player_index,
                                                player_square, player_square], 2)
            pygame.draw.rect(DISPLAYSURF, RED, [80, 5, 165, 35], 2)
            DISPLAYSURF.blit(*text_blit("Select to enter name; L/R to change section",
                                        fontinstructions, WHITE, (205, 460)))
        elif section_index == section_handicap:
            pygame.draw.rect(DISPLAYSURF, RED, [304, 8, 175, 20], 2)
            if mode_toggle == 1:
                pygame.draw.rect(DISPLAYSURF, RED, [304, 30, 175, 17], 2)
            elif mode_toggle == 2:
                pygame.draw.rect(DISPLAYSURF, RED, [mode_x + mode_hgap * mode_index, mode_y + mode_vgap * player_index,
                                                    mode_square, mode_square], 2)
            else:
                pygame.draw.rect(DISPLAYSURF, RED, [mode_x + mode_hgap * mode_index, mode_y + mode_vgap * player_index,
                                                    mode_square, mode_square], 2)
                pygame.draw.rect(DISPLAYSURF, RED, [mode_x + mode_hgap * mode_index - 2,
                                                    mode_y + mode_vgap * player_index - 2,
                                                    mode_square + 5, mode_square + 5], 1)
            DISPLAYSURF.blit(*text_blit("Start to toggle mode/enter; Select to activate cell",
                                        fontinstructions, WHITE, (240, 460)))
        elif section_index == section_start:
            pygame.draw.rect(DISPLAYSURF, RED, [580, 6, 120, 40], 2)
            DISPLAYSURF.blit(*text_blit("Start to Start Tournament",
                                        fontinstructions, WHITE, (300, 460)))
            if start_confirmation:
                pygame.draw.rect(DISPLAYSURF, GRAY, [200, 220, 400, 40])
                pygame.draw.rect(DISPLAYSURF, RED, [200, 220, 400, 40], 2)
                DISPLAYSURF.blit(*text_blit("Start to Start Tournament; Select to cancel",
                                            fontinstructions, WHITE, (400, 240)))
        else:
            pygame.draw.rect(DISPLAYSURF, RED, [rectposx, rectposy, 50, 50], 2)
            pygame.draw.rect(DISPLAYSURF, RED, [name_x + ii*name_gap, name_y + player_vgap * player_index,
                                                name_square, name_square], 2)
            DISPLAYSURF.blit(*text_blit("Select to enter letter; Start to return",
                                        fontinstructions, WHITE, (200, 460)))
        if seed_toggle:
            pygame.draw.rect(DISPLAYSURF, RED, [565, 70, 170, 25], 2)
        else:
            pygame.draw.rect(DISPLAYSURF, RED, [565, 100, 170, 25], 2)

        # PLAYER NAMES
        DISPLAYSURF.blit(fontplayer.render(Players[0], True, ORANGE), (45, 50))
        DISPLAYSURF.blit(fontplayer.render(Players[1], True, ORANGE), (45, 100))
        DISPLAYSURF.blit(fontplayer.render(Players[2], True, ORANGE), (45, 150))
        DISPLAYSURF.blit(fontplayer.render(Players[3], True, ORANGE), (45, 200))
        DISPLAYSURF.blit(fontplayer.render(Players[4], True, ORANGE), (45, 250))
        DISPLAYSURF.blit(fontplayer.render(Players[5], True, ORANGE), (45, 300))
        DISPLAYSURF.blit(fontplayer.render(Players[6], True, ORANGE), (45, 350))
        DISPLAYSURF.blit(fontplayer.render(Players[7], True, ORANGE), (45, 400))
        if mode_sets:
            DISPLAYSURF.blit(*text_blit("Quarter-Semi-Final", fontinstructions, WHITE, (390, 40)))
            DISPLAYSURF.blit(*text_blit(str(setlist[0]), fontplayer, WHITE, (350, 70)))
            DISPLAYSURF.blit(*text_blit(str(setlist[0]), fontplayer, GRAY, (350, 120)))
            DISPLAYSURF.blit(*text_blit(str(setlist[0]), fontplayer, GRAY, (350, 170)))
            DISPLAYSURF.blit(*text_blit(str(setlist[0]), fontplayer, GRAY, (350, 220)))
            DISPLAYSURF.blit(*text_blit(str(setlist[0]), fontplayer, GRAY, (350, 270)))
            DISPLAYSURF.blit(*text_blit(str(setlist[0]), fontplayer, GRAY, (350, 320)))
            DISPLAYSURF.blit(*text_blit(str(setlist[0]), fontplayer, GRAY, (350, 370)))
            DISPLAYSURF.blit(*text_blit(str(setlist[0]), fontplayer, GRAY, (350, 420)))
            DISPLAYSURF.blit(*text_blit(str(setlist[8]), fontplayer, WHITE, (390, 70)))
            DISPLAYSURF.blit(*text_blit(str(setlist[8]), fontplayer, GRAY, (390, 120)))
            DISPLAYSURF.blit(*text_blit(str(setlist[8]), fontplayer, GRAY, (390, 170)))
            DISPLAYSURF.blit(*text_blit(str(setlist[8]), fontplayer, GRAY, (390, 220)))
            DISPLAYSURF.blit(*text_blit(str(setlist[8]), fontplayer, GRAY, (390, 270)))
            DISPLAYSURF.blit(*text_blit(str(setlist[8]), fontplayer, GRAY, (390, 320)))
            DISPLAYSURF.blit(*text_blit(str(setlist[8]), fontplayer, GRAY, (390, 370)))
            DISPLAYSURF.blit(*text_blit(str(setlist[8]), fontplayer, GRAY, (390, 420)))
            DISPLAYSURF.blit(*text_blit(str(setlist[12]), fontplayer, WHITE, (430, 70)))
            DISPLAYSURF.blit(*text_blit(str(setlist[12]), fontplayer, GRAY, (430, 120)))
            DISPLAYSURF.blit(*text_blit(str(setlist[12]), fontplayer, GRAY, (430, 170)))
            DISPLAYSURF.blit(*text_blit(str(setlist[12]), fontplayer, GRAY, (430, 220)))
            DISPLAYSURF.blit(*text_blit(str(setlist[12]), fontplayer, GRAY, (430, 270)))
            DISPLAYSURF.blit(*text_blit(str(setlist[12]), fontplayer, GRAY, (430, 320)))
            DISPLAYSURF.blit(*text_blit(str(setlist[12]), fontplayer, GRAY, (430, 370)))
            DISPLAYSURF.blit(*text_blit(str(setlist[12]), fontplayer, GRAY, (430, 420)))
        else:
            DISPLAYSURF.blit(*text_blit("Status-Games-Hand.", fontinstructions, WHITE, (390, 40)))
            DISPLAYSURF.blit(*text_blit(player_status[0], fontmode, ORANGE, (350, 70)))
            DISPLAYSURF.blit(*text_blit(player_status[1], fontmode, ORANGE, (350, 120)))
            DISPLAYSURF.blit(*text_blit(player_status[2], fontmode, ORANGE, (350, 170)))
            DISPLAYSURF.blit(*text_blit(player_status[3], fontmode, ORANGE, (350, 220)))
            DISPLAYSURF.blit(*text_blit(player_status[4], fontmode, ORANGE, (350, 270)))
            DISPLAYSURF.blit(*text_blit(player_status[5], fontmode, ORANGE, (350, 320)))
            DISPLAYSURF.blit(*text_blit(player_status[6], fontmode, ORANGE, (350, 370)))
            DISPLAYSURF.blit(*text_blit(player_status[7], fontmode, ORANGE, (350, 420)))
            DISPLAYSURF.blit(*text_blit(str(player_games[0]), fontmode, ORANGE, (390, 70)))
            DISPLAYSURF.blit(*text_blit(str(player_games[1]), fontmode, ORANGE, (390, 120)))
            DISPLAYSURF.blit(*text_blit(str(player_games[2]), fontmode, ORANGE, (390, 170)))
            DISPLAYSURF.blit(*text_blit(str(player_games[3]), fontmode, ORANGE, (390, 220)))
            DISPLAYSURF.blit(*text_blit(str(player_games[4]), fontmode, ORANGE, (390, 270)))
            DISPLAYSURF.blit(*text_blit(str(player_games[5]), fontmode, ORANGE, (390, 320)))
            DISPLAYSURF.blit(*text_blit(str(player_games[6]), fontmode, ORANGE, (390, 370)))
            DISPLAYSURF.blit(*text_blit(str(player_games[7]), fontmode, ORANGE, (390, 420)))
            DISPLAYSURF.blit(*text_blit(str(player_handicap[0]), fontmode, ORANGE, (430, 70)))
            DISPLAYSURF.blit(*text_blit(str(player_handicap[1]), fontmode, ORANGE, (430, 120)))
            DISPLAYSURF.blit(*text_blit(str(player_handicap[2]), fontmode, ORANGE, (430, 170)))
            DISPLAYSURF.blit(*text_blit(str(player_handicap[3]), fontmode, ORANGE, (430, 220)))
            DISPLAYSURF.blit(*text_blit(str(player_handicap[4]), fontmode, ORANGE, (430, 270)))
            DISPLAYSURF.blit(*text_blit(str(player_handicap[5]), fontmode, ORANGE, (430, 320)))
            DISPLAYSURF.blit(*text_blit(str(player_handicap[6]), fontmode, ORANGE, (430, 370)))
            DISPLAYSURF.blit(*text_blit(str(player_handicap[7]), fontmode, ORANGE, (430, 420)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                init = False
            if section_index == section_player:
                if check_button(event, UPDOWN):
                    player_index = select_player(event, player_index)
                if check_button(event, LEFTRIGHT):
                    section_index = select_section(event, section_index)
                if check_button(event, SELECT):
                    section_index = 0
                    initials = list(Players[player_index])
                    ii = 0


            elif section_index == section_handicap:
                player_index = 0
                if mode_toggle == 1:
                    if check_button(event, START):
                        if mode_sets:
                            mode_sets = False
                        else:
                            mode_sets = True
                    if check_button(event, SELECT):
                        mode_toggle = 2
                    if check_button(event, LEFTRIGHT):
                        section_index = select_section(event, section_index)
                elif mode_toggle == 2:
                    if mode_sets:
                        if check_button(event, LEFT):
                            if mode_index == 0:
                                mode_index = 2
                            else:
                                mode_index -= 1
                        if check_button(event, RIGHT):
                            if mode_index == 2:
                                mode_index = 0
                            else:
                                mode_index += 1
                        if check_button(event, UP):
                            if mode_index == 0:
                                setlist[0] += 1
                                for e in range(1, 8):
                                    setlist[e] = setlist[0]
                            elif mode_index == 1:
                                setlist[8] += 1
                                for e in range(9, 12):
                                    setlist[e] = setlist[8]
                            else:
                                setlist[12] += 1
                                setlist[13] += 1
                        if check_button(event, DOWN):
                            if mode_index == 0:
                                setlist[0] -= 1
                                for e in range(1, 8):
                                    setlist[e] = setlist[0]
                            elif mode_index == 1:
                                setlist[8] -= 1
                                for e in range(9, 12):
                                    setlist[e] = setlist[8]
                            else:
                                setlist[12] -= 1
                                setlist[13] -= 1
                        if check_button(event, SELECT):
                            mode_toggle = 1
                    else:
                        if check_button(event, UPDOWN):
                            player_index = select_player(event, player_index)
                        if check_button(event, LEFTRIGHT):
                            mode_index = select_mode(event, mode_index)
                        if check_button(event, SELECT):
                            mode_toggle = 3
            elif section_index == section_start:  #
                if check_button(event, UPDOWN):
                    if seed_toggle:
                        seed_toggle = False
                    else:
                        seed_toggle = True
                if check_button(event, RIGHT):
                    section_index = section_player
                if check_button(event, LEFT):
                    section_index = section_handicap
                if check_button(event, START):
                    init = False
                    # TODO: confirmation box
            else:  # PICKING LETTERS
                if check_button(event, STICK):
                    rectposx, rectposy, x, y = letterpicker(event, rectposx, rectposy, x, y)
                if check_button(event, SELECT):
                    initials[ii] = letters[y][x]
                    Players[player_index] = "".join(initials)
                    ii += 1
                    if ii > 7:
                        ii = 0
                if check_button(event, START):
                    Players[player_index] = "".join(initials)
                    section_index = section_player
                    if player_index < 7:
                        player_index += 1
                    else:
                        player_index = 0
        pygame.display.update()

    plist = [str(Players[0]).strip(), str(Players[7]).strip(), str(Players[3]).strip(), str(Players[4]).strip(),
             str(Players[2]).strip(), str(Players[5]).strip(), str(Players[1]).strip(), str(Players[6]).strip()]
    if not seed_toggle:
        random.shuffle(plist)  # shuffle method
    wlist = [""] * 6
    plist.extend(wlist)
    # setlist = [3] * 8 + [5] * 4 + [7] * 2
    return plist, setlist


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    # DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # For screen on Raspberry Pi
    pygame.display.set_caption('Simple Elimination Tournament')

    player_list, sets_list = init_players()
    print(player_list)
    winner_list = [False] * 14
    # sysFont did not work on my MBP for some reason...
    # font must be present in the folder
    font_main_name = pygame.font.Font('OCRAStd.otf', 48)
    font_main_score = pygame.font.Font("OCRAStd.otf", 72)
    font_bracket = pygame.font.Font("OCRAStd.otf", 18)

    correction = False
    currentgame = 1
    scores = [0] * 14
    background_image = pygame.image.load("TournamentScorerBG.png").convert()

    while True:  # main game loop

        DISPLAYSURF.blit(background_image, (0, 0))

        # DISPLAY ALL TOURNAMENT ELEMENTS  (the * splits the returned list into arguments)
        # PLAYER NAMES - BRACKETS
        DISPLAYSURF.blit(*text_blit(player_list[0], font_bracket, WHITE, G1P1CXY))
        DISPLAYSURF.blit(*text_blit(player_list[1], font_bracket, WHITE, G1P2CXY))
        DISPLAYSURF.blit(*text_blit(player_list[2], font_bracket, WHITE, G2P1CXY))
        DISPLAYSURF.blit(*text_blit(player_list[3], font_bracket, WHITE, G2P2CXY))
        DISPLAYSURF.blit(*text_blit(player_list[4], font_bracket, WHITE, G3P1CXY))
        DISPLAYSURF.blit(*text_blit(player_list[5], font_bracket, WHITE, G3P2CXY))
        DISPLAYSURF.blit(*text_blit(player_list[6], font_bracket, WHITE, G4P1CXY))
        DISPLAYSURF.blit(*text_blit(player_list[7], font_bracket, WHITE, G4P2CXY))
        DISPLAYSURF.blit(*text_blit(player_list[8], font_bracket, WHITE, G5P1CXY))
        DISPLAYSURF.blit(*text_blit(player_list[9], font_bracket, WHITE, G5P2CXY))
        DISPLAYSURF.blit(*text_blit(player_list[10], font_bracket, WHITE, G6P1CXY))
        DISPLAYSURF.blit(*text_blit(player_list[11], font_bracket, WHITE, G6P2CXY))
        DISPLAYSURF.blit(*text_blit(player_list[12], font_bracket, WHITE, G7P1CXY))
        DISPLAYSURF.blit(*text_blit(player_list[13], font_bracket, WHITE, G7P2CXY))
        # PLAYER SCORE - BRACKETS
        DISPLAYSURF.blit(*text_blit(str(scores[0]), font_bracket, RED, G1S1CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[1]), font_bracket, RED, G1S2CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[2]), font_bracket, RED, G2S1CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[3]), font_bracket, RED, G2S2CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[4]), font_bracket, RED, G3S1CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[5]), font_bracket, RED, G3S2CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[6]), font_bracket, RED, G4S1CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[7]), font_bracket, RED, G4S2CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[8]), font_bracket, RED, G5S1CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[9]), font_bracket, RED, G5S2CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[10]), font_bracket, RED, G6S1CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[11]), font_bracket, RED, G6S2CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[12]), font_bracket, RED, G7S1CXY))
        DISPLAYSURF.blit(*text_blit(str(scores[13]), font_bracket, RED, G7S2CXY))
        # CURRENT GAME
        DISPLAYSURF.blit(*text_blit(player_list[currentgame*2-2], font_main_name, WHITE, MGP1CXY))
        DISPLAYSURF.blit(*text_blit(player_list[currentgame*2-1], font_main_name, WHITE, MGP2CXY))
        if correction:
            DISPLAYSURF.blit(*text_blit(str(scores[currentgame*2-2]), font_main_score, RED, MGS1CXY))
            DISPLAYSURF.blit(*text_blit(str(scores[currentgame*2-1]), font_main_score, RED, MGS2CXY))
        else:
            DISPLAYSURF.blit(*text_blit(str(scores[currentgame*2-2]), font_main_score, WHITE, MGS1CXY))
            DISPLAYSURF.blit(*text_blit(str(scores[currentgame*2-1]), font_main_score, WHITE, MGS2CXY))
        DISPLAYSURF.blit(*text_blit(str(sets_list[currentgame*2-2]), font_bracket, RED, MGSET1CXY))
        DISPLAYSURF.blit(*text_blit(str(sets_list[currentgame*2-1]), font_bracket, RED, MGSET2CXY))
        # GAME SELECTION RECTANGLE
        pygame.draw.rect(DISPLAYSURF, RED, (360, 135 + 24 * currentgame, 85, 24), 1)

        # TOURNAMENT LOGIC
        # Since all elements are refreshed at every tick, the tournament logic only updates variables
        #   currentgame : game number to be displayed in the main bloc
        #   player_list: for seeded players and winners
        #   scores: score list as they are entered
        for event in pygame.event.get():  # event handling loop
            print(event)
            print(check_button(event, START))
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE) or \
                    (event.type == pygame.JOYBUTTONDOWN and event.button == 9):  # START
                pygame.quit()
                sys.exit()

            if check_button(event, DOWN):
                if currentgame == 7:
                    currentgame = 1
                else:
                    currentgame += 1

            if check_button(event, UP):
                if currentgame == 1:
                    currentgame = 7
                else:
                    currentgame -= 1

            if check_button(event, SELECT):
                if correction:
                    correction = False
                else:
                    correction = True

            if check_button(event, LEFT) or check_button(event, RIGHT):
                if check_button(event, LEFT):
                    if correction:
                        scores[currentgame*2-2] -= 1
                        correction = False
                    else:
                        scores[currentgame * 2 - 2] += 1

                if check_button(event, RIGHT):
                    if correction:
                        scores[currentgame*2-1] -= 1
                        correction = False
                    else:
                        scores[currentgame*2-1] += 1

                # CHECK WINNER
                if sets_list[currentgame*2-2] == scores[currentgame*2-2]:
                    winner_list[currentgame*2-2] = True
                    winner_list[currentgame*2-1] = False
                    print(player_list[currentgame*2-2], ' wins')
                    if currentgame != 7:
                        player_list[currentgame+7] = player_list[currentgame*2-2]
                    # else:
                        # display_winner()

                elif sets_list[currentgame*2-1] == scores[currentgame*2-1]:
                    winner_list[currentgame*2-2] = False
                    winner_list[currentgame*2-1] = True
                    print(player_list[currentgame*2-1], ' wins')
                    if currentgame != 7:
                        player_list[currentgame+7] = player_list[currentgame*2-1]
                    # else:
                        # display_winner()
                else:
                    winner_list[currentgame * 2 - 2] = False
                    winner_list[currentgame * 2 - 1] = False
                    if currentgame != 7:
                        player_list[currentgame+7] = ""

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()