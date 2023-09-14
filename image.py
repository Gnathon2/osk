from osk.cercle import *

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



def resize(tupl, taille : int) :
    tup = tupl[:taille]
    return tup + (None,) * (taille - len(tup))
    

def adeballeur(amode, aargs) :
    if amode == None : amode = 'constant'
    AFONC = { # mode : (fonc, n_args)
        'constant' : (cst, 1),
        'gauss' : (gauss, 3),
        'gradient' : (gradient, 2),
    }
    if amode == 'multi' :
        rlim_f = []
        for rlim,mode,args in aargs :
            f = adeballeur(mode,args)
            rlim_f.append((rlim, f))
        fbase = oignon(*rlim_f, xy=False)
    else :
        f, n = AFONC[mode]
        args = resize(aargs, n)
        fbase = f(args)
    return fbase

def cdeballeur(cmode,cargs) :
    if cmode == None : cmode = 'plain'
    CFONC = {
        'plain' : (plain, 3),
        'radhue' : (radhue, 3),
    }
    if cmode == 'multi' :
        rlim_f = []
        for rlim,mode,args in cargs :
            f = adeballeur(mode,args)
            rlim_f.append((rlim, f))
        fbase = oignon(*rlim_f, xy=True)
    else :
        f, n = CFONC[mode]
        args = resize(cargs, n)
        fbase = f(args)
    return fbase


def F(  npix : int, 
        amode : str, aargs : tuple, 
        cmode : str, cargs : tuple, 
        rmin : float, rmax, amin, amax, aext) :

    fbase = adeballeur(amode, aargs)
    falpha = Falpha(fbase,amin,amax,rmin,rmax,aext)
    fclr = cdeballeur(cmode,cargs)

    return cercleur(falpha,fbase,npix)
    
    
    



