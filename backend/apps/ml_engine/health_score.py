import logging
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple, List

logger = logging.getLogger(__name__)

class FinancialHealthEngine:
    """
    Computes a financial health score and assigns a health label using scikit-learn.
    We use KMeans clustering on key financial indicators to dynamically segment 
    companies into 5 health tiers, and compute a continuous score based on distance 
    to the 'best' cluster.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        # Meaningful indicators:
        # Profitability (opm_percentage), Leverage (debt_to_equity, negative impact),
        # Growth (revenue_growth_percentage), Cashflow Quality (ocf_to_np)
        self.features = ['profitability', 'growth', 'leverage', 'cashflow_quality', 'cagr']
        self.is_fitted = False
        self.cluster_mapping = {}

    def fit_predict_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Trains the KMeans model on a batch of companies and assigns scores/labels.
        Input DataFrame must contain:
        - company_id
        - opm_percentage
        - revenue_growth_percentage
        - debt_to_equity
        - operating_cash_flow
        - net_profit
        - cagr_3yr
        """
        try:
            logger.info("Fitting scikit-learn KMeans model for Health Scoring.")
            
            # Prepare features
            data = df.copy()
            data['profitability'] = data['opm_percentage'].fillna(0)
            data['growth'] = data['revenue_growth_percentage'].fillna(0)
            data['leverage'] = data['debt_to_equity'].fillna(0) * -1 # Invert so higher is better
            
            # Cashflow quality
            ocf = data['operating_cash_flow'].fillna(0)
            np_val = data['net_profit'].fillna(0)
            # Avoid division by zero, cap at 5
            data['cashflow_quality'] = np.where(np_val > 0, np.minimum(ocf / np_val, 5), 0)
            data['cagr'] = data['cagr_3yr'].fillna(0)
            
            X = data[self.features].values
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Fit KMeans
            data['cluster'] = self.kmeans.fit_predict(X_scaled)
            self.is_fitted = True
            
            # Determine which cluster is which by summing the centroids (since we inverted leverage, higher sum = better)
            centroids = self.kmeans.cluster_centers_
            cluster_scores = centroids.sum(axis=1)
            
            # Sort clusters from worst (0) to best (4)
            sorted_clusters = np.argsort(cluster_scores)
            
            # Map sorted index to labels
            labels = ['POOR', 'WEAK', 'AVERAGE', 'GOOD', 'EXCELLENT']
            self.cluster_mapping = {sorted_clusters[i]: labels[i] for i in range(5)}
            
            # Assign labels
            data['health_label'] = data['cluster'].map(self.cluster_mapping)
            
            # Compute a continuous score (0-100) based on distance to worst/best centroids
            worst_centroid = centroids[sorted_clusters[0]]
            best_centroid = centroids[sorted_clusters[-1]]
            
            scores = []
            for i, x in enumerate(X_scaled):
                dist_to_worst = np.linalg.norm(x - worst_centroid)
                dist_to_best = np.linalg.norm(x - best_centroid)
                if dist_to_worst + dist_to_best == 0:
                    score = 50.0
                else:
                    # Normalize to 0-100
                    score = (dist_to_worst / (dist_to_worst + dist_to_best)) * 100
                scores.append(round(score, 2))
                
            data['health_score'] = scores
            
            return data[['company_id', 'health_score', 'health_label']]

        except Exception as e:
            logger.error(f"Error in ML health scoring batch: {e}")
            df['health_score'] = 50.0
            df['health_label'] = 'AVERAGE'
            return df[['company_id', 'health_score', 'health_label']]

    def compute_score(self, metrics: Dict[str, float]) -> Tuple[float, str]:
        """Fallback for single company scoring if model is fitted."""
        # If not fitted, return a dummy or train on the fly (not ideal).
        # In a real scenario, the model would be loaded from disk.
        if not self.is_fitted:
            return 50.0, 'AVERAGE'
            
        try:
            prof = metrics.get('opm_percentage', 0)
            growth = metrics.get('revenue_growth_percentage', 0)
            lev = metrics.get('debt_to_equity', 0) * -1
            ocf = metrics.get('operating_cash_flow', 0)
            np_val = metrics.get('net_profit', 0)
            cf_qual = (ocf / np_val) if np_val > 0 else 0
            cf_qual = min(cf_qual, 5)
            cagr = metrics.get('cagr_3yr', 0)
            
            X = np.array([[prof, growth, lev, cf_qual, cagr]])
            X_scaled = self.scaler.transform(X)
            
            cluster = self.kmeans.predict(X_scaled)[0]
            label = self.cluster_mapping.get(cluster, 'AVERAGE')
            
            # Approximate score
            centroids = self.kmeans.cluster_centers_
            cluster_scores = centroids.sum(axis=1)
            sorted_clusters = np.argsort(cluster_scores)
            
            worst_centroid = centroids[sorted_clusters[0]]
            best_centroid = centroids[sorted_clusters[-1]]
            
            dist_to_worst = np.linalg.norm(X_scaled[0] - worst_centroid)
            dist_to_best = np.linalg.norm(X_scaled[0] - best_centroid)
            
            if dist_to_worst + dist_to_best == 0:
                score = 50.0
            else:
                score = (dist_to_worst / (dist_to_worst + dist_to_best)) * 100
                
            return round(score, 2), label
        except Exception as e:
            logger.error(f"Error computing health score: {e}")
            return 0.0, "POOR"
