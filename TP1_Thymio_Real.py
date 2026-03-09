# TP1 : Application des Perceptrons au Robot Thymio II - Implémentation Réelle

from thymiodirect import Thymio, Connection
import sys
import os
import time

# ============================================================
# FONCTIONS DU PERCEPTRON
# ============================================================

def calculer_s(x1, x2, w0, w1, w2):
    """
    Calcule la somme pondérée s = w0 + x1*w1 + x2*w2
    """
    s = w0 + x1 * w1 + x2 * w2
    return s

def activation(s):
    """
    Fonction d'activation (seuil):
    Si s >= 0, y = 1 (robot avance)
    Si s < 0, y = 0 (robot s'arrête)
    """
    if s >= 0:
        y = 1
    else:
        y = 0
    return y

def perceptron(x1, x2, w0, w1, w2):
    """
    Perceptron complet : calcul de s puis activation
    Retourne y (0 ou 1)
    """
    s = calculer_s(x1, x2, w0, w1, w2)
    y = activation(s)
    return y

# ============================================================
# FONCTIONS DE CONTRÔLE DES LEDs
# ============================================================

def set_leds(th, id, R, G, B):
    """
    Configure la couleur des LEDs du haut du Thymio
    """
    src = """
        dc end_toc                  ; total size of event handler table
        dc _ev.init, init           ; id and address of init event
    end_toc:

    init:                           ; code executed on init event
        push.s 0                    ; initialize counter
        store counter
        push.s """
    src2 = """
        store _userdata
        push.s _userdata
        push.s """
    src3 = """
        store _userdata+1
        push.s _userdata+1
        push.s """
    src4 = """
        store _userdata+2
        push.s _userdata+2
        callnat _nf."""
    src5 = """
        stop                        ; stop program

    counter:
        equ _userdata+3
    """
    th.run_asm(id, src + str(B) + src2 + str(G) + src3 + str(R) + src4 + 'leds.top' + src5)

# ============================================================
# FONCTIONS DE LECTURE DES CAPTEURS
# ============================================================

def lire_capteurs_arriere(th, node_id):
    """
    Lit les capteurs de proximité arrière
    Retourne (x1, x2) normalisés en 0 ou 1
    
    capteur_gauche = prox.horizontal[5]
    capteur_droit = prox.horizontal[6]
    """
    # Seuil de détection d'obstacle (à ajuster selon le robot)
    SEUIL_OBSTACLE = 500  # Baissé pour meilleure détection
    
    try:
        capteurs = th[node_id]["prox.horizontal"]
        capteur_gauche = capteurs[5] if len(capteurs) > 5 else 0
        capteur_droit = capteurs[6] if len(capteurs) > 6 else 0
    except:
        capteur_gauche = 0
        capteur_droit = 0
    
    # Normalisation : 1 si obstacle détecté, 0 sinon
    x1 = 1 if capteur_gauche > SEUIL_OBSTACLE else 0
    x2 = 1 if capteur_droit > SEUIL_OBSTACLE else 0
    
    return x1, x2

def lire_capteurs_sol(th, node_id):
    """
    Lit les capteurs au sol
    Retourne (x1, x2) normalisés en 0 ou 1
    
    capteur_gauche = prox.ground.delta[0]
    capteur_droit = prox.ground.delta[1]
    """
    # Seuil de détection de surface (à ajuster selon le robot)
    SEUIL_SURFACE = 400
    
    try:
        capteurs_sol = th[node_id]["prox.ground.delta"]
        capteur_gauche = capteurs_sol[0] if len(capteurs_sol) > 0 else 0
        capteur_droit = capteurs_sol[1] if len(capteurs_sol) > 1 else 0
    except:
        capteur_gauche = 0
        capteur_droit = 0
    
    # Normalisation : 1 si surface détectée, 0 sinon (sol noir)
    x1 = 1 if capteur_gauche > SEUIL_SURFACE else 0
    x2 = 1 if capteur_droit > SEUIL_SURFACE else 0
    
    return x1, x2

# ============================================================
# COMPORTEMENTS DU ROBOT
# ============================================================

