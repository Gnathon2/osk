"""Pour fabriquer des cercles pour osu!, verion ultime.

r = rayon en pixels
n = taille d'image en pixels
a = alpha en [0;1]
e = epaisseur
th = angle en radians

f : r |-> alpha(r)

R,G,B : [0; 1]
l,c = indices ligne colonne

"""
# TODO Fclr avec 3 cannaux (h,s,v a priori)
# TODO faire en sorte que Fclr et Falpha prennent les memes args (r,th)

from math import sqrt, exp,sin, inf, atan2, pi
import numpy as np
from thomas import plt, plage
from thomas.couleur import hsv2rgb

rayon = lambda l,c : sqrt(l**2 + c**2)


def integrale(l,c,f_rayon, acc=8) :
    """fait des integrales, toujours pas de nom pixel malheureusement"""
    S = 0
    for dl in range(acc):
        ll = l + dl/acc
        for dc in range(acc):
            cc = c + dc/acc
            r = rayon(ll,cc)
            S += f_rayon(r)
    return S / (acc**2)


def cercleur(falpha,fcouleur,npix : int) :
    """crée une image nxn en rgba (0,1) probablement en forme de cercle

    falpha : r |-> α
    fcouleur : l,c |-> r,g,b
    """
    I = np.zeros((npix,npix,4), dtype='float32')
    n = npix//2
    for l in range(npix):
        x = l - n
        for c in range(npix):
            y = c - n
            A = integrale(x,y,falpha)
            R,G,B = fcouleur(x,y)
            assert 0 <= R <= 1
            I[l,c] = [R,G,B,A]
    return I


def alphaffiche(*Images):
    plt.clf()
    for I in Images:
        n = I.shape[0]//2
        plt.plot(I[n:n+1, n:, 3][0])
    plt.show()
    plt.close()

def falphaffiche(*funcs,rmax,dr = 1) :
    plt.clf()
    R = list(plage(0,rmax,dr))
    for f in funcs:
        A = [f(r) for r in R]
        plt.plot(R,A)
    plt.show()
    plt.close()


# def teinture(I,rgb) :
#     """ I en uint8"""
#     M = I.copy().astype('float32')
#     r,g,b = rgb

#     rgba = np.array([r,g,b,1])
#     for ligne in M :
#         for pix in ligne :
#             pix *= rgba
#     return M

def teinture(Img, rgb) :
    """Teint Img un array de pixel en float32 [0;1] (rgb)."""

    clr = np.array([[list(rgb) + [1.0]]])
    M = Img * clr
    return M

def showcircle(overlay, circle, clr) :
    plt.figure().set_facecolor((0,0,0))
    plt.axis('off')
    plt.imshow(teinture(circle,clr))
    plt.imshow(overlay)
    plt.show()
    plt.close()


## deco

def sup(func,rmax):
    def f(r):
        return func(r) if r<rmax else 0
    return f

def inf_(func,rmin):
    def f(r):
        return func(r) if rmin<=r else 0
    return f

def borne(func,rmin,rmax):
    def f(r):
        return func(r) if rmin<=r<rmax else 0
    return f

def antioverflow(func,amax,amin):
    return lambda r : min(amax,max(amin,func(r)))

def ascale(func,amin,amax) :
    """[0; 1] -> [amin; amax]"""
    return lambda r : func(r)*(amax-amin) + amin

## ope

def double(f1,rlim,f2,*,xy=False):
    if xy :
        def f(x,y) :
            r = sqrt(x**2+y**2)
            return f1(x,y) if r<rlim  else f2(x,y)
    else :
        f = lambda r : f1(r) if r<rlim else f2(r)
    return f

def triple(f1,r1,f2,r2,f3,*,xy=False):
    if xy :
        def f(x,y) :
            r = sqrt(x**2+y**2)
            if r < r1 : return f1(x,y)
            elif r < r2 : return f2(x,y)
            else : return f3(x,y)
    else :
        def f(r) :
            if r < r1 : return f1(r)
            elif r < r2 : return f2(r)
            else : return f3(r)
    return f

def oignon(*rlim_f,xy=False) :
    """fait des couronnes de f(...) a partir de rlim"""
    rlim_f = sorted(rlim_f, key = lambda x:x[0] if x[0]!=None else 0)
    if xy :
        def g(x,y) :
            r = sqrt(x**2+y**2)
            ref = rlim_f[0][1]
            for rlim,f in rlim_f :
                if rlim < r : ref = f
            return ref(x,y)
    else :
        def g(r) :
            ref = rlim_f[0][1]
            for rlim,f in rlim_f :
                if rlim < r : ref = f
            return ref(r)
    return g



def compose(*ARG):
    tup = ARG[-1]
    f = tup[0]
    arg = tup[1:]
    func = f(*arg)

    for tup in reversed(ARG[:-1]):
        f = tup[0]
        arg = tup[1:]
        func = f(func,*arg)
    return f

