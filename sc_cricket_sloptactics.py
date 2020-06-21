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

colScore = round(screenWidth / 4)
colMark = round(screenWidth * .17)
colTarget = screenWidth - 2 * colScore - 2 * colMark

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

def text_blit(text, font, clr, center):
    textrender = font.render(text, True, clr)
    return textrender, textrender.get_rect(center=center)


def check_input(event, test):
    if event.type == pygame.KEYUP:
        if test == START and event.key == pygame.K_SPACE:
            return True
        if test == SELECT and event.key == pygame.K_RETURN:
            return True
        if test == UP and event.key == pygame.K_UP:
            return True
        if test == RIGHT and event.key == pygame.K_RIGHT:
            return True
        if test == DOWN and event.key == pygame.K_DOWN:
            return True
        if test == LEFT and event.key == pygame.K_LEFT:
            return True
        if test == BULL and event.key == pygame.K_1:
            return True
        if test == TRIPLE and event.key == pygame.K_3:
            return True
        if test == DOUBLE and event.key == pygame.K_2:
            return True
        if test == TWENTY and event.key == pygame.K_0:
            return True
        if test == NINETEEN and event.key == pygame.K_9:
            return True
        if test == EIGHTEEN and event.key == pygame.K_8:
            return True
        if test == SEVENTEEN and event.key == pygame.K_7:
            return True
        if test == SIXTEEN and event.key == pygame.K_6:
            return True
        if test == FIFTEEN and event.key == pygame.K_5:
            return True
        if test == FOURTEEN and event.key == pygame.K_4:
            return True
    if event.type == pygame.JOYBUTTONUP:  # USING A GENERIC USB JOYSTICK
        if test == TWENTY and event.button == 0:  # K1
            return True
        if test == BULL and event.button == 1:  # K2
            return True
        if test == DOUBLE and event.button == 2:  # K3
            return True
        if test == TRIPLE and event.button == 3:  # K4
            return True
        if test == FOURTEEN and event.button == 4:  # L2
            return True
        if test == FIFTEEN and event.button == 5:  # R2
            return True
        if test == SIXTEEN and event.button == 6:  # L1
            return True
        if test == SEVENTEEN and event.button == 7:  # R1
            return True
        if test == EIGHTEEN and event.button == 8:  # SE
            return True
        if test == NINETEEN and event.button == 9:  # ST
            return True
        if test == START and event.button == 10:  # K11
            return True
        if test == SELECT and event.button == 11:  # K12
            return True
    if event.type == pygame.JOYAXISMOTION:
        if test == DOWN and event.axis == 0 and event.value < -JVT:  # DOWN , ALTERNATE: joystick.get_axis(0) == 1:
            return True
        if test == UP and event.axis == 0 and event.value > JVT:  # UP
            return True
        if test == LEFT and event.axis == 1 and event.value < -JVT:  # LEFT
            return True
        if test == RIGHT and event.axis == 1 and event.value > JVT:  # RIGHT
            return True
    return False


def getTargetIndex(t):
    TargetOrder = ["20", "19", "18", "17", "16", "15", "14", "D", "T", "B"]
    return TargetOrder.index(t)


def getPlayerTargetSuccess(p1, t):
    if p1:
        return playerMatrix[0, getTargetIndex(t)]
    else:
        return playerMatrix[1, getTargetIndex(t)]


def TargetCenter(p1, t):
    y = rowTop - rowHeight + round((getTargetIndex(t) + 1.5) * rowHeight)
    if p1:
        x = round(colScore + colMark / 2)
    else:
        x = round(screenWidth - colScore - colMark / 2)
    return int(x), int(y)


def addMark(p1, t, remove=False):
    xTarget, yTarget = TargetCenter(p1, t)
    tMark = getPlayerTargetSuccess(p1, t)
    # print(tMark)
    clr = 255 if remove else 0
    # print(clr)
    if tMark == 2:
        pygame.draw.line(screen, (clr, clr, clr), (xTarget - round(colMark / 3), yTarget + round(rowHeight / 3)),
                         (xTarget + round(colMark / 3), yTarget - round(rowHeight / 3)), 3)
    elif tMark == 1:
        pygame.draw.line(screen, (clr, clr, clr), (xTarget - round(colMark / 3), yTarget - round(rowHeight / 3)),
                         (xTarget + round(colMark / 3), yTarget + round(rowHeight / 3)), 3)
    else:
        pygame.draw.circle(screen, (clr, clr, clr), (xTarget, yTarget), int(round(min(colMark, rowHeight) / 2) - 5), 3)


