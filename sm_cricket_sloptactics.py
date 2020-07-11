import pygame
import numpy as np
# import platform
import sm_cricket_sloptactics_param as smp

# CONSTANTS
JVT = .9  # Joystick Value Threshold

P1 = "p1"
P2 = "p2"
START = "start"
SELECT = "select"
ESC = "escape"
UP = "up"
RIGHT = "right"
DOWN = "down"
LEFT = "Left"
BULL = "25"
TRIPLE = "3"
DOUBLE = "2"
TWENTY = "20"
NINETEEN = "19"
EIGHTEEN = "18"
SEVENTEEN = "17"
SIXTEEN = "16"
FIFTEEN = "15"
FOURTEEN = "14"
NUMBER = "number"
TACTICAL = "tactical"
MENU = "menu"
JOYSTICK = "joystick"

# COLOR   (R, G, B)
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


# VARIABLES

pygame.init()
# size of the e-ink 7.5-inch screen : width:384, height:640
# size for viewsonic : width:576, height:960
# size for 7inch hdmi lcd (b) - WaveShare w480 h800 (portrait orientation)
# screenWidth = 480
# screenHeight = 800
screen_width = smp.screenWidth
screen_height = smp.screenHeight
fullscreen = smp.fullscreen

col_score = round(screen_width / 4)
col_mark = round(screen_width * .17)
col_target = screen_width - 2 * col_score - 2 * col_mark

row_height = round(screen_height / 11)
row_top = screen_height - 10 * row_height

grid_offset = 8
p1_pos = (col_score + round(col_mark / 2), round(row_top / 2) + grid_offset)
p2_pos = (screen_width - col_score - round(col_mark / 2), round(row_top / 2) + grid_offset)
round_pos = (round(screen_width / 2), round(row_top / 2) + grid_offset)
round_txt_pos = (round(screen_width / 2), grid_offset)
p1_score_pos = (round(col_score / 2), round(row_top / 2) + grid_offset)
p2_score_pos = (round(screen_width - (col_score / 2)), round(row_top / 2) + grid_offset)
twenty_pos = (round(screen_width / 2), row_top + 0 * row_height + round(row_height / 2) + grid_offset)
nineteen_pos = (round(screen_width / 2), row_top + 1 * row_height + round(row_height / 2) + grid_offset)
eighteen_pos = (round(screen_width / 2), row_top + 2 * row_height + round(row_height / 2) + grid_offset)
seventeen_pos = (round(screen_width / 2), row_top + 3 * row_height + round(row_height / 2) + grid_offset)
sixteen_pos = (round(screen_width / 2), row_top + 4 * row_height + round(row_height / 2) + grid_offset)
fifteen_pos = (round(screen_width / 2), row_top + 5 * row_height + round(row_height / 2) + grid_offset)
fourteen_pos = (round(screen_width / 2), row_top + 6 * row_height + round(row_height / 2) + grid_offset)
double_pos = (round(screen_width / 2), row_top + 7 * row_height + round(row_height / 2) + grid_offset)
triple_pos = (round(screen_width / 2), row_top + 8 * row_height + round(row_height / 2) + grid_offset)
bull_pos = (round(screen_width / 2), row_top + 9 * row_height + round(row_height / 2) + grid_offset)

result_pos = (round(screen_width / 2), round(screen_height / 2))
result_rect = (0, round(screen_height / 20 * 9), screen_width, round(screen_height / 10))

if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # For screen on Raspberry Pi
else:
    screen = pygame.display.set_mode((screen_width, screen_height))

#  TODO add too the parameter file the font variables
pygame.display.set_caption("SLOP TACTICS CRICKET")
font = pygame.font.Font("HyningsHandwriting-Regular.ttf", 72)  # about screenHeight/20 - grid text
fontBig = pygame.font.Font("HyningsHandwriting-Regular.ttf", 72)  # about screenHeight/15 - final result text
fontScoreHist = pygame.font.Font("HyningsHandwriting-Regular.ttf", 40)  # about screenHeight/40 - score history
fontInfo = pygame.font.SysFont("HyningsHandwriting-Regular.ttf", 24)  # about screenHeight/80

