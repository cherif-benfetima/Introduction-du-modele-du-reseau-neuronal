# TP1 - Robot Thymio II : Guide d'Utilisation

## 📋 Description

Ce projet implémente des **perceptrons** pour contrôler un robot **Thymio II** avec plusieurs comportements :

### Partie 1 : Théorie des Perceptrons
- Implémentation des portes logiques OR et AND
- Étude de la séparabilité linéaire

### Partie 2 : Perceptrons Binaires (TOR)
- **Comportement A** : Le robot avance si les deux capteurs arrière détectent un obstacle (ET)
- **Comportement B** : Le robot avance si les deux capteurs au sol détectent une surface (ET)

### Partie 3 : Perceptron Analogique
- **Comportement proportionnel** : Le robot recule d'autant plus vite que l'obstacle avant est proche
- Contrôle continu avec valeurs normalisées (0 à 1)

## 📁 Fichiers du Projet

### Fichiers Python

| Fichier | Description | Partie |
|---------|-------------|--------|
| `TP1.py` | Portes logiques OR et AND avec perceptrons | Partie 1 |
| `TP1_Thymio_Real.py` | Comportements A et B (perceptrons binaires) | Partie 2 |
| `TP1_Partie3_Analogique.py` | Perceptron analogique (recul proportionnel) | Partie 3 |
| `test_comportement_A_ET.py` | Test validé du comportement A | Partie 2 |

### Documentation

| Fichier | Description |
|---------|-------------|
| `Reponses_TP1.md` | Réponses théoriques (séparabilité linéaire, XOR) |
| `Partie2_Robot_Thymio.md` | Documentation complète des comportements A et B |
| `Partie3_Perceptron_Analogique.md` | Documentation du perceptron analogique |
| `README.md` | Ce fichier - guide général |

## 🔧 Installation

### 1. Installer la bibliothèque thymiodirect

```powershell
pip install thymiodirect
```

### 2. Connecter le robot Thymio II

- **Connexion USB** : Branchez le Thymio avec le câble USB
- **Connexion sans fil** : Utilisez le dongle Thymio

### 3. Vérifier la connexion

```powershell
# Tester l'installation complète
python test_installation.py
```

**Note** : Si vous avez un robot Thymio II connecté, le script le détectera. Sinon, vous pouvez quand même utiliser les fichiers de simulation.

## 🚀 Utilisation

### Partie 1 : Test des perceptrons théoriques

```powershell
python TP1.py
```

Affiche les tables de vérité des portes OR et AND.

### Partie 2 : Comportements binaires (TOR)

```powershell
python TP1_Thymio_Real.py
```

Menu interactif pour choisir :
- **A** : Comportement avec capteurs arrière (détection obstacle)
- **B** : Comportement avec capteurs au sol (anti-chute)

### Partie 3 : Perceptron analogique

```powershell
python TP1_Partie3_Analogique.py
```

Le robot recule proportionnellement à la proximité d'un obstacle détecté devant lui.

### Contrôles

- **Démarrage** : Le robot démarre automatiquement après la connexion
- **Arrêt** : Appuyez sur le **bouton central** du Thymio
- **Interruption** : `Ctrl+C` dans le terminal

## 🎯 Fonctionnement des Comportements

### Comportement A : Détection d'obstacles à l'arrière

**Capteurs utilisés** : `prox.horizontal[5]` et `prox.horizontal[6]`

**Perceptron (Opérateur ET)** :
- $w_0 = -1.5$, $w_1 = 1$, $w_2 = 1$
- $s = w_0 + x_1 \cdot w_1 + x_2 \cdot w_2$

| Capteur Gauche | Capteur Droit | Décision |
|----------------|---------------|----------|
| Pas d'obstacle | Pas d'obstacle | Arrêt |
| Pas d'obstacle | Obstacle | Arrêt |
| Obstacle | Pas d'obstacle | Arrêt |
| Obstacle | Obstacle | **Avance** ✓ |

**Usage pratique** : Le robot avance quand il est poussé ou suivi par derrière

### Comportement B : Détection de surface au sol

**Capteurs utilisés** : `prox.ground.delta[0]` et `prox.ground.delta[1]`

**Perceptron (Opérateur ET)** :
- $w_0 = -1.5$, $w_1 = 1$, $w_2 = 1$
- $s = w_0 + x_1 \cdot w_1 + x_2 \cdot w_2$

| Capteur Gauche | Capteur Droit | Décision |
|----------------|---------------|----------|
| Pas de surface | Pas de surface | Arrêt |
| Pas de surface | Surface | Arrêt |
| Surface | Pas de surface | Arrêt |
| Surface | Surface | **Avance** ✓ |

**Usage pratique** : Le robot s'arrête au bord d'une table (sécurité anti-chute)

### Partie 3 : Perceptron Analogique (1 entrée)

**Capteur utilisé** : `prox.horizontal[2]` (capteur avant central)

