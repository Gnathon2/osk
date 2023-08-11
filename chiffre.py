from math import pi
from osk.cercle import integrale
from thomas import plt
import numpy as np




def genere_alphargs(n,r,t,gap,th0=0):
    """ => rmin,rmax,thetas """
    thetas=[]
    rmin=r-t
    if n==0:
        rmin=0
    elif n>1:
        # gap*=n
        delta=2*pi/n
        for i in range(n):
            T1=delta*i + th0 +pi*gap/2
            T2=T1+delta*(1-gap)

            T1=(T1+pi)%(2*pi) - pi
            T2=(T2+pi)%(2*pi) - pi
            thetas.append((T1,T2))
    return rmin,r,thetas



rad=pi/180
R0=35
R1=35
R2=65
T=10
G=0.3
kalpha=1/2
#en pourcentage de vide qu'en flat gap

L=(R2+T)*2

couleur=[255,255,255]

zero=[genere_alphargs(0,R0,T,G)]

un=[genere_alphargs(1,R2,T,G)]

deux=[genere_alphargs(1,R1,T,G),
            genere_alphargs(1,R2,T,G)]
trois=[genere_alphargs(1,R1,T,G),
            genere_alphargs(2,R2,T,G)]
quatre=[genere_alphargs(2,R1,T,G),
            genere_alphargs(2,R2,T,G,pi/2)]
cinq=[genere_alphargs(2,R1,T,G,pi/2),
            genere_alphargs(3,R2,T,G)]
six=[genere_alphargs(3,R1,T,G),
            genere_alphargs(3,R2,T,G,pi)]
sept=[genere_alphargs(3,R1,T,G,pi),
            genere_alphargs(4,R2,T,G)]
huit=[genere_alphargs(4,R1,T,G),
            genere_alphargs(4,R2,T,G,pi/4)]
neuf=[genere_alphargs(4,R1,T,G,pi/4),
            genere_alphargs(5,R2,T,G)]


YES=[zero,un,deux,trois,quatre,cinq,six,sept,huit,neuf]

for i in range(10):
    oui=YES[i]
    image=np.zeros((L,L,4),dtype='uint8')


    def f(i,j):
        x=abs(i+j*1j)
        A=0
        for rmin,rmax,TH in oui:
            if rmin-1<=x<=rmax+1:
                if TH!=[]:
                    a=1
                    A+=sum([integrale(i,j,rmin=rmin,rmax=rmax,thetas=th) for th in TH])
                else:
                    A+=integrale(i,j,rmax=rmax,rmin=rmin)
        return A
    for l in range(L):
        for c in range(L):
            image[l,c]=couleur+[f(l-L//2,c-L//2)*kalpha]
    plt.imsave(f'#test/chiffre-{i}@2x.png',image)






