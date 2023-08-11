# INSTRUCTIONS POUR DL LE LOGICIEL

dl dans osk :
    visual.py
    cercle.py
    data.py

tout mettre dans le meme dossier 
changer le deuxième bloc d'import pour :


import matplotlib.pyplot as plt
from cercle import *
from data import *

def multiline(*lines) :
    S = lines[0]
    for line in lines[1:] :
        S = S + '\n' + line
    return S

# oui la fonction aussi il faut la prendre
