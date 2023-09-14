# skinneur.fichier.py
"""fonctions de manip' de fichier, .ini notamment"""
import shutil
import configparser as cp
from osk.__init__ import DOSSIER_SKIN

def filename(item, skin = None) :
    """renvoie le chemin exact en absolu de 'item' dans 'skin'
    ou Skins si None"""
    if skin == None :
        return rf"{DOSSIER_SKIN}\{item}@2x.png"
    else :
        return rf"{DOSSIER_SKIN}\{skin}\{item}@2x.png"

def copypasta(skin,*items):
    """Copy-paste des fichiers du néant distordu vers le skin donné."""
    for item in items :
        shutil.copyfile(filename(item), filename(item, skin))

def lire_ini(skin) :
    parser =cp.ConfigParser()
    parser.read(f"{DOSSIER_SKIN}/{skin}/Skin.ini")
    return parser

def iniparser2dico(parser,dico={}) :
    for section in parser.sections() :
        dico[section] = {}
        for option,value in parser.items(section) :
            dico[section][option] = value
    return dico

def dico2iniparser(dico,parser=None) :
    if parser == None : parser = cp.ConfigParser()
    for section,dico2 in dico.items() :
        parser.add_section(section)
        for option,val in dico2.items() :
            parser.set(section,option,str(val))
    return parser

def ecrire_ini(parser,skin) :
    try :
        with open(f"{DOSSIER_SKIN}/{skin}/Skin.ini",'x') as skinini :
            parser.write(skinini)
    except FileExistsError :
        with open(f"{DOSSIER_SKIN}/{skin}/Skin.ini",'r+') as skinini:
            parser.write(skinini)
