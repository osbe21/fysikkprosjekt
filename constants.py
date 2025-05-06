# constants.py

# Skjerm
WIDTH = 800
HEIGHT = 600
FPS = 60

# Farger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)

# Fysikk-konstanter
k = 10.0          # Fjærkonstant (N/m)
m = 1.0           # Masse (kg)
b = 0.5           # Luftmotstand/demping (Ns/m)
x0 = 300          # Likevektsposisjon (px)
amplitude = 100   # Startforskyvning fra likevekt (px)
dt = 1 / FPS      # Tidssteg (s)

# Formler
def fjærkraft(x):
    """Hookes lov: F = -k * x"""
    return -k * (x - x0)

def luftmotstand(v):
    """Luftmotstand: F = -b * v"""
    return -b * v

def akselerasjon(x, v):
    """Total akselerasjon a = F / m"""
    F = fjærkraft(x) + luftmotstand(v)
    return F / m
