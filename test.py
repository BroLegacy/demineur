##-----Importation des Modules-----##

from tkinter import *
from random import *

##-----Définition des Variables globales-----##

decouvertes = []  # Liste avec les coordonnées des cases découvertes par le joueur
case_drapeau = []  # Liste avec les coordonnées des drapeaux
case_mine = []  # Liste avec les coordonnées des mines
nb_mines = 0  # Nombres de mines au tout départ
nb_drapeau = 0  # Nombres de drapeaux au tout départ
lignes = 15  # Nombre de cases en hauteur
colonnes = 20  # Nombre de cases en largeur
d = 15  # Dimensions d'une case carrée

# -#############################-----Tableaux-----#############################-##
#                                                                              ##
#  cellules est un tableau (liste de liste) contenant les états des cases :    ##
#       ₪ De 0 à 8 : la case est vide, le nombre est celui des voisines        ##
#         contenant des mines ;                                                ##
#       ₪ 9 : la case contient une mine.                                       ##
#                                                                              ##
#  Le tableau grille gère l'affichage de chaque case.                          ##
#  Il est en relation avec le tableau cellules :                               ##
#       ₪ Au départ, toutes les cases sont "grises"                            ##
#       ₪ Lorsque le joueur clique sur une case vide (0), celle-ci fait        ##
#         apparaître un carré blanc                                            ##
#       ₪ Lorsque le joueur clique sur une case vide (de 1 à 8), celle-ci      ##
#         fait apparaître le nombre                                            ##
#       ₪ Lorsque le joueur clique sur une mine, celle-ci apparaît et le jeu   ##
#         s'arrête.                                                            ##
#                                                                              ##
# -############################################################################-##

cellules = []  # Etats des cases
grille = []  # Affichage correspondant


##-----Définitions des Fonctions-----##

def clic_gauche(event):
    """Cette fonction détermine les coordonnées de la case où a eu lieu le clic gauche du joueur puis lance la fonction trace()."""
    global d

    j = (event.x - 2) // d  # colonne du clic
    i = (event.y - 2) // d  # ligne du clic
    trace(i, j)


def voisines(i, j):
    """Cette fonction renvoie une liste des coordonnées des cases adjacentes à la case cellule[i][j]."""
    global cellules, lignes, colonnes
    liste = []  # On crée une liste vide que l'on va remplir
    if i == 0 and j == 0:  # On définit les exceptions où les cases voisines sont spécifiques, à savoir les coins et les bordures
        liste.append(cellules[i][j + 1])
        liste.append(cellules[i + 1][j])
        liste.append(cellules[i + 1][j + 1])
    elif i == 0 and j > 0 and j < 19:
        liste.append(cellules[i][j - 1])
        liste.append(cellules[i][j + 1])
        liste.append(cellules[i + 1][j - 1])
        liste.append(cellules[i + 1][j])
        liste.append(cellules[i + 1][j + 1])
    elif i == 0 and j == 19:
        liste.append(cellules[i][j - 1])
        liste.append(cellules[i + 1][j - 1])
        liste.append(cellules[i + 1][j])
    elif i == 14 and j == 0:
        liste.append(cellules[i - 1][j])
        liste.append(cellules[i - 1][j + 1])
        liste.append(cellules[i][j + 1])
    elif i == 14 and j > 0 and j < 19:
        liste.append(cellules[i - 1][j - 1])
        liste.append(cellules[i - 1][j])
        liste.append(cellules[i - 1][j + 1])
        liste.append(cellules[i][j - 1])
        liste.append(cellules[i][j + 1])
    elif i == 14 and j == 19:
        liste.append(cellules[i - 1][j - 1])
        liste.append(cellules[i - 1][j])
        liste.append(cellules[i][j - 1])
    elif i > 0 and i < 14 and j == 0:
        liste.append(cellules[i - 1][j])
        liste.append(cellules[i - 1][j + 1])
        liste.append(cellules[i][j + 1])
        liste.append(cellules[i + 1][j])
        liste.append(cellules[i + 1][j + 1])
    elif i > 0 and i < 14 and j == 19:
        liste.append(cellules[i - 1][j - 1])
        liste.append(cellules[i - 1][j])
        liste.append(cellules[i][j - 1])
        liste.append(cellules[i + 1][j - 1])
        liste.append(cellules[i + 1][j])
    else:  # On ajoute les cases voisines dans les cas normaux (pas sur la bordure de la grille)
        liste.append(cellules[i - 1][j - 1])
        liste.append(cellules[i - 1][j])
        liste.append(cellules[i - 1][j + 1])
        liste.append(cellules[i][j - 1])
        liste.append(cellules[i][j + 1])
        liste.append(cellules[i + 1][j - 1])
        liste.append(cellules[i + 1][j])
        liste.append(cellules[i + 1][j + 1])

    return liste  # On renvoie la liste ainsi créée