player1 = True  # to be replaced by current_player
current_player = 0  # 0 for player 1, 1 for player 2 - i.e. the playerMatrix row
sitting_player = 1
scoreMultiplier = 1
currentRound = 1
prevTot1 = 0
prevTot2 = 0

# 20-14, D, T, B, score, score count
INITARRAY = np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0]])  # for restart test
playerMatrix = np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0]])
# 20-14, D, T, B, total score, score count
players_array = np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0]])
player_one_scores = np.array([0])  #  for individual scores
player_two_scores = np.array([0])

targets_order = [TWENTY, NINETEEN, EIGHTEEN, SEVENTEEN, SIXTEEN, FIFTEEN, FOURTEEN, DOUBLE, TRIPLE, BULL]

done = False
gameon = True

clock = pygame.time.Clock()
# screen.fill((255, 255, 255))


# FUNCTIONS


def text_blit(text, tb_font, clr, center):
    text_render = tb_font.render(text, True, clr)
    return text_render, text_render.get_rect(center=center)


def check_input(ci_event, test):
    if ci_event.type == pygame.KEYUP:
        if test == START and ci_event.key == pygame.K_SPACE:
            return True
        if test == SELECT and ci_event.key == pygame.K_RETURN:
            return True
        if test == UP and ci_event.key == pygame.K_UP:
            return True
        if test == RIGHT and ci_event.key == pygame.K_RIGHT:
            return True
        if test == DOWN and ci_event.key == pygame.K_DOWN:
            return True
        if test == LEFT and ci_event.key == pygame.K_LEFT:
            return True
        if test == BULL and ci_event.key == pygame.K_1:
            return True
        if test == TRIPLE and ci_event.key == pygame.K_3:
            return True
        if test == DOUBLE and ci_event.key == pygame.K_2:
            return True
        if test == TWENTY and ci_event.key == pygame.K_0:
            return True
        if test == NINETEEN and ci_event.key == pygame.K_9:
            return True
        if test == EIGHTEEN and ci_event.key == pygame.K_8:
            return True
        if test == SEVENTEEN and ci_event.key == pygame.K_7:
            return True
        if test == SIXTEEN and ci_event.key == pygame.K_6:
            return True
        if test == FIFTEEN and ci_event.key == pygame.K_5:
            return True
        if test == FOURTEEN and ci_event.key == pygame.K_4:
            return True
    if ci_event.type == pygame.JOYBUTTONUP:  # USING A GENERIC USB JOYSTICK
        if test == TWENTY and ci_event.button == 0:  # K1
            return True
        if test == BULL and ci_event.button == 1:  # K2
            return True
        if test == DOUBLE and ci_event.button == 2:  # K3
            return True
        if test == TRIPLE and ci_event.button == 3:  # K4
            return True
        if test == FOURTEEN and ci_event.button == 4:  # L2
            return True
        if test == FIFTEEN and ci_event.button == 5:  # R2
            return True
        if test == SIXTEEN and ci_event.button == 6:  # L1
            return True
        if test == SEVENTEEN and ci_event.button == 7:  # R1
            return True
        if test == EIGHTEEN and ci_event.button == 8:  # SE
            return True
        if test == NINETEEN and ci_event.button == 9:  # ST
            return True
        if test == START and ci_event.button == 10:  # K11
            return True
        if test == SELECT and ci_event.button == 11:  # K12
            return True
    if ci_event.type == pygame.JOYAXISMOTION:
        if test == DOWN and ci_event.axis == 0 and ci_event.value < -JVT:  # DOWN
            return True
        if test == UP and ci_event.axis == 0 and ci_event.value > JVT:  # UP
            return True
        if test == LEFT and ci_event.axis == 1 and ci_event.value < -JVT:  # LEFT
            return True
        if test == RIGHT and ci_event.axis == 1 and ci_event.value > JVT:  # RIGHT
            return True
    return False


