import numpy as np
import os
from thomas import plt

def sauveur2x(skin,objet,I):
    try:
        plt.imsave(f"{dossier_skin}{skin}/{objet}@2x.png",I)
        print("{objet}@2x sauvé")
    except FileNotFoundError:
        os.mkdir(str(skin)) # crée le dossier
        print("{skin} créé")
        plt.imsave(f"{dossier_skin}{skin}/{objet}@2x.png",I)
        print("{objet}@2x sauvé")

def sauveur(skin,objet, I):
    try:
        plt.imsave(f"{dossier_skin}{skin}/{objet}.png",I)
        print("{objet} sauvé")
    except FileNotFoundError:
        os.mkdir(str(skin)) # crée le dossier
        print(f'{skin} créé')
        plt.imsave(f"{dossier_skin}{skin}/{objet}.png",I)
        print("{objet} sauvé")

    
dossier_osu = r"C:\Users\Thomas\AppData\Local\osu!"
dossier_skin = dossier_osu + r'\Skins'
BLANK = np.zeros((1,1,4))

approach = 'approachcircle'
circle = 'hitcircle'
overlay = 'hitcircleoverlay'
select = 'hitcircleselect'

slistart = 'sliderstartcircle'
slistartoverlay = 'sliderstartcircleoverlay'
sliend = 'sliderendcircle'
sliendoverlay = 'sliderendcircleovelay'
followcircle = 'sliderfollowcircle'
ball = 'sliderb'
point = 'sliderscorepoint'
arrow = 'reversearrow'

SPIN = ['spinner-approachcircle','spinner-rpm','spinner-clear',]
SPIN1 = ['spinner-background','spinner-circle','spinner-metre','spinner-osu']
SPIN2 = ['spinner-glow','spinner-bottom','spinner-top','spinner-middle2','spinner-middle']

followpoint = 'followpoint'

blanked = ['comboburst','lightning',sliend,sliendoverlay,'spinner-spin','particle50','particule100','particule300']
blanked2 = ['hit300-0','hit300g-0','hit300k-0','star2']

cursor = 'cursor'
trail = 'cursortrail'
smoke = 'cursor-smoke'
middle = 'cursormiddle'


# TODO
'''
CIRCLE GAUSS
OVERLAY DEGRAD2
OVERLAY TRANS
CIRCLE GLOW

BALL GAUSS
BALL0
BALL REVERSE GAUSS

FOLLOWC0
APPROACH0

THETARCENCIEL


FOLLOWPOINT (fonction complète)
SKIN.INI

COULEURS (BLANC)

'''
blanc = (1,1,1)
noir = (0,0,0)


# from wiki skinning
n_approach = 126 * 2
r_approach = 126
n_circle = n0 = 128 * 2
r_circle = r0 = 118
n_follow = 256 * 2
r_follow = 256
n_point = 16 * 2
r_point = 16

e_circle = e0 = 15

aopaque = a0 = 1

NPIX = {
    overlay : n0,
    circle : n0,
    approach : n_approach,
    cursor : 200,
    trail : 200,
}