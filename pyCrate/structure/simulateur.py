import os
import time
from tkinter import Tk, Canvas, Label, Menu, PhotoImage, Toplevel, Button, LEFT, ALL

import pyCrate

# DISTANCE_ENTRE_CASE: int = 32  # distance par rapport à l'autre case
SCORE_BASE: int = 10000
LEVEL_FOLDER_PATH: str = os.path.abspath("./niveaux")
SCORE_FILE_PATH: str = os.path.abspath("./scores/scores.txt")


class Jeu:
    def __init__(self, can):
        self.nb_coups: int = 0
        self.started: bool = False
        self.score_start: bool = False
        self.niveau_en_cours: int = None
        self.temps_initial: float = 0
        self.nb_file: int = 1
        self.joueur: list = []
        self.caisses: list = []
        self.cibles: list = []
        self.murs: list = []
        self.vides: list = []
        self.liste_image: list = []
        self.dict_scores: dict = {}
        self.can: Canvas = can
        self.score_label: Label = None

    def refresh(self):
        self.joueur: list = []
        self.caisses: list = []
        self.cibles: list = []
        self.murs: list = []
        self.vides: list = []

        self.nb_coups: int = 0
        self.started: bool = False
        self.score_start: bool = False
        self.niveau_en_cours: int = None
        self.temps_initial: float = 0


def quitter(fenetre: Tk):
    """
    fonction qui ferme l'application
    :param fenetre:
    :return:
    """
    fenetre.quit()
    fenetre.destroy()


def affichage_jeu(jeu: Jeu):
    """
    fonction qui utilise le fichier texte du nom nivo1.txt, pour creer la liste ch du niveau 1
    :param jeu: configuration du jeu
    :return:
    """
    for j in jeu.vides:
        pyCrate.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[6])
    for j in jeu.murs:
        pyCrate.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[0])
    for j in jeu.cibles:
        pyCrate.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[1])
    for j in jeu.caisses:
        pyCrate.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[2])
        for c in jeu.cibles:
            if j == c:
                pyCrate.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[3])
    for j in jeu.joueur:
        pyCrate.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[4])
        for c in jeu.cibles:
            if j.get_x() == c.get_x() and j.get_y() == c.get_y():
                pyCrate.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[5])


def charger_niveau(jeu: Jeu, path: str):
    """
    charge la configuration du jeu pour un niveau
    :param jeu: configuration du jeu
    :param path: fichier avec la configuration du niveau
    :return:
    """
    jeu.can.delete(ALL)
    jeu.refresh()

    pyCrate.charger_niveau(jeu.joueur, jeu.caisses, jeu.cibles, jeu.murs, jeu.vides, path)
    affichage_jeu(jeu)
    jeu.can.bind_all("<Right>", lambda event: droite(jeu))
    jeu.can.bind_all("<Left>", lambda event: gauche(jeu))
    jeu.can.bind_all("<Up>", lambda event: haut(jeu))
    jeu.can.bind_all("<Down>", lambda event: bas(jeu))
    jeu.can.pack()

    tmp_str: str = path.split("level")[1]
    jeu.niveau_en_cours = int(tmp_str.replace(".txt", ""))
    jeu.started = True
    jeu.temps_initial = time.time()

    refresh_score(jeu)


def popup_aide():
    """
    fonction qui creer une fenetre popup
    :return:
    """
    popup = Toplevel()
    popup.title("Instructions")
    bouton = Button(popup, text="Fermer", command=popup.withdraw)
    bouton.pack()


def load_levels(jeu: Jeu, filemenu: Menu):
    """
    charge les niveaux
    :param jeu: configuration du jeu
    :param filemenu: menu pour charger les niveaux
    :return:
    """
    files: list = [f for f in os.listdir(LEVEL_FOLDER_PATH) if f.endswith(".txt")]
    for i in range(1, len(files)+1):
        tag: str = "Niveau %s" % i
        path: str = os.path.join(LEVEL_FOLDER_PATH, "level%d.txt" % i)
        filemenu.add_command(label=tag, command=lambda x=path: charger_niveau(jeu, x))


def init_menu(jeu: Jeu, fenetre: Tk):
    menu: Menu = Menu(fenetre)
    fenetre.config(menu=menu)
    filemenu: Menu = Menu(menu)
    menu.add_cascade(label="Choix du niveau", menu=filemenu)
    load_levels(jeu, filemenu)
    menu.add_command(label="Exit", command=lambda: update_score_file(jeu, fenetre))