def validate_input(ci_event):
    if ci_event.type == pygame.KEYUP:
        if ci_event.key == pygame.K_SPACE:
            return True, START, MENU
        if ci_event.key == pygame.K_RETURN:
            return True, SELECT, MENU
        if ci_event.key == pygame.K_UP:
            return True, UP, JOYSTICK
        if ci_event.key == pygame.K_RIGHT:
            return True, RIGHT, JOYSTICK
        if ci_event.key == pygame.K_DOWN:
            return True, DOWN, JOYSTICK
        if ci_event.key == pygame.K_LEFT:
            return True, LEFT, JOYSTICK
        if ci_event.key == pygame.K_1:
            return True, BULL, NUMBER
        if ci_event.key == pygame.K_3:
            return True, TRIPLE, TACTICAL
        if ci_event.key == pygame.K_2:
            return True, DOUBLE, TACTICAL
        if ci_event.key == pygame.K_0:
            return True, TWENTY, NUMBER
        if ci_event.key == pygame.K_9:
            return True, NINETEEN, NUMBER
        if ci_event.key == pygame.K_8:
            return True, EIGHTEEN, NUMBER
        if ci_event.key == pygame.K_7:
            return True, SEVENTEEN, NUMBER
        if ci_event.key == pygame.K_6:
            return True, SIXTEEN, NUMBER
        if ci_event.key == pygame.K_5:
            return True, FIFTEEN, NUMBER
        if ci_event.key == pygame.K_4:
            return True, FOURTEEN, NUMBER
    if ci_event.type == pygame.JOYBUTTONUP:  # USING A GENERIC USB JOYSTICK
        if ci_event.button == 0:  # K1
            return True, TWENTY, NUMBER
        if ci_event.button == 1:  # K2
            return True, BULL, NUMBER
        if ci_event.button == 2:  # K3
            return True, DOUBLE, TACTICAL
        if ci_event.button == 3:  # K4
            return True, TRIPLE, TACTICAL
        if ci_event.button == 4:  # L2
            return True, FOURTEEN, NUMBER
        if ci_event.button == 5:  # R2
            return True, FIFTEEN, NUMBER
        if ci_event.button == 6:  # L1
            return True, SIXTEEN, NUMBER
        if ci_event.button == 7:  # R1
            return True, SEVENTEEN, NUMBER
        if ci_event.button == 8:  # SE
            return True, EIGHTEEN, NUMBER
        if ci_event.button == 9:  # ST
            return True, NINETEEN, NUMBER
        if ci_event.button == 10:  # K11
            return True, START, MENU
        if ci_event.button == 11:  # K12
            return True, SELECT, MENU
    if ci_event.type == pygame.JOYAXISMOTION:
        if ci_event.axis == 0 and ci_event.value < -JVT:  # DOWN
            return True, DOWN, JOYSTICK
        if ci_event.axis == 0 and ci_event.value > JVT:  # UP
            return True, UP, JOYSTICK
        if ci_event.axis == 1 and ci_event.value < -JVT:  # LEFT
            return True, LEFT, JOYSTICK
        if ci_event.axis == 1 and ci_event.value > JVT:  # RIGHT
            return True, RIGHT, JOYSTICK
    return False, "none", "na"


def get_target_index(t):
    target_order = ["20", "19", "18", "17", "16", "15", "14", "2", "3", "25"]
    return target_order.index(t)


def get_player_target_success(p1, t):
    if p1:
        return playerMatrix[0, get_target_index(t)]
    else:
        return playerMatrix[1, get_target_index(t)]


def target_center(p1, t):
    tc_y = row_top - row_height + round((get_target_index(t) + 1.5) * row_height)
    if p1:
        tc_x = round(col_score + col_mark / 2)
    else:
        tc_x = round(screen_width - col_score - col_mark / 2)
    return int(tc_x), int(tc_y)


def target_center_new(p1, t):
    tc_y = row_top - row_height + round((get_target_index(t) + 1.5) * row_height)
    if p1 == 0:
        tc_x = round(col_score + col_mark / 2)
    else:
        tc_x = round(screen_width - col_score - col_mark / 2)
    return int(tc_x), int(tc_y)


def add_mark(p1, t, remove=False):
    x_target, y_target = target_center(p1, t)
    t_mark = get_player_target_success(p1, t)
    # print(t_mark)
    clr = 255 if remove else 0
    # print(clr)
    if t_mark == 2:
        pygame.draw.line(screen, (clr, clr, clr), (x_target - round(col_mark / 3), y_target + round(row_height / 3)),
                         (x_target + round(col_mark / 3), y_target - round(row_height / 3)), 3)
    elif t_mark == 1:
        pygame.draw.line(screen, (clr, clr, clr), (x_target - round(col_mark / 3), y_target - round(row_height / 3)),
                         (x_target + round(col_mark / 3), y_target + round(row_height / 3)), 3)
    else:
        pygame.draw.circle(screen, (clr, clr, clr), (x_target, y_target),
                           int(round(min(col_mark, row_height) / 2) - 5), 3)