def comportement_A(th, node_id):
    """
    Comportement A : Détection d'obstacles à l'arrière
    Le robot avance SI ET SEULEMENT SI les DEUX capteurs arrière
    détectent un obstacle (Opérateur ET/AND)
    """
    # Poids pour l'opérateur ET (AND)
    w0 = -1.5
    w1 = 1
    w2 = 1
    
    # Lire les capteurs arrière
    x1, x2 = lire_capteurs_arriere(th, node_id)
    
    # Calculer la décision avec le perceptron
    decision = perceptron(x1, x2, w0, w1, w2)
    
    # Debug - Afficher aussi les valeurs brutes
    try:
        capteurs = th[node_id]["prox.horizontal"]
        valeur_gauche = capteurs[5] if len(capteurs) > 5 else 0
        valeur_droite = capteurs[6] if len(capteurs) > 6 else 0
        print(f"Comportement A - Valeurs brutes: G={valeur_gauche:4d} D={valeur_droite:4d} | Normalisé: ({x1},{x2}) → Décision: {decision}")
    except:
        print(f"Comportement A - Capteurs: ({x1}, {x2}) -> Décision: {decision}")
    
    return decision

def comportement_B(th, node_id):
    """
    Comportement B : Détection de surface au sol
    Le robot avance SI ET SEULEMENT SI les DEUX capteurs au sol
    détectent une surface (Opérateur ET/AND)
    """
    # Poids pour l'opérateur ET (AND)
    w0 = -1.5
    w1 = 1
    w2 = 1
    
    # Lire les capteurs au sol
    x1, x2 = lire_capteurs_sol(th, node_id)
    
    # Calculer la décision avec le perceptron
    decision = perceptron(x1, x2, w0, w1, w2)
    
    # Debug
    print(f"Comportement B - Capteurs: ({x1}, {x2}) -> Décision: {decision}")
    
    return decision

# ============================================================
# CONTRÔLE DU ROBOT
# ============================================================

def appliquer_decision(th, node_id, decision):
    """
    Applique la décision du perceptron au robot
    decision = 1 : avancer
    decision = 0 : s'arrêter
    """
    VITESSE = 150  # Vitesse du robot (ajustable)
    
    if decision == 1:
        # Avancer
        th[node_id]["motor.left.target"] = VITESSE
        th[node_id]["motor.right.target"] = VITESSE
        set_leds(th, node_id, 0, 255, 0)  # LED verte
        print("🤖 Robot AVANCE")
    else:
        # Arrêter
        th[node_id]["motor.left.target"] = 0
        th[node_id]["motor.right.target"] = 0
        set_leds(th, node_id, 255, 0, 0)  # LED rouge
        print("🛑 Robot ARRÊTÉ")

# ============================================================
# CALLBACK PRINCIPAL
# ============================================================

def on_comm_error(error):
    """Gestion des erreurs de communication"""
    print(f"Erreur de communication: {error}")
    os._exit(1)

def callback_observer(node_id, mode='A'):
    """
    Callback appelé régulièrement pour contrôler le robot
    mode: 'A' pour comportement A, 'B' pour comportement B
    """
    global done, th
    
    if not done:
        # Vérifier si le bouton central est pressé pour arrêter
        if th[node_id]["button.center"]:
            print("⏹️  Bouton central pressé - Arrêt du programme")
            th[node_id]["motor.left.target"] = 0
            th[node_id]["motor.right.target"] = 0
            done = True
            return
        
        # Appliquer le comportement sélectionné
        try:
            if mode == 'A':
                # Lire capteurs arrière
                capteurs = th[node_id]["prox.horizontal"]
                capteur_gauche = capteurs[5] if len(capteurs) > 5 else 0
                capteur_droit = capteurs[6] if len(capteurs) > 6 else 0
                
                # Normaliser
                x1 = 1 if capteur_gauche > 500 else 0
                x2 = 1 if capteur_droit > 500 else 0
                
                # Perceptron ET
                s = -1.5 + x1 * 1 + x2 * 1
                decision = 1 if s >= 0 else 0
                
                # Affichage
                print(f"Mode A - G={capteur_gauche:4d} D={capteur_droit:4d} | ({x1},{x2}) → Décision: {decision}", end="")
                
            elif mode == 'B':
                # Lire capteurs sol
                capteurs_sol = th[node_id]["prox.ground.delta"]
                capteur_gauche = capteurs_sol[0] if len(capteurs_sol) > 0 else 0
                capteur_droit = capteurs_sol[1] if len(capteurs_sol) > 1 else 0
                
                # Normaliser
                x1 = 1 if capteur_gauche > 400 else 0
                x2 = 1 if capteur_droit > 400 else 0
                
                # Perceptron ET
                s = -1.5 + x1 * 1 + x2 * 1
                decision = 1 if s >= 0 else 0
                
                # Affichage
                print(f"Mode B - G={capteur_gauche:4d} D={capteur_droit:4d} | ({x1},{x2}) → Décision: {decision}", end="")
            else:
                decision = 0
            
            # Appliquer la décision
            if decision == 1:
                th[node_id]["motor.left.target"] = 150
                th[node_id]["motor.right.target"] = 150
                print(" | 🟢 AVANCE")
            else:
                th[node_id]["motor.left.target"] = 0
                th[node_id]["motor.right.target"] = 0
                print(" | 🔴 ARRÊTÉ")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")

# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("TP1 - THYMIO II : PERCEPTRONS EN ACTION")
    print("="*60)
    
    # Choix du mode
    print("\nChoisissez le comportement :")
    print("  A - Détection d'obstacles à l'arrière")
    print("  B - Détection de surface au sol")
    mode = input("Votre choix (A/B) : ").upper()
    
    if mode not in ['A', 'B']:
        print("❌ Mode invalide. Utilisation du mode A par défaut.")
        mode = 'A'
    
    print(f"\n✅ Mode {mode} sélectionné")
    print("📌 Appuyez sur le bouton central du Thymio pour arrêter\n")
    
    # Utiliser COM3 (port détecté sur votre système)
    serial_port = "COM3"
    print(f"🔌 Utilisation du port série: {serial_port}")
    
    # Connexion au Thymio
    try:
        print("\n🔄 Connexion au Thymio en cours...")
        coverage = {"prox.horizontal", "prox.ground.delta", "button.center"}
        
        th = Thymio(
            use_tcp=False,
            serial_port=serial_port,
            refreshing_coverage=coverage,
        )
    except Exception as error:
        print(f"\n❌ Erreur de connexion au Thymio : {error}")
        print("\n💡 Vérifications à faire :")
        print("  1. Le robot Thymio est-il allumé ?")
        print("  2. Le câble USB est-il bien branché ?")
        print("  3. Les drivers Thymio sont-ils installés ?")
        print("  4. Aucun autre programme n'utilise le Thymio ?")
        print("\n📖 Pour tester sans robot, lancez: python TP1_Thymio.py")
        exit(1)
    
    try:
        th.on_comm_error = on_comm_error
        th.connect()
        
        id = th.first_node()
        
        if id is None:
            print("❌ Aucun nœud Thymio trouvé après connexion")
            exit(1)
        
        done = False
        
        print("✅ Thymio connecté avec succès")
        
        # Configuration de l'observer avec le mode choisi
        th.set_variable_observer(id, lambda node_id: callback_observer(node_id, mode))
        
        print(f"\n🚀 Thymio en mode {mode} - Exécution en cours...")
        
        if mode == 'A':
            print("💡 Mode A - Placez vos DEUX MAINS derrière le robot (les deux capteurs)")
            print("   Le robot avance si LES DEUX capteurs arrière détectent")
        else:
            print("💡 Mode B - Mettez le robot sur une table")
            print("   Le robot avance si LES DEUX capteurs sol détectent la surface")
        
        print("="*60 + "\n")
        
        # Boucle principale
        try:
            while not done:
                time.sleep(0.1)  # Échantillonnage à 10 Hz
        except KeyboardInterrupt:
            print("\n⚠️  Interruption clavier détectée")
        
        # Arrêt
        print("\n" + "="*60)
        print("🔌 Arrêt du Thymio...")
        th[id]["motor.left.target"] = 0
        th[id]["motor.right.target"] = 0
        print("✅ Thymio arrêté avec succès")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Erreur pendant l'exécution : {e}")
        print("\nArrêt du programme...")
        exit(1)
