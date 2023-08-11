"""visual.py
Pour visualiser le skin ig avant de sauvegarder (full interface quoi)"""


# TODO chiffre
# TODO perfectstack : un autre cercle en dessous
# TODO slider (pour les couleurs) (moyen accurate mais osef)
# TODO Un 'copy' dans HELP pour set directement le truc concerné
# TODO spinner 
# TODO onoff pour curseurs et cercles (pour cumuler les deux)
# (pouvoir déplacer le centre du curseur)

from tkinter import *
from tkinter import ttk
import pygame as pg
import shutil

from cercle import *
from osk.data import *
from osk.data import plt
from thomas.builtins import multiline


tinted = '-tinted'
tint = 'tint'
aide = 'help'
genlabel = multiline('amin','amax','rmin','rmax','aext')
AMODES = ['constant', 'gauss', 'gradient']
CMODES = ['plain','radhue']

BG = {
    'fen' : '#000000', 
    'txt' : '#ffffff',
    circle : '#000055',
    overlay: '#551100',
    approach: '#330055',
    tint : '#005555',
    cursor : '#555500',
    trail : '#552211',
    'help1' : '#008899',      
}


def rescale(surf, k) :
    return pg.transform.scale(surf, k*pg.Vector2(surf.get_rect().size))

def filename(item, skin = None) :
    """renvoie le chemin exact en absolu de 'item' dans 'skin'
    ou Skins si None"""
    if skin == None :
        return rf"{dossier_skin}\{item}@2x.png"
    else :
        return rf"{dossier_skin}\{skin}\{item}@2x.png"

def copypasta(skin,*items):
    for item in items :
        shutil.copyfile(filename(item), filename(item, skin))

def sauvegarder() :
    """commande de sauvegarde (actually copier coller)"""
    skin = entry_skin.get()
    if ONOFF[circle].getbool() :
        copypasta(skin, overlay, circle, approach)
    if ONOFF[cursor].getbool() :
        copypasta(skin, cursor, trail)    
    print(f"saved in '{skin}'")


def centerblit(surf,x=0,y=0) :
    """blit surf tq centre de surf en (x,y) % au centre de screen"""
    rect = surf.get_rect()
    xx,yy = screen.get_rect().center
    xx += x
    yy += y
    rect.center = (xx,yy)
    screen.blit(surf,rect)

def grayfill(shade) :
    screen.fill((shade,)*3)
    pg.display.flip()
    
def fresh() :
    'peut planter'

    surf_over = pg.image.load(filename(overlay+tinted)).convert_alpha()
    surf_hit = pg.image.load(filename(circle+tinted)).convert_alpha()
    surf = pg.image.load(filename(approach+tinted)).convert_alpha()
    surf_appr = pg.transform.scale(surf, 2*pg.Vector2(surf.get_rect().size))

    grayfill(0)
    centerblit(surf_hit)
    centerblit(surf_over)
    centerblit(surf_appr)
    pg.display.flip()

def refresh_circle() :
    """actualise le visuel (pygame) à partir de la data interface"""
    grayfill(120) #pour voir que ça avance
    surf_over = update_circular(overlay)
    grayfill(80)
    TINT = get_tint()
    surf_hit = update_circular(circle, TINT)
    grayfill(40)
    surf_appr = update_circular(approach, TINT)
    surf_appr = rescale(surf_appr,2)
    grayfill(0) 
    centerblit(surf_hit)
    centerblit(surf_over)
    centerblit(surf_appr)
    pg.display.flip()
    print('circle refreshed')

def refresh_curseur() :
    grayfill(80) 
    surf_cursor = update_circular(cursor)
    grayfill(40) 
    # middle = combo_middle.get() == 'on'
    surf_trail = update_circular(trail)
    grayfill(0)
    for x in [-170,-100, -50,-30,-10,-7,-2,0] :
        centerblit(surf_trail, x = x)
    centerblit(surf_cursor)
    pg.display.flip()
    print('curseur refreshed')

