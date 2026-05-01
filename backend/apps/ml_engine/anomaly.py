import logging
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from scipy import stats
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """
    Detects financial anomalies using IsolationForest and Z-Score detection.
    Dynamic training is used since NIFTY 100 data size is relatively small.
    """
    
    def __init__(self, contamination: float = 0.05):
        self.contamination = contamination
        self.model = IsolationForest(contamination=self.contamination, random_state=42)
        
    def detect_anomalies(self, df: pd.DataFrame, features: List[str]) -> pd.DataFrame:
        """
        Runs IsolationForest on the dataset to flag anomalies.
        Returns the DataFrame with 'anomaly_flag' and 'anomaly_score'.
        """
        logger.info(f"Running IsolationForest anomaly detection on {len(df)} records.")
        if df.empty or len(df) < 10:
            logger.warning("Dataset too small for reliable anomaly detection.")
            df['anomaly_flag'] = False
            df['anomaly_score'] = 0.0
            return df
            
        try:
            # Drop nulls for model training
            train_df = df[features].fillna(df[features].median())
            
            # Fit and predict
            preds = self.model.fit_predict(train_df)
            scores = self.model.decision_function(train_df)
            
            # preds: -1 for anomalies, 1 for normal
            df['anomaly_flag'] = np.where(preds == -1, True, False)
            df['anomaly_score'] = scores
            
            logger.info(f"Detected {df['anomaly_flag'].sum()} anomalies out of {len(df)}.")
            return df
            
        except Exception as e:
            logger.error(f"Error during IsolationForest execution: {e}")
            df['anomaly_flag'] = False
            df['anomaly_score'] = 0.0
            return df

    def detect_zscore_spikes(self, df: pd.DataFrame, column: str, threshold: float = 3.0) -> pd.DataFrame:
        """
        Detects abnormal spikes in a specific column using Z-scores (e.g., suspicious revenue spikes).
        """
        if df.empty or column not in df.columns:
            return df
            
        try:
            z_scores = np.abs(stats.zscore(df[column].fillna(df[column].median())))
            flag_col = f'{column}_spike_flag'
            df[flag_col] = z_scores > threshold
            logger.info(f"Detected {df[flag_col].sum()} Z-score spikes in {column}.")
            return df
        except Exception as e:
            logger.error(f"Error during Z-score detection for {column}: {e}")
            df[f'{column}_spike_flag'] = False
            return df
