# TP1 - Partie 3 : Perceptron analogique à deux entrées (Fig. 3)

## Objectif
Implémenter un perceptron analogique à 2 entrées sur Thymio II avec des poids différents pour montrer qu’un capteur peut avoir plus d’influence sur la sortie.

## Modèle utilisé
- Entrées :
  - \(x_1\) : capteur avant gauche (`prox.horizontal[1]`), normalisé entre 0 et 1
  - \(x_2\) : capteur avant droit (`prox.horizontal[3]`), normalisé entre 0 et 1
- Poids : \(w_1 = 1.0\), \(w_2 = 0.4\)
- Somme pondérée :
  $$s = w_1 x_1 + w_2 x_2$$
- Activation analogique (bornée) :
  $$y = f(s) = \max(0, \min(1, s))$$
- Vitesse de recul :
  $$v = -y \cdot V_{max}, \quad V_{max} = 250$$

## Interprétation
- La contribution de chaque capteur est :
  - \(w_1 x_1\) pour le capteur gauche
  - \(w_2 x_2\) pour le capteur droit
- Comme \(w_1 > w_2\), à distance similaire (donc \(x_1 \approx x_2\)), le capteur gauche influence plus la sortie.

## Ce que montre le programme
Le script affiche en temps réel :
- valeurs brutes (`G`, `D`)
- valeurs normalisées (`x1`, `x2`)
- contributions (`w1*x1`, `w2*x2`)
- sortie (`y`) et vitesse (`v`)

Cela permet de vérifier expérimentalement quel capteur domine la décision.

## Protocole de test (validation demandée)
1. Lancer le script :
   - `python TP1_Partie3_Analogique_deux_entrees.py`
2. Approcher un obstacle du capteur gauche seul, noter `w1*x1` et `v`.
3. Approcher ensuite un obstacle du capteur droit seul, à distance similaire.
4. Comparer : la contribution du capteur avec poids plus fort est plus grande, et la vitesse de recul est plus élevée.

## Conclusion
Le modèle de perceptron analogique à deux entrées est correctement implanté :
- poids différents appliqués,
- sortie continue,
- influence du poids le plus fort visible via les contributions affichées.