def refresh(*,circle_on=None,cursor_on=None) :
    if circle_on == None : circle_on = ONOFF[circle].get()
    if cursor_on == None : cursor_on = ONOFF[cursor].get()
    grayfill(0)
    if circle_on :
        surf_over = update_circular(overlay)
        tint = get_tint()
        surf_hit = update_circular(circle, tint)
        surf_appr = update_circular(approach, tint)
        surf_appr = rescale(surf_appr,2)
        centerblit(surf_hit)
        centerblit(surf_over)
        centerblit(surf_appr)
        print("circle refreshed")
    if cursor_on :
        surf_cursor = update_circular(cursor)
        surf_trail = update_circular(trail)
        for x in [-170,-100, -50,-30,-10,-7,-2,0] :
            centerblit(surf_trail, x = x)
        centerblit(surf_cursor)
        print("cursor refreshed")
    pg.display.flip()



def recup(entry, default = None) :
    x = entry.get()
    try :
        x = float(x)
    except :
        x = default
    return x

def update_circular(item, tint=None) :
    """recupère la data dans l'interface pour l'overlaycircle
    renvoie ce dernier sous forme de pg.Surface"""
    
    data = TK[item]

    rmin = recup(data['rmin'])
    rmax = recup(data['rmax'])
    amin = recup(data['amin'])
    amax = recup(data['amax'])
    aext = recup(data['aext'])
    amode = data['amode'].get()
    a1 = recup(data['a1'])
    a2 = recup(data['a2'])
    a3 = recup(data['a3'])
    clrmode = data['cmode'].get()
    c1 = recup(data['c1'])
    c2 = recup(data['c2'])
    c3 = recup(data['c3'])

    crowns = CROWN[item]
    if len(crowns) :
        # print(f'crowned {item}')
        a1 = (None,amode,a1,a2,a3)
        c1 = (None,clrmode,c1,c2,c3)
        a2,c2 = get_crown(crowns[min(crowns)])
        amode = clrmode = 'double'
        a3 = c3 = None
        if len(crowns) > 1 :
            a3,c3 = get_crown(crowns[max(crowns)])
            amode=clrmode='triple'

    array = megafunc(
        NPIX[item],amode,a1,a2,a3,clrmode, c1,c2,c3,
        amin=amin,amax=amax,rmin=rmin,rmax=rmax,aext=aext
    )
    array_tinted = array if tint==None else teinture(array, tint)
    plt.imsave(filename(item), array)
    plt.imsave(filename(item + tinted), array_tinted)
    surf = pg.image.load(filename(item+tinted)).convert_alpha()
    return surf


def get_tint() :
    data = TK[tint]
    mode = data['combo'].get()
    if mode == 'rgb' :
        # r = recup(entry_tint_rh,1)
        # g = recup(entry_tint_gs, 1)
        # b = recup(entry_tint_bv, 1)
        rgb = recup_mentry(data['clr'])
    elif mode == 'hsv' :
        hsv = recup_mentry(data['clr'])
        rgb = hsv2rgb(hsv)
    return rgb




# def mode_circle() :
#     frame_curseur.grid_forget()
#     frame_circle.grid(row=1)
#     menu.entryconfig(2,command = refresh_circle,label='refresh(O)')

# def mode_curseur() :
#     frame_circle.grid_forget()
#     frame_curseur.grid(row=1)
#     menu.entryconfig(2,command = refresh_curseur, label='refresh(o)')

def change_mode(mode,command = None) :
    for frame in SUPERFRAMES.values() :
        frame.grid_forget()
    SUPERFRAMES[mode].grid(row=1)
    if command != None :
        menu.entryconfig(2,command = command)




## INTERFACE : TOOLS

def stronoff(boole) :
    return 'ON' if boole else 'OFF'

