import pygame
import numpy as np
import sm_cricket_sloptactics_param as smp

# -----------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------
JVT = .9  # Joystick Value Threshold

P1 = "p1"
P2 = "p2"
START = "start"
SELECT = "select"
UP = "up"
RIGHT = "right"
DOWN = "down"
LEFT = "Left"
BULL = "25"
BULL_TEXT = "B"
TRIPLE = "3"
TRIPLE_TEXT = "T"
DOUBLE = "2"
DOUBLE_TEXT = "D"
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

# COLORS   (R, G, B) 0-255
CLR_GRID = (0, 0, 0)
CLR_TARGETS = (0, 0, 0)
CLR_SCORES = (100, 100, 100)
CLR_INFO = (100, 100, 100)
CLR_MARKS = (0, 0, 0)
CLR_TACTICS = (50, 255, 50)
CLR_BACKGROUND = (255, 255, 255)
CLR_BOX = (255, 255, 0)
CLR_MESSAGE = (255, 0, 0)
CLR_ROUND = (0, 0, 0)
CLR_PLAYER = (0, 0, 0)
CLR_TOTAL = (0, 0, 0)
CLR_UNDO = (255, 0, 0)

# -----------------------------------------------------------------------------
# VARIABLES
# -----------------------------------------------------------------------------
# size of the e-ink 7.5-inch screen : width:384, height:640
# size for viewsonic : width:576, height:960
# size for 7inch hdmi lcd (b) - WaveShare w480 h800 (portrait orientation)
# -----------------------------------------------------------------------------
screen_width = smp.screenWidth
screen_height = smp.screenHeight
fullscreen = smp.fullscreen

# DYNAMIC SCORE SHEET CALCULATION ---------------------------------------------
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
double_pos_circle = (round(screen_width / 2), row_top + 7 * row_height + round(row_height / 2))
triple_pos = (round(screen_width / 2), row_top + 8 * row_height + round(row_height / 2) + grid_offset)
triple_pos_circle = (round(screen_width / 2), row_top + 8 * row_height + round(row_height / 2))
bull_pos = (round(screen_width / 2), row_top + 9 * row_height + round(row_height / 2) + grid_offset)

result_pos = (round(screen_width / 2), round(screen_height / 2))
result_pos_info = (round(screen_width / 2), round(screen_height / 80 * 43))  # todo more robust position...
result_rect = (0, round(screen_height / 20 * 9), screen_width, round(screen_height / 10))

# FULLSCREEN MODE FOR RASPBERRY PI --------------------------------------------
# NOTE: always fullscreen mode on raspberry pi when launch from command line (?)
if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # For screen on Raspberry Pi
else:
    screen = pygame.display.set_mode((screen_width, screen_height))

# PLAYER DATA AND GAME LOGIC --------------------------------------------------
current_player = 0  # 0 for player 1, 1 for player 2 - i.e. the players_array row
sitting_player = 1
scoreMultiplier = 1
currentRound = 1
other_target = 1

# 20-14, D, T, B, total score, score count
INITARRAY = np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0]])  # for restart test
players_array = np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0]])
player_one_scores = np.empty(0)  # for individual scores
player_two_scores = np.empty(0)

done = False
game_on = True

# -----------------------------------------------------------------------------
# PYGAME INITS
# -----------------------------------------------------------------------------
pygame.init()
#  TODO add too the parameter file the font variables
pygame.display.set_caption("SLOP TACTICS CRICKET")
font = pygame.font.Font("HyningsHandwriting-Regular.ttf", 72)  # about screenHeight/20 - grid text
fontBig = pygame.font.Font("HyningsHandwriting-Regular.ttf", 72)  # about screenHeight/15 - final result text
fontScoreHist = pygame.font.Font("HyningsHandwriting-Regular.ttf", 40)  # about screenHeight/40 - score history
fontInfo = pygame.font.SysFont("HyningsHandwriting-Regular.ttf", 24)  # about screenHeight/80

clock = pygame.time.Clock()
# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------


def text_blit(text, tb_font, clr, center):
    text_render = tb_font.render(text, True, clr)
    return text_render, text_render.get_rect(center=center)


