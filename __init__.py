# osk/__init__.py

import os
from matplotlib.pyplot import imsave 


DOSSIER_OSU = r"C:\Users\Thomas\AppData\Local\osu!"
DOSSIER_SKIN = DOSSIER_OSU + r'\Skins'


def sauveur2x(skin,objet,I):
    try:
        imsave(f"{DOSSIER_SKIN}{skin}/{objet}@2x.png",I)
        print("{objet}@2x sauvé")
    except FileNotFoundError:
        os.mkdir(str(skin)) # crée le dossier
        print("{skin} créé")
        imsave(f"{DOSSIER_SKIN}{skin}/{objet}@2x.png",I)
        print("{objet}@2x sauvé")

def sauveur(skin,objet, I):
    try:
        imsave(f"{DOSSIER_SKIN}{skin}/{objet}.png",I)
        print("{objet} sauvé")
    except FileNotFoundError:
        os.mkdir(str(skin)) # crée le dossier
        print(f'{skin} créé')
        imsave(f"{DOSSIER_SKIN}{skin}/{objet}.png",I)
        print("{objet} sauvé")
