import pygame as pg
import time as tm
import numpy as np
import pandas as pd
# import os.path
from os import path
# from str import join
# import sm_goat_param as sgp

# -----------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------
START = "start"
SELECT = "select"
UP = "up"
RIGHT = "right"
DOWN = "down"
LEFT = "left"
KEYUP = "keyup"
KEYDOWN = "keydown"
BUTTONDOWN = "buttondown"
BUTTONUP = "buttonup"
MOVE = "move"

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ",
           "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]
POINT_TYPES = ["HIGH SCORE", "LOW SCORE", "FASTEST", "CHAMPION"]

# COLORS   (R, G, B) 0-255
CLR_BACKGROUND = (0, 0, 0)
CLR_TITLE = (255, 255, 255)
CLR_POS = (255, 0, 0)
CLR_NOM = (0, 0, 255)
CLR_SELECTION = (100, 100, 255)
CLR_ENTETE = (100, 255, 100)
CLR_MODIF = (255, 140, 0)
CLR_CARRE = (50, 50, 50)

# -----------------------------------------------------------------------------
# VARIABLES
# -----------------------------------------------------------------------------
# size of the e-ink 7.5-inch screen : width:384, height:640
# size for viewsonic : width:576, height:960
# size for 7inch hdmi lcd (b) - WaveShare w480 h800 (portrait orientation)
# -----------------------------------------------------------------------------
screen_width = 480
screen_height = 800
full_screen = False
# police = "ParadroidMono-Light.ttf"
police = "whitrabt.ttf"

# DYNAMIC SCORE SHEET CALCULATION ---------------------------------------------
espace_vert = round(screen_height / 12)
jeu_hor = round(screen_width / 16 * 7)
pos_joueur = round(screen_width / 16 * 14)
pos_res = round(screen_width / 16 * 7)
pos_rang = round(screen_width / 16)
pos_entete_h = round(screen_width / 2)
pos_entete_v = round(screen_height / 24)
pos_soustitre_v = round(screen_height / 12)
# joueur_nom = round(screen_width / 16 * 11)

result_pos = (round(screen_width / 2), round(screen_height / 2))
result_pos_info = (round(screen_width / 2), round(screen_height / 80 * 43))  # todo more robust position...
result_rect = (0, round(screen_height / 20 * 9), screen_width, round(screen_height / 10))

# FULLSCREEN MODE FOR RASPBERRY PI --------------------------------------------
# NOTE: always full screen mode on raspberry pi when launch from command line (?)
if full_screen:
    ecran = pg.display.set_mode((0, 0), pg.FULLSCREEN)  # For screen on Raspberry Pi
else:
    ecran = pg.display.set_mode((screen_width, screen_height))

# GAMES DATA AND GAME LOGIC --------------------------------------------------
# comme première version, nous allons restreindre à 10 jeux et à 10 pointages
# par jeu.
page_index = 0  # 0: page de jeux, 1-10: pages de pointage
rangee_index = 0  # position de la rangée
col_index = 0  # position de la colonne

mode_bouge = True  # deplacement vs entree de characteres
srlgn_idx = 0  # 0:aucun, 1:titre, 2:soustitre, 3-12:positions
mot = ()
lettre_index = 0
mode_ecriture = False

if path.exists("sm_goat_data.csv"):
    jeux_df = pd.read_csv(r'sm_goat_data.csv', dtype=str).fillna('')
