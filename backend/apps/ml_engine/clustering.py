import logging
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from typing import List

logger = logging.getLogger(__name__)

class SectorClusteringEngine:
    """
    Groups companies into performance clusters using PCA and KMeans.
    Helps identify overperforming/underperforming groups within a sector.
    """
    
    def __init__(self, n_clusters: int = 3):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)

    def cluster_companies(self, df: pd.DataFrame, features: List[str]) -> pd.DataFrame:
        """
        Takes a DataFrame of companies, scales features, reduces dimensionality,
        and assigns a cluster label.
        """
        logger.info(f"Running clustering on {len(df)} companies.")
        if df.empty or len(df) < self.n_clusters:
            logger.warning("Not enough data to form clusters.")
            df['cluster_id'] = -1
            return df
            
        try:
            # Prepare feature matrix
            X = df[features].fillna(df[features].median())
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Dimensionality reduction (optional, good for viz)
            X_pca = self.pca.fit_transform(X_scaled)
            df['pca_x'] = X_pca[:, 0]
            df['pca_y'] = X_pca[:, 1]
            
            # KMeans Clustering
            cluster_labels = self.kmeans.fit_predict(X_scaled)
            df['cluster_id'] = cluster_labels
            
            logger.info("Clustering completed successfully.")
            return df
            
        except Exception as e:
            logger.error(f"Error during clustering: {e}")
            df['cluster_id'] = -1
            return df
