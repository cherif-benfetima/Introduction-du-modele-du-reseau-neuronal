# TP1 : Implémentation d'une porte logique avec un Perceptron

# Fonction calculant la somme pondérée s
def calculer_s(x1, x2, w0, w1, w2):
    s = w0 + x1 * w1 + x2 * w2
    return s

# Fonction d'activation retournant y

def activation(s):
    if s >= 0:
        y = 1
    else:
        y = 0
    return y

# Fonction pour tester un perceptron avec des poids donnés
def tester_perceptron(w0, w1, w2, nom_operateur):
    """
    Teste toutes les combinaisons d'entrées pour un perceptron
    """
    print(f"\n{'='*50}")
    print(f"Opérateur Logique {nom_operateur}")
    print(f"Poids: w0 = {w0}, w1 = {w1}, w2 = {w2}")
    print(f"{'='*50}")
    print(f"{'x1':<5} {'x2':<5} {'s':<10} {'y':<5}")
    print(f"{'-'*30}")
    
    # Tester toutes les combinaisons possibles
    for x1 in [0, 1]:
        for x2 in [0, 1]:
            s = calculer_s(x1, x2, w0, w1, w2)
            y = activation(s)
            print(f"{x1:<5} {x2:<5} {s:<10.2f} {y:<5}")


# Opérateur OU (OR)
# Pour OR: (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→1
# Poids possibles: w0 = -0.5, w1 = 1, w2 = 1
w0_or = -0.5
w1_or = 1
w2_or = 1
tester_perceptron(w0_or, w1_or, w2_or, "OU (OR)")

# Opérateur ET (AND)
# Pour AND: (0,0)→0, (0,1)→0, (1,0)→0, (1,1)→1
# Poids possibles: w0 = -1.5, w1 = 1, w2 = 1
w0_and = -1.5
w1_and = 1
w2_and = 1
tester_perceptron(w0_and, w1_and, w2_and, "ET (AND)")