else:  # todo demo data for dev. - empty dataframe for prod
    jeux = {'Name': ["PACMAN", "DONKEYKONG", "ROBOTRON", "NEW GAME", "NEW GAME",
                     "NEW GAME", "NEW GAME", "NEW GAME", "NEW GAME", "NEW GAME"],
            'ScoreType': ["HIGH SCORE", "LOW SCORE", "FASTEST", "HIGH SCORE", "HIGH SCORE",
                          "HIGH SCORE", "HIGH SCORE", "HIGH SCORE", "HIGH SCORE", "CHAMPION"],
            'Pos0nom': ["ABC", "VCB", "DGF", "ABC", "VCB", "DGF", "ABC", "VCB", "DGF", "AAA"],
            "Pos0res": ["200", "188", "178", "0", "4", "11", "1m30s", "2m", "2m10s", "2020/06/26"],
            "Pos1res": np.repeat(["123"], 10),
            "Pos1nom": np.repeat(["AAA"], 10),
            "Pos2res": np.repeat(["1234"], 10),
            "Pos2nom": np.repeat(["AAA"], 10),
            "Pos3res": np.repeat(["12345"], 10),
            "Pos3nom": np.repeat(["AAA"], 10),
            "Pos4res": np.repeat(["123456"], 10),
            "Pos4nom": np.repeat(["AAA"], 10),
            "Pos5res": np.repeat(["1234567"], 10),
            "Pos5nom": np.repeat(["AAA"], 10),
            "Pos6res": np.repeat(["12345678"], 10),
            "Pos6nom": np.repeat(["AAA"], 10),
            "Pos7res": np.repeat(["012345678"], 10),
            "Pos7nom": np.repeat(["AAA"], 10),
            "Pos8res": np.repeat([""], 10),
            "Pos8nom": np.repeat([""], 10),
            "Pos9res": np.repeat([""], 10),
            "Pos9nom": np.repeat([""], 10)
            }
    jeux_df = pd.DataFrame(jeux, columns=['Name', 'ScoreType',
                                          "Pos0res", "Pos0nom", "Pos1res", "Pos1nom",
                                          "Pos2res", "Pos2nom", "Pos3res", "Pos3nom",
                                          "Pos4res", "Pos4nom", "Pos5res", "Pos5nom",
                                          "Pos6res", "Pos6nom", "Pos7res", "Pos7nom",
                                          "Pos8res", "Pos8nom", "Pos9res", "Pos9nom"])

print(jeux_df)

# for index, row in jeux_df.iterrows():
#     print(row['Name'] + ".csv")
#     if path.exists(str(row['Name']) + ".csv"):
#         jeux_df = pd.read_csv(r'game_list.csv')
#     else:  # todo demo data for dev. - empty dataframe for prod
#         jeux = {'Name': ["PACMAN", "DONKEYKONG", "ROBOTRON"],
#                 'ScoreType': ["High Score", "Low Score", "Fastest"]
#                 }
#         jeux_df = pd.DataFrame(jeux, columns=['Name', 'ScoreType'])
# -----------------------------------------------------------------------------
# PYGAME INITS
# -----------------------------------------------------------------------------
pg.init()
#  TODO add too the parameter file the font variables
#  sysFont is very slow
pg.display.set_caption("G.O.A.T.")
police_texte = pg.font.Font(police, 48)  # about screenHeight/20 - grid text
police_pos = pg.font.Font(police, 36)  # about screenHeight/15 - final result text
police_entete = pg.font.Font(police, 60)  # about screenHeight/40 - score history
police_soustitre = pg.font.Font(police, 24)  # about screenHeight/80
police_info = pg.font.Font(police, 16)  # about
clock = pg.time.Clock()
# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------


def text_blit(text, tb_font, clr, center):
    text_render = tb_font.render(text, True, clr)
    return text_render, text_render.get_rect(center=center)


def validate_input(ci_event):
    if ci_event.type == pg.KEYUP:
        if ci_event.key == pg.K_RETURN:
            return True, SELECT, KEYUP
        if ci_event.key == pg.K_UP:
            return True, UP, KEYUP
        if ci_event.key == pg.K_RIGHT:
            return True, RIGHT, KEYUP
        if ci_event.key == pg.K_DOWN:
            return True, DOWN, MOVE
        if ci_event.key == pg.K_LEFT:
            return True, LEFT, KEYUP
    if ci_event.type == pg.JOYBUTTONDOWN:  # USING A GENERIC USB JOYSTICK
        if ci_event.button == 0:  # K1
            return True, UP, MOVE
        if ci_event.button == 1:  # K2
            return True, RIGHT, MOVE
        if ci_event.button == 2:  # K3
            return True, DOWN, MOVE
        if ci_event.button == 3:  # K4
            return True, LEFT, MOVE
        if ci_event.button == 9:  # SE
            return True, SELECT, BUTTONDOWN
        if ci_event.button == 10:  # ST
            return True, START, BUTTONDOWN
    return False, "none", "na"


