import pygame
import numpy as np
import platform
import sm_cricket_sloptactics_param as smp

pygame.init()
# size of the e-ink 7.5-inch screen : width:384, height:640
# size for viewsonic : width:576, height:960
# size for 7inch hdmi lcd (b) - waveshare w480 h800 (portrait orientation)
# screenWidth = 480
# screenHeight = 800
screenWidth = smp.screenWidth
screenHeight = smp.screenHeight
fullscreen = smp.fullscreen

col_score = round(screenWidth / 4)
colMark = round(screenWidth * .17)
colTarget = screenWidth - 2 * col_score - 2 * colMark

rowHeight = round(screenHeight / 11)
rowTop = screenHeight - 10 * rowHeight

if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # For screen on Raspberry Pi
else:
    screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("CRICKET")

font = pygame.font.SysFont("arial", 72)  # about screenHeigth/20
fontBig = pygame.font.SysFont("arial", 60)  # about screenHeigth/15
fontScoreHist = pygame.font.SysFont("arial", 40)  # about screenHeigth/40
fontDebug = pygame.font.SysFont("arial", 16)  # about screenHeigth/80

JVT = .9  # Joystick Value Threshold
# the values for the following constants are not used themselves
START = "start"
SELECT = "select"
ESC = "escape"
UP = "up"
RIGHT = "right"
DOWN = "down"
LEFT = "Left"
BULL = "bullseye"
TRIPLE = "triple"
DOUBLE = "double"
TWENTY = "20"
NINETEEN = "19"
EIGHTEEN = "18"
SEVENTEEN = "17"
SIXTEEN = "16"
FIFTEEN = "15"
FOURTEEN = "14"

player1 = True
scoreMultiplier = 1
currentRound = 1
prevTot1 = 0
prevTot2 = 0

text20 = font.render("20", True, (0, 0, 0))
text19 = font.render("19", True, (0, 0, 0))
text18 = font.render("18", True, (0, 0, 0))
text17 = font.render("17", True, (0, 0, 0))
text16 = font.render("16", True, (0, 0, 0))
text15 = font.render("15", True, (0, 0, 0))
text14 = font.render("14", True, (0, 0, 0))
textDouble = font.render("D", True, (0, 0, 0))
textTriple = font.render("T", True, (0, 0, 0))
textBull = font.render("B", True, (0, 0, 0))
textPlayer1 = font.render("P1", True, (0, 0, 0))
textPlayer2 = font.render("P2", True, (0, 0, 0))

# 20-14, D, T, B, score, score count
playerMatrix = np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0]])
# print(playerMatrix[1,0])

done = False
gameon = True

is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()
screen.fill((255, 255, 255))

# FUNCTIONS


def text_blit(text, tb_font, clr, center):
    textrender = tb_font.render(text, True, clr)
    return textrender, textrender.get_rect(center=center)


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


def get_target_index(t):
    target_order = ["20", "19", "18", "17", "16", "15", "14", "D", "T", "B"]
    return target_order.index(t)


def get_player_target_success(p1, t):
    if p1:
        return playerMatrix[0, get_target_index(t)]
    else:
        return playerMatrix[1, get_target_index(t)]


def target_center(p1, t):
    tc_y = rowTop - rowHeight + round((get_target_index(t) + 1.5) * rowHeight)
    if p1:
        tc_x = round(col_score + colMark / 2)
    else:
        tc_x = round(screenWidth - col_score - colMark / 2)
    return int(tc_x), int(tc_y)


def add_mark(p1, t, remove=False):
    x_target, y_target = target_center(p1, t)
    t_mark = get_player_target_success(p1, t)
    # print(t_mark)
    clr = 255 if remove else 0
    # print(clr)
    if t_mark == 2:
        pygame.draw.line(screen, (clr, clr, clr), (x_target - round(colMark / 3), y_target + round(rowHeight / 3)),
                         (x_target + round(colMark / 3), y_target - round(rowHeight / 3)), 3)
    elif t_mark == 1:
        pygame.draw.line(screen, (clr, clr, clr), (x_target - round(colMark / 3), y_target - round(rowHeight / 3)),
                         (x_target + round(colMark / 3), y_target + round(rowHeight / 3)), 3)
    else:
        pygame.draw.circle(screen, (clr, clr, clr), (x_target, y_target),
                           int(round(min(colMark, rowHeight) / 2) - 5), 3)


