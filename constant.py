# osk/constant.py

_APPROACH = 'approachcircle'
_CIRCLE = 'hitcircle'
_FOLLOW = 'sliderfollowcircle'
_POINT  = 'sliderscorepoint'
_CURSOR = 'cursor'

_NPIX = {
    _APPROACH : 126,
    _CIRCLE : 128,
    _FOLLOW : 256,
    _POINT : 16,
    _CURSOR : 100,
}

_RAY = {
    _APPROACH : 63,
    _CIRCLE : 58,
    _FOLLOW : 128,
    _POINT : 8,
}

N0 = _NPIX[_CIRCLE] * 2
R0 = _RAY[_CIRCLE] * 2
E0 = 15 # epaisseur
A0 = 255



class _Element :
    def __init__(self, name,ext = 'png', **data) :
        """        
        name : str # nom de fichier exact

        x2 : bool # version @2x ?
        npix : int # taille reco de l'image en pixels


        """

        data['ext'] = ext
        data['name'] = name
        self.__dict__ |= data
    
    def __str__(self) :
        return self.name
    
    def tinted(self) :
        return str(self) + '-tinted'

    def save(self,fichier) :
        ...



CIRCLE = _Element(_CIRCLE,'png', x2=True, 
                 npix = _NPIX[_CIRCLE]*2, ray = _RAY[_CIRCLE] * 2)
OVERLAY = _Element('hitcircleoverlay','png', x2=True, 
                  npix = 128*2, ray = 118, eps=15)
APPROACH = _Element('approachcircle','png', x2=True, 
                   npix=126*2, ray=126, )
SELECT = _Element('hitcircleselect','png', x2=True,
                  npix=_NPIX[_CIRCLE]*2, ray = _RAY[_CIRCLE]*2)

CURSOR = _Element('cursor','png', x2=True, npix=200)
TRAIL = _Element('cursortrail','png', x2=True, npix=200)
SMOKE = _Element('cursor-smoke','png', x2=True,)

INI = _Element('Skin','ini',)

# slider = 'sliderstartcircle'
# sliderover = 'sliderstartcircleoverlay'
# sliderend = 'sliderendcircle'
# sliderendover = 'sliderendcircleovelay'
# ball = 'sliderb'
# arrow = 'reversearrow'
# SPIN = ['spinner-approachcircle','spinner-rpm','spinner-clear',]
# SPIN1 = ['spinner-background','spinner-circle','spinner-metre','spinner-osu']
# SPIN2 = ['spinner-glow','spinner-bottom','spinner-top','spinner-middle2','spinner-middle']
# followpoint = 'followpoint'
# blanked = ['comboburst','lightning',slider,sliderover,'spinner-spin','particle50','particule100','particule300']
# blanked2 = ['hit300-0','hit300g-0','hit300k-0','star2']
# middle = 'cursormiddle'
# BLANK = np.zeros((1,1,4))


# pour le logiciel

TINT = 'tint'
AIDE = 'help'
INI = 'Skin.ini'


AMODES = ['constant', 'gauss', 'gradient']
CMODES = ['plain','radhue']

BG_DARK = {
    'fen' : '#000000', 
    'txt' : '#ffffff',
    'set' : '#111111',
    CIRCLE : '#002211',
    CURSOR : '#550044',
    AIDE : '#008899',
    'mdl dt1' : '#000000',
    INI : '#111111',
}

BG_LIGHT = {
    'txt' : '#000000',

}


BG = BG_DARK
FG = BG['txt']