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