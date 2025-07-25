"""
Pest Risk Prediction Module
===========================

This module provides pest risk prediction functionality for macadamia farming
using trained Random Forest models and expert knowledge.
"""

import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PestRiskPredictor:
    """
    Predicts pest risk levels for macadamia trees based on environmental conditions
    """
    
    def __init__(self, model_path: str = "macadamia_bot/models/saved"):
        """
        Initialize the pest risk predictor
        
        Args:
            model_path: Path to saved models directory
        """
        self.model_path = model_path
        self.model = None
        self.encoders = None
        self.scalers = None
        self.pest_knowledge = None
        self.load_models()
        self.load_pest_knowledge()
    
    def load_models(self):
        """Load trained models and preprocessing objects"""
        try:
            self.model = joblib.load(os.path.join(self.model_path, 'pest_risk_model.pkl'))
            self.encoders = joblib.load(os.path.join(self.model_path, 'encoders.pkl'))
            self.scalers = joblib.load(os.path.join(self.model_path, 'scalers.pkl'))
            logger.info("Pest risk prediction models loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load models: {e}. Using rule-based predictions.")
    
    def load_pest_knowledge(self):
        """Load pest management knowledge base"""
        try:
            with open('macadamia_bot/data/pest_management.json', 'r') as f:
                self.pest_knowledge = json.load(f)
            logger.info("Pest knowledge base loaded successfully")
        except Exception as e:
            logger.error(f"Could not load pest knowledge: {e}")
            self.pest_knowledge = {}
    
    def predict_pest_risk(self, 
                         soil_ph: float,
                         temperature: float,
                         humidity: float,
                         rainfall: float,
                         season: str,
                         tree_age: int) -> Dict[str, Any]:
        """
        Predict pest risk level based on environmental conditions
        
        Args:
            soil_ph: Soil pH level (5.0-7.5)
            temperature: Temperature in Celsius
            humidity: Relative humidity percentage
            rainfall: Rainfall in mm
            season: Season (spring, summer, autumn, winter)
            tree_age: Age of trees in years
            
        Returns:
            Dictionary with pest risk prediction and recommendations
        """
        try:
            # Prepare input data
            input_data = self._prepare_input_data(
                soil_ph, temperature, humidity, rainfall, season, tree_age
            )
            
            # Make prediction using ML model if available
            if self.model is not None:
                ml_prediction = self._ml_prediction(input_data)
            else:
                ml_prediction = None
            
            # Rule-based prediction as backup/supplement
            rule_based_prediction = self._rule_based_prediction(
                soil_ph, temperature, humidity, rainfall, season, tree_age
            )
            
            # Combine predictions
            final_prediction = self._combine_predictions(ml_prediction, rule_based_prediction)
            
            # Get specific pest risks and recommendations
            pest_analysis = self._analyze_specific_pests(
                temperature, humidity, rainfall, season
            )
            
            return {
                'overall_risk_level': final_prediction['risk_level'],
                'risk_score': final_prediction['risk_score'],
                'confidence': final_prediction['confidence'],
                'specific_pests': pest_analysis,
                'recommendations': self._get_recommendations(final_prediction['risk_level'], pest_analysis),
                'monitoring_advice': self._get_monitoring_advice(season, final_prediction['risk_level']),
                'prediction_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in pest risk prediction: {e}")
            return self._fallback_prediction()
    
    def _prepare_input_data(self, soil_ph, temperature, humidity, rainfall, season, tree_age):
        """Prepare input data for ML model"""
        # Encode season
        if self.encoders and 'season' in self.encoders:
            try:
                season_encoded = self.encoders['season'].transform([season])[0]
            except:
                season_encoded = 0  # Default fallback
        else:
            season_map = {'spring': 0, 'summer': 1, 'autumn': 2, 'winter': 3}
            season_encoded = season_map.get(season.lower(), 0)
        
        # Create feature array
        features = np.array([[soil_ph, temperature, humidity, rainfall, season_encoded, tree_age]])
        
        # Scale features if scaler is available
        if self.scalers and 'features' in self.scalers:
            features = self.scalers['features'].transform(features)
        
        return features
    
    def _ml_prediction(self, input_data):
        """Make prediction using ML model"""
        try:
            # Get prediction probabilities
            probabilities = self.model.predict_proba(input_data)[0]
            predicted_class = self.model.predict(input_data)[0]
            
            # Map encoded prediction back to risk level
            if self.encoders and 'pest_risk' in self.encoders:
                risk_levels = self.encoders['pest_risk'].classes_
                risk_level = risk_levels[predicted_class]
            else:
                risk_map = {0: 'very_low', 1: 'low', 2: 'medium', 3: 'high', 4: 'very_high'}
                risk_level = risk_map.get(predicted_class, 'medium')
            
            return {
                'risk_level': risk_level,
                'risk_score': float(max(probabilities)),
                'confidence': float(max(probabilities)),
                'method': 'machine_learning'
            }
        except Exception as e:
            logger.error(f"ML prediction error: {e}")
            return None
    
    def _rule_based_prediction(self, soil_ph, temperature, humidity, rainfall, season, tree_age):
        """Rule-based pest risk prediction"""
        risk_score = 0
        risk_factors = []
        
        # Temperature risk factors
        if temperature > 28:
            risk_score += 2
            risk_factors.append("High temperature favors pest activity")
        elif temperature > 25:
            risk_score += 1
            risk_factors.append("Moderate temperature increases pest risk")
        
        # Humidity risk factors
        if humidity > 80:
            risk_score += 2
            risk_factors.append("High humidity promotes pest development")
        elif humidity > 70:
            risk_score += 1
            risk_factors.append("Elevated humidity increases pest pressure")
        
        # Rainfall risk factors
        if rainfall < 50:
            risk_score += 1
            risk_factors.append("Low rainfall may stress trees, increasing susceptibility")
        elif rainfall > 200:
            risk_score += 1
            risk_factors.append("Excessive rainfall creates favorable pest conditions")
        
        # Seasonal risk factors
        if season.lower() == 'summer':
            risk_score += 2
            risk_factors.append("Summer season peak pest activity period")
        elif season.lower() in ['spring', 'autumn']:
            risk_score += 1
            risk_factors.append(f"{season.capitalize()} season moderate pest activity")
        
        # Tree age factors
        if tree_age < 3:
            risk_score += 1
            risk_factors.append("Young trees more vulnerable to pests")
        
        # Soil pH factors
        if soil_ph < 5.5 or soil_ph > 7.0:
            risk_score += 1
            risk_factors.append("Suboptimal soil pH may weaken tree defenses")
        
        # Convert score to risk level
        if risk_score >= 6:
            risk_level = 'very_high'
        elif risk_score >= 4:
            risk_level = 'high'
        elif risk_score >= 2:
            risk_level = 'medium'
        elif risk_score >= 1:
            risk_level = 'low'
        else:
            risk_level = 'very_low'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score / 8.0,  # Normalize to 0-1
            'confidence': 0.7,  # Rule-based confidence
            'risk_factors': risk_factors,
            'method': 'rule_based'
        }
    
    def _combine_predictions(self, ml_prediction, rule_prediction):
        """Combine ML and rule-based predictions"""
        if ml_prediction is None:
            return rule_prediction
        
        # Weight ML prediction higher if confidence is high
        if ml_prediction['confidence'] > 0.8:
            return ml_prediction
        else:
            # Average the risk scores
            combined_score = (ml_prediction['risk_score'] + rule_prediction['risk_score']) / 2
            
            # Use the higher risk level as precautionary measure
            risk_levels = ['very_low', 'low', 'medium', 'high', 'very_high']
            ml_level_idx = risk_levels.index(ml_prediction['risk_level'])
            rule_level_idx = risk_levels.index(rule_prediction['risk_level'])
            final_level_idx = max(ml_level_idx, rule_level_idx)
            
            return {
                'risk_level': risk_levels[final_level_idx],
                'risk_score': combined_score,
                'confidence': (ml_prediction['confidence'] + rule_prediction['confidence']) / 2,
                'method': 'combined'
            }
    
    def _analyze_specific_pests(self, temperature, humidity, rainfall, season):
        """Analyze risk for specific pest types"""
        specific_risks = {}
        
        if not self.pest_knowledge:
            return specific_risks
        
        # Macadamia nut borer risk
        borer_risk = 'low'
        if temperature > 24 and humidity > 65:
            if season.lower() in ['spring', 'summer']:
                borer_risk = 'high'
            else:
                borer_risk = 'medium'
        
        specific_risks['macadamia_nut_borer'] = {
            'risk_level': borer_risk,
            'description': self.pest_knowledge.get('common_pests', {}).get('macadamia_nut_borer', {}).get('description', ''),
            'peak_activity': 'Warm, humid conditions during flowering and nut development'
        }
        
        # Stink bug risk
        stink_bug_risk = 'low'
        if temperature > 22 and season.lower() in ['spring', 'summer']:
            stink_bug_risk = 'medium'
            if humidity > 70:
                stink_bug_risk = 'high'
        
        specific_risks['stink_bugs'] = {
            'risk_level': stink_bug_risk,
            'description': self.pest_knowledge.get('common_pests', {}).get('stink_bugs', {}).get('description', ''),
            'peak_activity': 'Spring and early summer, especially warm days'
        }
        
        # Scale insect risk
        scale_risk = 'low'
        if humidity > 75 or (temperature > 26 and rainfall < 80):
            scale_risk = 'medium'
            if humidity > 85:
                scale_risk = 'high'
        
        specific_risks['scale_insects'] = {
            'risk_level': scale_risk,
            'description': self.pest_knowledge.get('common_pests', {}).get('scale_insects', {}).get('description', ''),
            'peak_activity': 'Year-round, especially in humid or stressed conditions'
        }
        
        return specific_risks
    
    def _get_recommendations(self, overall_risk, specific_pests):
        """Get pest management recommendations based on risk level"""
        recommendations = []
        
        if overall_risk in ['high', 'very_high']:
            recommendations.extend([
                "Increase monitoring frequency to twice weekly",
                "Consider preventive organic treatments",
                "Check pheromone traps daily",
                "Inspect trees for early pest signs"
            ])
        elif overall_risk == 'medium':
            recommendations.extend([
                "Maintain weekly monitoring schedule",
                "Prepare organic treatment materials",
                "Monitor beneficial insect populations"
            ])
        else:
            recommendations.extend([
                "Continue regular monitoring",
                "Maintain orchard sanitation",
                "Support beneficial insect habitat"
            ])
        
        # Add specific pest recommendations
        for pest_name, pest_info in specific_pests.items():
            if pest_info['risk_level'] in ['high', 'very_high']:
                pest_data = self.pest_knowledge.get('common_pests', {}).get(pest_name, {})
                treatments = pest_data.get('organic_treatments', [])
                if treatments:
                    recommendations.append(f"For {pest_name.replace('_', ' ')}: {treatments[0]}")
        
        return recommendations
    
    def _get_monitoring_advice(self, season, risk_level):
        """Get monitoring advice based on season and risk level"""
        base_advice = [
            "Visual inspection of leaves and branches",
            "Check for pest damage signs",
            "Monitor beneficial insect populations"
        ]
        
        if risk_level in ['high', 'very_high']:
            base_advice.extend([
                "Daily inspection of high-risk areas",
                "Document pest populations and damage",
                "Check pheromone trap catches"
            ])
        
        seasonal_advice = {
            'spring': ["Monitor for emerging pest populations", "Check flowering trees carefully"],
            'summer': ["Intensive monitoring during peak pest season", "Focus on developing nuts"],
            'autumn': ["Monitor harvest areas", "Check for late-season pest buildup"],
            'winter': ["Reduced monitoring frequency", "Focus on orchard sanitation"]
        }
        
        base_advice.extend(seasonal_advice.get(season.lower(), []))
        return base_advice
    
    def _fallback_prediction(self):
        """Fallback prediction when models fail"""
        return {
            'overall_risk_level': 'medium',
            'risk_score': 0.5,
            'confidence': 0.3,
            'specific_pests': {},
            'recommendations': [
                "Regular monitoring recommended",
                "Maintain good orchard sanitation",
                "Consult local agricultural extension"
            ],
            'monitoring_advice': [
                "Weekly visual inspections",
                "Check for common pest signs",
                "Monitor weather conditions"
            ],
            'prediction_date': datetime.now().isoformat(),
            'note': 'Fallback prediction - limited model availability'
        }

