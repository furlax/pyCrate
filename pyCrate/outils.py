from structure.caisse import Caisse
from structure.case_vide import CaseVide
from structure.cible import Cible
from structure.mur import Mur
from structure.personnage import Personnage

DISTANCE_ENTRE_CASE: int = 32  # distance par rapport à l'autre case
X_PREMIERE_CASE: int = 20

def creer_image(can, x: int, y: int, image: object):
    """
    Fonction qui permet de créer/remplacer une image dans le canvas. Pour l'utiliser il faut préciser :
    :param can: un canvas (faites abstraction de ce que c'est et marquez : can
    :param x: une coordonnée dans l'axe des abscisses ( coordonnée x)
    :param y: une coordonnée dans l'axe des ordonnées ( coordonnée y)
    :param image: une image tirée de la liste d'image (voir énoncé pour quelle image choisir via quel index)
    :return:
    """
    can.create_image(x* DISTANCE_ENTRE_CASE + X_PREMIERE_CASE, y* DISTANCE_ENTRE_CASE + X_PREMIERE_CASE, image=image)


def creer_mur(x: int, y: int) -> Mur:
    """
    Fonction permettant de créer un mur.
    :param x: coordonnée en x du mur à créer
    :param y:coordonnée en y du mur à créer
    :return: la variable mur
    """
    return Mur(x, y)


def creer_caisse(x: int, y: int) -> Caisse:
    """
    Fonction permettant de créer une caisse.
    :param x: coordonnée en x de la caisse à créer
    :param y:coordonnée en y de la caisse à créer
    :return: la variable caisse
    """
    return Caisse(x, y)


def creer_cible(x: int, y: int):
    """
    Fonction permettant de créer une cible.
    :param x: coordonnée en x de la cible à créer
    :param y:coordonnée en y de la cible à créer
    :return: la variable cible
    """
    return Cible(x, y)


def creer_personnage(x: int, y: int) -> Personnage:
    """
    Fonction permettant de créer un personnage.
    :param x: coordonnée en x du personnage à créer
    :param y:coordonnée en y du personnage à créer
    :return: la variable personnage
    """
    return Personnage(x, y)


def creer_case_vide(x: int, y: int) -> CaseVide:
    """
    Fonction permettant de créer une case vide.
    :param x: coordonnée en x de la case vide à créer
    :param y:coordonnée en y de la case vide à créer
    :return: la variable case vide
    """
    return CaseVide(x, y)


def coordonnee_x(variable: object) -> int:
    """
    Fonction permettant de retourner la coordonnée en x de la variable.
    :param variable: la variable (Personnage,Caisse, CaseVide, Cible, Mur)
    :return: la coordonnée en x de la variable
    """
    return variable.get_x()


def coordonnee_y(variable: object) -> int:
    """
    Fonction permettant de retourner la coordonnée en y de la variable.
    :param variable: la variable (Personnage,Caisse, CaseVide, Cible, Mur)
    :return: la coordonnée en y de la variable
    """
    return variable.get_y()


def est_egal_a(variable1: object, variable2: object) -> bool:
    """
    Fonction permettant de tester l'égalité de position entre 2 variables (Personnage, Caisse, CaseVide, Cible, Mur).
    Ici si le x et y des deux variables sont identiques, la fonction retournera True. False sinon.
    :param variable1: variable (Personnage, Caisse, CaseVide, Cible, Mur)
    :param variable2: variable (Personnage, Caisse, CaseVide, Cible, Mur)
    :return: Booléen (True si les deux variables ont les mêmes coordonées, False sinon)
    """
    return variable1 == variable2
