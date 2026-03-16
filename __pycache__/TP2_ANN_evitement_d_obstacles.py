import time
import numpy as np
from thymiodirect import Thymio


# ============================================================
# CONFIGURATION
# ============================================================

SERIAL_PORT = "COM6"          
MAX_SPEED = 250               
CAPTEUR_MIN = 0.0
CAPTEUR_MAX = 4500.0

# Indices des capteurs avant du Thymio
# À ajuster si besoin selon votre configuration
IDX_GAUCHE = 0
IDX_CENTRE = 2
IDX_DROITE = 4

# Poids du réseau
w_fwd = 0.4
w_back = 1.4
w_pos = 0.8
w_neg = 0.8

# Matrice des poids (2 neurones de sortie x 4 entrées)
# x = [1, x1, x2, x3]^T
W = np.array([
    [w_fwd,  w_pos,   -w_back, -w_neg],
    [w_fwd, -w_neg,   -w_back,  w_pos]
], dtype=float)

done = False
th = None


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def normaliser_capteurs(valeurs_brutes: np.ndarray,
                        min_val: float = CAPTEUR_MIN,
                        max_val: float = CAPTEUR_MAX) -> np.ndarray:
    """
    Normalise les capteurs entre 0 et 1.
    """
    valeurs_brutes = np.clip(valeurs_brutes.astype(float), min_val, max_val)
    if max_val <= min_val:
        return np.zeros_like(valeurs_brutes, dtype=float)
    return (valeurs_brutes - min_val) / (max_val - min_val)


def activation(u: np.ndarray) -> np.ndarray:
    """
    Fonction d'activation non linéaire bornée.
    tanh permet d'obtenir une sortie dans [-1, 1].
    """
    return np.tanh(u)


def lire_capteurs_avant(node_id: int) -> np.ndarray:
    """
    Lit les 3 capteurs avant utiles au modèle :
    gauche, centre, droite.
    Retourne un ndarray numpy de taille 3.
    """
    prox = np.asarray(th[node_id]["prox.horizontal"], dtype=float)

    if prox.size < 5:
        # Sécurité minimale si la lecture est incomplète
        capteurs = np.zeros(3, dtype=float)
        if prox.size > IDX_GAUCHE:
            capteurs[0] = prox[IDX_GAUCHE]
        if prox.size > IDX_CENTRE:
            capteurs[1] = prox[IDX_CENTRE]
        if prox.size > IDX_DROITE:
            capteurs[2] = prox[IDX_DROITE]
        return capteurs

    return np.array([
        prox[IDX_GAUCHE],
        prox[IDX_CENTRE],
        prox[IDX_DROITE]
    ], dtype=float)


def construire_entree(capteurs_norm: np.ndarray) -> np.ndarray:
    """
    Construit le vecteur d'entrée x = [1, x1, x2, x3]^T.
    x1 = capteur gauche
    x2 = capteur centre
    x3 = capteur droite
    """
    return np.concatenate((np.array([1.0], dtype=float), capteurs_norm))


def reseau_braitenberg(x: np.ndarray, W: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Calcule :
    u = W @ x
    y = tanh(u)
    """
    u = W @ x
    y = activation(u)
    return u, y


def sorties_vers_moteurs(y: np.ndarray, max_speed: int = MAX_SPEED) -> np.ndarray:
    """
    Convertit les sorties du réseau (dans [-1,1]) en vitesses moteurs.
    y[0] -> roue gauche
    y[1] -> roue droite
    """
    vitesses = np.rint(y * max_speed).astype(int)
    vitesses = np.clip(vitesses, -max_speed, max_speed)
    return vitesses


def arreter_robot(node_id: int) -> None:
    th[node_id]["motor.left.target"] = 0
    th[node_id]["motor.right.target"] = 0


# ============================================================
# CALLBACK
# ============================================================

def callback_observer(node_id: int) -> None:
    global done

    if done:
        return

    try:
        # Arrêt avec le bouton central
        if th[node_id]["button.center"]:
            print("\nArrêt demandé par le bouton central.")
            arreter_robot(node_id)
            done = True
            return

        # 1. Lecture capteurs bruts
        capteurs_bruts = lire_capteurs_avant(node_id)

        # 2. Normalisation
        capteurs_norm = normaliser_capteurs(capteurs_bruts)

        # 3. Vecteur d'entrée
        x = construire_entree(capteurs_norm)

        # 4. Réseau vectoriel
        u, y = reseau_braitenberg(x, W)

        # 5. Conversion en vitesses roues
        vitesses = sorties_vers_moteurs(y)

        # 6. Commande moteurs
        th[node_id]["motor.left.target"] = int(vitesses[0])
        th[node_id]["motor.right.target"] = int(vitesses[1])

        # Affichage détaillé
        print(
            f"G={int(capteurs_bruts[0]):4d} "
            f"C={int(capteurs_bruts[1]):4d} "
            f"D={int(capteurs_bruts[2]):4d} | "
            f"x=[{x[0]:.1f}, {x[1]:.2f}, {x[2]:.2f}, {x[3]:.2f}] | "
            f"u=[{u[0]:.2f}, {u[1]:.2f}] | "
            f"y=[{y[0]:.2f}, {y[1]:.2f}] | "
            f"vL={vitesses[0]:4d} vR={vitesses[1]:4d}",
            end="\r"
        )

    except Exception as e:
        print(f"\nErreur dans le callback : {e}")
        arreter_robot(node_id)
        done = True


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main() -> None:
    global th, done

    print("=" * 70)
    print("TP - Véhicule de Braitenberg avec réseau de neurones vectoriel")
    print("=" * 70)
    print("Matrice des poids W :")
    print(W)
    print("\nRappel :")
    print("- Pas d'obstacle   -> avance")
    print("- Obstacle centre  -> recule")
    print("- Obstacle gauche  -> tourne à droite")
    print("- Obstacle droite  -> tourne à gauche")
    print("\nArrêt : bouton central du Thymio ou Ctrl+C")
    print("=" * 70)

    try:
        coverage = {"prox.horizontal", "button.center"}

        th = Thymio(
            use_tcp=False,
            serial_port=SERIAL_PORT,
            refreshing_coverage=coverage,
        )

        print(f"\nConnexion au Thymio sur {SERIAL_PORT}...")
        th.connect()

        node_id = th.first_node()
        if node_id is None:
            print("Aucun robot Thymio détecté.")
            return

        print(f"Connexion réussie au node {node_id}.")
        print("Démarrage du contrôle...\n")

        th.set_variable_observer(node_id, callback_observer)

        while not done:
            time.sleep(0.1)

        print("\n")
        arreter_robot(node_id)
        print("Robot arrêté proprement.")

    except KeyboardInterrupt:
        print("\nInterruption clavier détectée.")
        try:
            if 'node_id' in locals():
                arreter_robot(node_id)
        except Exception:
            pass

    except Exception as e:
        print(f"\nErreur : {e}")
        try:
            if 'node_id' in locals():
                arreter_robot(node_id)
        except Exception:
            pass

    finally:
        print("Programme terminé.")


if __name__ == "__main__":
    main()