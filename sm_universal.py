import pygame as pg
from datetime import timedelta


# -----------------------------------------------------------
# CONSTANTES
# -----------------------------------------------------------
K1 = "kun"  # Bouton joueur 1
K2 = "kdeux"  # Bouton joueur 2
K3 = "ktrois"  # Bouton pause
B_DOWN = "down"
B_UP = "UP"
TIME = "time"

# COULEURS   (R, G, B) 0-255
CLR_BACKGROUND = (0, 0, 0)
CLR_TEXTE = (255, 255, 255)
CLR_INFO = (100, 100, 100)
CLR_MESSAGE = (10, 10, 10)
CLR_BOITE = (60, 60, 60)
CLR_LIGNE = (100, 100, 255)

# -----------------------------------------------------------------------------
# VARIABLES
# -----------------------------------------------------------------------------
e_larg = 800
e_haut = 480
full_screen = False
# police = "ParadroidMono-Light.ttf"
police = "whitrabt.ttf"

# DYNAMIC SCORE SHEET CALCULATION ---------------------------------------------
pos_centre_v = round(e_haut / 2)
pos_centre_h = round(e_larg / 2)
pos_p1 = (round(e_larg / 4), round(e_haut / 2))
pos_p2 = (round(e_larg / 4 * 3), round(e_haut / 2))
pos_message = round(e_haut / 40 * 39)
rect_depart = (round(e_larg / 8), round(e_haut / 8), round(e_larg / 8 * 6), round(e_haut / 8 * 6))
pos_dep_ttr = (round(e_larg / 2), round(e_haut / 8 * 3))
pos_dep_sttr = (round(e_larg / 2), round(e_haut / 8 * 5))
pos_chrono_p1 = (round(e_larg / 3), round(e_haut / 4))
pos_chrono_p2 = (round(e_larg / 3 * 2), round(e_haut / 4 * 3))

# FULLSCREEN MODE FOR RASPBERRY PI --------------------------------------------
# NOTE: always full screen mode on raspberry pi when launch from command line (?)
if full_screen:
    ecran = pg.display.set_mode((0, 0), pg.FULLSCREEN)  # For screen on Raspberry Pi
else:
    ecran = pg.display.set_mode((e_larg, e_haut))

# GAMES DATA AND GAME LOGIC --------------------------------------------------
#
mode_pointage = True
point_p1 = 0
point_p2 = 0
duree_p1 = 0
duree_p2 = 0
j_actif = 1

# -----------------------------------------------------------------------------
# PYGAME INITS
# -----------------------------------------------------------------------------
pg.init()
#  TODO add too the parameter file the font variables
#  sysFont is very slow
pg.display.set_caption("Universal Scoring Machine")
police_point = pg.font.Font(police, 280)  # about screenHeight/20 - grid text
police_chrono = pg.font.Font(police, 120)  # about screenHeight/15 - final result text
police_titre = pg.font.Font(police, 60)  # about screenHeight/40 - score history
police_soustitre = pg.font.Font(police, 42)  # about screenHeight/80
police_info = pg.font.Font(police, 16)  # about
clock = pg.time.Clock()
pg.time.set_timer(pg.USEREVENT, 1000)  # evenement a chaque seconde
# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------


def text_blit(text, tb_font, clr, center):
    text_render = tb_font.render(text, True, clr)
    return text_render, text_render.get_rect(center=center)


def validate_input(ci_event):
    if ci_event.type == pg.KEYUP:
        if ci_event.key == pg.K_UP:
            return True, K1, B_UP
        if ci_event.key == pg.K_RIGHT:
            return True, K2, B_UP
        if ci_event.key == pg.K_DOWN:
            return True, K3, B_UP
    if ci_event.type == pg.JOYBUTTONDOWN:  # USING A GENERIC USB JOYSTICK
        if ci_event.button == 0:  # K1
            return True, K1, B_DOWN
        if ci_event.button == 1:  # K2
            return True, K2, B_DOWN
        if ci_event.button == 2:  # K3
            return True, K3, B_DOWN
    if ci_event.type == pg.USEREVENT:
        return True, TIME, TIME
    return False, "none", "na"


