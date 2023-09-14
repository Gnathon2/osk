# skinneur.main.py
"""Pour visualiser le skin ig avant de sauvegarder (full interface quoi)"""

# TODO TOUT PASSER EN UINT 8 
# TODO renommer constantes en capslock
# TODO ini
# tout compléter
# save fusion
# TODO chiffre
# TODO perfectstack : un autre cercle en dessous
# TODO slider (pour les couleurs) (moyen accurate mais osef)
# dont sliderball et followcircle
# TODO helper 
# écraser le DEFAULT quand on importe
# gestion des couronnes
# TODO spinner 
# TODO pouvoir déplacer le curseur % au cercle
# TODO lifebar
# TODO smoke
# TODO followpoint (nop)

# imports generaux
import pygame as pg
import matplotlib.pyplot as plt

# imports persos
from thomas import multiline
from thomas.couleur import hsv2rgb

# imports locaux
from cercle import megafunc, teinture
from constant import *
from skinneur.widget import *
from skinneur.apercu import *
from skinneur.fichier import *



def get_ini() :
    dico = {}
    for section,dico2 in TK[INI].items() :
        dico[section] = {}
        for option,entry in dico2.items() :
            dico[section][option] = entry.get()
    return dico

def sauvegarder(item_set) :
    """commande de sauvegarde (actually copier coller)"""
    skin = entry_skin.get()
    if item_set == 'all' :
        for iset in (CIRCLE,CURSOR,INI,) : 
            sauvegarder(iset)
    if item_set == CIRCLE :
        copypasta(skin, OVERLAY, CIRCLE, APPROACH)
        print(f"cercles sauvegardés dans '{skin}'")
    if item_set == CURSOR :
        copypasta(skin, CURSOR, TRAIL)
        print(f"curseur sauvegardé dans '{skin}'")
    if item_set == INI :
        dico = get_ini()
        parser = dico2iniparser(dico)
        ecrire_ini(parser,skin)
        print(f"Skin.ini sauvegardé dans '{skin}'")

    
def fresh() :
    'peut planter'

    surf_over = pg.image.load(filename(OVERLAY.tinted())).convert_alpha()
    surf_hit = pg.image.load(filename(CIRCLE.tinted())).convert_alpha()
    surf = pg.image.load(filename(APPROACH.tinted())).convert_alpha()
    surf_appr = pg.transform.scale(surf, 2*pg.Vector2(surf.get_rect().size))

    grayfill(screen,0)
    centerblit(screen,surf_hit)
    centerblit(screen,surf_over)
    centerblit(screen,surf_appr)
    pg.display.flip()



def refresh() :
    grayfill(screen,0)

    if onoff_circle.get() :
        print("refreshing CIRCLE",end = '')
        surf_over = update_circular(OVERLAY)
        TINT = get_tint()
        surf_hit = update_circular(CIRCLE, TINT)
        surf_appr = update_circular(APPROACH, TINT)
        surf_appr = rescale(surf_appr,2)
        centerblit(screen,surf_hit)
        centerblit(screen,surf_over)
        centerblit(screen,surf_appr)
        print(" | CIRCLE refreshed")

    if onoff_cursor.get() :
        print("refreshing CURSOR",end='')

        surf_cursor = update_circular(CURSOR)
        surf_trail = update_circular(TRAIL)
        for x in [-170,-100, -50,-30,-10,-7,-2,0] :
            centerblit(screen,surf_trail, x = x)
        centerblit(screen,surf_cursor)
        print(" | CURSOR refreshed")

    pg.display.flip()







def add_crown(item,root,col) :
    """commande de boutton pour ajouter une couronne"""
    row = max(CROWN[item])+1 if CROWN[item] else 2
    def com() :
        del CROWN[item][row]
    crown = grid_crown(item,root,row,col,command=com,bg=BG[item])
    CROWN[item][row] = crown



def get_circular(item) :
    ...
    
