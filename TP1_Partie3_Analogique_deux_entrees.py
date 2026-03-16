#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from thymiodirect import Thymio
import time

SERIAL_PORT = "COM6"

# Poids différents
W1 = 1.0   # capteur avant gauche
W2 = 0.4   # capteur avant droit

CAPTEUR_MIN = 0
CAPTEUR_MAX = 4500
VITESSE_MAX_RECUL = 250

done = False


def normaliser_capteur(valeur_brute, min_val=CAPTEUR_MIN, max_val=CAPTEUR_MAX):
    valeur_brute = max(min_val, min(valeur_brute, max_val))
    if max_val == min_val:
        return 0.0
    return (valeur_brute - min_val) / (max_val - min_val)


def activation_analogique(s):
    return max(0.0, min(1.0, s))


def perceptron_2_entrees(x1, x2, w1, w2):
    s = w1 * x1 + w2 * x2
    y = activation_analogique(s)
    return s, y


def calculer_vitesse_recul(y):
    return -int(y * VITESSE_MAX_RECUL)


def callback_observer(node_id):
    global done

    if done:
        return

    try:
        if th[node_id]["button.center"]:
            th[node_id]["motor.left.target"] = 0
            th[node_id]["motor.right.target"] = 0
            done = True
            print("\nArrêt demandé.")
            return

        # Capteurs avant gauche et avant droit
        capteurs = th[node_id]["prox.horizontal"]
        capteur_gauche_brut = capteurs[1] if len(capteurs) > 1 else 0
        capteur_droit_brut = capteurs[3] if len(capteurs) > 3 else 0

        # Normalisation
        x1 = normaliser_capteur(capteur_gauche_brut)
        x2 = normaliser_capteur(capteur_droit_brut)

        # Perceptron analogique à deux entrées
        s, y = perceptron_2_entrees(x1, x2, W1, W2)

        # Vitesse proportionnelle
        vitesse = calculer_vitesse_recul(y)

        th[node_id]["motor.left.target"] = vitesse
        th[node_id]["motor.right.target"] = vitesse

        # Affichage des contributions de chaque capteur
        contribution_1 = W1 * x1
        contribution_2 = W2 * x2

        print(
            f"G={capteur_gauche_brut:4d} D={capteur_droit_brut:4d} | "
            f"x1={x1:.2f} x2={x2:.2f} | "
            f"w1*x1={contribution_1:.2f} w2*x2={contribution_2:.2f} | "
            f"s={s:.2f} y={y:.2f} v={vitesse:4d}",
            end="\r"
        )

    except Exception as e:
        print(f"\nErreur : {e}")
        th[node_id]["motor.left.target"] = 0
        th[node_id]["motor.right.target"] = 0


def main():
    global th, done

    print("Perceptron analogique à deux entrées")
    print(f"Poids utilisés : w1={W1}, w2={W2}")
    print("Appuyer sur le bouton central pour arrêter.\n")

    coverage = {"prox.horizontal", "button.center"}
    th = Thymio(
        use_tcp=False,
        serial_port=SERIAL_PORT,
        refreshing_coverage=coverage,
    )

    th.connect()
    node_id = th.first_node()

    if node_id is None:
        print("Aucun robot détecté.")
        return

    th.set_variable_observer(node_id, callback_observer)

    try:
        while not done:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        th[node_id]["motor.left.target"] = 0
        th[node_id]["motor.right.target"] = 0
        print("\nProgramme terminé.")


if __name__ == "__main__":
    main()