def updateRound(r):
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(colScore + colMark + 1, 0, colTarget - 1, rowTop - 1))
    cround = font.render(str(r), True, (0, 0, 0))
    screen.blit(cround, (
    colScore + colMark + round((colTarget - cround.get_width()) / 2), round((rowTop - cround.get_height()) / 2)))


def updatePlayerMatrix(p1, t, sign=1):
    if p1:
        playerMatrix[0, getTargetIndex(t)] -= 1 * sign
        if playerMatrix[0, getTargetIndex(t)] > 3: playerMatrix[0, getTargetIndex(t)] = 3
    else:
        playerMatrix[1, getTargetIndex(t)] -= 1 * sign
        if playerMatrix[1, getTargetIndex(t)] > 3: playerMatrix[1, getTargetIndex(t)] = 3


def increasePlayerTotal(p1, t, sm):
    sIndex = getTargetIndex(t)
    if p1:
        playerMatrix[0, 10] += [20, 19, 18, 17, 16, 15, 14, 0, 0, 25][sIndex] * sm
        playerMatrix[0, 11] += 1
        addScoreDetail(p1, [20, 19, 18, 17, 16, 15, 14, 0, 0, 25][sIndex] * sm, playerMatrix[0, 11])
    else:
        playerMatrix[1, 10] += [20, 19, 18, 17, 16, 15, 14, 0, 0, 25][sIndex] * sm
        playerMatrix[1, 11] += 1
        addScoreDetail(p1, [20, 19, 18, 17, 16, 15, 14, 0, 0, 25][sIndex] * sm, playerMatrix[1, 11])


def scorePlayerThrow(p1, t, sm):
    xCenter, yDouble = TargetCenter(p1, "D")
    xCenter, yTriple = TargetCenter(p1, "T")
    xCenter = int(round(screenWidth / 2))
    radius = int(round(colMark * .4))

    # if sm > 1:
    #     increasePlayerTotal(p1, t, sm)
    #     global scoreMultiplier # TODO Try to remove this global variable : Return the scoreMultiplier instead!!
    #     scoreMultiplier = 1
    #     pygame.draw.circle(screen, (255, 255, 255), (xCenter, yDouble), radius, 1)
    #     pygame.draw.circle(screen, (255, 255, 255), (xCenter, yTriple), radius, 1)
    #
    # else:
    if getPlayerTargetSuccess(p1, t) > 0:
        updatePlayerMatrix(p1, t)
        addMark(p1, t)
    elif getPlayerTargetSuccess(not p1, t) > 0:
        if t == "D":
            # print("Double Scoring")
            pygame.draw.circle(screen, (0, 0, 0), (xCenter, yDouble), radius, 2)
            # scoreMultiplier = 2
            scoreMultiplierTarget(p1, 2)
            pygame.draw.circle(screen, (255, 255, 255), (xCenter, yDouble), radius, 2)
        elif t == "T":
            # print("Triple Scoring")
            pygame.draw.circle(screen, (0, 0, 0), (xCenter, yTriple), radius, 2)
            scoreMultiplierTarget(p1, 3)
            pygame.draw.circle(screen, (255, 255, 255), (xCenter, yTriple), radius, 2)
            # scoreMultiplier = 3
        else:
            increasePlayerTotal(p1, t, sm)


def updateScoreScreen(p1):
    if p1:
        p1Score = font.render(str(playerMatrix[0, 10]), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, colScore, rowTop))
        screen.blit(p1Score, (round(colScore - p1Score.get_width()) / 2, round((rowTop - p1Score.get_height()) / 2)))
    else:
        p2Score = font.render(str(playerMatrix[1, 10]), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(screenWidth - colScore + 1, 0, colScore, rowTop))
        screen.blit(p2Score, (screenWidth - colScore + round((colScore - p2Score.get_width()) / 2),
                              round((rowTop - p2Score.get_height()) / 2)))


