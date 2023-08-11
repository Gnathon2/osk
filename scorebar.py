import numpy as np
import matplotlib.pyplot as plt



def scorebar(long,large,epais,*couleurs,**KW):
    """Pour fabriquer:
    scorebar-color
    scorebar-bg

    #ARGS

    'epais' -> l'épaisseur du bord de bg
    par défaut le bord suivra les mêmes couleurs que color

    'couleurs' -> de gauche à droit les couleurs de scorebar-color
    (couleur de la forme [r,g,b,a] en uint8 )

    #'KW'
    'adresse' -> pour save les images génerées (en png) (simplement le nom du skin)
    'bords' -> liste des couleurs du bg

    #TODO:
    dégradés
    un color creux
    """
    if 'bords' in KW:
        bcouleurs=KW['bords']
    else:
        bcouleur=couleurs

    fond=[50,50,50,255]
    #mode segment

    color=np.zeros((large,long,4),dtype='uint8')
    n=long//len(couleurs)

    h=16 #correcteur en hauteur
    b=5 #correcteur du bord


    bg=np.zeros((large+h+2*epais,long+2*epais+b,4),dtype='uint8')
    m=(long+epais)//len(bcouleurs)



    for l in range(large):
        for k in range(len(couleurs)):
            couleur=couleurs[k]

            for c in range(k*n,k*n+n):
                color[l,c]=couleur
                bg[l+h,c+b]=fond
        for c in range(epais):
            bg[l+h,k*n+n+c+b]=bcouleurs[-1]


    for l in range(h-epais,h):

        for k in range(len(bcouleurs)):
            couleur=bcouleurs[k]
            for c in range(k*m,k*m+m):
                bg[l,c+b]=couleur
                bg[l+large+epais,c+b]=couleur



    if 'affiche' in KW and KW['affiche']:
        plt.figure('full life')
        plt.imshow(bg)
        plt.imshow(color)

        plt.figure('low life')
        plt.imshow(bg)

        plt.show()

    if 'adresse' in KW:
        plt.imsave(KW['adresse']+"/scorebar-colour.png",color)
        plt.imsave(KW['adresse']+"/scorebar-bg.png",bg)


scorebar(451,10,1,[128,171,255,200],[255,127,137,200],adresse='Taiko',bords=[[0,0,0,255]],affiche=True)
