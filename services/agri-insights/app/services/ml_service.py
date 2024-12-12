import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.seasonal import seasonal_decompose

class MLService:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.model_version = "1.0.0"

    def prepare_features(self, historical_data: pd.DataFrame) -> np.ndarray:
        """Prepare features for the ML model"""
        # Calculate rolling means and other technical indicators
        df = historical_data.copy()
        df['price_7d_ma'] = df['price'].rolling(window=7).mean()
        df['price_30d_ma'] = df['price'].rolling(window=30).mean()
        df['volume_7d_ma'] = df['volume'].rolling(window=7).mean()
        df['price_volatility'] = df['price'].rolling(window=30).std()
        
        # Create seasonal features
        df['month'] = pd.to_datetime(df['date']).dt.month
        df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
        
        features = ['price', 'volume', 'price_7d_ma', 'price_30d_ma', 
                   'volume_7d_ma', 'price_volatility', 'month', 'day_of_week']
        
        return df[features].dropna().values

    def train_model(self, historical_data: pd.DataFrame):
        """Train the ML model on historical data"""
        X = self.prepare_features(historical_data)
        y = historical_data['price'].iloc[30:].values  # Skip first 30 days due to rolling calculations
        
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict_price(self, historical_data: pd.DataFrame, horizon: int) -> Dict:
        """Make price predictions for the specified horizon"""
        X = self.prepare_features(historical_data)
        X_scaled = self.scaler.transform(X)
        
        predictions = []
        confidence_scores = []
        
        for i in range(horizon):
            pred = self.model.predict(X_scaled[-1:])
            predictions.append(pred[0])
            
            # Calculate confidence score based on prediction intervals
            confidence_score = 1.0 - self.model.estimators_.std() / pred[0]
            confidence_scores.append(max(0, min(1, confidence_score)))
        
        return {
            "predictions": predictions,
            "confidence_scores": confidence_scores,
            "model_version": self.model_version
        }

    def analyze_historical_data(self, data: pd.DataFrame, analysis_type: str) -> Dict:
        """Perform historical data analysis"""
        results = {}
        
        if analysis_type in ["trend", "all"]:
            # Trend analysis
            decomposition = seasonal_decompose(data['price'], period=30)
            trend = decomposition.trend.dropna()
            results["trend"] = {
                "direction": "up" if trend.iloc[-1] > trend.iloc[-2] else "down",
                "strength": abs(trend.iloc[-1] - trend.iloc[-2]) / trend.iloc[-2]
            }
        
        if analysis_type in ["seasonality", "all"]:
            # Seasonality analysis
            decomposition = seasonal_decompose(data['price'], period=30)
            seasonal = decomposition.seasonal.dropna()
            results["seasonality"] = {
                "pattern": seasonal.tolist()[-30:],  # Last 30 days of seasonal pattern
                "strength": seasonal.std() / data['price'].std()
            }
        
        if analysis_type in ["volatility", "all"]:
            # Volatility analysis
            volatility = data['price'].rolling(window=30).std().dropna()
            results["volatility"] = {
                "current": volatility.iloc[-1],
                "trend": "increasing" if volatility.iloc[-1] > volatility.iloc[-2] else "decreasing",
                "historical_mean": volatility.mean()
            }
        
        return results

ml_service = MLService() 