def changePlayer(p1):
    if p1:
        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(screenWidth - colScore - colMark + 1, 0, colMark - 1, rowTop))
        screen.blit(textPlayer1,
                    ((colScore + colMark / 2 - textPlayer1.get_width() / 2),
                     round((rowTop - textPlayer1.get_height()) / 2)))  # Remove y+9 (for testing)
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(colScore + 1, 0, colMark - 1, rowTop))
        screen.blit(textPlayer2, ((screenWidth - colScore - colMark / 2 - textPlayer2.get_width() / 2),
                                  round((rowTop - textPlayer2.get_height()) / 2)))


def checkWinner():
    if playerMatrix[0, 0:10].sum() == 0 and playerMatrix[0, 10] > playerMatrix[1, 10]:
        textP1Wins = fontBig.render("Player 1 WINS!", True, (0, 0, 0))
        screen.blit(textP1Wins, (round(screenWidth - textP1Wins.get_width()) / 2, screenHeight / 2))
    elif playerMatrix[1, 0:10].sum() == 0 and playerMatrix[0, 10] < playerMatrix[1, 10]:
        textP2Wins = fontBig.render("Player 2 WINS!", True, (0, 0, 0))
        screen.blit(textP2Wins, (round(screenWidth - textP2Wins.get_width()) / 2, screenHeight / 2))
    elif playerMatrix[:, 0:10].sum() == 0 and playerMatrix[0, 10] == playerMatrix[1, 10]:
        textDraw = fontBig.render("DRAW!", True, (0, 0, 0))
        screen.blit(textDraw, (round(screenWidth - textDraw.get_width()) / 2, screenHeight / 2))