def update_round(r):
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(col_score + col_mark + 1, 0, col_target - 1, row_top - 1))
    screen.blit(*text_blit(str(r), font, BLACK, round_pos))


def update_player_matrix(p1, t, sign=1):
    if p1:
        playerMatrix[0, get_target_index(t)] -= 1 * sign
        if playerMatrix[0, get_target_index(t)] > 3:
            playerMatrix[0, get_target_index(t)] = 3
    else:
        playerMatrix[1, get_target_index(t)] -= 1 * sign
        if playerMatrix[1, get_target_index(t)] > 3:
            playerMatrix[1, get_target_index(t)] = 3


def increase_player_total(p1, t, sm):
    s_index = get_target_index(t)
    if p1:
        playerMatrix[0, 10] += [20, 19, 18, 17, 16, 15, 14, 0, 0, 25][s_index] * sm
        playerMatrix[0, 11] += 1
        add_score_detail(p1, [20, 19, 18, 17, 16, 15, 14, 0, 0, 25][s_index] * sm, playerMatrix[0, 11])
    else:
        playerMatrix[1, 10] += [20, 19, 18, 17, 16, 15, 14, 0, 0, 25][s_index] * sm
        playerMatrix[1, 11] += 1
        add_score_detail(p1, [20, 19, 18, 17, 16, 15, 14, 0, 0, 25][s_index] * sm, playerMatrix[1, 11])


def score_player_throw(p1, t, sm):
    x_center, y_double = target_center(p1, "D")
    x_center, y_triple = target_center(p1, "T")
    x_center = int(round(screen_width / 2))
    radius = int(round(col_mark * .4))

    if get_player_target_success(p1, t) > 0:  # if the player has not closed the target
        update_player_matrix(p1, t)
        add_mark(p1, t)
    elif get_player_target_success(not p1, t) > 0:  # if target closed, check if the other player has closed
        if t == "D":
            # print("Double Scoring")
            pygame.draw.circle(screen, (0, 0, 0), (x_center, y_double), radius, 2)
            # scoreMultiplier = 2
            score_multiplier_target(p1, 2)
            pygame.draw.circle(screen, (255, 255, 255), (x_center, y_double), radius, 2)
        elif t == "T":
            # print("Triple Scoring")
            pygame.draw.circle(screen, (0, 0, 0), (x_center, y_triple), radius, 2)
            score_multiplier_target(p1, 3)
            pygame.draw.circle(screen, (255, 255, 255), (x_center, y_triple), radius, 2)
            # scoreMultiplier = 3
        else:
            increase_player_total(p1, t, sm)


def update_score_screen(p1):
    if p1:
        pygame.draw.rect(screen, WHITE, pygame.Rect(0, 0, col_score, row_top))
        screen.blit(*text_blit(str(playerMatrix[0, 10]), font, BLACK, p1_score_pos))
    else:
        pygame.draw.rect(screen, WHITE, pygame.Rect(screen_width - col_score + 1, 0, col_score, row_top))
        screen.blit(*text_blit(str(playerMatrix[1, 10]), font, BLACK, p2_score_pos))


def change_player(p1):
    if p1:
        pygame.draw.rect(screen, WHITE, pygame.Rect(screen_width - col_score - col_mark + 1, 0, col_mark - 1, row_top))
        screen.blit(*text_blit(P1, font, BLACK, p1_pos))
    else:
        pygame.draw.rect(screen, WHITE, pygame.Rect(col_score + 1, 0, col_mark - 1, row_top))
        screen.blit(*text_blit(P2, font, BLACK, p2_pos))


