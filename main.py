import random as rd # Importation de random pour les mine
from colorama import Fore, Back, Style # Importation de colorama pour mettre des couleur sur les bombe et les chiffre
import os

correspondance_couleur = {0 : Fore.WHITE, 1 : Fore.GREEN, 2 : Fore.CYAN, 3 : Fore.BLUE, 4 : Fore.YELLOW, 5 : Fore.MAGENTA, 6 : Fore.RED, 7 : Fore.RED, 8 : Fore.RED}

def creerGrille(N, M, v=0):
    return [[v for j in range(M)] for i in range(N)]  # Fonction pour crée la grille


def placerMines(grille, N, M, X, l, c):  # Fonction pour placer les mines aléatoirement
    cpt = 0
    while cpt != X:
        ligne = rd.randint(0, N - 1)
        case = rd.randint(0, M - 1)
        while (ligne == l and case == c) or grille[ligne][case] == 1 or (
                ligne == l and case == c + 1) or (ligne == l and case == c - 1) or (
                ligne == l - 1 and case == c - 1) or (
                ligne == l - 1 and case == c) or (ligne == l - 1 and case == c + 1) or (
                ligne == l + 1 and case == c - 1) or (
                ligne == l + 1 and case == c) or (ligne == l + 1 and case == c + 1):
            ligne = rd.randint(0, N - 1)
            case = rd.randint(0, M - 1)
        grille[ligne][case] = 1
        cpt += 1

def clear_console():
    os.system('clear')

def afficheSolution(grille):  # Fonction pour afficher la solution
    print(Style.RESET_ALL, end='')
    print(' ' * 3, end='')
    for i in range(len(grille[0])):
        sepa = ' ' * (3 - len(str(i + 1)))
        print(i + 1, end=sepa)
    print('\n')
    for l in range(len(grille)):
        sepa = ' ' * (3 - len(str(l + 1)))
        print(l + 1, end=sepa)
        for c in range(len(grille[l])):
            sepa2 = ' ' * 2
            if grille[l][c]:
                print(Back.RED + '*', end='')
                print(Style.RESET_ALL, end=sepa2)
            else:
                print('-', end=sepa2)
        print('')


def testMine(grille, l, c):  # Fonction qui permet de tester si une mine ce trouve sur cette case
    if grille[l][c] == 1:
        return True
    else:
        return False


def compteMinesVoisines(grille, l,
                        c):  # Fonction qui permet de compter le nombre de mine adjacente a la case choisi
    nbVoisines = 0
    for i in range(l - 1, l + 2):
        for j in range(c - 1, c + 2):
            if i >= 0 and i < len(grille) and j >= 0 and j < len(grille[l]):
                nbVoisines += grille[i][j]
    return nbVoisines


def afficheJeu(grille, casesD,
               drapeau):  # Fonction qui permet d'afficher le jeu aprer chaque tour et qui contient le code de colorama
    clear_console()
    print(Style.RESET_ALL, end='')
    print(' ' * 3, end='')
    for i in range(len(grille[0])):
        sepa = ' ' * (3 - len(str(i + 1)))
        print(i + 1, end=sepa)
    print('\n')
    for l in range(len(grille)):
        sepa = ' ' * (3 - len(str(l + 1)))
        print(l + 1, end=sepa)
        for c in range(len(grille[l])):
            sepa2 = ' ' * 2
            if casesD[l][c]:
                if grille[l][c]:
                    print(Back.RED + '*', end='')
                    print(Style.RESET_ALL, end=sepa2)
                else:
                    val = compteMinesVoisines(grille, l, c)
                    if val != 0:
                        print(correspondance_couleur.get(val) + str(val), end=sepa2)
                    else:
                        print(' ', end=sepa2)
                print(Style.RESET_ALL, end='')

            elif drapeau[l][c]:
                print(Back.WHITE + Fore.BLACK + '!', end='')
                print(Style.RESET_ALL, end=sepa2)

            else:
                print('?', end=sepa2)
        print(Style.RESET_ALL)


def getCoords(casesD, N, M):  # Fonction qui permet de demander a l'utilisateur la case qu'il veux choisir
    print('À toi de jouer !')
    casePrise = True
    while casePrise:
        l = input("Choisissez une ligne ? ")
        while not l:
            l = input("Choisissez une ligne ?")
        l = int(l) - 1
        c = input('Choisissez une colonne ? ')
        while not c:
            c = input("Choisissez une colonne ?")
        c = int(c) - 1
        while (not 0 <= l <= N - 1):
            l = int(input('0 ≤ ligne <', N, 'svp ? '))
        while (not 0 <= c <= M - 1):
            c = int(input('0 ≤ colonne <', M, 'svp ? '))
        if casesD[l][c]:
            print('La case est déjà dévoilée, veuillez recommencez !')
        else:
            casePrise = False
    return l, c


def victoire(grille, casesD, N, M):  # Fonction qui permet de definir si le joueur a gagner ou non
    for l in range(N):
        for c in range(M):
            if not grille[l][c] and not casesD[l][c]:
                return False
    return True