def grid_entry(root,row,col=1,label=None,textvar='',width=None) :
    entry = Entry(root,width=width)
    entry.insert(0,textvar)
    entry.grid(row=row,column=1)
    if label!=None :
        Label(root,text = label).grid(row=row,column=col-1)
    return entry


def grid_combo(root,row,col=1,*,values=[''],label=None,current = 0) :
    combo = ttk.Combobox(root,values=values)
    combo.grid(row=row, column=col)
    combo.current(current)
    if label != None :
        Label(root,text = label).grid(row=row,column=col-1)
    return combo

def grid_frame(root,row,col,*,title=None,bg=None,fg=None, col_title=1):
    frame = Frame(root,bg=bg)
    frame.grid(row=row,column=col)
    if title!=None :
        Label(frame,text=title,bg=bg,fg=fg).grid(row=0,column=col_title)
    return frame

def grid_label(root,row,col,text,bg=None,fg=None) :
    label = Label(root, text=text,bg=bg,fg=fg)
    label.grid(row=row,column=col)
    return label

def grid_button(root, row,col,*,text='<>',command) :
    button = Button(root, text=text,command=command)
    button.grid(row=row,column=col)
    return button

class OnOff(ttk.Combobox) :
    def __init__(self,*arg,**kwargs) :
        kwargs['values'] = ['off', 'on']
        return ttk.Combobox.__init__(self,*arg,**kwargs)
    
    def getbool(self) :
        """CUSTOM, Renvoie True si 'on'"""
        return bool(self.current())



def grid_onoff(root,row,col=1,*,label=None,current = 0) :
    onoff = OnOff(root)
    onoff.grid(row=row, column=col)
    onoff.current(current)
    if label != None :
        Label(root,text = label).grid(row=row,column=col-1)
    return onoff

def grid_mentry(n,root,row,col,*defaults,label=None,width=None) :
    """widget multientry : n entry pour aller plus vite"""
    # TODO mettre sur une seule ligne
    frame = grid_frame(root,row,col)
    if label != None :
        Label(root,text=label).grid(row=row,column=col-1)
    if (p := n-len(defaults)) > 0 :
        defaults += ('',)*p
    liste = []
    for i,txt in enumerate(defaults) :
        liste.append(grid_entry(frame,i,0,textvar=txt,width=width))
    return liste

def get_mentry(mentry) :
    return tuple([X.get() for X in mentry])

def recup_mentry(mentry,default=0) :
    got = get_mentry(mentry)
    L = []
    for x in got :
        try :
            x = float(x)
        except :
            x = default
        L.append(x)
    return tuple(L)

def grid_crown(item, root, row,col,*,title=None, bg=None ) :
    """widget couronne : pour des cercles à plusieurs couronnes.
    
    la data generale donnée vaut pour tout le cercle, sauf rmax qui devient le rlim de la couronne de base
    chaque couronne a un rlim, le plus grand devenant le rmax"""
    def command() :
        del CROWN[item][row]
        frame.destroy()
    frame = grid_frame(root,row,col,title=title,bg=bg)
    entry_r = grid_entry(frame,1,1,label='rlim')
    combo_a = grid_combo(frame,2,1, label='alpha', values=AMODES)
    mentry_a = grid_mentry(3, frame,3,1,label='aarg')
    combo_c = grid_combo(frame,4,1,label='clr',values=CMODES)
    mentry_c = grid_mentry(3, frame,5,1,label='carg')
    grid_button(frame,6,1,text='destroy',command = command)
    return entry_r, combo_a,mentry_a, combo_c,mentry_c


def add_crown(item,root,col) :
    """commande de boutton pour ajouter une couronne"""
    row = max(CROWN[item])+1 if CROWN[item] else 2
    crown = grid_crown(item,root,row,col,bg=BG[item])
    CROWN[item][row] = crown

def get_crown(crown) :
    er,ca,ma,cc,mc = crown 
    r = recup(er)
    amode = ca.get()
    aarg = recup_mentry(ma)
    cmode = cc.get()
    carg = recup_mentry(mc)
    return (r,amode) + aarg, (r,cmode)+carg

