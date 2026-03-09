# TP1 - Partie 3 : Perceptron Analogique

## 📋 Objectif

Implémenter un **perceptron à une entrée** avec sortie **analogique** (valeurs continues) sur le robot Thymio II.

Contrairement aux parties précédentes où les valeurs étaient binaires (0 ou 1), ici les entrées et sorties évoluent dans une gamme continue de valeurs entre 0 et 1.

---

## 🤖 Comportement du Robot

### Description
Le robot **recule** proportionnellement à la proximité d'un obstacle détecté devant lui.

**Plus l'obstacle est proche → Plus le robot recule vite**

### Différence avec les parties précédentes

| Caractéristique | Parties 1-2 (TOR) | Partie 3 (Analogique) |
|-----------------|-------------------|------------------------|
| Type de signal | Binaire (0 ou 1) | Continu (0.0 à 1.0) |
| Nombre d'entrées | 2 capteurs | 1 capteur |
| Fonction d'activation | Seuil (step) | Continue (linéaire) |
| Sortie moteurs | Vitesse fixe | Vitesse proportionnelle |
| Direction | Avance | Recule |

---

## 🧠 Modèle du Perceptron Analogique

### Architecture

```
x₁ (capteur avant) ──[w₁]──> [+] ──[f]──> y₁ (vitesse recul)
```

**Une seule entrée** :
- $x_1$ : Valeur du capteur de proximité avant (normalisée entre 0 et 1)

**Un poids** :
- $w_1 = 1.0$ : Poids associé à l'entrée

**Fonction d'activation analogique** :
- $f(s) = \max(0, \min(1, s))$ : Fonction identité avec clipping

**Sortie** :
- $y_1$ : Intensité de recul (entre 0 et 1)

### Équations

**1. Somme pondérée** :
$$s = w_1 \cdot x_1 = 1.0 \cdot x_1$$

**2. Fonction d'activation** :
$$y_1 = f(s) = \begin{cases} 
0 & \text{si } s < 0 \\
s & \text{si } 0 \leq s \leq 1 \\
1 & \text{si } s > 1
\end{cases}$$

**3. Vitesse de recul** :
$$v_{\text{recul}} = -y_1 \cdot V_{\text{max}}$$

Où $V_{\text{max}} = 250$ (vitesse maximale)

---

## 📊 Normalisation des Capteurs

### Capteur de proximité avant

Le capteur infrarouge avant retourne des valeurs brutes entre 0 et ~4500.

**Normalisation linéaire** :
$$x_1 = \frac{\text{valeur\_brute} - \text{min}}{\text{max} - \text{min}}$$

