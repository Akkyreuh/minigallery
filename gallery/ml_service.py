import pickle
import numpy as np
import os
import pandas as pd

class MLService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.metadata = None
        self._load_models()

    def _load_models(self):
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'ml_models')
        
        try:
            with open(os.path.join(model_dir, 'best_model.pkl'), 'rb') as f:
                self.model = pickle.load(f)
            with open(os.path.join(model_dir, 'scaler.pkl'), 'rb') as f:
                self.scaler = pickle.load(f)
            with open(os.path.join(model_dir, 'label_encoder.pkl'), 'rb') as f:
                self.label_encoder = pickle.load(f)
            with open(os.path.join(model_dir, 'metadata.pkl'), 'rb') as f:
                self.metadata = pickle.load(f)
            print("Modeles charges avec succes: SVM")
        except FileNotFoundError as e:
            print(f"Error loading ML models: {e}. Ensure 'ml_models' directory and files exist.")
            self.model = None
            self.scaler = None
            self.label_encoder = None
            self.metadata = None
        except Exception as e:
            print(f"An unexpected error occurred while loading ML models: {e}")
            self.model = None
            self.scaler = None
            self.label_encoder = None
            self.metadata = None

    def predict_purchase(self, age, gender, estimated_salary):
        if not all([self.model, self.scaler, self.label_encoder, self.metadata]):
            return {'success': False, 'error': 'ML models not loaded.'}

        try:
            gender_encoded = self.label_encoder.transform([gender])[0]
            input_data = pd.DataFrame([[age, estimated_salary, gender_encoded]], 
                                    columns=['Age', 'EstimatedSalary', 'Gender_encoded'])
            input_scaled = self.scaler.transform(input_data)

            prediction = self.model.predict(input_scaled)[0]
            probabilities = self.model.predict_proba(input_scaled)[0]

            will_purchase = bool(prediction)
            confidence = max(probabilities)
            probability_purchase = probabilities[1] if len(probabilities) > 1 else 0.0
            probability_no_purchase = probabilities[0] if len(probabilities) > 1 else 0.0

            return {
                'success': True,
                'will_purchase': will_purchase,
                'confidence': confidence,
                'probability_purchase': probability_purchase,
                'probability_no_purchase': probability_no_purchase,
                'model_name': self.metadata.get('model_name', 'Unknown'),
                'accuracy': self.metadata.get('accuracy', 0.0) * 100
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_model_info(self):
        if self.metadata:
            return {
                'model_name': self.metadata.get('model_name', 'N/A'),
                'accuracy': self.metadata.get('accuracy', 0.0) * 100,
                'training_date': self.metadata.get('training_date', 'N/A'),
                'features': self.metadata.get('features', [])
            }
        return None

ml_service = MLService()