def update_round(r):
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(col_score + colMark + 1, 0, colTarget - 1, rowTop - 1))
    cround = font.render(str(r), True, (0, 0, 0))
    screen.blit(cround, (
        col_score + colMark + round((colTarget - cround.get_width()) / 2), round((rowTop - cround.get_height()) / 2)))


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
    x_center = int(round(screenWidth / 2))
    radius = int(round(colMark * .4))

    if get_player_target_success(p1, t) > 0:
        update_player_matrix(p1, t)
        add_mark(p1, t)
    elif get_player_target_success(not p1, t) > 0:
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
        p1_score = font.render(str(playerMatrix[0, 10]), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, col_score, rowTop))
        screen.blit(p1_score, (round(col_score - p1_score.get_width()) / 2,
                               round((rowTop - p1_score.get_height()) / 2)))
    else:
        p2_score = font.render(str(playerMatrix[1, 10]), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(screenWidth - col_score + 1, 0, col_score, rowTop))
        screen.blit(p2_score, (screenWidth - col_score + round((col_score - p2_score.get_width()) / 2),
                               round((rowTop - p2_score.get_height()) / 2)))


def change_player(p1):
    if p1:
        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(screenWidth - col_score - colMark + 1, 0, colMark - 1, rowTop))
        screen.blit(textPlayer1,
                    ((col_score + colMark / 2 - textPlayer1.get_width() / 2),
                     round((rowTop - textPlayer1.get_height()) / 2)))  # Remove y+9 (for testing)
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(col_score + 1, 0, colMark - 1, rowTop))
        screen.blit(textPlayer2, ((screenWidth - col_score - colMark / 2 - textPlayer2.get_width() / 2),
                                  round((rowTop - textPlayer2.get_height()) / 2)))


def check_winner():
    if playerMatrix[0, 0:10].sum() == 0 and playerMatrix[0, 10] > playerMatrix[1, 10]:
        text_p1_wins = fontBig.render("Player 1 WINS!", True, (0, 0, 0))
        screen.blit(text_p1_wins, (round(screenWidth - text_p1_wins.get_width()) / 2, screenHeight / 2))
    elif playerMatrix[1, 0:10].sum() == 0 and playerMatrix[0, 10] < playerMatrix[1, 10]:
        text_p2_wins = fontBig.render("Player 2 WINS!", True, (0, 0, 0))
        screen.blit(text_p2_wins, (round(screenWidth - text_p2_wins.get_width()) / 2, screenHeight / 2))
    elif playerMatrix[:, 0:10].sum() == 0 and playerMatrix[0, 10] == playerMatrix[1, 10]:
        text_draw = fontBig.render("DRAW!", True, (0, 0, 0))
        screen.blit(text_draw, (round(screenWidth - text_draw.get_width()) / 2, screenHeight / 2))


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
        other_target_text = font.render(str(other_target), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(col_score + colMark + 1, 0, colTarget - 1, rowTop - 1))
        screen.blit(other_target_text, (
            round((screenWidth - other_target_text.get_width()) / 2),
            round((rowTop - other_target_text.get_height()) / 2)))
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
        other_target_text = font.render(str(other_target), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(col_score + colMark + 1, 0, colTarget - 1, rowTop - 1))
        screen.blit(other_target_text, (
            round((screenWidth - other_target_text.get_width()) / 2),
            round((rowTop - other_target_text.get_height()) / 2)))
        # pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 484, 20))
        # playerdata = fontDebug.render(str(playerMatrix), True, (0, 255, 255))
        # screen.blit(playerdata, (2, 0))
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
            asd_y = rowTop + round(((n - 1) % 20) * rowHeight / 2) + round((rowHeight - mark.get_height()) / 8)
            screen.blit(mark, (asd_x, asd_y))
        else:
            asd_x = round(screenWidth - cc * col_score / 4 - mark.get_width() / 2)
            asd_y = rowTop + round(((n - 1) % 20) * rowHeight / 2) + round((rowHeight - mark.get_height()) / 8)
            screen.blit(mark, (asd_x, asd_y))


