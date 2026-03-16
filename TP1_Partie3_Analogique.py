#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TP1 - Partie 3 : Perceptron Analogique
======================================

Implémentation d'un perceptron à une entrée avec sortie analogique (continue).

Comportement :
- Le robot RECULE proportionnellement à la proximité d'un obstacle devant lui
- Plus l'obstacle est proche, plus le robot recule vite
- Entrée : capteur de proximité avant (valeur normalisée entre 0 et 1)
- Sortie : vitesse de recul (proportionnelle, valeur entre 0 et 1)

Modèle du perceptron :
    x1 (capteur avant) → w1 → f(.) → y1 (vitesse recul)
"""

from thymiodirect import Connection, Thymio
import time

# ================== CONFIGURATION ==================

# Connexion série
SERIAL_PORT = "COM6"

# Paramètres du perceptron analogique
W1 = 1.0  # Poids de l'entrée (capteur avant)

# Normalisation du capteur de proximité
CAPTEUR_MAX = 4500  # Valeur maximale du capteur avant (obstacle très proche)
CAPTEUR_MIN = 0     # Valeur minimale (pas d'obstacle)

# Vitesse maximale des moteurs
VITESSE_MAX_RECUL = 250  # Vitesse maximale de recul

# ================== PERCEPTRON ANALOGIQUE ==================

def normaliser_capteur(valeur_brute, min_val=CAPTEUR_MIN, max_val=CAPTEUR_MAX):
    """
    Normalise la valeur du capteur entre 0 et 1.
    
    Args:
        valeur_brute: Valeur brute du capteur
        min_val: Valeur minimale possible
        max_val: Valeur maximale possible
    
    Returns:
        Valeur normalisée entre 0 et 1
    """
    # Clipping pour éviter les dépassements
    valeur_brute = max(min_val, min(valeur_brute, max_val))
    
    # Normalisation linéaire
    if max_val == min_val:
        return 0.0
    
    valeur_normalisee = (valeur_brute - min_val) / (max_val - min_val)
    return valeur_normalisee


def fonction_activation_analogique(s):
    """
    Fonction d'activation pour perceptron analogique.
    Retourne une valeur continue entre 0 et 1.
    
    Args:
        s: Somme pondérée (weighted sum)
    
    Returns:
        Valeur activée entre 0 et 1
    """
    # Fonction identité avec clipping (le plus simple pour un contrôle proportionnel)
    return max(0.0, min(1.0, s))


def perceptron_analogique(x1, w1):
    """
    Perceptron à une entrée avec sortie analogique.
    
    Args:
        x1: Entrée normalisée (0 à 1)
        w1: Poids de l'entrée
    
    Returns:
        Sortie du perceptron (0 à 1)
    """
    # Calcul de la somme pondérée
    s = w1 * x1
    
    # Application de la fonction d'activation
    y1 = fonction_activation_analogique(s)
    
    return y1


def calculer_vitesse_recul(y1):
    """
    Convertit la sortie du perceptron en vitesse de recul.
    
    Args:
        y1: Sortie du perceptron (0 à 1)
    
    Returns:
        Vitesse de recul (valeur négative pour reculer)
    """
    # Vitesse proportionnelle (négative pour reculer)
    vitesse = -int(y1 * VITESSE_MAX_RECUL)
    return vitesse


# ================== CONTRÔLE DU ROBOT ==================


# ================== BOUCLE PRINCIPALE ==================

# Variable globale pour gérer l'arrêt
done = False

def callback_observer(node_id):
    """
    Callback appelé périodiquement pour contrôler le robot.
    Implémente le perceptron analogique.
    """
    global done
    
    if not done:
        try:
            # Vérifier si le bouton central est pressé (arrêt)
            if th[node_id]["button.center"]:
                print("\n🛑 Arrêt demandé (bouton central)")
                th[node_id]["motor.left.target"] = 0
                th[node_id]["motor.right.target"] = 0
                done = True
                return
            
            # ==== PERCEPTRON ANALOGIQUE ====
            
            # 1. Lire le capteur avant central (index 2)
            capteurs = th[node_id]["prox.horizontal"]
            capteur_avant_brut = capteurs[2] if len(capteurs) > 2 else 0
            
            # 2. Normaliser l'entrée (0 à 1)
            x1 = normaliser_capteur(capteur_avant_brut)
            
            # 3. Appliquer le perceptron
            y1 = perceptron_analogique(x1, W1)
            
            # 4. Calculer la vitesse de recul (négative pour reculer)
            vitesse_recul = -int(y1 * VITESSE_MAX_RECUL)
            
            # 5. Appliquer la commande aux moteurs
            th[node_id]["motor.left.target"] = vitesse_recul
            th[node_id]["motor.right.target"] = vitesse_recul
            
            # 6. Affichage en temps réel
            if y1 > 0.1:  # Afficher seulement si obstacle détecté
                intensite = "🔴" if y1 > 0.7 else "🟠" if y1 > 0.4 else "🟡"
                action = f"⬅️ RECUL ({abs(vitesse_recul)} u/s)"
            else:
                intensite = "🟢"
                action = "ARRET (pas d'obstacle)"
            
            print(f"Capteur={capteur_avant_brut:4d} | x1={x1:.2f} | y1={y1:.2f} | {intensite} {action}", end="\r")
            
        except Exception as e:
            print(f"\n⚠️ Erreur dans callback : {e}")
            th[node_id]["motor.left.target"] = 0
            th[node_id]["motor.right.target"] = 0


# ================== PROGRAMME PRINCIPAL ==================

def main():
    """
    Point d'entrée principal du programme.
    """
    global th, done
    
    print("="*60)
    print("TP1 - Partie 3 : Perceptron Analogique à Une Entrée")
    print("="*60)
    print()
    print(" Comportement :")
    print("  - Le robot RECULE quand un obstacle est détecté devant")
    print("  - Plus l'obstacle est proche, plus le robot recule vite")
    print("  - Réponse proportionnelle (analogique, pas tout-ou-rien)")
    print()
    print(" Test :")
    print("  - Approchez votre main du capteur AVANT du robot")
    print("  - Observez la vitesse de recul augmenter")
    print()
    print(" Arrêt : Bouton CENTRAL du Thymio ou Ctrl+C")
    print("="*60)
    print()
    
    try:
        # Connexion au Thymio
        print(f"🔌 Connexion au Thymio sur {SERIAL_PORT}...")
        
        coverage = {"prox.horizontal", "button.center"}
        th = Thymio(
            use_tcp=False,
            serial_port=SERIAL_PORT,
            refreshing_coverage=coverage,
        )
        
        th.connect()
        node_id = th.first_node()
        
        if node_id is None:
            print("❌ Aucun robot Thymio détecté")
            return
        
        print(f"✅ Connecté au node {node_id}")
        print(f"✅ Robot connecté : node {node_id}")
        print()
        print("🚀 Démarrage du perceptron analogique...")
        print("📊 Affichage : Capteur | x1 (normalisé) | y1 (sortie) | Action")
        print("-" * 60)
        
        # Enregistrer le callback
        th.set_variable_observer(node_id, callback_observer)
        
        # Boucle principale
        while not done:
            time.sleep(0.1)  # 10 Hz
        
        # Arrêt propre
        print("\n" + "-" * 60)
        print("🛑 Arrêt des moteurs...")
        th[node_id]["motor.left.target"] = 0
        th[node_id]["motor.right.target"] = 0
        
    except KeyboardInterrupt:
        print("\n\n🛑 Interruption utilisateur (Ctrl+C)")
        if 'node_id' in locals():
            th[node_id]["motor.left.target"] = 0
            th[node_id]["motor.right.target"] = 0
    
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        if 'node_id' in locals():
            th[node_id]["motor.left.target"] = 0
            th[node_id]["motor.right.target"] = 0
    
    finally:
        print("✅ Programme terminé")
        print()


if __name__ == "__main__":
    main()