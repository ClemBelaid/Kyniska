# Projet Kyniska

## Objectif

Identifier et numéroter automatiquement les billes projetées en 2D à partir d’une mire 3D connue.

Le but final est de retrouver la correspondance entre :

- les billes de la mire (points 3D avec ids fixes)
- les points détectés sur une image radiographique 2D

---

## Structure actuelle du projet

### main.py

Fichier de test / exécution rapide.

### mire.py

Contient actuellement :

* classe `Mire` : représentation d’une mire 3D
* classe `Observation` : représentation d’une projection / liste de points 2D

---

## Structures de données

### Mire

Objet 3D contenant :

* positions des billes en 3D
* ids fixes de chaque bille

### Observation

Liste de points 2D obtenus après projection.

<<<<<<< HEAD
## Fichiers JSON

Les fichiers JSON servent ici à stocker les données du projet dans un format simple et standardisé. L’idée est de pouvoir sauvegarder des structures (par exemple une mire 3D ou une observation 2D), les relire plus tard, les échanger entre plusieurs programmes/scripts, ou conserver des jeux de tests sans devoir regénérer les données à chaque fois.

Dans notre cas, on y stocke :

* pour une **mire** : la liste des billes avec leur `id` fixe et leurs coordonnées `x, y, z`
* pour une **observation** : la liste des points projetés avec éventuellement leur `id`, et leurs coordonnées `u, v`

Exemple : un program peut générer une projection bruitée, l’enregistrer en JSON, puis un autre peut la charger pour tester un algorithme d’identification.

Introduction rapide au format JSON : https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Scripting/JSON

La librairie python : https://docs.python.org/3/library/json.html

=======
>>>>>>> 2019281 (README + documentation mire.py)
---

## Étapes

* structure `Mire`
* structure `Observation`
* sauvegarde JSON
* chargement JSON

### Géométrie

* projection sur plan
* rotations 3D
* génération de poses aléatoires

### Génération de données

* créer projections simulées
* ajouter bruit
* retirer ids pour créer cas réel

### Identification

* retrouver les ids à partir des points 2D
* tester :

  * bi-rapport
  * enveloppe convexe
  * voisinage / distances

### Validation

* comparer résultat avec vérité terrain
* taux de réussite
* robustesse au bruit

---

## Méthode de travail GitHub

Ne pas travailler directement sur `main`.

Créer une branche :

```bash
git checkout -b nom-branche
```

Puis commit / push / Pull Request.

---

## Remarque

Le projet est encore en phase de structuration.
L’objectif actuel est d’avoir une base claire (structure de code) avant d’attaquer les algorithmes principaux.