def check_winner():
    if playerMatrix[0, 0:10].sum() == 0 and playerMatrix[0, 10] > playerMatrix[1, 10]:
        pygame.draw.rect(screen, WHITE, result_rect)
        screen.blit(*text_blit("Player 1 WINS!", fontBig, RED, result_pos))
    elif playerMatrix[1, 0:10].sum() == 0 and playerMatrix[0, 10] < playerMatrix[1, 10]:
        pygame.draw.rect(screen, WHITE, result_rect)
        screen.blit(*text_blit("Player 2 WINS!", fontBig, RED, result_pos))
    elif playerMatrix[:, 0:10].sum() == 0 and playerMatrix[0, 10] == playerMatrix[1, 10]:
        pygame.draw.rect(screen, WHITE, result_rect)
        screen.blit(*text_blit("DRAW!", fontBig, RED, result_pos))


def score_multiplier_target(p1, sm):
    # TODO: block triple bull
    other_target = 1
    smt_done = False
    while not smt_done:
        for smt_event in pygame.event.get():
            if check_input(smt_event, LEFT):   # LEFT
                other_target += 1
            if check_input(smt_event, RIGHT):   # RIGHT
                other_target += 4
            if check_input(smt_event, UP):   # UP
                other_target *= 2
            if check_input(smt_event, DOWN):   # DOWN
                update_round(currentRound)
                if p1:
                    playerMatrix[0, 10] += other_target * sm
                    playerMatrix[0, 11] += 1
                    add_score_detail(p1, other_target * sm, playerMatrix[0, 11])
                else:
                    playerMatrix[1, 10] += other_target * sm
                    playerMatrix[1, 11] += 1
                    add_score_detail(p1, other_target * sm, playerMatrix[1, 11])
                smt_done = True

            if check_input(smt_event, TWENTY):
                increase_player_total(p1, "20", sm)
                # print("button 0 pressed")
                smt_done = True
            if check_input(smt_event, NINETEEN):
                increase_player_total(p1, "19", sm)
                smt_done = True
            if check_input(smt_event, EIGHTEEN):
                increase_player_total(p1, "18", sm)
                smt_done = True
            if check_input(smt_event, SEVENTEEN):
                increase_player_total(p1, "17", sm)
                smt_done = True
            if check_input(smt_event, SIXTEEN):
                increase_player_total(p1, "16", sm)
                smt_done = True
            if check_input(smt_event, FIFTEEN):
                increase_player_total(p1, "15", sm)
                smt_done = True
            if check_input(smt_event, FOURTEEN):
                increase_player_total(p1, "14", sm)
                smt_done = True
            if check_input(smt_event, BULL):
                increase_player_total(p1, "B", sm)
                smt_done = True

        # print("other Target loop:", otherTarget)
        if other_target > 13:
            other_target = 1
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(col_score + col_mark + 1, 0, col_target - 1, row_top - 1))
        screen.blit(*text_blit(str(other_target), font, BLACK, round_pos))
        pygame.display.flip()
        update_round(currentRound)  # todo global variable...
        clock.tick(20)


def score_correction(p1):
    other_target = -1
    sc_done = False
    while not sc_done:
        for sc_event in pygame.event.get():
            if check_input(sc_event, DOWN):  # DOWN
                update_round(currentRound)
                if p1:
                    playerMatrix[0, 10] += other_target
                    playerMatrix[0, 11] += 1
                    add_score_detail(p1, other_target, playerMatrix[0, 11])
                else:
                    playerMatrix[1, 10] += other_target
                    playerMatrix[1, 11] += 1
                    add_score_detail(p1, other_target, playerMatrix[1, 11])
                sc_done = True
            if check_input(sc_event, LEFT):   # LEFT
                other_target -= 1
            if check_input(sc_event, RIGHT):  # RIGHT
                other_target -= 4
            if check_input(sc_event, UP):  # UP
                other_target *= 2
            if check_input(sc_event, TWENTY):
                add_mark(p1, "20", True)
                update_player_matrix(p1, "20", -1)
                sc_done = True
            if check_input(sc_event, NINETEEN):
                add_mark(p1, "19", True)
                update_player_matrix(p1, "19", -1)
                sc_done = True
            if check_input(sc_event, EIGHTEEN):
                add_mark(p1, "18", True)
                update_player_matrix(p1, "18", -1)
                sc_done = True
            if check_input(sc_event, SEVENTEEN):
                add_mark(p1, "17", True)
                update_player_matrix(p1, "17", -1)
                sc_done = True
            if check_input(sc_event, SIXTEEN):
                add_mark(p1, "16", True)
                update_player_matrix(p1, "16", -1)
                sc_done = True
            if check_input(sc_event, FIFTEEN):
                add_mark(p1, "15", True)
                update_player_matrix(p1, "15", -1)
                sc_done = True
            if check_input(sc_event, FOURTEEN):
                add_mark(p1, "14", True)
                update_player_matrix(p1, "14", -1)
                sc_done = True
            if check_input(sc_event, TRIPLE):
                add_mark(p1, "T", True)
                update_player_matrix(p1, "T", -1)
                sc_done = True
            if check_input(sc_event, DOUBLE):
                add_mark(p1, "D", True)
                update_player_matrix(p1, "D", -1)
                sc_done = True
            if check_input(sc_event, BULL):
                add_mark(p1, "B", True)
                update_player_matrix(p1, "B", -1)
                sc_done = True

        # print("other Target loop:", otherTarget)
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(col_score + col_mark + 1, 0, col_target - 1, row_top - 1))
        screen.blit(*text_blit(str(other_target), font, BLACK, round_pos))
        pygame.display.flip()
        update_round(currentRound)  # todo global variable...
        clock.tick(20)


