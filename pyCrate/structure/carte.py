import os.path

from tkinter import Canvas, PhotoImage, NW


def dessine_image(canvas):
    photo = PhotoImage(file=os.path.abspath("./images/floor.png"))
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.pack()


def init_map(nom_niveau, fenetre):
    NB_DE_CASES = 10
    COTE = 400
    PAS = COTE / NB_DE_CASES
    fichier = open(os.path.abspath("../niveaux/" + nom_niveau + ".txt"), "r")
    grille = []
    x = 0
    canvas = Canvas(fenetre, width=400, height=400)
    for i in fichier:
        canvas.create_line(0, PAS * x, COTE, PAS * x, fill='black')
        ligne = []
        y = 0
        for j in i:
            canvas.create_line(PAS * y, 0, PAS * y, COTE, fill='black')
            if j == '-':
                ligne.append("Vide")
            elif j == '$':
                ligne.append("Caisse")
                # dessine_image(canvas,y,x,"images\\box.png")
            elif j == '@':
                ligne.append("Homme")
                # dessine_image(canvas,y,x,"images\\worker.png")
            elif j == '.':
                ligne.append("Emplacement")
                # dessine_image(canvas,y,x,"images\\dock.png")
            elif j == '#':
                ligne.append("Mur")
                # dessine_image(canvas,y,x,"images\\wall.png")
            y += 1
        grille.append(ligne)
        x = x + 1
    print(grille)
    canvas.pack()
    fichier.close()
    return canvas