def compte_mines(i, j):
    """Cette fonction affecte à la case cellules[i][j] le nombre de voisines contenant une mine."""
    global cellules, lignes, colonnes
    listage = list(voisines(i, j))  # On affecte la liste des voisines à la liste 'listage'
    nb_voisines = listage.count(9)  # .. et on compte le nombre d'apparitions du chiffre 9 dans cette nouvelle liste
    return nb_voisines  # On renvoie ainsi le nombre de mines au voisinage de la case selectionnée


def connexe(i, j):
    """Cette fonction propage la révélation des cases depuis une case ne contenant pas de mines et n'étant pas voisine avec une mine."""
    global cellules

    trace(i - 1, j - 1)  # On applique la fonction trace aux cases adjacentes afin de créer une boucle recursive
    trace(i - 1, j)
    trace(i - 1, j + 1)
    trace(i, j - 1)
    trace(i, j + 1)
    trace(i + 1, j - 1)
    trace(i + 1, j)
    trace(i + 1, j + 1)


def clic_droit(event):
    j = (event.x - 2) // d  # colonne du clic
    i = (event.y - 2) // d  # ligne du clic
    drapeau(i, j)  # On applique la fonction 'drapeau' à la case de coordonnées (i,j)


##-----Fonctions graphiques-----##
def reinit():
    """Cette fonction réinitialise les tableaux de jeu."""
    global cellules, grille, lignes, colonnes, d, nb_mines, decouvertes, case_drapeau, nb_drapeau, case_mine

    dessin.delete(ALL)  # On efface tout

    message.configure(
        text='Nombre de mines à trouver :')  # On remet ce message ici pour qu'il se réaffiche à chaque début de partie
    message_drapeau.configure(text='Nombre de drapeaux restants :')  # Parallèlement que pour les mines ci-dessus

    nb_mines = 0  # Initialisation du nombre de mines
    decouvertes = []  # Création de la liste des cases découvertes (vide au début de la partie)
    case_drapeau = []  # Parallèlement pour la liste des drapeaux
    case_mine = []  # ..ainsi que pour la liste des mines

    cellules = []  # Etats des cases
    grille = []  # Affichage correspondant

    for i in range(lignes):  # Pour chaque ligne

        cellules.append([])
        grille.append([])

        for j in range(colonnes):

            chance_mine = random()  # On affecte un nombre décimal compris entre 0 et 1 à la variable chance_mine
            grille[i].append(
                dessin.create_rectangle(2 + j * d, 2 + i * d, 2 + (j + 1) * d, 2 + (i + 1) * d, outline='black',
                                        fill='gray'))

            if chance_mine <= 0.15:  # Si le nombre aléatoire est inférieur ou égal à 0.15, soit  15% de chance,
                cellules[i].append(
                    9)  # Alors on a ajoute a la liste de cette case le numéro 9 ce qui signifie qu'elle a une bombe
                nb_mines = nb_mines + 1  # Le nombre de mine au total sur le terrain augmente donc de 1
                nombre_mines.configure(
                    text=nb_mines)  # ...et l'on met à jour le texte affiché de nombre_mines à l'écran
                liste_rapide = [i, j]  # On crée une liste rapide avec les coordonnées de la mine

                case_mine.append(liste_rapide)  # .. que l'on ajoute à la liste des coordonnées des mines

            else:

                cellules[i].append(
                    0)  # Sinon on ajoute a la liste de cette case le numéro 0 ce qui signifie qu'elle n'a pas de bombe
    nb_drapeau = nb_mines  # On possède au début de la partie le même nombre de drapeaux que de mines
    nombre_drapeau.configure(text=nb_drapeau)  # On met à jour le texte du nombre de drapeau disponible à l'écran