def add_score_detail(p1, score, n):
    mark = fontScoreHist.render(str(score), True, (0, 0, 0))
    cc = 3 if n <= 20 else 1  # start with colonne interieure, ensuite exterieure
    if n < 41:
        if p1:
            asd_x = round(cc * col_score / 4 - mark.get_width() / 2)
            # x = round((m.floor(n/21)+1) * colScore/4 - mark.get_width()/2)
            asd_y = row_top + round(((n - 1) % 20) * row_height / 2) + round((row_height - mark.get_height()) / 8)
            screen.blit(mark, (asd_x, asd_y))
        else:
            asd_x = round(screen_width - cc * col_score / 4 - mark.get_width() / 2)
            asd_y = row_top + round(((n - 1) % 20) * row_height / 2) + round((row_height - mark.get_height()) / 8)
            screen.blit(mark, (asd_x, asd_y))


def init_score_board():
    screen.fill((255, 255, 255))
    # column Grid
    pygame.draw.line(screen, (0, 0, 0,), (col_score, 0), (col_score, screen_height), 1)
    pygame.draw.line(screen, (0, 0, 0,), (col_score + col_mark, 0), (col_score + col_mark, screen_height), 1)
    pygame.draw.line(screen, (0, 0, 0,), (col_score + col_mark + col_target, 0),
                     (col_score + col_mark + col_target, screen_height), 1)
    pygame.draw.line(screen, (0, 0, 0,), (col_score + 2 * col_mark + col_target, 0),
                     (col_score + 2 * col_mark + col_target, screen_height), 1)
    # Row Grid
    for r in range(1, 10):
        pygame.draw.line(screen, (0, 0, 0,), (col_score, row_top + r * row_height),
                         (screen_width - col_score, row_top + r * row_height), 1)
        # Draw double first line
    pygame.draw.line(screen, (0, 0, 0,), (0, row_top + 2), (screen_width, row_top + 2), 1)
    pygame.draw.line(screen, (0, 0, 0,), (0, row_top), (screen_width, row_top), 1)

    # Targets
    screen.blit(*text_blit(P1, font, BLACK, p1_pos))
    screen.blit(*text_blit(TWENTY, font, BLACK, twenty_pos))
    screen.blit(*text_blit(NINETEEN, font, BLACK, nineteen_pos))
    screen.blit(*text_blit(EIGHTEEN, font, BLACK, eighteen_pos))
    screen.blit(*text_blit(SEVENTEEN, font, BLACK, seventeen_pos))
    screen.blit(*text_blit(SIXTEEN, font, BLACK, sixteen_pos))
    screen.blit(*text_blit(FIFTEEN, font, BLACK, fifteen_pos))
    screen.blit(*text_blit(FOURTEEN, font, BLACK, fourteen_pos))
    screen.blit(*text_blit(DOUBLE, font, BLACK, double_pos))
    screen.blit(*text_blit(TRIPLE, font, BLACK, triple_pos))
    screen.blit(*text_blit(BULL, font, BLACK, bull_pos))

    screen.blit(*text_blit(str(currentRound), font, BLACK, round_pos))

    # print("="*40, "System Information", "="*40)
    # uname = platform.uname()
    # print(f"System: {uname.system}")
    # print(f"Node Name: {uname.node}")
    # print(f"Release: {uname.release}")
    # print(f"Version: {uname.version}")
    # print(f"Machine: {uname.machine}")
    # print(f"Processor: {uname.processor}")