def update_circular(item, tint=None) :
    """recupère la data dans l'interface pour l'overlaycircle
    renvoie ce dernier sous forme de pg.Surface
    
    très sale, peut-être qua ça changera ... ."""
    
    data = TK[item]

    rmin = recup_entry(data['rmin'])
    rmax = recup_entry(data['rmax'])
    amin = recup_entry(data['amin'])
    amax = recup_entry(data['amax'])
    aext = recup_entry(data['aext'])
    amode = data['amode'].get()
    a1 = recup_entry(data['a1'])
    a2 = recup_entry(data['a2'])
    a3 = recup_entry(data['a3'])
    clrmode = data['cmode'].get()
    c1 = recup_entry(data['c1'])
    c2 = recup_entry(data['c2'])
    c3 = recup_entry(data['c3'])

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
        item.npix,amode,a1,a2,a3,clrmode, c1,c2,c3,
        amin=amin,amax=amax,rmin=rmin,rmax=rmax,aext=aext
    )
    array_tinted = array if tint==None else teinture(array, tint)
    plt.imsave(filename(item), array)
    plt.imsave(filename(item.tinted()), array_tinted)
    surf = pg.image.load(filename(item.tinted())).convert_alpha()
    return surf


def get_tint() :
    data = TK[TINT]
    mode = data['combo'].get()
    if mode == 'rgb' :
        # r = recup_entry(entry_tint_rh,1)
        # g = recup_entry(entry_tint_gs, 1)
        # b = recup_entry(entry_tint_bv, 1)
        rgb = recup_mentry(data['clr'])
    elif mode == 'hsv' :
        hsv = recup_mentry(data['clr'])
        rgb = hsv2rgb(hsv)
    return rgb

 
def change_mode(mode) :
    """Button command"""
    for frame in SUPERFRAMES.values() :
        frame.grid_forget()
    SUPERFRAMES[mode].grid(row=1)