**Perceptron Analogique** :
- $w_1 = 1.0$
- $s = w_1 \cdot x_1$ (où $x_1$ est normalisé entre 0 et 1)
- $y_1 = f(s)$ (fonction d'activation continue)
- Vitesse de recul : $v = -y_1 \cdot V_{\text{max}}$

| Distance Obstacle | $x_1$ normalisé | $y_1$ sortie | Vitesse Recul |
|-------------------|-----------------|--------------|---------------|
| Très loin (>30cm) | 0.0 | 0.0 | 0 (arrêt) |
| Moyen (~15cm) | 0.5 | 0.5 | -125 (50%) |
| Proche (~5cm) | 1.0 | 1.0 | -250 (100%) |

**Usage pratique** : Évitement progressif d'obstacles, contrôle proportionnel fluide

**Différence avec Partie 2** :
- Signaux continus (0.0 à 1.0) au lieu de binaires (0 ou 1)
- Réponse proportionnelle au lieu de tout-ou-rien
- Mouvement fluide au lieu de saccadé

## 🎨 Affichage Console

Le programme affiche l'état en temps réel dans la console :
- 🟢 **AVANCE** : Robot en mouvement (décision = 1)
- 🔴 **ARRÊTÉ** : Robot immobile (décision = 0)
- Valeurs brutes des capteurs et entrées normalisées (0 ou 1)

**Exemple** :
```
Mode A - G=1850 D= 520 | (1,1) → Décision: 1 | 🟢 AVANCE
```

## ⚙️ Paramètres Ajustables

### Partie 2 : Perceptrons binaires

Dans `TP1_Thymio_Real.py` :

```python
# Vitesse du robot
VITESSE = 150  # Ajuster entre 0 et 500

# Seuils de détection
SEUIL_OBSTACLE = 500  # Capteurs arrière (ajusté après tests)
SEUIL_SURFACE = 400   # Capteurs sol
```

### Partie 3 : Perceptron analogique

Dans `TP1_Partie3_Analogique.py` :

```python
# Poids du perceptron
W1 = 1.0  # Sensibilité (0.5 = doux, 1.5 = vif)

# Normalisation
CAPTEUR_MAX = 4500  # Valeur max du capteur avant

# Vitesse maximale
VITESSE_MAX_RECUL = 250  # Vitesse max de recul
```

## 🧪 Tests et Validation

### Test du comportement A isolé

```powershell
python test_comportement_A_ET.py
```

Test validé du comportement A (capteurs arrière) avec affichage en temps réel.

### Tests théoriques

```powershell
python TP1.py
```

Validation des portes logiques OR et AND sans robot physique.

## 📚 Structure du Code

### Partie 2 : TP1_Thymio_Real.py

```
├── Fonctions du Perceptron
│   ├── calculer_s()          # Calcul : s = w0 + x1*w1 + x2*w2
│   ├── activation()          # Seuil : y = 1 si s≥0 sinon 0
│   └── perceptron()          # Perceptron complet (2 entrées)
│
├── Lecture des Capteurs
│   ├── lire_capteurs_arriere()  # Capteurs [5] et [6]
│   └── lire_capteurs_sol()      # Capteurs [0] et [1]
│
├── Comportements (Opérateur ET)
│   ├── comportement_A()      # Les DEUX capteurs arrière
│   └── comportement_B()      # Les DEUX capteurs sol
│
└── Boucle de Contrôle
    └── callback_observer()   # Exécution à 10 Hz
```

### Partie 3 : TP1_Partie3_Analogique.py

```
├── Normalisation
│   └── normaliser_capteur()   # Valeur brute → [0, 1]
│
├── Perceptron Analogique
│   ├── fonction_activation_analogique()  # f(s) continu
│   └── perceptron_analogique()           # 1 entrée, sortie continue
│
├── Contrôle Proportionnel
│   └── calculer_vitesse_recul()  # y1 → vitesse moteurs
│
└── Boucle de Contrôle
    └── callback_observer()       # Recul proportionnel
```

## 🔍 Dépannage

### Le robot n'est pas détecté

1. Vérifiez que le Thymio est allumé
2. Vérifiez la connexion USB/dongle
3. Installez les drivers Thymio : https://www.thymio.org/

### Le robot ne bouge pas

1. Vérifiez que les capteurs détectent bien (affichage console)
2. Ajustez les seuils `SEUIL_OBSTACLE` et `SEUIL_SURFACE`
3. Augmentez la `VITESSE`

### Erreur d'importation

```powershell
pip install --upgrade thymiodirect
```

## 📖 Documentation Complète

### Guides détaillés

| Document | Contenu |
|----------|---------|
| [Reponses_TP1.md](Reponses_TP1.md) | Questions théoriques : séparabilité linéaire, impossibilité du XOR |
| [Partie2_Robot_Thymio.md](Partie2_Robot_Thymio.md) | Comportements A et B (perceptrons binaires ET) |
| [Partie3_Perceptron_Analogique.md](Partie3_Perceptron_Analogique.md) | Perceptron analogique, contrôle proportionnel |

### Références externes

- Documentation Thymio II : https://www.thymio.org/
- Bibliothèque thymiodirect : https://github.com/mbonani/thymiodirect
- Cours IA et Robotique

## 🎓 Concepts Couverts

### Partie 1 : Théorie
✅ Perceptron simple (2 entrées, 1 sortie)  
✅ Portes logiques OR et AND  
✅ Séparabilité linéaire  
✅ Impossibilité du XOR avec un perceptron simple  

### Partie 2 : Perceptrons Binaires
✅ Opérateur logique ET (AND)  
✅ Traitement TOR (Tout-Ou-Rien)  
✅ Normalisation par seuillage  
✅ Boucle de contrôle temps réel  

### Partie 3 : Perceptron Analogique
✅ Signaux continus (0.0 à 1.0)  
✅ Normalisation linéaire Min-Max  
✅ Fonction d'activation continue  
✅ Contrôle proportionnel  

## 👨‍💻 Auteur

TP1 - Intelligence Artificielle  
Chapitre 1 - Introduction méthodologique et prise en main
