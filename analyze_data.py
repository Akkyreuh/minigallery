import pandas as pd
import numpy as np

# Charger les données
df = pd.read_csv('data.csv')

print("=== ANALYSE DES DONNÉES ===")
print(f"Nombre de lignes: {len(df)}")
print(f"Nombre de colonnes: {len(df.columns)}")
print("\nColonnes:", df.columns.tolist())
print("\nTypes de données:")
print(df.dtypes)
print("\nPremières lignes:")
print(df.head())
print("\nStatistiques descriptives:")
print(df.describe())
print("\nValeurs manquantes:")
print(df.isnull().sum())
print("\nDistribution de la variable cible (Purchased):")
print(df['Purchased'].value_counts())
print(f"Pourcentage d'achat: {df['Purchased'].mean()*100:.1f}%")
