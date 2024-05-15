from os import remove
import time

from structure import simulateur
from structure.personnage import Personnage
from outils import \
    creer_image, \
    creer_caisse, creer_case_vide, creer_cible, creer_mur, creer_personnage, \
    coordonnee_x, coordonnee_y, est_egal_a

# Le projet a été réalisé par Luca Furlan et Cindy Lopes Godinho

# Constante à utiliser

VALEUR_COUP: int = 50

# Fonctions à développer

def jeu_en_cours(caisses: list, cibles: list) -> bool:
    """
    Fonction testant si le jeu est encore en cours et retournant un booléen comme réponse sur l'état de la partie.
    :param caisses: La liste des caisses du niveau en cours
    :param cibles: La liste des cibles du niveau en cours
    :return: True si la partie est finie, False sinon
    """
    # On met la variable False pour définir que le jeu est en cours
    jeu_fini: bool = False

    # Boucle qui parcourt toute la liste des cibles
    for cible in cibles:
        jeu_fini = False
        # Boucle qui parcourt toute la liste des caisses
        for caisse in caisses:
            # Si la caisse est égal au cible alors le jeu_fini devient true et le jeu est terminé
            if est_egal_a(caisse, cible):
                jeu_fini = True
                break
        if jeu_fini == False:
            return False
    return True

def charger_niveau(joueur: list, caisses: list, cibles: list, murs: list, vides: list, path: str):
    """
    Fonction permettant de charger depuis un fichier.txt et de remplir les différentes listes permettant le
    fonctionnement du jeu (joueur, caisses, murs, cibles)
    :param joueur: liste des personnages
    :param caisses: liste des caisses
    :param cibles: liste des cibles
    :param murs: liste des murs
    :param path: chemin du fichier.txt
    :return:
    """

    # On crée les variables pour les tours de boucle
    y = 0
    x = 0

    # Vérifie si les fichiers niveaux sont présents
    try:
        open(path, "r")
    except FileNotFoundError:
        print("Le fichier",path,"est introuvable!")
    else:
        # On ouvre le dossier niveau en mode lecture
        with open(path, "r") as line:
            lignes = line.readlines()
            # Boucle qui parcourt chaque ligne
            for ligne in lignes:
                # Boucle qui va parcourir un à un chaque caractère dans le fichier
                for elt in ligne:
                    if elt == '#':
                        murs.append(creer_mur(x, y))
                    elif elt == '@':
                        joueur.append(creer_personnage(x, y))
                    elif elt == '.':
                        cibles.append(creer_cible(x, y))
                    elif elt == '$':
                        caisses.append(creer_caisse(x, y))
                    elif elt == '-':
                        vides.append(creer_case_vide(x, y))
                    x += 1
                x = 0
                y += 1


def definir_mouvement(direction: str, can, joueur: list, murs: list, caisses: list, liste_image: list):
    """
    Fonction permettant de définir les cases de destinations (il y en a 2 si le joueur pousse une caisse) selon la
    direction choisie.
    :param direction: Direction dans laquelle le joueur se déplace (droite, gauche, haut, bas)
    :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param joueur: liste des joueurs
    :param murs: liste des murs
    :param caisses: liste des caisses
    :param liste_image: liste des images (murs, caisses etc...) détaillée dans l'énoncé
    :return:
    """
    deplace_joueur_x = None
    deplace_joueur_y = None
    deplace_caisse_x = None
    deplace_caisse_y = None

    if direction == "gauche":
        deplace_joueur_x = coordonnee_x(joueur[0]) - 1
        deplace_joueur_y = coordonnee_y(joueur[0])
        deplace_caisse_x = coordonnee_x(joueur[0]) - 2
        deplace_caisse_y = coordonnee_y(joueur[0])
    if direction == "droite":
        deplace_joueur_x = coordonnee_x(joueur[0]) + 1
        deplace_joueur_y = coordonnee_y(joueur[0])
        deplace_caisse_x = coordonnee_x(joueur[0]) + 2
        deplace_caisse_y = coordonnee_y(joueur[0])
    if direction == "haut":
        deplace_joueur_y = coordonnee_y(joueur[0]) - 1
        deplace_joueur_x = coordonnee_x(joueur[0])
        deplace_caisse_y = coordonnee_y(joueur[0]) - 2
        deplace_caisse_x = coordonnee_x(joueur[0])
    if direction == "bas":
        deplace_joueur_y = coordonnee_y(joueur[0]) + 1
        deplace_joueur_x = coordonnee_x(joueur[0])
        deplace_caisse_y = coordonnee_y(joueur[0]) + 2
        deplace_caisse_x = coordonnee_x(joueur[0])


    effectuer_mouvement(caisses, murs, joueur, can, deplace_caisse_x, deplace_caisse_y, deplace_joueur_x, deplace_joueur_y, liste_image)

