import numpy as np
from matplotlib import pyplot as plt
from math import *
from random import *
import time
from thomas.couleur import hsv2rgb

def collage(C,c):
    """C c en rgba int
    C dessous
    c dessus"""
    r,g,b,a=c
    R,G,B,A=C
    r,g,b,R,G,B=int(r),int(g),int(b),int(R),int(G),int(B)
    x=min(A,255-a)
    aa=min(255,a+A)
    if a==0 and x==0:
        return 0,0,0,0
    else:
        rr=int((r*a + R*x)/((a+x+1)))
        rr=int(r*(a/(a+x)) + R*(x/(a+x)))
        gg=int((g*a + G*x)/((a+x+1)))
        bb=int((b*a + B*x)/((a+x)))
        return rr,gg,bb,aa





"""
A nombres de trucs sur la meme couronne
R nombre de courronnes


Rmin debut des taches
Rtot plage des taches

il faut  rmin+rtot<l sinon cringe
"""
skin='#test'
name='3'
plus=''


A=1
R=1

RMIN=100
RANGE=300

L=(RMIN+RANGE)*2+1


transparence=128
taille_radiale=10
taille_angulaire=pi/3

I=np.zeros((L,L,4),dtype='uint8')
def alpha(x,y):
    '''alpha pour (x,y) entre les angles a et b de rayon r a s'''
    d=8
    alpha=0
    for dx in range(x*d,(x+1)*d):
        dx=dx/d-L/2
        for dy in range(y*d,(y+1)*d):
            dy=dy/d-L/2
            if r1<=sqrt(dx**2+dy**2)<=r2 and a1<=atan2(dx,dy)<=a2:
                alpha+=1

    return int(transparence*alpha/d/d)

def taches(ka,kr):
    """generateur de taches
    renvoie une nliste de (rmin ramax amin amax r g b)

    a dans [-pi;pi]
    r dans ]0;L/2[
    rgb en uint8 c l a s s i q u e"""

    da=2*pi / ka
    dr=RANGE/kr


    T=[]
    for i in range(kr):
        #todo mettre un truc pour decaler tous les a sur un couronne (pour pas voir les cases)
        for j in range(ka):
            r=abs(gauss(taille_radiale,0.1)) #taille radiale

            rmin=uniform(i*dr,i*dr +dr -5)+RMIN


            rmax=rmin+r


            a=abs(gauss(taille_angulaire,0.3)) #taille angulaire
            amin=max(-pi,uniform(j*da,j*da+da)-pi)

            amax=min(amin+a,pi)


            r,g,b=hsv2rgb((randint(0,359),1,1))

            T.append((rmin,rmax,amin,amax,r,g,b))

    return T



