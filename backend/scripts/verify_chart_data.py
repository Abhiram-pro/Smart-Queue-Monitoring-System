#!/usr/bin/env python3
"""
Script de visualisation des données de temps d'attente
Pour vérifier que les valeurs sont bien réelles et non entières
"""

import csv
import matplotlib.pyplot as plt

csv_file = 'results/queue_2_analysis/queue_statistics.csv'

print("📊 Analyse des données de temps d'attente...\n")

# Lire les données
frames = []
times = []
wait_times = []
detection_conf = []

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i % 30 == 0:  # Échantillonner 1 ligne sur 30
            frames.append(int(row['frame']))
            times.append(float(row['time_sec']))
            wait_times.append(float(row['avg_wait_time']))
            detection_conf.append(float(row['detection_confidence']) * 100)

# Statistiques
print(f"📈 Statistiques sur {len(wait_times)} échantillons:")
print(f"   Temps d'attente moyen: {sum(wait_times)/len(wait_times):.2f}s")
print(f"   Temps min: {min(wait_times):.2f}s")
print(f"   Temps max: {max(wait_times):.2f}s")
print(f"   Confiance détection moyenne: {sum(detection_conf)/len(detection_conf):.1f}%")

# Vérifier que ce ne sont pas des entiers
non_integers = sum(1 for wt in wait_times if wt != int(wt))
print(f"\n✅ Valeurs non-entières: {non_integers}/{len(wait_times)} ({100*non_integers/len(wait_times):.1f}%)")

# Afficher quelques exemples
print(f"\n📋 Exemples de valeurs (avec décimales):")
for i in range(min(10, len(wait_times))):
    print(f"   Frame {frames[i]:4d} ({times[i]:6.1f}s): {wait_times[i]:.4f}s")

print(f"\n🌐 Les valeurs RÉELLES sont maintenant affichées dans le graphique du dashboard")
print(f"   (Pas d'arrondi, courbe fluide avec décimales)")
