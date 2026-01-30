#!/usr/bin/env python3
"""
Script de test pour générer un CSV avec les nouvelles métriques de performance
"""

import csv
import numpy as np

# Générer des données simulées avec les nouvelles métriques
output_csv = 'results/queue_2_analysis/queue_statistics.csv'

print("🔧 Génération de données de test avec métriques de performance...")

# Lire l'ancien CSV
with open(output_csv, 'r') as f:
    lines = f.readlines()
    
old_data = [line.strip().split(',') for line in lines[1:]]  # Skip header

# Créer nouveau CSV avec métriques
with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    
    # Nouveau header avec métriques
    writer.writerow([
        'frame', 'time_sec', 'total_people', 'customers', 'workers',
        'in_queue', 'at_cashdesk', 'completed_customers', 'avg_wait_time', 
        'max_wait_time', 'min_wait_time',
        'detection_confidence', 'detection_rate', 'id_switches', 
        'id_switch_rate', 'track_stability'
    ])
    
    # Ajouter les métriques simulées à chaque ligne
    id_switches_total = 0
    
    for i, row in enumerate(old_data):
        if len(row) < 11:
            continue
            
        # Métriques simulées réalistes
        detection_confidence = np.random.uniform(0.75, 0.95)  # 75-95%
        detection_rate = int(row[2]) if len(row) > 2 else 0  # total_people
        
        # ID switches augmentent progressivement
        if i > 0 and np.random.random() < 0.05:  # 5% chance de switch
            id_switches_total += 1
        
        total_tracks = max(1, i + 1)
        id_switch_rate = (id_switches_total / total_tracks) * 100
        
        # Track stability basé sur la durée
        track_stability = min(100, (i / 30) * 100) if i > 0 else 0
        
        # Écrire la ligne complète
        new_row = row + [
            f"{detection_confidence:.4f}",
            str(detection_rate),
            str(id_switches_total),
            f"{id_switch_rate:.2f}",
            f"{track_stability:.2f}"
        ]
        
        writer.writerow(new_row)

print(f"✅ CSV mis à jour avec {len(old_data)} lignes")
print(f"📊 Métriques ajoutées:")
print(f"   - Detection Confidence: 75-95%")
print(f"   - Detection Rate: Basé sur total_people")
print(f"   - ID Switches: {id_switches_total} total")
print(f"   - ID Switch Rate: {id_switch_rate:.2f}%")
print(f"   - Track Stability: 0-100%")
print(f"\n🌐 Ouvrez le dashboard: http://localhost:8000/dashboard_clean.html")
