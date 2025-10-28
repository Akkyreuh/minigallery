import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
import os
from datetime import datetime

# Charger les données
print("Chargement des donnees...")
df = pd.read_csv('data.csv')

# Préparation des données
print("Preparation des donnees...")

# Encoder la variable catégorielle Gender
le = LabelEncoder()
df['Gender_encoded'] = le.fit_transform(df['Gender'])

# Sélectionner les features (sans User ID)
X = df[['Gender_encoded', 'Age', 'EstimatedSalary']].values
y = df['Purchased'].values

# Division train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Normalisation des features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Donnees d'entrainement: {X_train.shape[0]} echantillons")
print(f"Donnees de test: {X_test.shape[0]} echantillons")

# Entraînement du modèle SVM
print("Entrainement du modele SVM...")
model = SVC(random_state=42, probability=True)
model.fit(X_train_scaled, y_train)

# Prédictions
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)

# Évaluation
accuracy = accuracy_score(y_test, y_pred)
cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')

print(f"Accuracy: {accuracy:.3f}")
print(f"CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})")

# Rapport détaillé
print("\nRapport detaille:")
print(classification_report(y_test, y_pred))

# Matrice de confusion
cm = confusion_matrix(y_test, y_pred)
print(f"\nMatrice de confusion:")
print(cm)

# Sauvegarde du modèle
print("\nSauvegarde du modele...")

# Créer le dossier ml_models s'il n'existe pas
os.makedirs('ml_models', exist_ok=True)

# Sauvegarder le modèle
with open('ml_models/best_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('ml_models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
with open('ml_models/label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)

# Sauvegarder les métadonnées
metadata = {
    'model_name': 'SVM',
    'accuracy': accuracy,
    'training_date': datetime.now().isoformat(),
    'features': ['Gender_encoded', 'Age', 'EstimatedSalary'],
    'target': 'Purchased',
    'test_samples': len(X_test)
}

with open('ml_models/metadata.pkl', 'wb') as f:
    pickle.dump(metadata, f)

print("Modele sauvegarde avec succes!")
print(f"Fichiers crees:")
print(f"   - ml_models/best_model.pkl")
print(f"   - ml_models/scaler.pkl")
print(f"   - ml_models/label_encoder.pkl")
print(f"   - ml_models/metadata.pkl")