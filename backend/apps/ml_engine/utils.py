import os
import joblib
import logging
import pandas as pd
from typing import Any
from django.conf import settings

logger = logging.getLogger(__name__)

# Directory to persist trained models
MODELS_DIR = os.path.join(settings.BASE_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

def save_model(model: Any, filename: str) -> None:
    """Serialize and persist an ML model using joblib."""
    file_path = os.path.join(MODELS_DIR, filename)
    try:
        joblib.dump(model, file_path)
        logger.info(f"Successfully saved model to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save model {filename}: {e}")
        raise

def load_model(filename: str) -> Any:
    """Load a serialized ML model using joblib."""
    file_path = os.path.join(MODELS_DIR, filename)
    if not os.path.exists(file_path):
        logger.warning(f"Model file {file_path} does not exist.")
        return None
    try:
        model = joblib.load(file_path)
        logger.info(f"Successfully loaded model from {file_path}")
        return model
    except Exception as e:
        logger.error(f"Failed to load model {filename}: {e}")
        raise

def extract_features(df: pd.DataFrame, feature_cols: list) -> pd.DataFrame:
    """
    Standardize and handle missing values for feature columns.
    Returns a DataFrame containing only the cleaned features.
    """
    if df.empty:
        return pd.DataFrame()
    
    # Select only relevant columns
    features_df = df[feature_cols].copy()
    
    # Handle missing values (e.g., fill with median)
    for col in feature_cols:
        if features_df[col].isnull().any():
            median_val = features_df[col].median()
            features_df[col].fillna(median_val, inplace=True)
            
    return features_df

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning a default if denominator is zero."""
    if denominator == 0 or pd.isna(denominator):
        return default
    return numerator / denominator