def effectuer_mouvement(caisses: list, murs: list, joueur: list, can, deplace_caisse_x: int, deplace_caisse_y: int, deplace_joueur_x: int, deplace_joueur_y: int, liste_image: list):
    """
    Fonction permettant d'effectuer le déplacement ou de ne pas l'effectuer si celui-ci n'est pas possible.
    Voir énoncé "Quelques règles".
    Cette methode est appelée par mouvement.
    :param caisses: liste des caisses
    :param murs: liste des murs
    :param joueur: liste des joueurs
    :param can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param deplace_caisse_x: coordonnée à laquelle la caisse va être déplacée en x (si le joueur pousse une caisse)
    :param deplace_caisse_y: coordonnée à laquelle la caisse va être déplacée en y (si le joueur pousse une caisse)
    :param deplace_joueur_x: coordonnée en x à laquelle le joueur va être après le mouvement
    :param deplace_joueur_y: coordonnée en y à laquelle le joueur va être après le mouvement
    :param liste_image: liste des images (murs, caisses etc...) détaillée dans l'énoncé
    :return:
    """
    case_joueur = creer_case_vide(deplace_joueur_x, deplace_joueur_y)
    case_caisse = creer_case_vide(deplace_caisse_x, deplace_caisse_y)

    caisse_joueur: bool = False
    caisse_caisse: bool = False
    mur_joueur: bool = False
    mur_caisse: bool = False

    # Boucle qui parcourt la liste des murs
    for mur in murs:
        # Vérifie si il y a un mur
        if est_egal_a(case_joueur, mur):
            mur_joueur = True
        #  Vérifie si il y a mur
        if est_egal_a(case_caisse, mur):
            mur_caisse = True

    # Boucle qui parcourt la liste des caisses
    for caisse in caisses:
        # Vérifie si il y a une caisse sur la cas joueur
        if est_egal_a(case_joueur, caisse):
            caisse_joueur = True
        # Vérifie si il y a une caisse
        if est_egal_a(case_caisse, caisse):
            caisse_caisse = True

    # Si il n'y a pas de mur il peut avancer
    if mur_joueur == False:
        # Le personnage peut se déplacer
        if caisse_joueur == False:
            creer_image(can, coordonnee_x(joueur[0]), coordonnee_y(joueur[0]), liste_image[6])
            del joueur[0]
            joueur.append(creer_personnage(deplace_joueur_x, deplace_joueur_y))
        else:
            # Si il y pas un mur ou une caisse derrière une caisse alors on peut bouger le personnage et la caisse.
            if mur_caisse == False and caisse_caisse == False:
                creer_image(can, coordonnee_x(joueur[0]), coordonnee_y(joueur[0]), liste_image[6])
                del joueur[0]
                joueur.append(creer_personnage(deplace_joueur_x, deplace_joueur_y))

                caisses.remove(creer_caisse(deplace_joueur_x,deplace_joueur_y))
                caisses.append(creer_caisse(deplace_caisse_x, deplace_caisse_y))

def chargement_score(scores_file_path: str, dict_scores: dict):
    """
    Fonction chargeant les scores depuis un fichier.txt et les stockent dans un dictionnaire
    :param scores_file_path: le chemin d'accès du fichier
    :param dict_scores:  le dictionnaire pour le stockage
    :return:
    """
    new_list: list = []
    cle: int = None
    liste_fichier_score: list = []

    # Vérifie si le fichier est présent
    try:
        open(scores_file_path, "r")
    except FileNotFoundError:
        print("Le fichier",scores_file_path,"est introuvable!")
    else:
        # On ouvre le fichier en mode lecture
        with open(scores_file_path, "r") as score_text:
            # Boucle qui parcourt chaque ligne du fichier texte
            for score in score_text.readlines():
                new_list = []
                liste_fichier_score = score.split(";")
                # Boucle qui parcourt l'index de chaque élément dans le fichier score et ajouter les éléments dans une liste avec une clé
                for i in range(len(liste_fichier_score)):
                    if i == 0:
                        cle = liste_fichier_score[i]
                    else:
                        new_list.append(liste_fichier_score[i])
                        dict_scores[cle] = new_list

