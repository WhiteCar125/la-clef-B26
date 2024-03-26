import pyxel, random


# taille de la fenetre 128x128 pixels
# ne pas modifier
pyxel.init(128, 128, title="Retro game")


# position initiale du vaisseau
# (origine des positions : coin haut gauche)
vaisseau_x = 10
vaisseau_y = 120
vaisseau_l = 7
vaisseau_h = 8
ennemi_l = 7
ennemi_h = 8
# initialisation des tirs
tirs_liste = []
# initialisation des tirs
ennemis_liste = []
explosions_liste = []
score_de_vies_liste = []
# chargement des images
pyxel.load("images.pyxres")


def tirs_creation(x, y, tirs_liste):
   """création d'un tir avec la barre d'espace"""
   # btnr pour eviter les tirs multiples
   if pyxel.btnr(pyxel.KEY_SPACE):
       tirs_liste.append([x+vaisseau_l//2, y])
   return tirs_liste


def tirs_deplacement(tirs_liste):
   """déplacement des tirs vers le haut et suppression s'ils sortent du cadre"""
   for tir in tirs_liste:
       tir[1] = tir[1] - 1 # le tir se déplace vers le haut
       if  tir[1] < 0: #le tir sort de l'écran
           tirs_liste.remove(tir) # je supprime ce tir de la liste des tirs
      
   return tirs_liste

def vaisseau_deplacement(x, y):
  """déplacement avec les touches de directions"""


  if pyxel.btn(pyxel.KEY_RIGHT) and vaisseau_x<128-vaisseau_l+1:
      x = x + 2
   
  if pyxel.btn(pyxel.KEY_LEFT) and vaisseau_x>0:
      x = x - 2


  if pyxel.btn(pyxel.KEY_UP) and vaisseau_y>0:
      y = y - 2
     
  if pyxel.btn(pyxel.KEY_DOWN) and vaisseau_y<128-vaisseau_h:
      y = y + 2
 
  return x, y # retourne les coordonnées mise à jour


def ennemis_creation(ennemis_liste):
  if pyxel.frame_count % 30 == 0:
      ennemis_liste.append([random.randrange(0,127-ennemi_l), 0])


  return ennemis_liste


def ennemis_maj(ennemis_liste):
   """
   déplacement et suppression éventuelle des ennemis
   """
   for ennemi in ennemis_liste:
       ennemi[1] = ennemi[1]+1
       if  ennemi[1] > 127: #le tir sort de l'écran
           ennemis_liste.remove(ennemi) # je supprime ce tir de la liste des tirs
      
   return ennemis_liste

def collision(x1,  y1, l1, h1, x2, y2, l2, h2):
    """
    x1:abscisse de l'objet1
    y1:ordonnée de l'objet1
    l1:largeur de l'objet1
    h1:hauteur de l'objet1
    x2:abscisse de l'objet2
    y2:ordonnée de l'objet2
    l2:largeur de l'objet2
    h2:hauteur de l'objet2
    Retourne True si collision, False sinon
    """
    if x1 <= x2+l2 and x1+l1>=x2 and y1 <= y2+h2 and y1+h1>=y2:
        return True
    return False


   
def collision_tirs_ennemis():
    for tir in tirs_liste:
        for ennemi in ennemis_liste:
            if collision(tir[0], tir[1], 1, 4, ennemi[0], ennemi[1], ennemi_l, ennemi_h):
                tirs_liste.remove(tir)
                ennemis_liste.remove(ennemi)
                explosions_creation(ennemi[0], ennemi[1])
                # creation d'une explosion


def explosions_creation(x, y):
    """explosions aux points de collision entre deux objets"""
    explosions_liste.append([x, y, 0])


def explosions_animation():
    """animation des explosions"""
    for explosion in explosions_liste:
        explosion[2] +=1
        if explosion[2] == 12:
            explosions_liste.remove(explosion)

def collision_ennemis_vaisseau():
    for ennemi in ennemis_liste:
        if collision( ennemi[0], ennemi[1], ennemi_l, ennemi_h, vaisseau_x, vaisseau_y, vaisseau_l, vaisseau_h):
            ennemis_liste.remove(ennemi)
            explosions_creation(ennemi[0], ennemi[1])
            explosions_creation(vaisseau_x, vaisseau_y)     
             
 
def score_vies():
    # Initialisation du score
 score_vies = 3

 # Si une collision se produit, enlever une vie
 for collision in collision_ennemis_vaisseau():
     score_vies[1] = score_vies - 1

# Affichage du score mis à jour
print("Score de vies :", score_vies)


  
# =========================================================
# == UPDATE
# =========================================================
def update():
   """mise � jour des variables (30 fois par seconde)"""


   global vaisseau_x, vaisseau_y, vaisseau_l, vaisseau_h,tirs_liste, ennemis_liste
   vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)
   vaisseau_deplacement(vaisseau_x, vaisseau_y)
   tirs_creation(vaisseau_x, vaisseau_y, tirs_liste)
   tirs_deplacement(tirs_liste), 
   tirs_liste = tirs_deplacement(tirs_liste)
   ennemis_creation(ennemis_liste)
   ennemis_maj(ennemis_liste)
   print(ennemis_liste)
   collision_tirs_ennemis()
   explosions_animation()
   collision_ennemis_vaisseau()
  

  
# =========================================================
# == DRAW
# =========================================================
def draw():
    """dessin des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)
    

    
    # tirs
    for tir in tirs_liste: # je boucle sur ma liste de tirs
        pyxel.rect(tir[0], tir[1], 1, 4, 10) #je dessine un rectangle
    # vaisseau (carre 8x8)
    # x, y, largeur, hauteur, couleur
    if pyxel.frame_count % 30 <= 15:
        pyxel.blt(vaisseau_x, vaisseau_y, 0, 0, 0, 8, 8)
    else:
        pyxel.blt(vaisseau_x, vaisseau_y, 0, 8, 0, 8, 8)
    # ennemis
    for ennemi in ennemis_liste:
        if pyxel.frame_count % 30 <= 15:
            pyxel.blt(ennemi[0], ennemi[1], 0, 0, 8, 8, 8)
        else:
            pyxel.blt(ennemi[0], ennemi[1], 0, 8, 8, 8, 8)
    # explosions (cercles de plus en plus grands)
    for explosion in explosions_liste:
        pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3) 

   # ennemis dessin

# lance le programme principal
pyxel.run(update, draw)
