from constant import *
import pygame as pg

def rescale(surf, k) :
    return pg.transform.scale(surf, k*pg.Vector2(surf.get_rect().size))

def centerblit(screen,surf,x=0,y=0) :
    """blit surf tq centre de surf en (x,y) % au centre de screen"""
    rect = surf.get_rect()
    xx,yy = screen.get_rect().center
    xx += x
    yy += y
    rect.center = (xx,yy)
    screen.blit(surf,rect)

def grayfill(screen,shade) :
    """Remplit l'écran pygame d'une nuance de gris"""
    screen.fill((shade,)*3)
    pg.display.flip()
