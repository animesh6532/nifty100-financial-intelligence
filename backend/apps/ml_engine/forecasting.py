import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from statsmodels.tsa.holtwinters import ExponentialSmoothing
# Try importing Prophet, fallback gracefully if not installed yet
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False

from .utils import save_model, load_model

logger = logging.getLogger(__name__)

class ForecastingEngine:
    """
    Time-Series forecasting engine for revenue, profit, and cash flow.
    Supports Prophet (primary) and Holt-Winters (fallback).
    Models are persisted using joblib for future inference.
    """
    
    def __init__(self, target_col: str = 'revenue'):
        self.target_col = target_col

    def train_and_forecast(self, df: pd.DataFrame, company_id: int, periods: int = 3) -> Tuple[List[float], Any]:
        """
        Trains a model on historical data and predicts the next 'periods' (years).
        Returns a tuple of (forecast_values, model_artifact).
        """
        logger.info(f"Training forecast model for company {company_id} on {self.target_col}")
        
        if df.empty or len(df) < 3:
            logger.warning("Insufficient data points for forecasting (minimum 3 required).")
            return [0.0] * periods, None
            
        try:
            # Sort chronologically
            df = df.sort_values(by='year_value')
            
            if PROPHET_AVAILABLE and len(df) >= 5:
                # Prophet expects 'ds' (datestamp) and 'y' (target)
                # Convert year to dummy datetime for Prophet
                pdf = pd.DataFrame({
                    'ds': pd.to_datetime(df['year_value'].astype(str) + '-03-31'), # Assuming Indian FY ending March
                    'y': df[self.target_col].fillna(df[self.target_col].median())
                })
                model = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
                model.fit(pdf)
                
                future = model.make_future_dataframe(periods=periods, freq='Y')
                forecast = model.predict(future)
                
                # Get the future predictions only
                future_preds = forecast['yhat'].iloc[-periods:].tolist()
                
                # Save model
                model_name = f"prophet_{company_id}_{self.target_col}.joblib"
                save_model(model, model_name)
                
                return future_preds, model
                
            else:
                # Fallback to Holt-Winters / Exponential Smoothing
                logger.info("Using Holt-Winters fallback for forecasting.")
                y = df[self.target_col].fillna(df[self.target_col].median()).values
                
                # Simple exponential smoothing if data is very small
                model = ExponentialSmoothing(y, trend='add', seasonal=None, initialization_method="estimated")
                fitted_model = model.fit()
                
                forecast = fitted_model.forecast(periods).tolist()
                
                # Save model
                model_name = f"hw_{company_id}_{self.target_col}.joblib"
                save_model(fitted_model, model_name)
                
                return forecast, fitted_model

        except Exception as e:
            logger.error(f"Error during forecasting for {company_id}: {e}")
            return [0.0] * periods, None

    def load_and_predict(self, company_id: int, model_type: str = 'prophet', periods: int = 1) -> List[float]:
        """Loads a persisted model and generates a forecast."""
        model_name = f"{model_type}_{company_id}_{self.target_col}.joblib"
        model = load_model(model_name)
        
        if not model:
            return [0.0] * periods
            
        try:
            if 'prophet' in model_type.lower() and PROPHET_AVAILABLE:
                # Prophet logic to advance
                future = model.make_future_dataframe(periods=periods, freq='Y')
                forecast = model.predict(future)
                return forecast['yhat'].iloc[-periods:].tolist()
            else:
                # Statsmodels HW
                return model.forecast(periods).tolist()
        except Exception as e:
            logger.error(f"Failed to predict using loaded model {model_name}: {e}")
            return [0.0] * periods