def init_score_board():
    screen.fill((255, 255, 255))
    # Initialize the joysticks
    # pygame.joystick.init()
    # column Grid
    pygame.draw.line(screen, (0, 0, 0,), (col_score, 0), (col_score, screenHeight), 1)
    pygame.draw.line(screen, (0, 0, 0,), (col_score + colMark, 0), (col_score + colMark, screenHeight), 1)
    pygame.draw.line(screen, (0, 0, 0,), (col_score + colMark + colTarget, 0),
                     (col_score + colMark + colTarget, screenHeight), 1)
    pygame.draw.line(screen, (0, 0, 0,), (col_score + 2 * colMark + colTarget, 0),
                     (col_score + 2 * colMark + colTarget, screenHeight), 1)
    # Row Grid
    for r in range(1, 10):
        pygame.draw.line(screen, (0, 0, 0,), (col_score, rowTop + r * rowHeight),
                         (screenWidth - col_score, rowTop + r * rowHeight), 1)
        # Draw double first line
    pygame.draw.line(screen, (0, 0, 0,), (0, rowTop + 2), (screenWidth, rowTop + 2), 1)
    pygame.draw.line(screen, (0, 0, 0,), (0, rowTop), (screenWidth, rowTop), 1)

    # Target TODO Better center the text with textVar.get_width(), get_heigth() & round()
    screen.blit(textPlayer1, ((col_score + colMark / 2 - textPlayer1.get_width() / 2),
                              round((rowTop - textPlayer1.get_height()) / 2)))  # Remove y+9 (for testing)
    # screen.blit(textPlayer2,((screenWidth-colScore-colMark/2 - textPlayer2.get_width()/2), 9))
    screen.blit(text20,
                (round((screenWidth - text20.get_width()) / 2), rowTop + round((rowHeight - text20.get_height()) / 2)))
    screen.blit(text19, (round((screenWidth - text19.get_width()) / 2),
                         rowTop + 1 * rowHeight + round((rowHeight - text19.get_height()) / 2)))
    screen.blit(text18, (round((screenWidth - text18.get_width()) / 2),
                         rowTop + 2 * rowHeight + round((rowHeight - text18.get_height()) / 2)))
    screen.blit(text17, (round((screenWidth - text17.get_width()) / 2),
                         rowTop + 3 * rowHeight + round((rowHeight - text17.get_height()) / 2)))
    screen.blit(text16, (round((screenWidth - text16.get_width()) / 2),
                         rowTop + 4 * rowHeight + round((rowHeight - text16.get_height()) / 2)))
    screen.blit(text15, (round((screenWidth - text15.get_width()) / 2),
                         rowTop + 5 * rowHeight + round((rowHeight - text15.get_height()) / 2)))
    screen.blit(text14, (round((screenWidth - text14.get_width()) / 2),
                         rowTop + 6 * rowHeight + round((rowHeight - text14.get_height()) / 2)))
    screen.blit(textDouble, (round((screenWidth - textDouble.get_width()) / 2),
                             rowTop + 7 * rowHeight + round((rowHeight - textDouble.get_height()) / 2)))
    screen.blit(textTriple, (round((screenWidth - textTriple.get_width()) / 2),
                             rowTop + 8 * rowHeight + round((rowHeight - textTriple.get_height()) / 2)))
    screen.blit(textBull, (round((screenWidth - textBull.get_width()) / 2),
                           rowTop + 9 * rowHeight + round((rowHeight - textBull.get_height()) / 2)))
    init_round = font.render(str(currentRound), True, (0, 0, 0))
    screen.blit(init_round,
                (round((screenWidth - init_round.get_width()) / 2), round((rowTop - init_round.get_height()) / 2)))

    print("="*40, "System Information", "="*40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")


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
    print(joystick.get_button(10))
    print(joystick.get_button(1))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                gameon = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # is_blue = not is_blue
                done = True
                gameon = False
            if check_input(event, DOWN):
                player1 = not player1
                change_player(player1)
                scoreMultiplier = 1
                if player1:
                    # print("increase round")
                    currentRound = currentRound + 1
                    update_round(currentRound)

            #     # print("button pressed")
            #     # print(joystick.get_button(0))
            if check_input(event, TWENTY):
                # print("button 20 pressed")
                score_player_throw(player1, "20", scoreMultiplier)
            if check_input(event, NINETEEN):
                score_player_throw(player1, "19", scoreMultiplier)
            if check_input(event, EIGHTEEN):
                score_player_throw(player1, "18", scoreMultiplier)
            if check_input(event, SEVENTEEN):
                score_player_throw(player1, "17", scoreMultiplier)
            if check_input(event, SIXTEEN):
                score_player_throw(player1, "16", scoreMultiplier)
            if check_input(event, FIFTEEN):
                score_player_throw(player1, "15", scoreMultiplier)
            if check_input(event, FOURTEEN):
                score_player_throw(player1, "14", scoreMultiplier)
            if check_input(event, TRIPLE):
                score_player_throw(player1, "T", scoreMultiplier)
            if check_input(event, DOUBLE):
                score_player_throw(player1, "D", scoreMultiplier)
            if check_input(event, BULL):
                score_player_throw(player1, "B", scoreMultiplier)
            if check_input(event, START):
                # todo ask for confirmation or activate on game end only
                # reset variable
                playerMatrix = np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0]])
                player1 = True
                currentRound = 1
                scoreMultiplier = 1
                print("Start button pressed")
                # redraw screen
                pygame.display.flip()
                done = True
                # initScoreBoard()

            if check_input(event, SELECT):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(11):
                score_correction(player1)

            check_winner()
            update_score_screen(player1)
            pygame.display.flip()

    # ---------------------------------------------
    # logfile.close()

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