## ALPHA

def cst(alpha=None):
    if alpha==None : alpha = 1
    return lambda r : alpha

def gradient(pente,ordalor):
    assert pente!=None and ordalor!=None
    return lambda r : pente*r + ordalor

def gauss(sigma,puiss=None,mu=None):
    """
    sigma # etale
    mu # centre 
    """
    assert sigma!=None
    if puiss == None : puiss = 2
    if mu == None : mu = 0

    return lambda r : exp(-abs((r-mu)/sigma)**puiss)

def sinus(omega,phi=0):
    return lambda r : (sin(omega*r + phi) + 1) / 2

class Falpha :
    def __init__(self, fbase, amin = None, amax = None, rmin =None, rmax = None,aext=None) :
        if amin == None : amin = 0
        if amax == None : amax = 1
        if rmin == None : rmin = 0
        if rmax == None : rmax = inf
        if aext == None : aext = 0
        self.f = fbase
        self.a = (amin,amax)
        self.aext= aext
        self.r = (rmin,rmax)
            
    def __call__(self, r) :
        rmin,rmax = self.r
        if not rmin <= r <= rmax  :
            a = self.aext
        else :
            amin,amax = self.a
            a = self.f(r)
            if a < 0 : a = 0
            if a > 1 : a = 1
            a = a*(amax - amin) + amin
            assert amin <= a <= amax
        return a
    
    def data(self) :
        return f"a : {self.a}, r : {self.r}, aext : {self.aext}"

def fa_anneau_plain(alpha, rmax, epais = None) :
    '''crée un anneau blanc avec la data donnée'''
    if epais == None : epais = rmax
    f = Falpha(cst(alpha), rmin = rmax - epais, rmax = rmax)
    return f

def fa_anneau_grad(amin,amax,rmax,epais=None) :
    if epais == None : epais = rmax
    rmin = rmax - epais
    pente = (amax - amin) / epais
    ordalor = amin - pente*rmin
    amin,amax = sorted([amin,amax])
    return Falpha(gradient(pente,ordalor),amin,amax,rmin,rmax)

def fa_disque_gauss(sigma, puiss, rmax, amin,amax) :
    """Disque à la bloomoon"""
    f = Falpha(gauss(sigma,puiss),amin,amax,rmax = rmax )
    return f


## COULEURS 


def plain(r,g,b):
    if r==g==b==None :
        rgb = (1,1,1)
    elif r==None or g==None or b==None :
        raise TypeError('None non expecté(s)')
    else :
        rgb = (r,g,b)
    return lambda *args : rgb


def radhue(s=None,v=None,phi=None) :
    if s==None : s = 1
    if v==None : v = 1
    if phi==None : phi = 0

    def f(l,c) :
        h = (phi + atan2(l,c)) / (2 * pi)
        if h<0 : h = 0
        elif h>1 : h=1
        return hsv2rgb((h,s,v))
    
    return f

## USINES

def anneau_plain(npix,rmax,epais = None, alpha = 1, clr = (1,1,1)) :
    fa = fa_anneau_plain(alpha,rmax,epais)
    fclr = plain(clr)
    return cercleur(fa,fclr,npix)

def megafunc(npix , amode=None, a1=None, a2=None, a3=None, 
             clrmode = None, c1=None, c2=None,c3=None, * ,
             amin = None, amax = None, 
             rmin = None,rmax = None, 
             aext = None, ) :
    """Une fonction pour les gouverner toutes."""
    # TODO gestion des multi

    def deballeur(x,xy:bool) :
        _,mode,a,b,c = x

        if mode == 'double' :
            f,g = deballeur(a),deballeur(b)
            r =b[0]
            f = double(f,r,g,xy=xy)
        elif mode == 'triple' :
            f,g,h = deballeur(a),deballeur(b),deballeur(c)
            r1,r2 = b[0], c[0]
            f = triple(f,r1,g,r2,h,xy=xy)
        elif mode == 'plain' :
            f = plain(a,b,c)
        elif mode == 'radhue' :
            f = radhue(a,b,c)
        elif mode == 'gauss' :
            f = gauss(a,b,c)
        elif mode == 'gradient' :
            f = gradient(a,b) 
        elif mode == 'constant' :
            f = cst(a)
        else :
            raise ValueError(f'mode "{mode}" inconnu')
        return f
    
    if clrmode == None : clrmode = 'plain'
    fclr = deballeur((None,clrmode,c1,c2,c3),True)

    if amode == None : amode = 'constant'
    fbase = deballeur((None,amode,a1,a2,a3),False)
    if rmax==None : rmax = int(npix/2 - 1)
    falpha = Falpha(fbase, amin, amax, rmin, rmax, aext)

    return cercleur(falpha, fclr, npix)