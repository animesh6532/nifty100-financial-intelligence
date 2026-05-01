import logging
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from typing import List

logger = logging.getLogger(__name__)

class PeerRecommendationEngine:
    """
    Identifies comparable companies using Cosine Similarity on financial metrics.
    Dynamic execution.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()

    def get_peers(self, df: pd.DataFrame, target_company_id: int, features: List[str], top_n: int = 5) -> List[int]:
        """
        Given a dataframe of companies and a target company ID, 
        returns the top N most similar company IDs based on financial features.
        """
        logger.info(f"Finding peers for company_id: {target_company_id}")
        
        if df.empty or target_company_id not in df['company_id'].values:
            logger.warning(f"Target company {target_company_id} not found in dataset.")
            return []
            
        try:
            # Prepare matrix
            X = df[features].fillna(df[features].median())
            company_ids = df['company_id'].values
            
            # Find target index
            target_idx = df.index[df['company_id'] == target_company_id].tolist()[0]
            
            # Scale
            X_scaled = self.scaler.fit_transform(X)
            
            # Compute cosine similarity
            sim_matrix = cosine_similarity(X_scaled)
            
            # Get similarity scores for the target company
            sim_scores = list(enumerate(sim_matrix[target_idx]))
            
            # Sort by similarity, excluding the company itself
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            top_peers = [company_ids[i[0]] for i in sim_scores if company_ids[i[0]] != target_company_id]
            
            logger.info(f"Found {len(top_peers[:top_n])} peers.")
            return top_peers[:top_n]
            
        except Exception as e:
            logger.error(f"Error computing peer recommendations: {e}")
            return []