def grid_circular(item, superroot,col,*,bg=None,fg=None,
                  rmin=None,rmax=None,amin=None,amax=None,aext=None,
                  comboa=0,a1=None,a2=None,a3=None,
                  comboc=0,c1=None,c2=None,c3=None) :
    """pour des trucs circulaires toutes options
    'superroot' et 'col' sont pour le boutton add_crown"""
    tv = lambda x : '' if x == None else str(x)
    dico = {
        'rmin' : grid_entry(FRAMES[item],1,label='rmin',textvar=tv(rmin),bg=bg,fg=fg),
        'rmax' : grid_entry(FRAMES[item],2,label='rmax',textvar=tv(rmax),bg=bg,fg=fg),
        'amin' : grid_entry(FRAMES[item],3,label='amin',textvar=tv(amin),bg=bg,fg=fg),
        'amax' : grid_entry(FRAMES[item],4,label='amax',textvar=tv(amax),bg=bg,fg=fg),
        'aext' : grid_entry(FRAMES[item],5,label='aext',textvar=tv(aext),bg=bg,fg=fg),
        'amode' : grid_combo(FRAMES[item],6, label='alpha',
                              values=AMODES, current=comboa,bg=bg,fg=fg),
        'a1' : grid_entry(FRAMES[item],7,label='a1', textvar=tv(a1),bg=bg,fg=fg),
        'a2' : grid_entry(FRAMES[item],8,label='a2',textvar=tv(a2),bg=bg,fg=fg),
        'a3' : grid_entry(FRAMES[item],9,label='a3',textvar=tv(a3),bg=bg,fg=fg),
        'cmode' : grid_combo(FRAMES[item],11, label='clr',
                              values=CMODES, current=comboc,bg=bg,fg=fg),
        'c1' : grid_entry(FRAMES[item],12,label='c1',textvar=tv(c1),bg=bg,fg=fg),
        'c2' : grid_entry(FRAMES[item],13,label='c2',textvar=tv(c2),bg=bg,fg=fg),
        'c3' : grid_entry(FRAMES[item],14,label='c3',textvar=tv(c3),bg=bg,fg=fg),
        'addbutt' : grid_button(FRAMES[item],20,1,text='add crown',
                        command=lambda:add_crown(item,superroot,col),bg=bg,fg=fg),
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

def grid_help(root,row,col,nom,*desc,bg=None,fg=None,**items) :
    frame = grid_frame(root,row,col,bg=bg,fg=fg)
    frame_desc = grid_frame(frame,0,0,bg=bg,fg=fg)
    grid_button(frame_desc,0,0,text=nom,command=lambda:megaset(items))
    grid_label(frame_desc,1,0,text=multiline(*desc))
    # grid_description(frame,0,0,nom,*desc,bg=bg,fg=fg)
    col = 1
    for item,argval in items.items() :
        grid_helper(frame,0,col,item=item,bg=bg,fg=fg,**argval)
        col += 1
    return items

def set_item(item:str,argval) :
    
    where = TK[locals()[item]]
    # parce que item sera une 
    for arg,val in argval.items() :
        if arg.endswith('mode') :
            # combobox
            where[arg].set(val)
        else :
            # Entry
            where[arg].delete(0,tk.END)
            where[arg].insert(0,val)

def megaset(dico) : 
    "fonction de bouton"
    for item,argval in dico.items() :
        set_item(item,argval)
        
def grid_inisection(root,row,col,section,bg=None,fg=None,**options) :
    frame = grid_frame(root,row,col,title=section,bg=bg,fg=fg,col_title=0)
    row = 1
    dico = {}
    for option,value in options.items() :
        dico[option] = grid_entry(frame,row,1,option,value,bg=bg,fg=fg)
        row += 1
    return dico

def grid_checkbutton(root,row,col,text,**kw) :
    var = tk.IntVar()
    cb = tk.Checkbutton(root,text=text,variable=var,**kw) 
    cb.grid(row=row,column=col)
    return var
 


## INIT INTERFACE

CROWN = {
    OVERLAY : {},
    CIRCLE : {},
    APPROACH : {},
    CURSOR : {},
    TRAIL : {},
}

fenetre = tk.Tk()
# fenetre.attributes('-fullscreen',True)
fenetre.config(bg = BG['fen'])

menu = tk.Menu(fenetre)
fenetre.config(menu = menu)

menu_save = tk.Menu(menu,tearoff=0)
menu_save.add_command(label = 'refresh', command=refresh)
menu_save.add_separator()
menu_save.add_command(label='save ALL', command=lambda:sauvegarder('all'))
menu_save.add_command(label='save circle',command=lambda:sauvegarder(CIRCLE))
menu_save.add_command(label='save cursor',command=lambda:sauvegarder(CURSOR))
menu_save.add_command(label='save skin.ini',command=lambda:sauvegarder(INI))
menu_save.add_separator()
menu_save.add_command(label = 'adios amigos', command=fenetre.destroy,
                      underline=0)

menu.add_cascade(label='file',menu=menu_save)
menu.add_separator()
menu.add_command(label='cercles', command=lambda:change_mode(CIRCLE))
menu.add_command(label='curseur', command=lambda:change_mode(CURSOR))
menu.add_command(label='Skin.ini', command=lambda:change_mode(INI))
menu.add_command(label='templates', command=lambda:change_mode(AIDE))




frame_settings = grid_frame(fenetre,0,0,bg=BG['set'],fg=FG)
grid_label(frame_settings, 0,0,text="Skin : ", bg=BG['set'],fg=FG)
entry_skin = grid_entry(frame_settings,1,0,textvar='test', bg=BG['set'],fg=FG)
onoff_circle = grid_checkbutton(frame_settings,1,3,
    'cercles',bg=BG[CIRCLE],fg=FG,selectcolor=BG['set'])
onoff_cursor = grid_checkbutton(frame_settings,0,3,
    'curseur',bg=BG[CURSOR],fg=FG,selectcolor=BG['set'])

style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground=BG['fen'],
                background=BG['fen'],foreground=FG,
                darkcolor = BG['fen'],
                lightcolor = BG['fen'],
                )


SUPERFRAMES = { # onglets escamotables | 1 SF par mode
    CIRCLE : grid_frame(fenetre,1,0,title='CIRCLE',bg=BG[CIRCLE],fg=FG),
    CURSOR : grid_frame(fenetre, 1,0,title='CURSOR',bg=BG[CURSOR],fg =FG),
    AIDE : grid_frame(fenetre, 1,0, title='AIDE', bg=BG[AIDE],fg=BG['txt']),
    INI : grid_frame(fenetre,1,0, title='SKIN.INI',bg=BG[INI],fg=FG),
}