def trace(i, j):
    """Cette fonction révèle le contenu de la case choisie par l'utilisateur."""
    global cellules, grille, d, decouvertes, colonnes, lignes, nb_mines

    liste_rapide = [i, j]  # On crée une liste rapide avec les coordonnées du clic de la souris
    verif = decouvertes.count(
        liste_rapide)  # On crée une variable permettant de vérifier si les coordonnées se trouvent dans cette liste
    verif2 = case_drapeau.count(liste_rapide)  # .. de même pour les drapeaux

    if verif == 0 and i >= 0 and i <= 14 and j >= 0 and j <= 19 and verif2 == 0:  # Si la case n'a pas été découverte, qu'elle n'a pas de drapeau et qu'elle se                          trouve bien dans la grille de jeu

        decouvertes.append(liste_rapide)  # .. Alors on ajoute ces coordonnées à la liste des cases découvertes

        if cellules[i][j] == 0:  # On vérifie si la cellule ne comporte pas de mine

            a = compte_mines(i, j)  # On affecte à une variable a le nombre de mines autour de la case
            if a == 0:  # Si il n'y a aucune mine au voisinage de celle-ci,

                dessin.itemconfigure(grille[i][j], fill='white')  # .. alors on colore la case en blanc
                connexe(i, j)  # .. et on lui applique la fonction connexe car il n'y a pas de mine aux alentours
            else:

                dessin.itemconfigure(grille[i][j], fill='white')  # On remplit la case en blanc
                dessin.create_text(2 + d * (j + 0.5), 2 + (i + 0.5) * d, fill='black', state=DISABLED,
                                   font=('Courier', '10', 'bold'), text=str(
                        a))  # On écrit le nombre de mines autour de la case sans affecter la fonction connexe
        elif cellules[i][
            j] == 9:  # Si par contre la cellule porte le chiffre 9 dans sa liste, c'est à dire si la cellule est minée,
            dessin.itemconfigure(grille[i][j], fill='red')  # ..alors on remplit la case de rouge
            dessin.create_oval(5 + j * d, 5 + i * d, (j + 1) * d - 1, (i + 1) * d - 1, outline='black',
                               fill='black')  # ..et l'on y trace un disque noir symbolisant la mine
            nombre_mines.configure(text='')
            message.configure(text='Vous avez perdu.')

            nombre_drapeau.configure(text='')
            message_drapeau.configure(text='')

            # On indique au joueur qu'il a perdu la partie
            decouvertes = []

            for i in range(lignes):  # On révèle toutes les cases du jeu

                for j in range(colonnes):

                    if cellules[i][j] == 0:

                        dessin.itemconfigure(grille[i][j], fill='white')
                        liste_fin = [i, j]
                        decouvertes.append(liste_fin)

                    else:

                        dessin.itemconfigure(grille[i][j], fill='red')
                        dessin.create_oval(5 + j * d, 5 + i * d, (j + 1) * d - 1, (i + 1) * d - 1, outline='black',
                                           fill='black')
                        liste_fin = [i, j]
                        decouvertes.append(liste_fin)

        nb_terme = len(decouvertes)  # On va vérifier le nombre de cases découvertes

        if nb_terme == 300 - nb_mines:  # Si ce nombre est égal au nombre de cases totales auquel on a soustrait le nombre de mines,
            message.configure(text='Vous avez gagné !!!')  # Alors on indique au joueur qu'il a gagné la partie
            nombre_mines.configure(text='')
            decouvertes = []
            nombre_drapeau.configure(text='')
            message_drapeau.configure(text='')

            for i in range(lignes):  # On révèle au joueur l'emplacement des mines et des cases vides
                for j in range(colonnes):

                    if cellules[i][j] == 0:

                        dessin.itemconfigure(grille[i][j], fill='white')
                        liste_fin = [i, j]
                        decouvertes.append(liste_fin)

                    else:

                        dessin.itemconfigure(grille[i][j], fill='lightgreen')
                        dessin.create_oval(5 + j * d, 5 + i * d, (j + 1) * d - 1, (i + 1) * d - 1, outline='black',
                                           fill='black')
                        liste_fin = [i, j]
                        decouvertes.append(liste_fin)