def confirm_restart():
    #pygame.draw.rect(screen, WHITE, result_rect)
    pygame.draw.rect(screen, WHITE, (0, 0, screen_width, round(screen_height / 12)))
    screen.blit(*text_blit("Confirm restart", fontBig, RED, (round(screen_width / 2), round(screen_height / 20))))
    pygame.display.flip()
    restart = True
    while restart:
        for event in pygame.event.get():
            if check_input(event, START):
                restart = False
                return True
            if check_input(event, SELECT):
                restart = False
                return False


# Main game loop
while gameon:
    clock.tick(20)
    # logfile = open("CricketEpaper.log", "a")
    # logline = ""
    # pygame.init()
    print("Game On!")
    init_score_board()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    done = False
    pygame.display.flip()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                gameon = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                done = True
                gameon = False
            # if check_input(event, DOWN):
            #     player1 = not player1  # to be removed
            #     if current_player == 0:
            #         current_player = 1
            #         sitting_player = 0
            #     else:
            #         current_player = 0
            #         sitting_player = 1
            #     change_player(player1)
            #     scoreMultiplier = 1
            #     if player1:
            #         currentRound = currentRound + 1
            #         update_round(currentRound)

            # if check_input(event, TWENTY):
            #     score_player_throw(player1, TWENTY, scoreMultiplier)
            #     if scoreMultiplier == 1:
            #         if players_array[current_player, get_target_index(TWENTY)] > 0:  # if the player has not closed
            #             players_array[current_player, get_target_index(TWENTY)] -= 1
            #         elif players_array[sitting_player, get_target_index(TWENTY)] > 0:  # if opponent has not closed
            #             players_array[current_player, 10] += 20
            #             players_array[current_player, 11] += 1
            #     else:
            #         players_array[current_player, 10] += 20 * scoreMultiplier
            #         scoreMultiplier = 1
            # if check_input(event, NINETEEN):
            #     score_player_throw(player1, NINETEEN, scoreMultiplier)
            #     if scoreMultiplier == 1:
            #         if players_array[current_player, get_target_index(NINETEEN)] > 0:  # if the player has not closed
            #             players_array[current_player, get_target_index(NINETEEN)] -= 1
            #         elif players_array[sitting_player, get_target_index(NINETEEN)] > 0:  # if opponent has not closed
            #             players_array[current_player, 10] += int(NINETEEN)
            #             players_array[current_player, 11] += 1
            #     else:
            #         players_array[current_player, 10] += int(NINETEEN) * scoreMultiplier
            #         scoreMultiplier = 1
            # if check_input(event, EIGHTEEN):
            #     score_player_throw(player1, EIGHTEEN, scoreMultiplier)
            # if check_input(event, SEVENTEEN):
            #     score_player_throw(player1, SEVENTEEN, scoreMultiplier)
            # if check_input(event, SIXTEEN):
            #     score_player_throw(player1, SIXTEEN, scoreMultiplier)
            # if check_input(event, FIFTEEN):
            #     score_player_throw(player1, FIFTEEN, scoreMultiplier)
            # if check_input(event, FOURTEEN):
            #     score_player_throw(player1, FOURTEEN, scoreMultiplier)
            # if check_input(event, TRIPLE):
            #     # score_player_throw(player1, TRIPLE, scoreMultiplier)
            #     if scoreMultiplier == 1:
            #         if players_array[current_player, get_target_index(TRIPLE)] > 0:  # if the player has not closed
            #             players_array[current_player, get_target_index(TRIPLE)] -= 1
            #         elif players_array[sitting_player, get_target_index(TRIPLE)] > 0:  # if opponent has not closed
            #             scoreMultiplier = 3
            # if check_input(event, DOUBLE):
            #     score_player_throw(player1, DOUBLE, scoreMultiplier)
            # if check_input(event, BULL):
            #     score_player_throw(player1, BULL, scoreMultiplier)

            valid_input, input_value, input_type = validate_input(event)

            if valid_input and input_type == NUMBER:
                if scoreMultiplier == 1:
                    if players_array[current_player, get_target_index(input_value)] > 0:  # if the player has not closed
                        players_array[current_player, get_target_index(input_value)] -= 1
                    elif players_array[sitting_player, get_target_index(input_value)] > 0:  # if opponent has not closed
                        players_array[current_player, 10] += int(input_value)
                        players_array[current_player, 11] += 1
                else:
                    players_array[current_player, 10] += int(input_value) * scoreMultiplier
                    scoreMultiplier = 1

            if valid_input and input_type == TACTICAL:
                # score_player_throw(player1, TRIPLE, scoreMultiplier)
                if scoreMultiplier == 1:
                    if players_array[current_player, get_target_index(input_value)] > 0:  # if the player has not closed
                        players_array[current_player, get_target_index(input_value)] -= 1
                    elif players_array[sitting_player, get_target_index(input_value)] > 0:  # if opponent has not closed
                        scoreMultiplier = int(input_value)

            if valid_input and input_type == JOYSTICK:
                if scoreMultiplier == 1 and input_value == DOWN:
                    # player1 = not player1  # to be removed
                    if current_player == 0:
                        current_player = 1
                        sitting_player = 0
                    else:
                        current_player = 0
                        sitting_player = 1
                        currentRound += 1
                    # change_player(player1)
                    scoreMultiplier = 1
                    # if player1:
                    #     currentRound = currentRound + 1
                    #     update_round(currentRound)

            if valid_input:
                print("validate:", valid_input, input_value, input_type)
                #print(event)
                print(players_array)
                print("player:", current_player)

            if check_input(event, START):

                if confirm_restart():
                    # reset variable (python references variables...)
                    playerMatrix = np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0]])
                    player1 = True
                    current_player = 0
                    currentRound = 1
                    scoreMultiplier = 1
                    print("Start button pressed")
                    # redraw screen
                    pygame.display.flip()
                    done = True

            if check_input(event, SELECT):  # X/oops/correction button
                comparison = playerMatrix == INITARRAY  # arrays cannot be compared directly with ==
                equal_arrays = comparison.all()
                if equal_arrays:  # if at beginning of game; exit program
                    done = True
                    gameon = False
                else:
                    score_correction(player1)

            check_winner()
            update_score_screen(player1)


            # REFRESH DISPLAY
            # init_score_board()
            # print(event)
            # print(playerMatrix, players_array)
            # print(current_player)
            screen.blit(*text_blit(str(currentRound), font, ORANGE, round_pos))
            screen.blit(*text_blit("round", fontInfo, GRAY, round_txt_pos))
            screen.blit(*text_blit(str(players_array[0, 10]), font, ORANGE, p1_score_pos))
            screen.blit(*text_blit(str(players_array[1, 10]), font, ORANGE, p2_score_pos))
            if current_player == 0:
                screen.blit(*text_blit(P1, font, ORANGE, p1_pos))
            if current_player == 1:
                screen.blit(*text_blit(P2, font, ORANGE, p2_pos))
            for t in range(10):
                for p in range(2):
                    #  x_target, y_target = target_center_new(p, t+1)
                    y_target = int(row_top - row_height + round((t + 1.5) * row_height))
                    x_target = int(round(p * screen_width + (1 - 2 * p) * col_score + (1 - 2 * p) * col_mark / 2))
                    #print(t, p, x_target, y_target)
                    #print(player_one_scores)
                    if players_array[p, t] < 3:
                        # print("draw first line")
                        pygame.draw.line(screen, ORANGE,
                                        (x_target - round(col_mark / 3), y_target + round(row_height / 3)),
                                        (x_target + round(col_mark / 3), y_target - round(row_height / 3)), 8)
                    if players_array[p, t] < 2:
                        # print("draw second line")
                        pygame.draw.line(screen, ORANGE,
                                        (x_target - round(col_mark / 3), y_target - round(row_height / 3)),
                                        (x_target + round(col_mark / 3), y_target + round(row_height / 3)), 8)
                    if players_array[p, t] < 1:
                        # print("draw third line")
                        pygame.draw.circle(screen, ORANGE, (x_target, y_target),
                                           int(round(min(col_mark, row_height) / 2) - 5), 6)
            pygame.display.flip()
    # ---------------------------------------------
    # logfile.close()

pygame.quit()
