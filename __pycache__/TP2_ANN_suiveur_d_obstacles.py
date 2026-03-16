import time
import numpy as np
from thymiodirect import Thymio

# ============================================================
# CONFIGURATION
# ============================================================

SERIAL_PORT = "COM6"      # À adapter si besoin
MAX_SPEED = 250           # Vitesse max des roues
CAPTEUR_MIN = 0.0
CAPTEUR_MAX = 4500.0

# Capteurs avant du Thymio
IDX_GAUCHE = 0
IDX_CENTRE = 2
IDX_DROITE = 4

# Poids pour le suivi d'objet
w_fwd = 0.8
w_back = 0.8
w_pos = 0.4
w_neg = 0.4

# Matrice des poids :
# x = [1, x1, x2, x3]^T
# x1 = capteur gauche
# x2 = capteur centre
# x3 = capteur droit
W = np.array(
    (
        (w_fwd, -w_neg, -w_back,  w_pos),
        (w_fwd,  w_pos, -w_back, -w_neg),
    ),
    dtype=float
)

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
    valeurs = np.clip(valeurs_brutes.astype(float), min_val, max_val)
    if max_val <= min_val:
        return np.zeros(valeurs.shape, dtype=float)
    return (valeurs - min_val) / (max_val - min_val)


def activation(u: np.ndarray) -> np.ndarray:
    """
    Fonction d'activation non linéaire bornée.
    tanh borne naturellement les sorties entre -1 et 1.
    """
    return np.tanh(u)


def lire_capteurs_avant(node_id: int) -> np.ndarray:
    """
    Lit les trois capteurs avant utiles :
    gauche, centre, droite.
    Retourne un ndarray numpy de taille 3.
    """
    prox = np.asarray(th[node_id]["prox.horizontal"], dtype=float)

    capteurs = np.zeros(3, dtype=float)

    if prox.size > IDX_GAUCHE:
        capteurs[0] = prox[IDX_GAUCHE]
    if prox.size > IDX_CENTRE:
        capteurs[1] = prox[IDX_CENTRE]
    if prox.size > IDX_DROITE:
        capteurs[2] = prox[IDX_DROITE]

    return capteurs


def construire_entree(capteurs_norm: np.ndarray) -> np.ndarray:
    """
    Construit x = [1, x1, x2, x3]^T
    """
    x = np.empty(4, dtype=float)
    x[0] = 1.0
    x[1:] = capteurs_norm
    return x


def reseau_suivi_objet(x: np.ndarray, W: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
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
    Convertit les sorties normalisées en vitesses moteurs.
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

        # 1. Lire les capteurs
        capteurs_bruts = lire_capteurs_avant(node_id)

        # 2. Normaliser
        capteurs_norm = normaliser_capteurs(capteurs_bruts)

        # 3. Construire le vecteur d'entrée
        x = construire_entree(capteurs_norm)

        # 4. Calcul vectoriel du réseau
        u, y = reseau_suivi_objet(x, W)

        # 5. Convertir vers les vitesses des roues
        vitesses = sorties_vers_moteurs(y)

        # 6. Appliquer aux moteurs
        th[node_id]["motor.left.target"] = int(vitesses[0])
        th[node_id]["motor.right.target"] = int(vitesses[1])

        # Affichage
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

    print("=" * 72)
    print("TP - Réseau de neurones vectoriel : stratégie de suivi d'objet")
    print("=" * 72)
    print("Matrice des poids W :")
    print(W)
    print("\nComportement visé :")
    print("- Pas d'objet          -> avance")
    print("- Objet à gauche       -> tourne à gauche")
    print("- Objet à droite       -> tourne à droite")
    print("- Objet très proche au centre -> arrêt")
    print("\nArrêt : bouton central du Thymio ou Ctrl+C")
    print("=" * 72)

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
            if "node_id" in locals():
                arreter_robot(node_id)
        except Exception:
            pass

    except Exception as e:
        print(f"\nErreur : {e}")
        try:
            if "node_id" in locals():
                arreter_robot(node_id)
        except Exception:
            pass

    finally:
        print("Programme terminé.")


if __name__ == "__main__":
    main()