def scoreMultiplierTarget(p1, sm):
    # TODO: block triple bull
    otherTarget = 1
    done = False
    while not done:
        for event in pygame.event.get():
            # JOYSTICK INPUTS

            #if event.type == pygame.JOYAXISMOTION:
            if check_input(event, LEFT):  #event.axis == 1 and event.value < -JVT:  # LEFT
                otherTarget += 1
            if check_input(event, RIGHT):  #event.axis == 1 and event.value > JVT:  # RIGHT
                otherTarget += 4
            if check_input(event, UP):  #event.axis == 0 and event.value > JVT:  # UP
                otherTarget *= 2
            if check_input(event, DOWN):  #event.axis == 0 and event.value < -JVT:  # DOWN
                updateRound(currentRound)
                if p1:
                    playerMatrix[0, 10] += otherTarget * sm
                    playerMatrix[0, 11] += 1
                    addScoreDetail(p1, otherTarget * sm, playerMatrix[0, 11])
                else:
                    playerMatrix[1, 10] += otherTarget * sm
                    playerMatrix[1, 11] += 1
                    addScoreDetail(p1, otherTarget * sm, playerMatrix[1, 11])
                done = True

            if check_input(event, TWENTY):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(0):
                increasePlayerTotal(p1, "20", sm)
                # print("button 0 pressed")
                done = True
            if check_input(event, NINETEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(9):
                increasePlayerTotal(p1, "19", sm)
                done = True
            if check_input(event, EIGHTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(8):
                increasePlayerTotal(p1, "18", sm)
                done = True
            if check_input(event, SEVENTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(7):
                increasePlayerTotal(p1, "17", sm)
                done = True
            if check_input(event, SIXTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(6):
                increasePlayerTotal(p1, "16", sm)
                done = True
            if check_input(event, FIFTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(5):
                increasePlayerTotal(p1, "15", sm)
                done = True
            if check_input(event, FOURTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(4):
                increasePlayerTotal(p1, "14", sm)
                done = True
            if check_input(event, BULL):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(1):
                increasePlayerTotal(p1, "B", sm)
                done = True

        # print("other Target loop:", otherTarget)
        if otherTarget > 13: otherTarget = 1
        otherTargetText = font.render(str(otherTarget), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(colScore + colMark + 1, 0, colTarget - 1, rowTop - 1))
        screen.blit(otherTargetText, (
        round((screenWidth - otherTargetText.get_width()) / 2), round((rowTop - otherTargetText.get_height()) / 2)))
        pygame.display.flip()
        updateRound(currentRound)  # todo global variable...
        clock.tick(20)


def scoreCorrection(p1):
    otherTarget = -1
    done = False
    while not done:
        for event in pygame.event.get():

            # JOYSTICK INPUTS
            #if event.type == pygame.JOYAXISMOTION:
            if check_input(event, DOWN):  # event.axis == 0 and event.value < -JVT:  # DOWN
                updateRound(currentRound)
                if p1:
                    playerMatrix[0, 10] += otherTarget
                    playerMatrix[0, 11] += 1
                    addScoreDetail(p1, otherTarget, playerMatrix[0, 11])
                else:
                    playerMatrix[1, 10] += otherTarget
                    playerMatrix[1, 11] += 1
                    addScoreDetail(p1, otherTarget, playerMatrix[1, 11])
                done = True
            if check_input(event, LEFT):  # event.axis == 1 and event.value < -JVT:  # LEFT
                otherTarget -= 1
            if check_input(event, RIGHT):  # event.axis == 1 and event.value > JVT:  # RIGHT
                otherTarget -= 4
            if check_input(event, UP):  # event.axis == 0 and event.value > JVT:  # UP
                otherTarget *= 2
            if check_input(event, TWENTY):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(0):
                addMark(p1, "20", True)
                updatePlayerMatrix(p1, "20", -1)
                done = True
            if check_input(event, NINETEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(9):
                addMark(p1, "19", True)
                updatePlayerMatrix(p1, "19", -1)
                done = True
            if check_input(event, EIGHTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(8):
                addMark(p1, "18", True)
                updatePlayerMatrix(p1, "18", -1)
                done = True
            if check_input(event, SEVENTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(7):
                addMark(p1, "17", True)
                updatePlayerMatrix(p1, "17", -1)
                done = True
            if check_input(event, SIXTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(6):
                addMark(p1, "16", True)
                updatePlayerMatrix(p1, "16", -1)
                done = True
            if check_input(event, FIFTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(5):
                addMark(p1, "15", True)
                updatePlayerMatrix(p1, "15", -1)
                done = True
            if check_input(event, FOURTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(4):
                addMark(p1, "14", True)
                updatePlayerMatrix(p1, "14", -1)
                done = True
            if check_input(event, TRIPLE):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(3):
                addMark(p1, "T", True)
                updatePlayerMatrix(p1, "T", -1)
                done = True
            if check_input(event, DOUBLE):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(2):
                addMark(p1, "D", True)
                updatePlayerMatrix(p1, "D", -1)
                done = True
            if check_input(event, BULL):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(1):
                addMark(p1, "B", True)
                updatePlayerMatrix(p1, "B", -1)
                done = True

        # print("other Target loop:", otherTarget)
        otherTargetText = font.render(str(otherTarget), True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(colScore + colMark + 1, 0, colTarget - 1, rowTop - 1))
        screen.blit(otherTargetText, (
        round((screenWidth - otherTargetText.get_width()) / 2), round((rowTop - otherTargetText.get_height()) / 2)))
        # pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 484, 20))
        # playerdata = fontDebug.render(str(playerMatrix), True, (0, 255, 255))
        # screen.blit(playerdata, (2, 0))
        pygame.display.flip()
        updateRound(currentRound)  # todo global variable...
        clock.tick(20)


def addScoreDetail(p1, score, n):
    mark = fontScoreHist.render(str(score), True, (0, 0, 0))
    cc = 3 if n <= 20 else 1  # start with colonne interieure, ensuite exterieure
    if n < 41:
        if p1:
            x = round(cc * colScore / 4 - mark.get_width() / 2)
            # x = round((m.floor(n/21)+1) * colScore/4 - mark.get_width()/2)
            y = rowTop + round(((n - 1) % 20) * rowHeight / 2) + round((rowHeight - mark.get_height()) / 8)
            screen.blit(mark, (x, y))
        else:
            x = round(screenWidth - cc * colScore / 4 - mark.get_width() / 2)
            y = rowTop + round(((n - 1) % 20) * rowHeight / 2) + round((rowHeight - mark.get_height()) / 8)
            screen.blit(mark, (x, y))


def initScoreBoard():
    screen.fill((255, 255, 255))
    # Initialize the joysticks
    # pygame.joystick.init()
    # column Grid
    pygame.draw.line(screen, (0, 0, 0,), (colScore, 0), (colScore, screenHeight), 1)
    pygame.draw.line(screen, (0, 0, 0,), (colScore + colMark, 0), (colScore + colMark, screenHeight), 1)
    pygame.draw.line(screen, (0, 0, 0,), (colScore + colMark + colTarget, 0),
                     (colScore + colMark + colTarget, screenHeight), 1)
    pygame.draw.line(screen, (0, 0, 0,), (colScore + 2 * colMark + colTarget, 0),
                     (colScore + 2 * colMark + colTarget, screenHeight), 1)
    # Row Grid
    for r in range(1, 10):
        pygame.draw.line(screen, (0, 0, 0,), (colScore, rowTop + r * rowHeight),
                         (screenWidth - colScore, rowTop + r * rowHeight), 1)
        # Draw double first line
    pygame.draw.line(screen, (0, 0, 0,), (0, rowTop + 2), (screenWidth, rowTop + 2), 1)
    pygame.draw.line(screen, (0, 0, 0,), (0, rowTop), (screenWidth, rowTop), 1)

    # Target TODO Better center the text with textVar.get_width(), get_heigth() & round()
    screen.blit(textPlayer1, ((colScore + colMark / 2 - textPlayer1.get_width() / 2),
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
    initRound = font.render(str(currentRound), True, (0, 0, 0))
    screen.blit(initRound,
                (round((screenWidth - initRound.get_width()) / 2), round((rowTop - initRound.get_height()) / 2)))
    # pygame.display.flip()
    #pygame.image.save(screen, "./screen.bmp")
    #imageportrait = Image.open('./screen.bmp')
    #imagelandscape = imageportrait.rotate(90, expand=1)
    #epd.display_frame(epd.get_frame_buffer(imagelandscape))


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
    initScoreBoard()
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
            if check_input(event, DOWN):  # event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                player1 = not player1
                changePlayer(player1)
                scoreMultiplier = 1
                if player1:
                    # print("increase round")
                    currentRound = currentRound + 1
                    updateRound(currentRound)

            #     # print("button pressed")
            #     # print(joystick.get_button(0))
            if check_input(event, TWENTY):  # event.type == pygame.JOYBUTTONDOWN and event.button == 0:  # this works; next line also
                # print("button 20 pressed")
                scorePlayerThrow(player1, "20", scoreMultiplier)
            if check_input(event, NINETEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(9):
                scorePlayerThrow(player1, "19", scoreMultiplier)
            if check_input(event, EIGHTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(8):
                scorePlayerThrow(player1, "18", scoreMultiplier)
            if check_input(event, SEVENTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(7):
                scorePlayerThrow(player1, "17", scoreMultiplier)
            if check_input(event, SIXTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(6):
                scorePlayerThrow(player1, "16", scoreMultiplier)
            if check_input(event, FIFTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(5):
                scorePlayerThrow(player1, "15", scoreMultiplier)
            if check_input(event, FOURTEEN):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(4):
                scorePlayerThrow(player1, "14", scoreMultiplier)
            if check_input(event, TRIPLE):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(3):
                scorePlayerThrow(player1, "T", scoreMultiplier)
            if check_input(event, DOUBLE):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(2):
                scorePlayerThrow(player1, "D", scoreMultiplier)
            if check_input(event, BULL):  # event.type == pygame.JOYBUTTONDOWN and joystick.get_button(1):
                scorePlayerThrow(player1, "B", scoreMultiplier)
            if check_input(event, START):  # event.type == pygame.JOYBUTTONDOWN and event.button == 10:
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
                scoreCorrection(player1)

            checkWinner()
            updateScoreScreen(player1)
            pygame.display.flip()

    # ---------------------------------------------
    # logfile.close()

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()