Avec :
- $\text{min} = 0$ (pas d'obstacle)
- $\text{max} = 4500$ (obstacle très proche)

### Exemple de normalisation

| Distance | Valeur Brute | $x_1$ Normalisé | $y_1$ Sortie | Vitesse Recul |
|----------|--------------|-----------------|--------------|---------------|
| Très loin | 0 | 0.00 | 0.00 | 0 (arrêt) |
| Loin | 900 | 0.20 | 0.20 | -50 |
| Moyen | 2250 | 0.50 | 0.50 | -125 |
| Proche | 3600 | 0.80 | 0.80 | -200 |
| Très proche | 4500 | 1.00 | 1.00 | -250 (max) |

**Interprétation** :
- Pas d'obstacle (x₁=0) → Pas de recul (v=0)
- Obstacle à 50% de proximité → Recul à 50% de vitesse max
- Obstacle très proche (x₁=1) → Recul maximal

---

## 💻 Implémentation

### Fichier : `TP1_Partie3_Analogique.py`

#### Fonctions principales

```python
def normaliser_capteur(valeur_brute, min_val=0, max_val=4500):
    """Convertit valeur brute (0-4500) en valeur normalisée (0-1)"""
    valeur_brute = max(min_val, min(valeur_brute, max_val))
    return (valeur_brute - min_val) / (max_val - min_val)

def fonction_activation_analogique(s):
    """Fonction d'activation continue avec clipping"""
    return max(0.0, min(1.0, s))

def perceptron_analogique(x1, w1):
    """Perceptron à une entrée"""
    s = w1 * x1
    y1 = fonction_activation_analogique(s)
    return y1

def calculer_vitesse_recul(y1):
    """Convertit sortie (0-1) en vitesse moteurs"""
    return -int(y1 * VITESSE_MAX_RECUL)
```

#### Boucle de contrôle

```python
def callback_observer(node_id):
    # 1. Lire capteur avant (index 2)
    capteur_avant_brut = th[node_id]["prox.horizontal"][2]
    
    # 2. Normaliser (0-4500 → 0-1)
    x1 = normaliser_capteur(capteur_avant_brut)
    
    # 3. Perceptron analogique
    y1 = perceptron_analogique(x1, w1=1.0)
    
    # 4. Calculer vitesse (négative = recul)
    vitesse_recul = calculer_vitesse_recul(y1)
    
    # 5. Appliquer aux moteurs
    th[node_id]["motor.left.target"] = vitesse_recul
    th[node_id]["motor.right.target"] = vitesse_recul
```

---

## 🚀 Utilisation

### Lancement du programme

```powershell
python TP1_Partie3_Analogique.py
```

### Affichage en temps réel

```
Capteur=2340 | x1=0.52 | y1=0.52 | 🟠 ⬅️ RECUL (130 u/s)
```

**Légende** :
- **Capteur** : Valeur brute du capteur avant
- **x1** : Entrée normalisée du perceptron
- **y1** : Sortie du perceptron
- **Emoji** : 🟢 (loin) → 🟡 (moyen) → 🟠 (proche) → 🔴 (très proche)
- **Action** : Vitesse de recul en unités/seconde

### Test pratique

1. **Lancez le programme**
2. **Approchez votre main** du capteur avant du robot (capteur central)
3. **Observez** :
   - x₁ augmente (0.0 → 1.0)
   - y₁ augmente proportionnellement
   - Le robot recule de plus en plus vite
4. **Éloignez votre main** :
   - x₁ diminue
   - Le robot ralentit progressivement
   - Le robot s'arrête quand aucun obstacle n'est détecté

### Arrêt

- **Bouton central** du Thymio
- **Ctrl+C** dans le terminal

---

## 🎯 Concepts Démontrés

### 1. Signal analogique vs binaire

**Binaire (TOR - Tout-Ou-Rien)** :
```
Obstacle détecté → x = 1 → Vitesse fixe
Pas d'obstacle   → x = 0 → Arrêt
```

**Analogique (Continu)** :
```
Très proche  → x = 1.0 → Vitesse max
Proche       → x = 0.8 → Vitesse 80%
Moyen        → x = 0.5 → Vitesse 50%
Loin         → x = 0.2 → Vitesse 20%
Très loin    → x = 0.0 → Arrêt
```

### 2. Contrôle proportionnel

Le perceptron analogique implémente un **contrôle proportionnel** :
$$\text{Commande} \propto \text{Mesure}$$

C'est la base des systèmes de régulation (PID = Proportionnel Intégral Dérivé).

### 3. Normalisation des données

**Pourquoi normaliser ?**
- Les capteurs retournent des valeurs dans différentes gammes
- Les réseaux de neurones fonctionnent mieux avec des valeurs [0, 1] ou [-1, 1]
- Facilite la comparaison et le réglage des poids

**Méthode Min-Max** :
$$x_{\text{norm}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$$

### 4. Fonction d'activation continue

**Fonction identité avec clipping** :
- Simple et efficace pour contrôle proportionnel
- Garantit que la sortie reste dans [0, 1]
- Pas de saturation au milieu de la plage

**Alternatives** :
- **Sigmoïde** : $f(s) = \frac{1}{1 + e^{-s}}$ (courbe en S)
- **ReLU** : $f(s) = \max(0, s)$ (sans borne supérieure)
- **Tanh** : $f(s) = \tanh(s)$ (sortie entre -1 et 1)

---

## 📈 Courbe de Réponse

### Relation Entrée-Sortie

```
Sortie y₁
    1.0 |         ╱─────────
        |        ╱
    0.8 |       ╱
        |      ╱
    0.6 |     ╱
        |    ╱
    0.4 |   ╱
        |  ╱
    0.2 | ╱
        |╱
    0.0 +──────────────────> Entrée x₁
        0  0.2  0.4  0.6  0.8  1.0
```

**Avec w₁ = 1.0** : Relation linéaire parfaite (y₁ = x₁)

### Modification du poids

**Si w₁ = 0.5** : Réponse atténuée
```python
W1 = 0.5  # Robot recule plus doucement
```

**Si w₁ = 2.0** : Réponse amplifiée (attention au clipping)
```python
W1 = 2.0  # Robot recule plus vigoureusement
```

---

## 🔧 Paramètres Ajustables

### Dans le code

```python
# Poids du perceptron
W1 = 1.0  # Modifier pour changer la sensibilité

# Normalisation
CAPTEUR_MAX = 4500  # Ajuster selon votre robot
CAPTEUR_MIN = 0

# Vitesse maximale
VITESSE_MAX_RECUL = 250  # Limiter si trop rapide
```

### Expériences

**Test 1 - Sensibilité réduite** :
```python
W1 = 0.5
```
→ Le robot recule moins vite (plus prudent)

**Test 2 - Sensibilité accrue** :
```python
W1 = 1.5
```
→ Le robot recule plus vigoureusement

**Test 3 - Vitesse limitée** :
```python
VITESSE_MAX_RECUL = 150
```
→ Vitesse maximale réduite (plus sécuritaire)

---

## 🎓 Applications Pratiques

### 1. Évitement d'obstacles
- Ralentir progressivement en approchant d'un mur
- Parking automatique

### 2. Suivi de ligne
- Correction proportionnelle de la trajectoire
- Virage doux au lieu de saccadé

### 3. Contrôle de vitesse adaptatif
- Vitesse réduite en environnement encombré
- Vitesse maximale en espace dégagé

### 4. Régulation de distance
- Maintenir une distance constante avec un objet
- Suivi de cible mobile

---

## 📊 Comparaison Partie 2 vs Partie 3

| Aspect | Partie 2 (Binaire) | Partie 3 (Analogique) |
|--------|--------------------|-----------------------|
| **Entrées** | 2 capteurs | 1 capteur |
| **Type** | Discret (0/1) | Continu (0.0-1.0) |
| **Activation** | Seuil (step) | Linéaire (identité) |
| **Comportement** | ON/OFF | Proportionnel |
| **Mouvement** | Saccadé | Fluide |
| **Précision** | Faible | Élevée |
| **Cas d'usage** | Décisions binaires | Contrôle fin |

**Analogie** :
- **Binaire** = Interrupteur (lumière ON/OFF)
- **Analogique** = Variateur (intensité variable)

---

## ✅ Validation Expérimentale

### Tests à effectuer

| Test | Procédure | Résultat attendu |
|------|-----------|------------------|
| **Test 1** | Main loin (>30 cm) | Robot arrêté (v=0) |
| **Test 2** | Main à 15 cm | Recul lent (~50% vitesse) |
| **Test 3** | Main à 5 cm | Recul rapide (~90% vitesse) |
| **Test 4** | Main en approche graduelle | Accélération progressive |
| **Test 5** | Main en retrait graduel | Décélération progressive |

### Critères de réussite

✅ **Linéarité** : Vitesse proportionnelle à la proximité  
✅ **Fluidité** : Pas de changements brusques  
✅ **Réactivité** : Réponse immédiate au changement  
✅ **Stabilité** : Pas d'oscillations  

---

## 🔍 Dépannage

### Le robot ne recule pas
1. Vérifiez que le **capteur avant** (index 2) fonctionne
2. Affichez la valeur brute : `print(capteur_avant_brut)`
3. Approchez votre main à **moins de 10 cm**
4. Utilisez un objet **clair/blanc** (meilleure détection)

### Le robot recule trop vite
```python
VITESSE_MAX_RECUL = 150  # Réduire la vitesse max
```

### Le robot recule trop lentement
```python
W1 = 1.5  # Augmenter le gain
CAPTEUR_MAX = 3000  # Réduire pour saturer plus tôt
```

### Valeurs affichées = 0
→ Problème de connexion, relancez le programme

---

## 🎯 Conclusion

Cette partie démontre l'utilisation de **perceptrons analogiques** pour un contrôle **proportionnel** et **fluide** d'un robot. 

**Concepts clés acquis** :
- ✅ Normalisation de données continues
- ✅ Fonction d'activation analogique
- ✅ Contrôle proportionnel
- ✅ Différence entre traitement binaire et analogique
- ✅ Application du perceptron à une entrée

**Transition** :
Ce type de perceptron analogique est la base des **réseaux de neurones modernes** qui traitent des signaux continus (images, sons, capteurs).

---

## 📌 Commandes Rapides

```powershell
# Lancer le perceptron analogique
python TP1_Partie3_Analogique.py

# Arrêter : Bouton central du Thymio ou Ctrl+C
```

---

## 📚 Pour Aller Plus Loin

### Extensions possibles

1. **Ajout d'un biais** : $s = w_0 + w_1 \cdot x_1$ (décalage de la courbe)
2. **Fonction sigmoïde** : Courbe en S au lieu de linéaire
3. **Deux capteurs** : Perceptron à 2 entrées analogiques
4. **Zone morte** : Pas de réaction si obstacle très loin
5. **Hystérésis** : Éviter les oscillations

### Code zone morte

```python
def perceptron_avec_zone_morte(x1, w1, seuil_min=0.1):
    if x1 < seuil_min:
        return 0.0  # Zone morte
    else:
        return fonction_activation_analogique(w1 * x1)
```