def decouvreCase(grille, casesD, l, c, add, listeToDecouvre):  # Fonction qui permet de découvrire la case
    for i in range(l - 1, l + 2):
        for j in range(c - 1, c + 2):
            if i >= 0 and i < len(grille) and j >= 0 and j < len(grille[l]):
                add.append([i, j])
                if compteMinesVoisines(grille, i, j) == 0 and not grille[i][j]:
                    if not casesD[i][j]:
                        listeToDecouvre.append([i, j])
                casesD[i][j] = True


def decouvreCoter(grille, casesD, l,
                  c):  # Fonction qui permet de découvrire toute les case autour de la case séléctioner
    add = []
    ligne = l
    case = c
    listeToDecouvre = [[ligne, case]]
    while len(listeToDecouvre) != 0:
        for i in listeToDecouvre:
            ligne = i[0]
            case = i[1]
            if ligne == l and case == c:
                decouvreCase(grille, casesD, ligne, case, add, listeToDecouvre)
                listeToDecouvre.remove([ligne, case])
            elif casesD[ligne][case] and grille[ligne][case] == 0 and compteMinesVoisines(grille, ligne, case) == 0:
                decouvreCase(grille, casesD, ligne, case, add, listeToDecouvre)
                listeToDecouvre.remove([ligne, case])
    for i in add:
        casesD[i[0]][i[1]] = True


# PROGRAMME PRINCIPAL
# création du menu

def jouer_jeux():  # fonction pour choisir si on veut jouer ou quitter et choisire les différents niveaux : Simple, Medium, Difficile et Personnalisé
    global N, M, X
    jouer = str(input("Veux tu jouer ou quitter ?\n"
                      "1:Jouer\n"
                      "2:Quitter\n"))
    if jouer == "1":
        niveau = str(input("Quel niveaux choisis-tu ?\n"
                           "1:Simple\n"
                           "2:Medium\n"
                           "3:Difficile\n"
                           "4:Personnalisé\n"))
        if niveau == "1":
            N = 9
            M = 9
            X = 10
            print("Vous avez choisi le mode Simple ! Le jeux vas commencer")
        elif niveau == "2":
            N = 16
            M = 16
            X = 40
            print("Vous avez choisi le mode Medium ! Le jeux vas commencer")
        elif niveau == "3":
            N = 30
            M = 16
            X = 99
            print("Vous avez choisi le mode Difficile ! Le jeux vas commencer")
        elif niveau == "4":
            print("Vous avez choisi le mode Personnalisé ! Configurer vôtre partie !\n")
            N = int(input("Combien de ligne voulez vous ?\n"))
            M = int(input("Combien de colone voulez vous ?\n"))
            X = int(input("Combien de mine voulez vous ?\n"))
        else:
            print("\nVous n'avez choisi aucun mode ! Veuillez choisir le mode 1, 2, 3 ou 4 !\n")
            return jouer_jeux()
    else:
        print("A bientôt")
        exit()


jouer_jeux()
grille = creerGrille(N, M)  # Appele de la fonction pour créer la grille
drapeau = creerGrille(N, M)

# Premier coup
nbCoups = 1
print('\nCoup numéro', nbCoups)
casesD = [[False for j in range(M)] for i in range(N)]
afficheJeu(grille, casesD, drapeau)
l, c = getCoords(casesD, N, M)
casesD[l][c] = True
placerMines(grille, N, M, X, l, c)
if compteMinesVoisines(grille, l, c) == 0:
    decouvreCoter(grille, casesD, l, c)

perdu = False
gagne = victoire(grille, casesD, N, M)

# Tour de jeu
while not gagne and not perdu:
    print('\nCoup numéro', nbCoups)
    afficheJeu(grille, casesD, drapeau)
    drap = input(
        'Placer un drapeau ?\n⏎ : Pour ignorer \n1 : Pour placer \n0 : Pour enlever un drapeau')
    l, c = getCoords(casesD, N, M)
    if drap == '':
        nbCoups += 1
        casesD[l][c] = True
        if testMine(grille, l, c):
            perdu = True
        if compteMinesVoisines(grille, l, c) == 0 and not perdu:
            decouvreCoter(grille, casesD, l, c)
        gagne = victoire(grille, casesD, N, M)
    elif drap == '1':
        drapeau[l][c] = 1
    elif drap == '0':
        drapeau[l][c] = 0
    else:
        print("Vous n'avez fais aucun choix !")

if gagne:  # Si toute les case sont découvert sauf les bombe alors il gagne au contraire il touche une mine et il peut rejouer ou quitter si il le shouaite
    print('\nBravo, tu gagnes en', nbCoups, 'coups !\n')
    casesD = [[True for j in range(M)] for i in range(N)]
    afficheJeu(grille, casesD, drapeau)
    nom = input('Quel est ton nom ?\n')

else:
    print('\nPerdu, touché une mine !')
    print('\nTon jeu :')
    afficheJeu(grille, casesD, drapeau)
    print('\nLa solution était :')
    afficheSolution(grille)

jouer_jeux()