def check_status(jeu: Jeu):
    if pyCrate.jeu_en_cours(jeu.caisses, jeu.cibles) and jeu.started:
        affichage_jeu(jeu)
        save_score(jeu)
        jeu.can.bind_all("<Right>")
        jeu.can.bind_all("<Left>")
        jeu.can.bind_all("<Up>")
        jeu.can.bind_all("<Down>")
        jeu.started = False
    else:
        affichage_jeu(jeu)


def mouvement(jeu: Jeu, direction: str):
    if jeu.started:
        pyCrate.definir_mouvement(direction, jeu.can, jeu.joueur, jeu.murs, jeu.caisses, jeu.liste_image)
    jeu.nb_coups += 1
    check_status(jeu)


def droite(jeu: Jeu):
    mouvement(jeu, "droite")


def gauche(jeu: Jeu):
    mouvement(jeu, "gauche")


def haut(jeu: Jeu):
    mouvement(jeu, "haut")


def bas(jeu: Jeu):
    mouvement(jeu, "bas")


def load_scores(jeu: Jeu):
    pyCrate.chargement_score(SCORE_FILE_PATH, jeu.dict_scores)


def refresh_score(jeu: Jeu):
    score_affichage = pyCrate.maj_score(jeu.niveau_en_cours, jeu.dict_scores)
    jeu.score_label.config(text=score_affichage)


def save_score(jeu: Jeu):
    pyCrate.enregistre_score(jeu.temps_initial, jeu.nb_coups, SCORE_BASE, jeu.dict_scores, jeu.niveau_en_cours)
    refresh_score(jeu)


def update_score_file(jeu: Jeu, fenetre: Tk):
    pyCrate.update_score_file(SCORE_FILE_PATH, jeu.dict_scores)
    quitter(fenetre)


def simulate():
    title: str = "Projet 63-11"

    fenetre: Tk = Tk()
    fenetre.title(title)

    # Référence sur les images (obligatoire avec tkinter)

    img_mur: PhotoImage = PhotoImage(file=os.path.abspath("./images/mur.gif"))
    img_cible: PhotoImage = PhotoImage(file=os.path.abspath("./images/pokeball_ouverte.png"))
    img_boite: PhotoImage = PhotoImage(file=os.path.abspath("./images/pokemon.gif"))
    img_boite_correcte: PhotoImage = PhotoImage(file=os.path.abspath("./images/pokeball_ferme.png"))
    img_joueur: PhotoImage = PhotoImage(file=os.path.abspath("./images/dresseur.gif"))
    img_joueur_cible: PhotoImage = PhotoImage(file=os.path.abspath("./images/dresseur_pokeball.gif"))
    img_sol: PhotoImage = PhotoImage(file=os.path.abspath("./images/herbe.gif"))
    can: Canvas = Canvas(fenetre, height=760, width=1000, bg="#98e2bb")
    can.pack(side=LEFT)
    jeu: Jeu = Jeu(can)

    jeu.liste_image.append(img_mur)
    jeu.liste_image.append(img_cible)
    jeu.liste_image.append(img_boite)
    jeu.liste_image.append(img_boite_correcte)
    jeu.liste_image.append(img_joueur)
    jeu.liste_image.append(img_joueur_cible)
    jeu.liste_image.append(img_sol)

    score_label: Label = Label(fenetre, anchor="nw", font="Cooper", justify="left", bg="#a7a7a7", fg="black",
                               text=load_scores(jeu), height=21, width=38)
    score_label.pack()
    jeu.score_label = score_label

    init_menu(jeu, fenetre)

    _help: str = """_______________________________________
    
    Règles du jeu
    
    Déplacez le personnage à l'aide des flèches 
    du clavier afin de placer toutes les caisses
    sur les emplacements."""

    t: Label = Label(fenetre, anchor="s", font="Cooper", bg="#a7a7a7", fg="black", pady="20", text=_help, height=18, width=38)
    t.pack(side=LEFT)
    fenetre.resizable(height=0, width=0)
    fenetre.protocol("WM_DELETE_WINDOW", lambda: update_score_file(jeu, fenetre))
    fenetre.mainloop()
