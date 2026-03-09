# TP1 - Partie 2 : Application des Perceptrons au Robot Thymio II

## 📋 Objectif

Implémenter deux comportements intelligents sur le robot Thymio II en utilisant des **perceptrons** avec l'opérateur logique **ET (AND)**.

---

## 🤖 Comportement A : Détection d'obstacles à l'arrière

### Description
Le robot se déplace vers l'avant **SI ET SEULEMENT SI** les **deux capteurs de proximité arrière** détectent la présence d'un obstacle.

### Capteurs utilisés
- **capteur_gauche** : `prox.horizontal[5]`
- **capteur_droit** : `prox.horizontal[6]`

### Perceptron (Opérateur ET)

**Poids** :
- $w_0 = -1.5$ (biais)
- $w_1 = 1$ (capteur gauche)
- $w_2 = 1$ (capteur droit)

**Calcul** :
$$s = w_0 + x_1 \cdot w_1 + x_2 \cdot w_2 = -1.5 + x_1 + x_2$$

**Fonction d'activation** :
$$y = \begin{cases} 
1 & \text{si } s \geq 0 \text{ (robot avance)} \\
0 & \text{si } s < 0 \text{ (robot s'arrête)}
\end{cases}$$

### Table de vérité

| Capteur Gauche | Capteur Droit | $x_1$ | $x_2$ | $s$ | Décision $y$ | Action |
|----------------|---------------|-------|-------|-----|--------------|--------|
| Pas d'obstacle | Pas d'obstacle | 0 | 0 | -1.5 | 0 | Arrêter |
| Pas d'obstacle | Obstacle | 0 | 1 | -0.5 | 0 | Arrêter |
| Obstacle | Pas d'obstacle | 1 | 0 | -0.5 | 0 | Arrêter |
| **Obstacle** | **Obstacle** | **1** | **1** | **0.5** | **1** | **Avancer ✓** |

### Normalisation des capteurs

Pour convertir les valeurs brutes des capteurs en entrées binaires (0 ou 1) :

```python
SEUIL_OBSTACLE = 500  # Valeur à ajuster selon le robot

x1 = 1 si capteur_gauche > SEUIL_OBSTACLE sinon 0
x2 = 1 si capteur_droit > SEUIL_OBSTACLE sinon 0
```

### Test pratique

Pour tester ce comportement :
1. **Placez vos DEUX MAINS** derrière le robot (une de chaque côté)
2. **Rapprochez-les** à environ 3-5 cm des capteurs arrière
3. Le robot doit **avancer** (affichage console 🟢) quand les deux capteurs détectent
4. Le robot **s'arrête** (affichage console 🔴) si un seul ou aucun capteur ne détecte

### Utilisation pratique

Ce comportement permet au robot de :
- Suivre quelqu'un qui le pousse par derrière
- Avancer quand il est coincé entre deux obstacles à l'arrière
- Réagir à une "pression" arrière symétrique

---

## 🏁 Comportement B : Détection de surface au sol

### Description
Le robot se déplace vers l'avant **SI ET SEULEMENT SI** les **deux capteurs au sol** détectent une surface (évitement de chute).

### Capteurs utilisés
- **capteur_gauche** : `prox.ground.delta[0]`
- **capteur_droit** : `prox.ground.delta[1]`

### Perceptron (Opérateur ET)

**Poids** :
- $w_0 = -1.5$ (biais)
- $w_1 = 1$ (capteur sol gauche)
- $w_2 = 1$ (capteur sol droit)

**Calcul** :
$$s = w_0 + x_1 \cdot w_1 + x_2 \cdot w_2 = -1.5 + x_1 + x_2$$

**Fonction d'activation** :
$$y = \begin{cases} 
1 & \text{si } s \geq 0 \text{ (robot avance)} \\
0 & \text{si } s < 0 \text{ (robot s'arrête)}
\end{cases}$$

### Table de vérité

| Capteur Sol Gauche | Capteur Sol Droit | $x_1$ | $x_2$ | $s$ | Décision $y$ | Action |
|--------------------|-------------------|-------|-------|-----|--------------|--------|
| Pas de surface | Pas de surface | 0 | 0 | -1.5 | 0 | Arrêter |
| Pas de surface | Surface | 0 | 1 | -0.5 | 0 | Arrêter |
| Surface | Pas de surface | 1 | 0 | -0.5 | 0 | Arrêter |
| **Surface** | **Surface** | **1** | **1** | **0.5** | **1** | **Avancer ✓** |

### Normalisation des capteurs

Pour convertir les valeurs brutes des capteurs en entrées binaires (0 ou 1) :

```python
SEUIL_SURFACE = 400  # Valeur à ajuster selon le robot

x1 = 1 si capteur_sol_gauche > SEUIL_SURFACE sinon 0
x2 = 1 si capteur_sol_droit > SEUIL_SURFACE sinon 0
```

### Test pratique

Pour tester ce comportement :
1. **Placez le robot sur une table** (surface claire de préférence)
2. Le robot doit **avancer** (affichage console 🟢) car les deux capteurs détectent la surface
3. **Approchez le robot du bord** de la table
4. Le robot doit **s'arrêter** (affichage console 🔴) quand un capteur ne détecte plus la surface

### Utilisation pratique

Ce comportement permet au robot de :
- **Éviter de tomber** d'une table ou d'un rebord
- **Sécurité anti-chute** automatique
- Naviguer en toute sécurité sur des surfaces surélevées

---

## 💻 Fichiers du projet

### Fichiers principaux

| Fichier | Description | Utilisation |
|---------|-------------|-------------|
| **TP1_Thymio_Real.py** | Programme principal interactif | `python TP1_Thymio_Real.py` |
| **test_comportement_A_ET.py** | Test dédié au comportement A | `python test_comportement_A_ET.py` |

### Fichier principal : `TP1_Thymio_Real.py`

Programme interactif permettant de choisir entre les comportements A et B.

**Lancement** :
```powershell
python TP1_Thymio_Real.py
```

**Menu** :
```
Choisissez le comportement :
  A - Détection d'obstacles à l'arrière
  B - Détection de surface au sol
Votre choix (A/B) : 
```

**Affichage en temps réel** :
```
Mode A - G=1850 D= 520 | (1,1) → Décision: 1 | 🟢 AVANCE
Mode B - G= 953 D= 951 | (1,1) → Décision: 1 | 🟢 AVANCE
```

---

## 🔧 Configuration

### Port série
Le robot est configuré pour utiliser **COM3**. Si votre robot est sur un autre port :

```python
serial_port = "COM3"  # Modifiez selon votre configuration
```

### Seuils des capteurs

Les seuils peuvent être ajustés selon votre robot :

```python
# Dans le code
SEUIL_OBSTACLE = 500  # Comportement A (capteurs arrière)
SEUIL_SURFACE = 400   # Comportement B (capteurs sol)
```

**Recommandations** :
- Si les capteurs sont **trop sensibles** → augmentez le seuil
- Si les capteurs **ne détectent pas** → baissez le seuil (300, 200)
- Testez avec des objets **clairs/blancs** (mieux détectés que le noir)

---

## 🎯 Résultats attendus

### Comportement A (Opérateur ET)
✅ **Robot arrêté** si 0 ou 1 seul capteur détecte  
✅ **Robot avance** uniquement si les 2 capteurs détectent  
✅ Affichage console : 🔴 ARRÊTÉ / 🟢 AVANCE  

### Comportement B (Opérateur ET)
✅ **Robot arrêté** si proche du bord (0 ou 1 capteur sol)  
✅ **Robot avance** sur surface stable (2 capteurs détectent)  
✅ Système anti-chute fonctionnel  

---

## 📊 Architecture du code

```
Programme Principal
├── Connexion au Thymio (COM3)
├── Choix du comportement (A ou B)
├── Callback observer (boucle à 10 Hz)
│   ├── Lecture des capteurs
│   ├── Normalisation (valeurs brutes → 0 ou 1)
│   ├── Calcul avec perceptron ET
│   │   └── s = -1.5 + x1 + x2
│   ├── Activation (s ≥ 0 → y=1, sinon y=0)
│   └── Action moteurs + affichage
└── Arrêt (bouton central ou Ctrl+C)
```

---

## 🧪 Validation expérimentale

### Tests effectués

| Test | Comportement A | Comportement B |
|------|----------------|----------------|
| Un capteur détecte | ❌ Robot arrêté | ❌ Robot arrêté |
| Deux capteurs détectent | ✅ Robot avance | ✅ Robot avance |
| Aucun capteur | ❌ Robot arrêté | ❌ Robot arrêté |

### Opérateur ET validé

L'opérateur logique **ET (AND)** a été validé sur le robot réel :
- Table de vérité respectée
- Normalisation fonctionnelle
- Perceptron calcule correctement
- Actions cohérentes avec les décisions

---

## 🎓 Concepts démontrés

1. ✅ **Perceptron simple** : somme pondérée + fonction d'activation
2. ✅ **Opérateur logique ET** : nécessite toutes les conditions vraies
3. ✅ **Normalisation des données** : capteurs bruts → entrées binaires
4. ✅ **Seuillage adaptatif** : ajustement selon le matériel
5. ✅ **Boucle de contrôle temps réel** : décisions à 10 Hz
6. ✅ **Application robotique concrète** : évitement, détection, sécurité

---

## 📌 Commandes rapides

```powershell
# Programme principal (menu interactif)
python TP1_Thymio_Real.py

# Test direct du comportement A
python test_comportement_A_ET.py

# Arrêter le robot
# → Appuyez sur le bouton CENTRAL du Thymio
# → Ou faites Ctrl+C dans le terminal
```

---

## 🔍 Dépannage

### Le robot ne détecte pas (mode A)
1. Vérifiez que vos **deux mains** sont proches des capteurs arrière
2. Baissez le seuil : `SEUIL_OBSTACLE = 300`
3. Utilisez un **objet large** (livre, boîte)
4. Consultez les valeurs brutes affichées

### Le robot tombe de la table (mode B)
1. Augmentez le seuil : `SEUIL_SURFACE = 600`
2. Testez sur une **surface claire** (meilleure détection)
3. Vérifiez que les capteurs au sol sont propres

### Erreur de connexion
```
❌ Erreur de connexion: PermissionError
```
→ Un autre programme utilise le Thymio (fermez Aseba Studio)  
→ Débranchez et rebranchez le câble USB

---

## ✅ Conclusion

Ce TP démontre l'implémentation réussie de **perceptrons** sur un robot réel pour créer des comportements intelligents basés sur la logique **ET (AND)**. Les deux comportements montrent comment un calcul simple (somme pondérée + seuil) peut produire des décisions robustes pour la navigation et la sécurité d'un robot autonome.

**Compétences acquises** :
- Programmation d'un robot réel
- Implémentation de réseaux de neurones simples
- Traitement de données de capteurs
- Réglage de paramètres en temps réel