def get_target_index(gti):
    target_order = ["20", "19", "18", "17", "16", "15", "14", "2", "3", "25"]
    return target_order.index(gti)


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


def init_score_board():
    screen.fill(CLR_BACKGROUND)
    # column Grid
    pygame.draw.line(screen, CLR_GRID, (col_score, 0), (col_score, screen_height), 1)
    pygame.draw.line(screen, CLR_GRID, (col_score + col_mark, 0), (col_score + col_mark, screen_height), 1)
    pygame.draw.line(screen, CLR_GRID, (col_score + col_mark + col_target, 0),
                     (col_score + col_mark + col_target, screen_height), 1)
    pygame.draw.line(screen, CLR_GRID, (col_score + 2 * col_mark + col_target, 0),
                     (col_score + 2 * col_mark + col_target, screen_height), 1)
    # Row Grid
    for r in range(1, 10):
        pygame.draw.line(screen, CLR_GRID, (col_score, row_top + r * row_height),
                         (screen_width - col_score, row_top + r * row_height), 1)
        # Draw double first line
    pygame.draw.line(screen, CLR_GRID, (0, row_top + 2), (screen_width, row_top + 2), 1)
    pygame.draw.line(screen, CLR_GRID, (0, row_top), (screen_width, row_top), 1)

    # Targets
    screen.blit(*text_blit(TWENTY, font, CLR_TARGETS, twenty_pos))
    screen.blit(*text_blit(NINETEEN, font, CLR_TARGETS, nineteen_pos))
    screen.blit(*text_blit(EIGHTEEN, font, CLR_TARGETS, eighteen_pos))
    screen.blit(*text_blit(SEVENTEEN, font, CLR_TARGETS, seventeen_pos))
    screen.blit(*text_blit(SIXTEEN, font, CLR_TARGETS, sixteen_pos))
    screen.blit(*text_blit(FIFTEEN, font, CLR_TARGETS, fifteen_pos))
    screen.blit(*text_blit(FOURTEEN, font, CLR_TARGETS, fourteen_pos))
    screen.blit(*text_blit(DOUBLE_TEXT, font, CLR_TARGETS, double_pos))
    screen.blit(*text_blit(TRIPLE_TEXT, font, CLR_TARGETS, triple_pos))
    screen.blit(*text_blit(BULL_TEXT, font, CLR_TARGETS, bull_pos))


def confirm_restart():
    pygame.draw.rect(screen, CLR_BOX, result_rect)
    screen.blit(*text_blit("Confirm restart", fontBig, CLR_MESSAGE, result_pos))
    screen.blit(*text_blit("START to confirm, SELECT to cancel", fontInfo, CLR_INFO, result_pos_info))
    pygame.display.flip()
    restart = True
    while restart:  # stay in loop as long as a MENU button is pressed
        for rs_event in pygame.event.get():
            rs_valid_input, rs_input_value, rs_input_type = validate_input(rs_event)
            if rs_valid_input and rs_input_value == START:
                return True  # return exits loop
            if rs_valid_input and rs_input_value == SELECT:
                return False


# -----------------------------------------------------------------------------
# MAIN GAME LOOP
# -----------------------------------------------------------------------------