# -----------------------------------------------------------------------------
# MAIN GAME LOOP
# -----------------------------------------------------------------------------
# TODO keep scrolling through letters while holding joystick up/down
clock.tick(1)
print("Game On!")
pg.joystick.init()
joystick = pg.joystick.Joystick(0)
joystick.init()
pg.event.set_blocked([pg.MOUSEMOTION, pg.ACTIVEEVENT])
# pg.mouse.set_visible(0)
scroll_on = False
main_loop = True
while main_loop:
    for e in pg.event.get():
        valid_input, input_value, input_type = validate_input(e)
        if e.type == pg.QUIT:
            main_loop = False
        if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
            main_loop = False
        # if e.type == pg.JOYBUTTONDOWN or e.type == pg.JOYBUTTONUP:
        #     print("in time loop")
        #     if e.button == 9 and e.type == pg.JOYBUTTONDOWN:  # ST
        #         dt = tm.time()  # Getting time in sec
        #         scroll_on = True
        #         cnt = 1
        #     if e.button == 9 and e.type == pg.JOYBUTTONUP:  #
        #         ut = tm.time()
        #         print("Pressed Key", e.button, "for", str(ut - dt))
        #         scroll_on = False
        # PAGE DES JEUX  ------------------------------------------------------
        if valid_input:
            if page_index == 0 and mode_bouge:
                if input_type == MOVE:
                    if input_value == DOWN:
                        rangee_index += 1
                        if rangee_index > 9:
                            rangee_index = 0
                    if input_value == UP:
                        rangee_index -= 1
                        if rangee_index < 0:
                            rangee_index = 9
                if input_type == MOVE:
                    if input_value == RIGHT:
                        page_index = rangee_index + 1
            # PAGES DES TABLEAUX DES MENEURS  -------------------------------------
            elif page_index > 0:
                if mode_bouge:
                    if input_type == MOVE:
                        if input_value == RIGHT:
                            page_index += 1
                            if page_index > 9:
                                page_index = 1
                        if input_value == LEFT:
                            page_index -= 1
                            if page_index < 1:
                                page_index = 9
                        if input_value == UP or input_value == DOWN:
                            page_index = 0
                    if input_value == SELECT:
                        mode_bouge = False
                        srlgn_idx = 1
                elif not mode_bouge and not mode_ecriture:  # en mode entrée de characteres
                    if input_value == SELECT:
                        mode_bouge = True
                        srlgn_idx = 0
                        # SAVE DATA to csv
                        jeux_df.to_csv("sm_goat_data.csv", index=False)
                    if input_value == DOWN:
                        srlgn_idx += 1
                        if srlgn_idx > 12:
                            srlgn_idx = 1
                    if input_value == UP:
                        srlgn_idx -= 1
                        if srlgn_idx < 1:
                            srlgn_idx = 12
                    if input_value == LEFT or input_value == RIGHT:
                        if srlgn_idx == 1:
                            mot = list(jeux_df.iloc[page_index - 1, srlgn_idx - 1].ljust(10, ' '))
                            jeux_df.iloc[page_index - 1, srlgn_idx - 1] = "".join(mot)
                            mode_ecriture = True
                            lettre_index = 0
                        elif srlgn_idx == 2:  # change directement le type de pointage
                            if input_value == LEFT:
                                type_index_suiv = POINT_TYPES.index(jeux_df.iloc[page_index - 1, srlgn_idx - 1]) - 1
                                if type_index_suiv < 0:
                                    type_index_suiv = len(POINT_TYPES) - 1
                                # mot[lettre_index] = LETTERS[type_index_suiv]
                                jeux_df.iloc[page_index - 1, srlgn_idx - 1] = POINT_TYPES[type_index_suiv]
                            if input_value == RIGHT:
                                type_index_suiv = POINT_TYPES.index(jeux_df.iloc[page_index - 1, srlgn_idx - 1]) + 1
                                if type_index_suiv > len(POINT_TYPES) - 1:
                                    type_index_suiv = 0
                                # mot[lettre_index] = LETTERS[type_index_suiv]
                                jeux_df.iloc[page_index - 1, srlgn_idx - 1] = POINT_TYPES[type_index_suiv]
                        else:
                            if input_value == LEFT:  # UPDATE
                                mot = list(jeux_df.iloc[page_index - 1, 2*(srlgn_idx - 2)].ljust(10, ' ') + " " +
                                           jeux_df.iloc[page_index - 1, 2 * (srlgn_idx - 2) + 1].ljust(3, ' '))
                                jeux_df.iloc[page_index - 1, 2*(srlgn_idx - 2)] = "".join(mot[0:10])
                                jeux_df.iloc[page_index - 1, 2 * (srlgn_idx - 2) + 1] = "".join(mot[11:])
                                mode_ecriture = True
                                lettre_index = 0
                            if input_value == RIGHT:  # INSERT
                                for r in range(9, srlgn_idx - 3, -1):
                                    print("insert loop:", r)
                                    jeux_df.iloc[page_index - 1, 2 * r + 3] = \
                                        jeux_df.iloc[page_index - 1, 2 * r + 1]
                                    jeux_df.iloc[page_index - 1, 2 * r + 2] = \
                                        jeux_df.iloc[page_index - 1, 2 * r + 0]
                                mot = [" "] * 14
                                jeux_df.iloc[page_index - 1, 2*(srlgn_idx - 2)] = "".join(mot[0:10])
                                jeux_df.iloc[page_index - 1, 2 * (srlgn_idx - 2) + 1] = "".join(mot[11:])
                                mode_ecriture = True
                                lettre_index = 0
                elif mode_ecriture:  # mode ecriture
                    if srlgn_idx == 1:
                        if input_value == RIGHT:
                            lettre_index += 1
                            if lettre_index > 9:
                                lettre_index = 0
                        if input_value == LEFT:
                            lettre_index -= 1
                            if lettre_index < 0:
                                lettre_index = 9
                        if input_value == DOWN:
                            lettre_index_suiv = LETTERS.index(mot[lettre_index]) + 1
                            if lettre_index_suiv > len(LETTERS) - 1:
                                lettre_index_suiv = 0
                            mot[lettre_index] = LETTERS[lettre_index_suiv]
                            jeux_df.iloc[page_index - 1, 0] = "".join(mot)
                        if input_value == UP:
                            lettre_index_suiv = LETTERS.index(mot[lettre_index]) - 1
                            if lettre_index_suiv < 0:
                                lettre_index_suiv = len(LETTERS) - 1
                            mot[lettre_index] = LETTERS[lettre_index_suiv]
                            jeux_df.iloc[page_index - 1, 0] = "".join(mot)
                        if input_value == SELECT:
                            jeux_df.iloc[page_index - 1, 0] = "".join(mot).strip()
                            mode_ecriture = False
                            mode_bouge = True
                            srlgn_idx = 0
                            lettre_index = 0
                            # SAVE DATA to csv
                            jeux_df.to_csv("sm_goat_data.csv", index=False)
                    elif srlgn_idx > 2:  # index 2 sauté
                        if input_value == RIGHT:
                            lettre_index += 1
                            if lettre_index > 13:
                                lettre_index = 0
                        if input_value == LEFT:
                            lettre_index -= 1
                            if lettre_index < 0:
                                lettre_index = len(mot) - 1
                        if input_value == DOWN:
                            lettre_index_suiv = LETTERS.index(mot[lettre_index]) + 1
                            if lettre_index_suiv > len(LETTERS) - 1:
                                lettre_index_suiv = 0
                            mot[lettre_index] = LETTERS[lettre_index_suiv]
                            jeux_df.iloc[page_index - 1, 2 * (srlgn_idx - 2)] = "".join(mot[0:10])
                            jeux_df.iloc[page_index - 1, 2 * (srlgn_idx - 2) + 1] = "".join(mot[11:])
                        if input_value == UP:
                            lettre_index_suiv = LETTERS.index(mot[lettre_index]) - 1
                            if lettre_index_suiv < 0:
                                lettre_index_suiv = 37
                            mot[lettre_index] = LETTERS[lettre_index_suiv]
                            jeux_df.iloc[page_index - 1, 2 * (srlgn_idx - 2)] = "".join(mot[0:10])
                            jeux_df.iloc[page_index - 1, 2 * (srlgn_idx - 2) + 1] = "".join(mot[11:])
                        if input_value == SELECT:
                            jeux_df.iloc[page_index - 1, 2 * (srlgn_idx - 2)] = "".join(mot[0:10]).strip()
                            jeux_df.iloc[page_index - 1, 2 * (srlgn_idx - 2) + 1] = "".join(mot[11:]).strip()
                            mode_ecriture = False
                            mode_bouge = True
                            srlgn_idx = 0
                            lettre_index = 0
                            # SAVE DATA to csv
                            jeux_df.to_csv("sm_goat_data.csv", index=False)

        # -----------------------------------------------------------------
        # DEBUGGING
        # -----------------------------------------------------------------
        # print(tm.time(), e)
        print(jeux_df)
        # np.savetxt('data.csv', jeux, delimiter=',', fmt="%20s")
        # data = np.loadtxt('data.csv', delimiter=',')
        print(e)
        print("page index:", page_index)
        print("evenement:", valid_input, input_value, input_type)
        print("bouge:", mode_bouge)
        print("surligneur:", srlgn_idx)
        print("lettre index:", lettre_index)
        print("mot:", mot)
        print("ecriture:", mode_ecriture, lettre_index)

        # print(type(valid_input), type(input_value), type(input_type))
        # print(jeux_df.Name[1])
        # print(jeux_df.iloc[1,3])

    # -------------------------------------------------------------------------
    # BUILD DISPLAY -----------------------------------------------------------
    # -------------------------------------------------------------------------
    ecran.fill(CLR_BACKGROUND)
    # PAGE PRINCIPALE ---------------------------------------------------------
    if page_index == 0:
        ecran.blit(*text_blit("G.O.A.T. S.M.", police_entete, CLR_ENTETE, (pos_entete_h, pos_entete_v)))
        for ind, row in jeux_df.iterrows():
            if ind == rangee_index:
                couleur = CLR_SELECTION
            else:
                couleur = CLR_TITLE
            # ecran.blit(*text_blit(str(index + 1), font, CLR_TITLE, (20, espace_vert * index + espace_vert * 2)))
            ecran.blit(*text_blit(row["Name"], police_texte, couleur, (jeu_hor, espace_vert * ind + espace_vert * 2)))
            ecran.blit(*text_blit(">", police_texte, CLR_SELECTION, (screen_width - 20,
                                                                     espace_vert * rangee_index + espace_vert * 2)))
    # PAGES TABLEAUX DES MENEURS ----------------------------------------------
    if page_index > 0:
        if srlgn_idx == 0:
            ecran.blit(*text_blit("SELECT to enter/exit update mode",
                                  police_info, CLR_CARRE, (screen_width / 2, screen_height - 20)))

        if srlgn_idx == 1:  # Titre --------------------------------------
            # 10 carrés gris
            if mode_ecriture:
                for cg in range(10):
                    pg.draw.rect(ecran, CLR_CARRE, [36 * cg + 67, 7, 34, 46])
                    if tm.time() % 1 > 0.5 and cg == lettre_index:
                        pg.draw.rect(ecran, CLR_BACKGROUND, [36 * cg + 67, 7, 34, 46])
            ecran.blit(*text_blit(jeux_df.Name[page_index - 1], police_entete, CLR_MODIF, (pos_entete_h, pos_entete_v)))
            ecran.blit(*text_blit("LEFT to update, UP/DOWN to move",
                                  police_info, CLR_CARRE, (screen_width / 2, screen_height - 20)))
        else:
            ecran.blit(*text_blit(jeux_df.Name[page_index - 1], police_entete, CLR_TITLE, (pos_entete_h, pos_entete_v)))
            ecran.blit(*text_blit("<", police_texte, CLR_CARRE, (20, pos_entete_v)))
            ecran.blit(*text_blit(">", police_texte, CLR_CARRE, (screen_width - 20, pos_entete_v)))
        if srlgn_idx == 2:  # Sous titre ---------------------------------
            if mode_ecriture:
                pg.draw.rect(ecran, CLR_CARRE, [166, 54, 150, 26])
                if tm.time() % 1 > 0.5:
                    pg.draw.rect(ecran, CLR_BACKGROUND, [166, 54, 150, 26])
            ecran.blit(*text_blit(jeux_df.ScoreType[page_index - 1], police_soustitre,
                                  CLR_MODIF, (pos_entete_h, pos_soustitre_v)))
            ecran.blit(*text_blit("LEFT/RIGHT to change, UP/DOWN to move",
                                  police_info, CLR_CARRE, (screen_width / 2, screen_height - 20)))
        else:  # surligneur > 2 -----------------------------------------------
            ecran.blit(*text_blit(jeux_df.ScoreType[page_index - 1], police_soustitre,
                                  CLR_POS, (pos_entete_h, pos_soustitre_v)))
        for i in range(10):
            if srlgn_idx == i + 3:
                # 14 carrés gris
                if mode_ecriture:
                    for cg in range(14):
                        pg.draw.rect(ecran, CLR_CARRE, [27 * cg + 75, (srlgn_idx - 3) * 67 + 110, 25, 44])
                        if tm.time() % 1 > 0.5 and cg == lettre_index:
                            pg.draw.rect(ecran, CLR_BACKGROUND, [27 * cg + 75, (srlgn_idx - 3) * 67 + 110, 25, 44])
                ecran.blit(*text_blit(jeux_df.iloc[page_index - 1, i * 2 + 2],
                                      police_texte, CLR_MODIF, (pos_res, espace_vert * i + espace_vert * 2)))
                # if mode_ecriture:
                #     for cg in range(3):
                #         pg.draw.rect(ecran, CLR_CARRE, [27 * cg + 380, (surligneur_idx - 3) * 67 + 110, 25, 44])
                #         if tm.time() % 1 > 0.5 and cg == lettre_index:
                #             pg.draw.rect(ecran, CLR_BACKGROUND, [27 * cg + 380, (surligneur_idx - 3) * 67 + 110, 25, 44])
                ecran.blit(*text_blit(str(i + 1), police_pos, CLR_MODIF, (pos_rang, espace_vert * i + espace_vert * 2)))
                ecran.blit(*text_blit(jeux_df.iloc[page_index - 1, i * 2 + 3],
                                      police_texte, CLR_MODIF, (27 * 13 + 70, espace_vert * i + espace_vert * 2)))
                ecran.blit(*text_blit("LEFT to update, RIGHT to insert, UP/DOWN to move",
                                      police_info, CLR_CARRE, (screen_width / 2, screen_height - 20)))
            else:
                ecran.blit(*text_blit(str(i + 1), police_pos, CLR_POS, (pos_rang, espace_vert * i + espace_vert * 2)))
                ecran.blit(*text_blit(jeux_df.iloc[page_index - 1, i * 2 + 2],
                                      police_texte, CLR_TITLE, (pos_res, espace_vert * i + espace_vert * 2)))
                ecran.blit(*text_blit(jeux_df.iloc[page_index - 1, i * 2 + 3],
                                      police_texte, CLR_NOM, (pos_joueur, espace_vert * i + espace_vert * 2)))
                # ecran.blit(*text_blit("SELECT to update",
                #                       police_info, CLR_CARRE, (screen_width / 2, screen_height - 20)))
    pg.display.flip()

pg.quit()