class Noentry :
    """pour passer dans 'recup' avec des constantes"""
    def __init__(self, text) :
        self.text = str(text)
    
    def get(self):
        return self.text
    
def grid_noentry() :
    ...

def grid_circular(item, superroot,col,*,
                  rmin=None,rmax=None,amin=None,amax=None,aext=None,
                  comboa=0,a1=None,a2=None,a3=None,
                  comboc=0,c1=None,c2=None,c3=None) :
    """pour des trucs circulaires toutes options
    'superroot' et 'col' sont pour le boutton add_crown"""
    tv = lambda x : '' if x == None else str(x)

    dico = {
        'rmin' : grid_entry(FRAMES[item],1,label='rmin',textvar=tv(rmin)),
        'rmax' : grid_entry(FRAMES[item],2,label='rmax',textvar=tv(rmax)),
        'amin' : grid_entry(FRAMES[item],3,label='amin',textvar=tv(amin)),
        'amax' : grid_entry(FRAMES[item],4,label='amax',textvar=tv(amax)),
        'aext' : grid_entry(FRAMES[item],5,label='aext',textvar=tv(aext)),
        'amode' : grid_combo(FRAMES[item],6, label='alpha',
                              values=AMODES, current=comboa),
        'a1' : grid_entry(FRAMES[item],7,label='a1', textvar=tv(a1)),
        'a2' : grid_entry(FRAMES[item],8,label='a2',textvar=tv(a2)),
        'a3' : grid_entry(FRAMES[item],9,label='a3',textvar=tv(a3)),
        'cmode' : grid_combo(FRAMES[item],11, label='clr',
                              values=CMODES, current=comboc),
        'c1' : grid_entry(FRAMES[item],12,label='c1',textvar=tv(c1)),
        'c2' : grid_entry(FRAMES[item],13,label='c2',textvar=tv(c2)),
        'c3' : grid_entry(FRAMES[item],14,label='c3',textvar=tv(c3)),
        'addbutt' : grid_button(FRAMES[item],20,1,text='add crown',
                        command=lambda:add_crown(item,superroot,col)),
    } 
    return dico

def grid_description(root,row,col,nom,*desc,bg=None,fg=None) :
    frame = grid_frame(root,row,col,bg=bg,fg=fg,title=nom)
    grid_label(frame,1,1,text=multiline(*desc))
    return frame

def grid_helper(root,row,col,item,bg=None,fg=None,**argval) :
    """possible kwarg :
    amin,amax,aext,rmin,rmax,
    amode,a1,a2,a3,
    """
    frame = grid_frame(root,row,col,title=item,bg=bg,fg=fg)
    i = 1
    for arg,val in argval.items() :
        grid_label(frame,i,0,arg)
        grid_label(frame,i,1,val)
        i+=1
    return argval


    
## INTERFACE : INIT

fenetre = Tk()
# fenetre.attributes('-fullscreen',True)
fenetre.config(bg = BG['fen'])



menu = Menu(fenetre,fg = "black")
fenetre.config(menu = menu)
menu.add_command(label = 'X', command = fenetre.destroy)
menu.add_command(label = 'refresh', command = refresh)
menu.add_command(label = 'save', command = sauvegarder)
menu.add_command(label='circle', command=lambda:change_mode(circle,refresh))
menu.add_command(label='cursor', command=lambda:change_mode(cursor,refresh))
menu.add_command(label='help', command=lambda:change_mode(aide))


frame_settings = grid_frame(fenetre,0,0,bg=BG['fen'],fg=BG['txt'])
grid_label(frame_settings, 0,0,text="Skin : ", bg=BG['fen'],fg=BG['txt'])
entry_skin = grid_entry(frame_settings,1,0,textvar='test')
grid_label(frame_settings,0,1,text="circle",bg=BG['fen'],fg=BG['txt'])
grid_label(frame_settings,0,2,text="cursor",bg=BG['fen'],fg=BG['txt'])


