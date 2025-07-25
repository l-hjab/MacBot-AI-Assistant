"""
Model Training Module for Macadamia Farming Predictions
======================================================

This module handles training and evaluation of Random Forest models
for various farming prediction tasks.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, mean_squared_error, r2_score
import joblib
import os
from typing import Dict, Tuple, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MacadamiaModelTrainer:
    """
    Handles training of Random Forest models for macadamia farming predictions
    """
    
    def __init__(self, data_path: str = "macadamia_bot/data/farming_dataset.csv"):
        """
        Initialize the model trainer
        
        Args:
            data_path: Path to the farming dataset CSV file
        """
        self.data_path = data_path
        self.models = {}
        self.encoders = {}
        self.scalers = {}
        self.feature_columns = ['soil_ph', 'temperature', 'humidity', 'rainfall', 'season', 'tree_age']
        
    def load_and_prepare_data(self) -> pd.DataFrame:
        """
        Load and prepare the farming dataset
        
        Returns:
            Prepared DataFrame with encoded categorical variables
        """
        try:
            df = pd.read_csv(self.data_path)
            logger.info(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns")
            
            # Encode categorical variables
            if 'season' in df.columns:
                le_season = LabelEncoder()
                df['season_encoded'] = le_season.fit_transform(df['season'])
                self.encoders['season'] = le_season
                
            # Encode target variables that are categorical
            categorical_targets = ['pest_risk', 'fertilizer_need', 'harvest_ready']
            for target in categorical_targets:
                if target in df.columns:
                    le = LabelEncoder()
                    df[f'{target}_encoded'] = le.fit_transform(df[target])
                    self.encoders[target] = le
                    
            return df
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """
        Prepare feature matrix for training
        
        Args:
            df: DataFrame with farming data
            
        Returns:
            Feature matrix as numpy array
        """
        feature_cols = ['soil_ph', 'temperature', 'humidity', 'rainfall', 'season_encoded', 'tree_age']
        X = df[feature_cols].values
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        self.scalers['features'] = scaler
        
        return X_scaled
    
    def train_pest_risk_model(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Train Random Forest model for pest risk prediction
        
        Args:
            df: Prepared DataFrame
            
        Returns:
            Dictionary with model performance metrics
        """
        logger.info("Training pest risk prediction model...")
        
        X = self.prepare_features(df)
        y = df['pest_risk_encoded'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Random Forest
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        rf_model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = rf_model.score(X_train, y_train)
        test_score = rf_model.score(X_test, y_test)
        
        # Cross-validation
        cv_scores = cross_val_score(rf_model, X, y, cv=5)
        
        # Predictions for detailed evaluation
        y_pred = rf_model.predict(X_test)
        
        # Store model
        self.models['pest_risk'] = rf_model
        
        # Save model
        os.makedirs('macadamia_bot/models/saved', exist_ok=True)
        joblib.dump(rf_model, 'macadamia_bot/models/saved/pest_risk_model.pkl')
        
        results = {
            'model_type': 'pest_risk_classifier',
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_importance': dict(zip(
                ['soil_ph', 'temperature', 'humidity', 'rainfall', 'season', 'tree_age'],
                rf_model.feature_importances_
            ))
        }
        
        logger.info(f"Pest risk model trained - Test accuracy: {test_score:.3f}")
        return results
    
    def train_fertilizer_need_model(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Train Random Forest model for fertilizer need prediction
        
        Args:
            df: Prepared DataFrame
            
        Returns:
            Dictionary with model performance metrics
        """
        logger.info("Training fertilizer need prediction model...")
        
        X = self.prepare_features(df)
        y = df['fertilizer_need_encoded'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Random Forest
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        rf_model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = rf_model.score(X_train, y_train)
        test_score = rf_model.score(X_test, y_test)
        cv_scores = cross_val_score(rf_model, X, y, cv=5)
        
        # Store model
        self.models['fertilizer_need'] = rf_model
        
        # Save model
        joblib.dump(rf_model, 'macadamia_bot/models/saved/fertilizer_need_model.pkl')
        
        results = {
            'model_type': 'fertilizer_need_classifier',
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_importance': dict(zip(
                ['soil_ph', 'temperature', 'humidity', 'rainfall', 'season', 'tree_age'],
                rf_model.feature_importances_
            ))
        }
        
        logger.info(f"Fertilizer need model trained - Test accuracy: {test_score:.3f}")
        return results
    
    def train_harvest_readiness_model(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Train Random Forest model for harvest readiness prediction
        
        Args:
            df: Prepared DataFrame
            
        Returns:
            Dictionary with model performance metrics
        """
        logger.info("Training harvest readiness prediction model...")
        
        X = self.prepare_features(df)
        y = df['harvest_ready_encoded'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Random Forest
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        rf_model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = rf_model.score(X_train, y_train)
        test_score = rf_model.score(X_test, y_test)
        cv_scores = cross_val_score(rf_model, X, y, cv=5)
        
        # Store model
        self.models['harvest_ready'] = rf_model
        
        # Save model
        joblib.dump(rf_model, 'macadamia_bot/models/saved/harvest_ready_model.pkl')
        
        results = {
            'model_type': 'harvest_readiness_classifier',
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_importance': dict(zip(
                ['soil_ph', 'temperature', 'humidity', 'rainfall', 'season', 'tree_age'],
                rf_model.feature_importances_
            ))
        }
        
        logger.info(f"Harvest readiness model trained - Test accuracy: {test_score:.3f}")
        return results
    
    def train_yield_prediction_model(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Train Random Forest model for yield prediction (regression)
        
        Args:
            df: Prepared DataFrame
            
        Returns:
            Dictionary with model performance metrics
        """
        logger.info("Training yield prediction model...")
        
        X = self.prepare_features(df)
        y = df['yield_prediction'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest Regressor
        rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        rf_model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = rf_model.score(X_train, y_train)
        test_score = rf_model.score(X_test, y_test)
        
        # Predictions
        y_pred = rf_model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        # Cross-validation
        cv_scores = cross_val_score(rf_model, X, y, cv=5)
        
        # Store model
        self.models['yield_prediction'] = rf_model
        
        # Save model
        joblib.dump(rf_model, 'macadamia_bot/models/saved/yield_prediction_model.pkl')
        
        results = {
            'model_type': 'yield_prediction_regressor',
            'train_r2': train_score,
            'test_r2': test_score,
            'rmse': rmse,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_importance': dict(zip(
                ['soil_ph', 'temperature', 'humidity', 'rainfall', 'season', 'tree_age'],
                rf_model.feature_importances_
            ))
        }
        
        logger.info(f"Yield prediction model trained - Test R²: {test_score:.3f}, RMSE: {rmse:.3f}")
        return results
    
    def train_all_models(self) -> Dict[str, Any]:
        """
        Train all farming prediction models
        
        Returns:
            Dictionary with all model performance metrics
        """
        logger.info("Starting training of all macadamia farming models...")
        
        # Load and prepare data
        df = self.load_and_prepare_data()
        
        # Train all models
        results = {}
        results['pest_risk'] = self.train_pest_risk_model(df)
        results['fertilizer_need'] = self.train_fertilizer_need_model(df)
        results['harvest_ready'] = self.train_harvest_readiness_model(df)
        results['yield_prediction'] = self.train_yield_prediction_model(df)
        
        # Save encoders and scalers
        joblib.dump(self.encoders, 'macadamia_bot/models/saved/encoders.pkl')
        joblib.dump(self.scalers, 'macadamia_bot/models/saved/scalers.pkl')
        
        logger.info("All models trained successfully!")
        return results
    
    def optimize_hyperparameters(self, model_type: str, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Optimize hyperparameters for a specific model using GridSearchCV
        
        Args:
            model_type: Type of model to optimize ('pest_risk', 'fertilizer_need', etc.)
            df: Prepared DataFrame
            
        Returns:
            Best parameters and performance metrics
        """
        logger.info(f"Optimizing hyperparameters for {model_type} model...")
        
        X = self.prepare_features(df)
        
        if model_type == 'yield_prediction':
            y = df['yield_prediction'].values
            model = RandomForestRegressor(random_state=42)
        else:
            y = df[f'{model_type}_encoded'].values
            model = RandomForestClassifier(random_state=42)
        
        # Parameter grid
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 8, 10, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        # Grid search
        grid_search = GridSearchCV(
            model, param_grid, cv=5, scoring='r2' if model_type == 'yield_prediction' else 'accuracy',
            n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X, y)
        
        results = {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'cv_results': grid_search.cv_results_
        }
        
        logger.info(f"Best parameters for {model_type}: {grid_search.best_params_}")
        logger.info(f"Best cross-validation score: {grid_search.best_score_:.3f}")
        
        return results

def main():
    """
    Main function to train all models
    """
    trainer = MacadamiaModelTrainer()
    results = trainer.train_all_models()
    
    print("\n" + "="*60)
    print("MACADAMIA FARMING MODEL TRAINING RESULTS")
    print("="*60)
    
    for model_name, metrics in results.items():
        print(f"\n{model_name.upper()} MODEL:")
        print("-" * 30)
        for key, value in metrics.items():
            if key == 'feature_importance':
                print(f"{key}:")
                for feature, importance in value.items():
                    print(f"  {feature}: {importance:.3f}")
            else:
                print(f"{key}: {value}")

if __name__ == "__main__":
    main()

