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

