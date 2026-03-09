# Réponses aux Questions - TP1 : Perceptron et Portes Logiques

## Question 1 : Est-ce qu'on peut obtenir des poids satisfaisant les valeurs des opérateurs logiques ET/OU ?

### Réponse : **OUI**

Les opérateurs logiques ET et OU peuvent être représentés par un perceptron simple car ils sont **linéairement séparables**.

### Opérateur OU (OR)

**Poids trouvés :** $w_0 = -0.5$, $w_1 = 1$, $w_2 = 1$

Formule : $s = w_0 + x_1 \cdot w_1 + x_2 \cdot w_2$

| $x_1$ | $x_2$ | $s$ | $y$ | Résultat attendu |
|-------|-------|-----|-----|------------------|
| 0 | 0 | -0.5 | 0 | ✓ |
| 0 | 1 | 0.5 | 1 | ✓ |
| 1 | 0 | 0.5 | 1 | ✓ |
| 1 | 1 | 1.5 | 1 | ✓ |

**Tous les cas sont corrects !**

### Opérateur ET (AND)

**Poids trouvés :** $w_0 = -1.5$, $w_1 = 1$, $w_2 = 1$

| $x_1$ | $x_2$ | $s$ | $y$ | Résultat attendu |
|-------|-------|-----|-----|------------------|
| 0 | 0 | -1.5 | 0 | ✓ |
| 0 | 1 | -0.5 | 0 | ✓ |
| 1 | 0 | -0.5 | 0 | ✓ |
| 1 | 1 | 0.5 | 1 | ✓ |

**Tous les cas sont corrects !**

### Explication

Ces opérateurs sont **linéairement séparables**, ce qui signifie qu'on peut tracer une ligne droite dans l'espace $(x_1, x_2)$ pour séparer les points où $y = 1$ des points où $y = 0$. Le perceptron trouve précisément cette frontière de décision linéaire.

---

## Question 2 : Est-ce qu'on peut représenter à l'aide d'un perceptron l'opérateur OU-Exclusif ?

### Réponse : **NON**

### Table de vérité du XOR

| $x_1$ | $x_2$ | $y$ |
|-------|-------|-----|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

### Pourquoi c'est impossible ?

L'opérateur XOR (OU-Exclusif) n'est **pas linéairement séparable**. 

**Visualisation du problème :**

```
     x2
      |
   1  | ● (1,0)  ○ (1,1)
      |    y=1     y=0
   0  | ○ (0,0)  ● (0,1)
      |    y=0     y=1
      |___________________ x1
         0         1
```

Légende :
- ○ = sortie 0 (points rouges)
- ● = sortie 1 (points bleus)

**Le problème :** Il est impossible de tracer une seule ligne droite qui sépare les points bleus (●) des points rouges (○). Les points sont disposés en "échiquier" ou en diagonale opposée.

### Démonstration mathématique

Pour qu'un perceptron fonctionne, il faut trouver des poids $w_0, w_1, w_2$ tels que :
- $w_0 + 0 \cdot w_1 + 0 \cdot w_2 < 0$ (pour (0,0) → 0)
- $w_0 + 0 \cdot w_1 + 1 \cdot w_2 \geq 0$ (pour (0,1) → 1)
- $w_0 + 1 \cdot w_1 + 0 \cdot w_2 \geq 0$ (pour (1,0) → 1)
- $w_0 + 1 \cdot w_1 + 1 \cdot w_2 < 0$ (pour (1,1) → 0)

Ce qui donne :
1. $w_0 < 0$
2. $w_0 + w_2 \geq 0$
3. $w_0 + w_1 \geq 0$
4. $w_0 + w_1 + w_2 < 0$

Des équations (2) et (3) : $w_1 \geq -w_0$ et $w_2 \geq -w_0$

Donc : $w_1 + w_2 \geq -2w_0$

Ce qui implique : $w_0 + w_1 + w_2 \geq w_0 - 2w_0 = -w_0 > 0$

**Contradiction avec l'équation (4) !**

Il n'existe donc **aucun ensemble de poids** satisfaisant simultanément toutes les conditions.

### Solution : Perceptron Multi-Couches (MLP)

Pour implémenter XOR, il faut utiliser un **perceptron multi-couches** avec au moins :
- **1 couche cachée** contenant au moins 2 neurones
- **1 couche de sortie**

Cette architecture peut créer des frontières de décision non-linéaires nécessaires pour séparer les points du XOR.

---

## Résumé

| Opérateur | Possible avec perceptron simple ? | Raison |
|-----------|-----------------------------------|--------|
| **OU (OR)** | ✓ OUI | Linéairement séparable |
| **ET (AND)** | ✓ OUI | Linéairement séparable |
| **XOR** | ✗ NON | Non linéairement séparable |

**Conclusion :** Le perceptron simple est limité aux problèmes linéairement séparables. Pour des problèmes plus complexes comme XOR, il faut utiliser des réseaux de neurones plus profonds.
