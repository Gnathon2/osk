import numpy as np
from matplotlib import pyplot as plt
from thomas import affiche,Acouleur
import random as rd

model=plt.imread('menuboutton.png')



def menubt(skin):
    C=1400
    L=187

    a=200
    z=0
    x=25
    I=np.zeros((L,C,4),dtype='uint8')

    for l in range(L):
        for c in range(C):
            if c<x:
                I[l,c]=[255,255,255,255]
            # elif l<z:
            #     I[l,c]=[255,255,255,0]
            else:
                I[l,c]=[255,255,255,0]



    for l in range(L):
        for c in range(C):
            I[l,c]=[255,255,255,rd.randint(0,int(max(0,255*(-1 + 2 *c/C ))))] #- (abs(-L/2  + l))/L
    plt.imsave(skin+'/menu-button-background@2x.png',I)


    return I

menubt("#test")