def maj_score(niveau_en_cours: int, dict_scores: dict) -> str:
    """
    Fonction mettant à jour l'affichage des scores en stockant dans un str l'affichage visible
    sur la droite du jeu.
    ("Niveau x
      1) 7699
      2) ... ").
    :param niveau_en_cours: le numéro du niveau en cours
    :param dict_scores: le dictionnaire pour stockant les scores
    :return: On retourne le score
    """
    affichage_score: str = ""
    position_score: int = 1

    # On ajoute le score [0,0,0,0,0,0,0,0] dans la clé qui n'a pas encore de score pour les niveaux en cours.
    if str(niveau_en_cours) not in dict_scores.keys():
        dict_scores[str(niveau_en_cours)] = [0,0,0,0,0,0,0,0,0,0]

    affichage_score += f"Niveau {niveau_en_cours} \n\n"
    # Boucle qui va récupérer les valeurs du niveau actuel
    for val in dict_scores[str(niveau_en_cours)]:
            affichage_score += f"{position_score}) {val} \n"
            position_score += 1

    return affichage_score


def calcule_score(temps_initial: float, nb_coups: int, score_base: int) -> int:
    """
    calcule le score du joueur
    :param temps_initial: debut du jeu
    :param nb_coups: nombre des mouvements
    :param score_base: score de base
    :return: Le calcul score du joueur
    """
    temps_actuel: float = time.time()
    new_score: int = int(round(score_base - (temps_actuel - temps_initial) - (nb_coups * VALEUR_COUP)))
    return new_score


def enregistre_score(temps_initial: float, nb_coups: int, score_base: int, dict_scores: dict,
                     niveau_en_cours: int):
    """
    Fonction enregistrant un nouveau score réalisé par le joueur. Le calcul de score est le suivant :
    score_base - (temps actuel - temps initial) - (nombre de coups * valeur d'un coup)
    Ce score est arrondi sans virgule et stocké en tant que int. Le score est mis à jour dans le
    dictionnaire.
    :param temps_initial: le temps initial
    :param nb_coups: le nombre de coups que l'utilisateurs à fait (les mouvements)
    :param score_base: Le score de base identique pour chaque partie
    :param dict_scores: Le dictionnaire stockant les scores
    :param niveau_en_cours: Le numéro du niveau en cours
    """
    # Valeur temporaire à remplacer dans la liste des scores
    tmp: int = 0

    # On récupère la valeur de la fonction pour mettre à jour le score
    score: int = calcule_score(temps_initial, nb_coups, score_base)

    change_score = str(score)

    # Boucle qui parcourt l'index de position de chaque élément pour chaque clé et mettre les score du plus grand au plus petit.
    for elt in range(0, len(dict_scores[str(niveau_en_cours)])):
        if int(dict_scores[str(niveau_en_cours)][elt]) < score:
            tmp = dict_scores[str(niveau_en_cours)][elt]
            dict_scores[str(niveau_en_cours)][elt] = change_score
            change_score = tmp

def update_score_file(scores_file_path: str, dict_scores: dict):
    """
    Fonction sauvegardant tous les scores dans le fichier.txt.
    :param scores_file_path: le chemin d'accès du fichier de stockage des scores
    :param dict_scores: Le dictionnaire stockant les scores
    :return:
    """
    # On crée une variable avec une valeur vide pour la remplir ensuite
    score_save: str = ""

    # Vérifie si le fichier scores est présent
    try:
        open(scores_file_path, "r")
    except FileNotFoundError:
        print("Le fichier",scores_file_path,"est introuvable!")
    else:
        # On ouvre le fichier en mode écriture pour mettre à jour le fichier score avec les scores obtenues.
        with open(scores_file_path, "w") as score_text:
            # Boucle qui parcourt les clés du dictionnaire
            for key in dict_scores.keys():
                score_save += str(key)
                # Boucle qui parcourt tous les éléments d'une clé du dictionnaire
                for elt in dict_scores[key]:
                    score_save += ";" + str(elt)
                score_save += "\n"
            score_text.write(score_save)


if __name__ == '__main__':
    simulateur.simulate()