FRAMES = { # 1 frame par section
    # CIRCLE
    OVERLAY : grid_frame(SUPERFRAMES[CIRCLE], 1, 0,
                         title='OVERLAY', bg=BG[CIRCLE], fg=FG),
    CIRCLE : grid_frame(SUPERFRAMES[CIRCLE], 1, 1, 
                        title='HITCIRCLE', bg=BG[CIRCLE], fg=FG),
    APPROACH : grid_frame(SUPERFRAMES[CIRCLE], 1, 2,
                          title='APPROACH', bg=BG[CIRCLE], fg=FG),
    TINT : grid_frame(SUPERFRAMES[CIRCLE], 1, 3, 
                      title='TEINTE', bg=BG[CIRCLE], fg=FG),
    # CURSOR
    CURSOR : grid_frame(SUPERFRAMES[CURSOR], 1, 0, 
                        title='CURSEUR',bg=BG[CURSOR],fg=FG),
    TRAIL : grid_frame(SUPERFRAMES[CURSOR], 1, 1, 
                       title='TRAIL', bg=BG[CURSOR],fg=FG),
} # c'est sale mais obligé de laisser à cause des couronnes

TK = { # elements de skin
    OVERLAY : grid_circular(
        OVERLAY,SUPERFRAMES[CIRCLE],0,
        bg=BG[CIRCLE], fg=FG,
        rmin = OVERLAY.ray - OVERLAY.eps,
        rmax = OVERLAY.ray,
        a1 = 1
    ),
    CIRCLE : grid_circular(
        CIRCLE,SUPERFRAMES[CIRCLE], 1,
        bg=BG[CIRCLE], fg=FG,
        rmax = CIRCLE.ray,
        a1 = .5
    ),
    APPROACH : grid_circular(
        APPROACH, SUPERFRAMES[CIRCLE], 2,
        bg=BG[CIRCLE], fg=FG,
        rmax = APPROACH.ray,
        rmin = APPROACH.ray - 3,
    ),
    TINT : {
        'combo' : grid_combo(
            FRAMES[TINT], 1, 
            bg=BG[CIRCLE], fg=FG,
            values=['rgb', 'hsv'], 
            label='mode'),
        'clr' : grid_mentry(
            3, FRAMES[TINT],2,1,
            '1','.8','0',
            bg=BG[CIRCLE], fg=FG,
            label=multiline('r/h','g/s','b/v')),
    },
    CURSOR : grid_circular(
        CURSOR, SUPERFRAMES[CURSOR], 0,
        bg=BG[CURSOR], fg=FG,
        rmax = 20,
        c1 = 1,
        c2 = 1,
        c3 = 0,
    ),
    TRAIL : grid_circular(
        TRAIL, SUPERFRAMES[CURSOR], 1,
        bg=BG[CURSOR], fg=FG,
        rmax = 15,
        a1 = .4,
    ),
    INI : {
        'General' : grid_inisection(
            SUPERFRAMES[INI],1,0,'GENERAL',
            bg=BG[INI], fg=FG,
            Name = 'test',
            Author = 'Gnathon',
            Version = 'latest',
            AnimationFramerate = 60,
            AllowSliderBallTint = 1,
            CursorExpand = 0,
            CursorRotate = 0,
        ),
        'Colours' : grid_inisection(
            SUPERFRAMES[INI],1,1,'COULEURS',
            bg=BG[INI], fg=FG,
            Combo1 = '255,0,0',
            Combo2 = '255,255,0',
            Combo3 = '0,255,0',
            Combo4 = '0,0,255',
            Combo5 = None,
        ),
        'Fonts' : grid_inisection(
            SUPERFRAMES[INI],1,2,'Fonts',
            rien = 'rien',
        ),    
    },
    "template DT" : grid_help(
        SUPERFRAMES[AIDE],1,0,
        "DT CLASSIQUE",
        "Juste rond blanc",
        "Plus classique tu meurt",
        bg=BG['mdl dt1'], fg=FG,
        CIRCLE = {
            'amode':'constant',
            'a1':0
        },
    ),
    "template zero" : grid_help(
        SUPERFRAMES[AIDE],50,0,
        "CIRCLE DEFAULT",
        "TOUTE la data par defaut pour les cercles",
        # bg = BG[CIRCLE], fg=BG['txt'],
        CIRCLE = {
            'rmin':0, 'rmax':R0, 
        },
        OVERLAY = {
            'amin':0, 'amax':0,
        }
    ),
}


## EXE

if __name__=='__main__' :
    pg.init()
    screen = pg.display.set_mode((2*N0,2*N0))
    change_mode(CIRCLE)
    try :
        fresh()
    except :
        print('initialisation')
        refresh()

    print('up')
    fenetre.mainloop()
    pg.quit()
    print('down')