def confirm_restart():
    pg.draw.rect(ecran, CLR_BOITE, rect_depart)
    ecran.blit(*text_blit("Confirm restart", police_titre, CLR_MESSAGE, pos_dep_ttr))
    ecran.blit(*text_blit("P1 for goals, P2 for time, PAUSE to cancel", police_info, CLR_INFO, pos_dep_sttr))
    pg.display.flip()
    restart = True
    while restart:  # stay in loop as long as a MENU button is pressed
        for rs_event in pg.event.get():
            rs_valid_input, rs_input_value, rs_input_type = validate_input(rs_event)
            if rs_valid_input and rs_input_value == K1:
                return True, True
            if rs_valid_input and rs_input_value == K2:
                return True, False
            if rs_valid_input and rs_input_value == K3:
                return False, True  # la valeur True sera ignorée ici


# -----------------------------------------------------------------------------
# MAIN GAME LOOP
# -----------------------------------------------------------------------------
clock.tick(1)
print("Game On!")
pg.joystick.init()
joystick = pg.joystick.Joystick(0)
joystick.init()
pg.event.set_blocked([pg.MOUSEMOTION, pg.ACTIVEEVENT])
# pg.mouse.set_visible(0)
main_loop = True
while main_loop:
    for e in pg.event.get():
        valid_input, input_value, input_type = validate_input(e)
        if e.type == pg.QUIT:
            main_loop = False
        if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
            main_loop = False

        # LOGIQUE POUR POINTAGE -------------------------------------------
        if valid_input:
            if mode_pointage:
                if input_value == K1:
                    point_p1 += 1
                if input_value == K2:
                    point_p2 += 1
                if input_value == K3:
                    n_p, mode = confirm_restart()
                    if n_p:
                        if mode:
                            mode_pointage = True
                            point_p1 = 0
                            point_p2 = 0
                            duree_p1 = 0
                            duree_p2 = 0
                            j_actif = 1
                        else:
                            mode_pointage = False
                            point_p1 = 0
                            point_p2 = 0
                            duree_p1 = 0
                            duree_p2 = 0
                            j_actif = 1

        # LOGIQUE POUR MINUTERIE ------------------------------------------
            else:
                if input_value == K1:
                    j_actif = 2
                if input_value == K2:
                    j_actif = 1
                if e.type == pg.USEREVENT:
                    if j_actif == 1:
                        duree_p1 += 1
                    else:
                        duree_p2 += 1
                if input_value == K3:
                    n_p, mode = confirm_restart()
                    if n_p:
                        if mode:
                            mode_pointage = True
                            point_p1 = 0
                            point_p2 = 0
                            duree_p1 = 0
                            duree_p2 = 0
                            j_actif = 1
                        else:
                            mode_pointage = False
                            point_p1 = 0
                            point_p2 = 0
                            duree_p1 = 0
                            duree_p2 = 0
                            j_actif = 1

        # -----------------------------------------------------------------
        # DEBUGGING
        # -----------------------------------------------------------------
        # print(tm.time(), e)
        print("event:", e)

    # -------------------------------------------------------------------------
    # BUILD DISPLAY -----------------------------------------------------------
    # -------------------------------------------------------------------------
    ecran.fill(CLR_BACKGROUND)
    # PAGE POINTAGE -----------------------------------------------------------
    if mode_pointage:
        pg.draw.line(ecran, CLR_LIGNE, (round(e_larg / 2), 0), (round(e_larg / 2), e_haut), 4)
        ecran.blit(*text_blit(str(point_p1), police_point, CLR_TEXTE, pos_p1))
        ecran.blit(*text_blit(str(point_p2), police_point, CLR_TEXTE, pos_p2))
    else:
        pg.draw.line(ecran, CLR_LIGNE, (0, e_haut), (e_larg, 0), 4)
        ecran.blit(*text_blit(str(timedelta(seconds=duree_p1)),
                              police_chrono, CLR_TEXTE, pos_chrono_p1))
        ecran.blit(*text_blit(str(timedelta(seconds=duree_p2)),
                              police_chrono, CLR_TEXTE, pos_chrono_p2))
    pg.display.flip()

pg.quit()
