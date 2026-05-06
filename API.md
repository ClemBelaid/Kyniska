# API Kyniska

## Import principal

```python
from core import Mire, Observation
```

Imports complémentaires :

```python
from core.projection import project_mire_to_plane
from core.geometry import calculBirapport, perpendicular_vector
from core.generation import generer_cube, generer_cone_tronque, generer_cone_tronque_creux
from core.matching import detecter_quadruple_alignes_observation, identification
```

---

## Classes

## Mire

```python
Mire(points, ids=None)
```

Représentation d'une mire 3D.

### Attributs

* `points` : tableau numpy de forme `(n,3)`
* `ids` : identifiants des billes
* `alignes` : `None` ou liste de quadruplets `(a,b,c,d)`

### Méthodes

```python
len(m)
str(m)
m.draw(ax=None)
m.copy()
m.save_json(filename)
Mire.load_json(filename)
```

---

## Observation

```python
Observation(points2d, ids=None, v=None)
```

Représentation d'une observation 2D.

### Attributs

* `points` : tableau numpy de forme `(n,2)`
* `ids` : identifiants optionnels
* `v` : vecteur normal du plan de projection (optionnel)
* `alignes` : métadonnée optionnelle

### Méthodes

```python
len(obs)
str(obs)
obs.draw(ax=None)
obs.copy()
obs.save_json(filename)
Observation.load_json(filename)
obs.ajouterBruit(posRatio, negRatio)
```

---

## Géométrie

## calculBirapport

```python
calculBirapport(a, b, c, d)
```

Calcule le birapport de quatre points alignés.

## perpendicular_vector

```python
perpendicular_vector(v)
```

Renvoie un vecteur perpendiculaire à `v`.

---

## Projection

## project_mire_to_plane

```python
project_mire_to_plane(mire, v)
```

Projette une mire 3D sur un plan normal à `v`.

Retourne une `Observation`.

---

## Génération

## generer_cube

```python
generer_cube(nb_billes, ids=None, largeur=200.0, longueur=200.0, epaisseur=30.0)
```

## generer_cone_tronque

```python
generer_cone_tronque(nb_billes, ids=None, rayon_base=100.0, rayon_sommet=50.0, hauteur=30.0)
```

## generer_cone_tronque_creux

```python
generer_cone_tronque_creux(nb_billes, ids=None, rayon_base=100.0, rayon_sommet=50.0, hauteur=30.0)
```

Ces fonctions retournent une `Mire`.

---

## Identification

## detecter_quadruple_alignes_observation

```python
detecter_quadruple_alignes_observation(obs, eps=0)
```

Détecte des quadruplets alignés dans une observation 2D.

## identification

```python
identification(m, p1, p2, p3, epsilon=0.01)
```

Tente d'identifier les points à partir de trois projections.

---

## Règle de maintenance

Toute modification d'une signature publique doit être reportée dans ce fichier.