def drapeau(i, j):  # Cette fonction sert à poser et enlever des drapeaux sur les cases
    global cellules, grille, lignes, colonnes, d, nb_mines, decouvertes, case_drapeau, nb_drapeau, case_mine

    liste_rapide = [i, j]  # On crée une liste rapide constituée des coordonnées du clic du joueur
    verif = case_drapeau.count(liste_rapide)  # On vérifie si un drapeau se trouve sur cette case
    verif2 = decouvertes.count(liste_rapide)  # On vérifie également si cette carte a été découverte

    if verif == 0 and verif2 == 0 and nb_drapeau > 0:  # Si ces deux conditions sont remplies et qu'il reste des drapeaux à placer au joueur, alors il est en mesure de poser un drapeau sur la case de son choix

        dessin.itemconfigure(grille[i][j], fill='orange')  # WORK IN PROGRESS#
        case_drapeau.append(liste_rapide)  # WORK IN PROGRESS#
        nb_drapeau = nb_mines - len(case_drapeau)
        nombre_drapeau.configure(text=nb_drapeau)

    elif verif != 0 and verif2 == 0 and nb_drapeau >= 0:  # Si il y a déjà un drapeau sur cette case

        dessin.itemconfigure(grille[i][j], fill='grey')  # .. alors on le retire visuellement
        case_drapeau.remove(liste_rapide)  # ..ainsi que dans sa liste
        nb_drapeau = nb_mines - len(case_drapeau)  # On met à jour le nombre de drapeaux disponibles pour le joueur
        nombre_drapeau.configure(text=nb_drapeau)

    verifliste1 = sorted(case_drapeau)
    verifliste2 = sorted(case_mine)

    if verifliste1 == verifliste2:

        message.configure(text='Vous avez gagné !!!')
        nombre_mines.configure(text='')
        decouvertes = []
        nombre_drapeau.configure(text='')
        message_drapeau.configure(text='')

        for i in range(lignes):

            for j in range(colonnes):

                if cellules[i][j] == 0:

                    dessin.itemconfigure(grille[i][j], fill='white')
                    liste_fin = [i, j]
                    decouvertes.append(liste_fin)

                else:

                    dessin.itemconfigure(grille[i][j], fill='lightgreen')
                    dessin.create_oval(5 + j * d, 5 + i * d, (j + 1) * d - 1, (i + 1) * d - 1, outline='black',
                                       fill='black')
                    liste_fin = [i, j]
                    decouvertes.append(liste_fin)


##-----Création de la fenêtre-----##

fen = Tk()  # Stockée dans la variable "fen"
fen.title('Démineur')  # Titre de la fenêtre
fen.resizable(width=False, height=False)  # Interdiction de redimensionner la fenêtre

##-----Création des zones de texte-----##

message = Label(fen, text='Nombre de mines à trouver :')
message.grid(row=0, column=0, padx=3, pady=3, sticky=E)

nombre_mines = Label(fen, text='')
nombre_mines.grid(row=0, column=1, padx=3, pady=3, sticky=W)

message_drapeau = Label(fen, text='Nombre de drapeaux restants :')
message_drapeau.grid(row=1, column=0, padx=3, pady=3, sticky=E)

nombre_drapeau = Label(fen, text=nb_drapeau)
nombre_drapeau.grid(row=1, column=1, padx=3, pady=3, sticky=W)

##-----Création des boutons-----##

bouton_quitter = Button(fen, text='Quitter', command=fen.quit)
bouton_quitter.grid(row=3, column=1, sticky=S + W + E, padx=15, pady=5)

bouton_reload = Button(fen, text='Nouvelle partie', command=reinit)
bouton_reload.grid(row=3, column=0, sticky=S + W + E, padx=15, pady=5)

##-----Création d'un canevas et d'une grille dans le canevas-----##

dessin = Canvas(fen, bg='white', width=d * colonnes + 1, height=d * lignes + 1)
dessin.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

##-----Programme principal-----##

dessin.bind('<Button-1>', clic_gauche)
dessin.bind('<Button-3>', clic_droit)
reinit()

fen.mainloop()  # Boucle d'attente des événements
try:
    fen.destroy()  # Fermeture "correcte" de la fenêtre
except TclError:
    pass 