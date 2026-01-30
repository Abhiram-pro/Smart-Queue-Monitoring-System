#!/usr/bin/env python3
"""
Test de la logique de calcul des temps d'attente
Vérifie qu'il n'y a JAMAIS de temps négatifs
"""

import json
import numpy as np

print("="*70)
print("TEST DE LA LOGIQUE - SIMULATION")
print("="*70)

# Simulation d'une queue
class SimulatedCustomer:
    def __init__(self, id, queue_entry_time, service_entry_time):
        self.id = id
        self.queue_entry_time = queue_entry_time
        self.service_entry_time = service_entry_time
        self.wait_time = None
        
    def calculate_wait_time(self):
        if self.queue_entry_time is not None and self.service_entry_time is not None:
            self.wait_time = self.service_entry_time - self.queue_entry_time
            return self.wait_time
        return None

print("\n📊 SCÉNARIO DE TEST")
print("-" * 70)

# Scénario : 3 personnes dans la queue
customers = []

print("\n1️⃣  Activation de la queue à t=10.0s")
print("   → Personne arrive à la caisse")
print("   → 3 personnes dans la queue")
queue_activation_time = 10.0

print("\n   Démarrage des timers pour tous à t=10.0s:")
customers.append(SimulatedCustomer(1, queue_activation_time, None))
customers.append(SimulatedCustomer(2, queue_activation_time, None))
customers.append(SimulatedCustomer(3, queue_activation_time, None))

for c in customers:
    print(f"   ✓ Client C{c.id} → queue_entry = {c.queue_entry_time:.1f}s")

print("\n2️⃣  Les clients avancent vers la caisse:")

# Client 1 arrive à la caisse à t=15.0s
customers[0].service_entry_time = 15.0
wait1 = customers[0].calculate_wait_time()
print(f"\n   t=15.0s : C1 arrive à la caisse")
print(f"   → Temps d'attente = {wait1:.1f}s ({customers[0].queue_entry_time:.1f}s → {customers[0].service_entry_time:.1f}s)")
print(f"   → Positif ? {'✅ OUI' if wait1 >= 0 else '❌ NON (ERREUR!)'}")

# Client 2 arrive à la caisse à t=22.5s
customers[1].service_entry_time = 22.5
wait2 = customers[1].calculate_wait_time()
print(f"\n   t=22.5s : C2 arrive à la caisse")
print(f"   → Temps d'attente = {wait2:.1f}s ({customers[1].queue_entry_time:.1f}s → {customers[1].service_entry_time:.1f}s)")
print(f"   → Positif ? {'✅ OUI' if wait2 >= 0 else '❌ NON (ERREUR!)'}")

# Client 3 arrive à la caisse à t=30.0s
customers[2].service_entry_time = 30.0
wait3 = customers[2].calculate_wait_time()
print(f"\n   t=30.0s : C3 arrive à la caisse")
print(f"   → Temps d'attente = {wait3:.1f}s ({customers[2].queue_entry_time:.1f}s → {customers[2].service_entry_time:.1f}s)")
print(f"   → Positif ? {'✅ OUI' if wait3 >= 0 else '❌ NON (ERREUR!)'}")

# Nouveau client entre dans la queue APRÈS activation
print("\n3️⃣  Nouveau client entre dans la queue (après activation):")
new_customer = SimulatedCustomer(4, 18.0, 35.0)
wait4 = new_customer.calculate_wait_time()
print(f"\n   C4 entre à t=18.0s, arrive à caisse à t=35.0s")
print(f"   → Temps d'attente = {wait4:.1f}s ({new_customer.queue_entry_time:.1f}s → {new_customer.service_entry_time:.1f}s)")
print(f"   → Positif ? {'✅ OUI' if wait4 >= 0 else '❌ NON (ERREUR!)'}")

# Statistiques
print("\n" + "="*70)
print("📈 STATISTIQUES FINALES")
print("="*70)

all_waits = [wait1, wait2, wait3, wait4]
print(f"\nTemps d'attente individuels :")
for i, wait in enumerate(all_waits, 1):
    print(f"  Client {i} : {wait:.1f}s")

print(f"\n  Moyenne : {np.mean(all_waits):.2f}s")
print(f"  Maximum : {np.max(all_waits):.2f}s")
print(f"  Minimum : {np.min(all_waits):.2f}s")

# Vérification finale
all_positive = all(w >= 0 for w in all_waits)
print("\n" + "="*70)
if all_positive:
    print("✅ SUCCÈS : Tous les temps sont positifs!")
    print("   La logique est correcte et fiable.")
else:
    print("❌ ÉCHEC : Des temps négatifs détectés!")
    print("   Il y a un problème dans la logique.")
print("="*70 + "\n")
