# Projet Kyniska


## Objectif

Identifier et numéroter les billes projetées en 2D à partir d’une mire 3D connue.

Le but final est de retrouver la correspondance entre :

- les billes de la mire (points 3D avec ids fixes)
- les points détectés sur une image radiographique 2D

---

## Structure du projet

Le projet comprend 3 dossiers principaux :

-> "old" contenant tous les fichiers obsolètes qu'on n'a pas pu intégrer au code final soit par manque de temps(ex: triangulation.py ) soit par parceque ça ne menait nulle part(exemple : le matching_convex qui devait nous servir à réaliser la méthode de l'enveloppe convexe jugée finalement un peu trop complexe à mettre en oeuvre).

-> "src/core" : le noeud de tout ce projet où se trouvent tous les fichiers nécessaires à la génération, les calculs projectifs , géométriques(ex: perpendicular_vector dans geometry.py ) et également ceux permettant de faire fonctionner le véritable main du projet ( le compare.py ). 

-> "tests" : dossier qui contient les tests de certains fichiers du src/core
NB: Certains tests pourraient ne pas passer, ayant été réalisés au tout début du projet avec un code de leurs fichiers correspondants du src/core légèrement ou complètement différents du code actuel. Ils n'ont pas pu être mis à jour faute de temps. 

# Commandes à exécuter:

python generer.py "forme de mire" "nombre de billes" : obtient un vrMire(.json) 
python simulate.py "le mire.json de la vrai mire" : obtient un Mir_rot(.json) et obs_ref(.json)
python -m src.core.compare 

# Résultats : **
-> L'animation 
-> L'angle obtenu 
-> les meilleurs candidats xm et ym points de la mire 
-> le score obtenu
-> La différence entre la mire avec pose de base et la mire obtenu avec la pose "bricolée" par le compare 
Remarque : Pour voir l'angle , score , etc ... dans le terminal , il faut fermer la fenetre de l'animation. Un bug surement lié à animation.py. 


## Structures de données

### Mire

Objet 3D contenant :

* positions des billes en 3D
* ids fixes de chaque bille
stockés dans un dico. 

### Observation

points 2D avec leurs ID obtenus après projection(également dans un dico).

## Fichiers JSON

Les fichiers JSON servent ici à stocker les données du projet dans un format simple et standardisé. L’idée est de pouvoir sauvegarder des structures (par exemple une mire 3D ou une observation 2D), les relire plus tard, les échanger entre plusieurs programmes/scripts, ou conserver des jeux de tests sans devoir regénérer les données à chaque fois.

Dans notre cas, on y stocke :

* pour une **mire** : la liste des billes avec leur `id` fixe et leurs coordonnées `x, y, z`
* pour une **observation** : la liste des points projetés avec éventuellement leur `id`, et leurs coordonnées `u, v`


Introduction rapide au format JSON : https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Scripting/JSON

La librairie python : https://docs.python.org/3/library/json.html



---

## Méthode de travail GitHub

Ne pas travailler directement sur `main`.

Créer une branche :

```bash
git checkout -b nom-branche
```

Puis commit / push / Pull Request.









---

