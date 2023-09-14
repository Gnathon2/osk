# widget.py
"""des fonctions et widgets en plus pour tkinter"""
import tkinter as tk
from tkinter import ttk
from constant import *


def grid_entry(root,row,col=1,label=None,textvar=None,**kw) :
    if textvar == None : textvar = ''
    entry = tk.Entry(root,**kw)
    entry.insert(0,textvar)
    entry.grid(row=row,column=col)
    if label!=None :
        tk.Label(root,text = label,**kw).grid(row=row,column=col-1)
    return entry

def recup_entry(entry, default = None) :
    x = entry.get()
    try : x = float(x)
    except : x = default
    return x

def grid_combo(root,row,col=1,*,
               values=[''], label=None, 
               current=0, bg=None, fg=None) :
    
    combo = ttk.Combobox(root,values=values,)
    combo.grid(row=row, column=col)
    combo.current(current)
    if label != None :
        tk.Label(root,text = label, bg=bg, fg=fg).grid(row=row,column=col-1)
    return combo

def grid_frame(root,row,col,*,title=None,bg=None,fg=None,col_title=1) :
    frame = tk.Frame(root,bg=bg)
    frame.grid(row=row,column=col)
    if title!=None :
        tk.Label(frame,text=title,bg=bg,fg=fg).grid(row=0,column=col_title)
    return frame

def grid_label(root,row,col,text,*,bg=None,fg=None) :
    label = tk.Label(root, text=text,bg=bg,fg=fg)
    label.grid(row=row,column=col)
    return label

def grid_button(root, row,col,*,text='<>',command,**options) :
    button = tk.Button(root, text=text,command=command,**options)
    button.grid(row=row,column=col)
    return button

class OnOff(ttk.Combobox) :
    def __init__(self,*arg,**kwargs) :
        kwargs['values'] = ['off', 'on']
        return ttk.Combobox.__init__(self,*arg,**kwargs)
    
    def getbool(self) :
        """CUSTOM, Renvoie True si 'on'"""
        return bool(self.current())

def get_onoff(onoff) :
    return onoff.getbool()

def grid_onoff(root,row,col=1,*,label=None,current = 0) :
    onoff = OnOff(root)
    onoff.grid(row=row, column=col)
    onoff.current(current)
    if label != None :
        tk.Label(root,text = label).grid(row=row,column=col-1)
    return onoff

def grid_mentry(n,root,row,col,*defaults, bg=None,fg=None, label=None,width=None) :
    """widget multientry : n entry pour aller plus vite"""
    # TODO mettre sur une seule ligne
    frame = grid_frame(root,row,col)
    if label != None :
        tk.Label(root,text=label,bg=bg,fg=fg).grid(row=row,column=col-1)
    if (p := n-len(defaults)) > 0 :
        defaults += ('',)*p
    liste = []
    for i,txt in enumerate(defaults) :
        liste.append(grid_entry(frame,i,0,textvar=txt,width=width,bg=bg,fg=fg))
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

def grid_crown(item, root, row,col,*,command=None,title=None, bg=None ) :
    """widget couronne : pour des cercles à plusieurs couronnes.
    
    la data generale donnée vaut pour tout le cercle, sauf rmax qui devient le rlim de la couronne de base
    chaque couronne a un rlim, le plus grand devenant le rmax"""
    def real_command() :
        command()
        frame.destroy()
        
    frame = grid_frame(root,row,col,title=title,bg=bg)
    entry_r = grid_entry(frame,1,1,label='rlim')
    combo_a = grid_combo(frame,2,1, label='alpha', values=AMODES)
    mentry_a = grid_mentry(3, frame,3,1,label='aarg')
    combo_c = grid_combo(frame,4,1,label='clr',values=CMODES)
    mentry_c = grid_mentry(3, frame,5,1,label='carg')
    grid_button(frame,6,1,text='destroy',command = real_command)
    return entry_r, combo_a,mentry_a, combo_c,mentry_c


def get_crown(crown) :
    er,ca,ma,cc,mc = crown 
    r = recup_entry(er)
    amode = ca.get()
    aarg = recup_mentry(ma)
    cmode = cc.get()
    carg = recup_mentry(mc)
    return (r,amode) + aarg, (r,cmode)+carg

# class Noentry :
#     """pour passer dans 'recup_entry' avec des constantes"""
#     def __init__(self, text) :
#         self.text = str(text)
    
#     def get(self):
#         return self.text
    
# def grid_noentry() :
#     ...