ONOFF = {
    circle : grid_onoff(frame_settings,1,1,current=1),
    cursor : grid_onoff(frame_settings,1,2,current=0),
}
MODES = {
    circle : (circle,overlay,approach,tint),
    cursor : (cursor,trail),
    aide : (),
}
SUPERFRAMES = {
    circle : grid_frame(fenetre,1,0,title='CIRCLE',bg=BG['fen'],fg=BG['txt']),
    cursor : grid_frame(fenetre, 1,0,title='CURSOR',bg=BG['fen'],fg =BG['txt']),
    aide : grid_frame(fenetre, 1,0, title='AIDE', bg=BG['fen'],fg=BG['txt']),
}
FRAMES = {
    overlay : grid_frame(SUPERFRAMES[circle],1,0, title='OVERLAY', bg=BG[overlay], fg=BG['txt']),
    circle : grid_frame(SUPERFRAMES[circle],1,1, title='HITCIRCLE', bg=BG[circle], fg=BG['txt']),
    approach : grid_frame(SUPERFRAMES[circle],1,2,title='APPROACH', bg = BG[approach],fg = BG['txt']),
    tint : grid_frame(SUPERFRAMES[circle], 1,3, title='TEINTE', bg=BG[tint], fg=BG['txt']),

    cursor : grid_frame(SUPERFRAMES[cursor],1,0, title='CURSEUR',bg=BG[cursor],fg=BG['txt']),
    trail : grid_frame(SUPERFRAMES[cursor], 1,1, title='TRAIL', bg=BG[trail],fg=BG['txt']),
}
TK = {
    overlay : grid_circular(
        overlay,SUPERFRAMES[circle],0,
        rmin=r0-e0,
        rmax=r0,
        a1=1
    ),
    circle : grid_circular(
        circle,SUPERFRAMES[circle], 1,
        rmax = r0,
        a1 = .5
    ),
    approach : grid_circular(
        approach, SUPERFRAMES[circle], 2,
        rmax = r_approach,
        rmin = r_approach - 3,
    ),
    tint : {
        'combo' : grid_combo(FRAMES[tint], 1, values=['rgb', 'hsv'], label='mode'),
        'clr' : grid_mentry(3, FRAMES[tint],2,1,
                            '1','.8','0',label=multiline('r/h','g/s','b/v')),
    },
    cursor : grid_circular(
        cursor, SUPERFRAMES[cursor], 0,
        rmax = 20,
        c1 = 1,
        c2 = 1,
        c3 = 0,
    ),
    trail : grid_circular(
        trail, SUPERFRAMES[cursor], 1,
        rmax = 15,
        a1 = .4,
    ),
}

HELPERS : {
    "dt classique" : {
        aide : grid_description(
            SUPERFRAMES[aide],1,0,
            "DT CLASSIQUE",
            "plus classique tu meurt",
            "rond blanc pour l'overlay",
            "pas de hitcircle",
        ),
        overlay : grid_helper(
            SUPERFRAMES[aide],1,1,overlay,
            amin=0, amax=1, aext=0,
            rmin=r0-e0, rmax=r0,
            amode=AMODES[0],a1=a0,
            # cmode=CMODES[0],c1=1,c2=1,c3=1
        ),
        circle : grid_helper(
            SUPERFRAMES[aide],1,2,circle,
            amode=AMODES[0],a1=0,
        ),
    },
}


CROWN = {
    overlay : {},
    circle : {},
    approach : {},
    cursor : {},
    trail : {},
}



## EXE

pg.init()
screen = pg.display.set_mode((2*n0,2*n0))
change_mode(circle)
try :
    fresh()
except :
    print('initialisation')
    # refresh_circle()
    refresh()

print('up')
fenetre.mainloop()
pg.quit()
print('down')