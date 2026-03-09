# Comportement A - Réglage du seuil pour faire fonctionner l'opérateur ET
# Le robot avance si LES DEUX capteurs arrière détectent un obstacle

from thymiodirect import Thymio
import time
import os

print("="*60)
print("COMPORTEMENT A - OPÉRATEUR ET (Ajustable)")
print("="*60)

done = False
th = None
id = None

# SEUIL AJUSTABLE - Essayez de baisser si ça ne marche pas
SEUIL_OBSTACLE = 500  # Baissé de 1000 à 500 pour plus de sensibilité

def calculer_s(x1, x2, w0, w1, w2):
    return w0 + x1 * w1 + x2 * w2

def activation(s):
    return 1 if s >= 0 else 0

def perceptron_ET(x1, x2):
    """Opérateur ET : avance si x1=1 ET x2=1"""
    w0 = -1.5
    w1 = 1
    w2 = 1
    s = calculer_s(x1, x2, w0, w1, w2)
    return activation(s)

def on_comm_error(error):
    print(f"\n❌ Erreur: {error}")
    os._exit(1)

def obs(node_id):
    global done, th, id
    
    if not done:
        try:
            # Lire capteurs arrière
            capteurs = th[node_id]["prox.horizontal"]
            capteur_gauche = capteurs[5] if len(capteurs) > 5 else 0
            capteur_droit = capteurs[6] if len(capteurs) > 6 else 0
            
            # Normaliser avec le seuil
            x1 = 1 if capteur_gauche > SEUIL_OBSTACLE else 0
            x2 = 1 if capteur_droit > SEUIL_OBSTACLE else 0
            
            # Décision avec perceptron ET
            decision = perceptron_ET(x1, x2)
            
            # Affichage détaillé
            print(f"Capteurs: G={capteur_gauche:4d} D={capteur_droit:4d} | Normalisé: ({x1},{x2}) → Décision: {decision}", end="")
            
            # Appliquer
            if decision == 1:
                th[node_id]["motor.left.target"] = 150
                th[node_id]["motor.right.target"] = 150
                print(" | 🟢 AVANCE ✓")
            else:
                th[node_id]["motor.left.target"] = 0
                th[node_id]["motor.right.target"] = 0
                print(" | 🔴 ARRÊTÉ")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        # Bouton central
        if th[node_id]["button.center"]:
            print("\n⏹️  Arrêt")
            th[node_id]["motor.left.target"] = 0
            th[node_id]["motor.right.target"] = 0
            done = True

# Connexion
print(f"\n⚙️  Seuil de détection configuré à: {SEUIL_OBSTACLE}")
print("💡 Si ça ne marche pas, modifiez SEUIL_OBSTACLE dans le code\n")
print("🔌 Connexion sur COM3...")

try:
    th = Thymio(
        use_tcp=False,
        serial_port="COM3",
        refreshing_coverage={"prox.horizontal", "button.center"},
    )
    
    th.on_comm_error = on_comm_error
    th.connect()
    
    id = th.first_node()
    if id is None:
        print("❌ Thymio non trouvé")
        exit(1)
    
    print("✅ Thymio connecté!")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    exit(1)

print("\n" + "="*60)
print("🚀 COMPORTEMENT A - Opérateur ET")
print("📌 Placez vos DEUX MAINS derrière le robot (de chaque côté)")
print("📌 Ou utilisez un OBJET LARGE qui couvre les deux capteurs")
print("📌 Les valeurs s'affichent en temps réel")
print("📌 Bouton central pour arrêter")
print("="*60 + "\n")

th.set_variable_observer(id, obs)

try:
    while not done:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n⚠️  Arrêt")

print("\n✅ Test terminé")
print("\n💡 CONSEILS si ça ne marche pas:")
print("   1. Rapprochez vos mains du robot (< 5cm)")
print("   2. Utilisez un objet blanc/clair (meilleure détection)")
print("   3. Couvrez bien LES DEUX capteurs en même temps")
print("   4. Baissez le seuil à 300 ou 200 dans le code si nécessaire")