while game_on:
    clock.tick(20)
    print("Game On!")
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                game_on = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                done = True
                game_on = False

            valid_input, input_value, input_type = validate_input(event)
            # -----------------------------------------------------------------
            # NUMBER SCORING
            # -----------------------------------------------------------------
            if valid_input and input_type == NUMBER:
                if scoreMultiplier == 1:
                    if players_array[current_player, get_target_index(input_value)] > 0:  # if not closed
                        players_array[current_player, get_target_index(input_value)] -= 1
                    elif players_array[sitting_player, get_target_index(input_value)] > 0:  # if opponent not closed
                        players_array[current_player, 10] += int(input_value)
                        players_array[current_player, 11] += 1
                        if current_player == 0:
                            player_one_scores = np.append(player_one_scores, int(input_value))
                        else:
                            player_two_scores = np.append(player_two_scores, int(input_value))
                elif scoreMultiplier == -1:
                    if players_array[current_player, get_target_index(input_value)] < 3:  # if the player has scored
                        players_array[current_player, get_target_index(input_value)] += 1
                        scoreMultiplier = 1
                else:
                    if input_value != BULL or scoreMultiplier != 3:  # ignore triple-bull scoring
                        players_array[current_player, 10] += int(input_value) * scoreMultiplier
                        if current_player == 0:
                            player_one_scores = np.append(player_one_scores, int(input_value) * scoreMultiplier)
                        else:
                            player_two_scores = np.append(player_two_scores, int(input_value) * scoreMultiplier)
                        scoreMultiplier = 1
            # -----------------------------------------------------------------
            # TACTICAL SCORING
            # -----------------------------------------------------------------
            if valid_input and input_type == TACTICAL:
                other_target = 1
                if scoreMultiplier == 1:
                    if players_array[current_player, get_target_index(input_value)] > 0:  # if not closed
                        players_array[current_player, get_target_index(input_value)] -= 1
                    elif players_array[sitting_player, get_target_index(input_value)] > 0:  # if opponent not closed
                        scoreMultiplier = int(input_value)
                elif scoreMultiplier == -1:
                    if players_array[current_player, get_target_index(input_value)] < 3:  # if the player has scored
                        players_array[current_player, get_target_index(input_value)] += 1
                        scoreMultiplier = 1
            # -----------------------------------------------------------------
            # JOYSTICK LOGIC
            # -----------------------------------------------------------------
            if valid_input and input_type == JOYSTICK:
                if scoreMultiplier == 1 and input_value == DOWN:
                    if current_player == 0:
                        current_player = 1
                        sitting_player = 0
                    else:
                        current_player = 0
                        sitting_player = 1
                        currentRound += 1
                    scoreMultiplier = 1
                else:
                    if input_value == LEFT:
                        other_target += 1
                    if input_value == RIGHT:
                        other_target += 4
                    if input_value == UP:
                        other_target *= 2
                    if other_target > 13 and scoreMultiplier != -1:
                        other_target = 1
                    if input_value == DOWN:
                        players_array[current_player, 10] += other_target * scoreMultiplier
                        players_array[current_player, 11] += 1
                        if current_player == 0:
                            player_one_scores = np.append(player_one_scores, int(other_target * scoreMultiplier))
                        else:
                            player_two_scores = np.append(player_two_scores, int(other_target * scoreMultiplier))
                        scoreMultiplier = 1
            # -----------------------------------------------------------------
            # MENU LOGIC
            # -----------------------------------------------------------------
            if valid_input and input_type == MENU and input_value == START:
                if scoreMultiplier != 1:  # exit from special scoring modes
                    scoreMultiplier = 1
                elif confirm_restart():
                    # reset variable (python references variables...)
                    players_array = np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
                                              [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0]])
                    player_one_scores = np.empty(0)
                    player_two_scores = np.empty(0)
                    current_player = 0
                    sitting_player = 1
                    currentRound = 1
                    scoreMultiplier = 1

            if valid_input and input_type == MENU and input_value == SELECT:
                # todo if at beginning of game; exit program - test purposes only
                comparison = players_array == INITARRAY  # arrays cannot be compared directly with ==
                equal_arrays = comparison.all()
                if equal_arrays:
                    done = True
                    game_on = False
                else:
                    other_target = 1
                    scoreMultiplier = -1

            # -----------------------------------------------------------------
            # DEBUGGING
            # -----------------------------------------------------------------
            # if valid_input:
            #     print("validate:", valid_input, input_value, input_type)
            #     # print(event)
            #     print(players_array)
            #     print(player_one_scores, player_two_scores)
            #     print("player:", current_player, sitting_player)
            #     print("multiplier:", scoreMultiplier)
            #     print("other target:", other_target)
            # -----------------------------------------------------------------
            # BUILD AND REFRESH DISPLAY
            # -----------------------------------------------------------------
            init_score_board()
            # TOP ROW ---------------------------------------------------------
            if scoreMultiplier == 1:
                screen.blit(*text_blit("round", fontInfo, CLR_INFO, round_txt_pos))
                screen.blit(*text_blit(str(currentRound), font, CLR_ROUND, round_pos))
            if scoreMultiplier == 2:
                screen.blit(*text_blit("doubling", fontInfo, CLR_INFO, round_txt_pos))
                screen.blit(*text_blit(str(other_target), font, CLR_TACTICS, round_pos))
                pygame.draw.circle(screen, CLR_TACTICS, double_pos_circle, int(round(row_height / 2)), 5)
            if scoreMultiplier == 3:
                screen.blit(*text_blit("tripling", fontInfo, CLR_INFO, round_txt_pos))
                screen.blit(*text_blit(str(other_target), font, CLR_TACTICS, round_pos))
                pygame.draw.circle(screen, CLR_TACTICS, triple_pos_circle, int(round(row_height / 2)), 5)
            if scoreMultiplier == -1:
                screen.blit(*text_blit("oh no!", fontInfo, CLR_INFO, round_txt_pos))
                screen.blit(*text_blit(str(other_target * scoreMultiplier), font, CLR_UNDO, round_pos))
            screen.blit(*text_blit(str(players_array[0, 10]), font, CLR_TOTAL, p1_score_pos))  # total score
            screen.blit(*text_blit(str(players_array[1, 10]), font, CLR_TOTAL, p2_score_pos))  # total score
            if current_player == 0:
                screen.blit(*text_blit(P1, font, CLR_PLAYER, p1_pos))
            if current_player == 1:
                screen.blit(*text_blit(P2, font, CLR_PLAYER, p2_pos))
            # ADD TARGET MARKS ------------------------------------------------
            for t in range(10):
                for p in range(2):
                    y_target = int(row_top - row_height + round((t + 1.5) * row_height))
                    x_target = int(round(p * screen_width + (1 - 2 * p) * col_score + (1 - 2 * p) * col_mark / 2))
                    if players_array[p, t] < 3:
                        pygame.draw.line(screen, CLR_MARKS,
                                         (x_target - round(col_mark / 3), y_target + round(row_height / 3)),
                                         (x_target + round(col_mark / 3), y_target - round(row_height / 3)), 8)
                    if players_array[p, t] < 2:
                        pygame.draw.line(screen, CLR_MARKS,
                                         (x_target - round(col_mark / 3), y_target - round(row_height / 3)),
                                         (x_target + round(col_mark / 3), y_target + round(row_height / 3)), 8)
                    if players_array[p, t] < 1:
                        pygame.draw.circle(screen, CLR_MARKS, (x_target, y_target),
                                           int(round(min(col_mark, row_height) / 2) - 5), 6)
            # ADD INDIVIDUAL SCORES -------------------------------------------
            for idx, s in enumerate(player_one_scores):
                cc = 3 if idx < 20 else 1
                p_one_x = round(cc * col_score / 4)
                p_one_y = row_top + round((idx % 20 + 1) * row_height / 2 - row_height / 5)
                screen.blit(*text_blit(str(int(s)), fontScoreHist, CLR_SCORES, (p_one_x, p_one_y)))
            for idx, s in enumerate(player_two_scores):
                cc = 3 if idx < 20 else 1
                p_two_x = round(screen_width - cc * col_score / 4)
                p_two_y = row_top + round((idx % 20 + 1) * row_height / 2 - row_height / 5)
                screen.blit(*text_blit(str(int(s)), fontScoreHist, CLR_SCORES, (p_two_x, p_two_y)))
            # CHECK WINNER ----------------------------------------------------
            if players_array[0, 0:10].sum() == 0 and players_array[0, 10] > players_array[1, 10]:
                pygame.draw.rect(screen, CLR_BOX, result_rect)
                screen.blit(*text_blit("Player 1 WINS!", fontBig, CLR_MESSAGE, result_pos))
            elif players_array[1, 0:10].sum() == 0 and players_array[0, 10] < players_array[1, 10]:
                pygame.draw.rect(screen, CLR_BOX, result_rect)
                screen.blit(*text_blit("Player 2 WINS!", fontBig, CLR_MESSAGE, result_pos))
            elif players_array[:, 0:10].sum() == 0 and players_array[0, 10] == players_array[1, 10]:
                pygame.draw.rect(screen, CLR_BOX, result_rect)
                screen.blit(*text_blit("DRAW!", fontBig, CLR_MESSAGE, result_pos))
            # REFRESH ---------------------------------------------------------
            pygame.display.flip()
pygame.quit()
