import logging
import pandas as pd
from django.db import transaction, connection
from .health_score import FinancialHealthEngine
from .anomaly import AnomalyDetector
from .clustering import SectorClusteringEngine
from .peer_engine import PeerRecommendationEngine
from .forecasting import ForecastingEngine

logger = logging.getLogger(__name__)

class MLEngineService:
    """
    Orchestrates the entire ML pipeline: fetches data from the warehouse, 
    runs all engines, and persists the results to `fact_ml_scores`.
    """
    
    def __init__(self):
        self.health_engine = FinancialHealthEngine()
        self.anomaly_engine = AnomalyDetector()
        self.clustering_engine = SectorClusteringEngine()
        self.peer_engine = PeerRecommendationEngine()
        self.forecaster = ForecastingEngine(target_col='revenue')

    def run_pipeline_for_all(self):
        """Runs the full suite of ML models for all companies."""
        logger.info("Starting ML Engine full pipeline run.")
        
        # 1. Fetch denormalized data
        df = self._fetch_warehouse_data()
        if df.empty:
            logger.error("No data found in warehouse.")
            return
            
        # 2. Anomaly Detection (Batch)
        anomaly_features = ['opm_percentage', 'debt_to_equity', 'roce_percentage']
        df = self._safe_anomaly_detection(df, anomaly_features)
        
        # 3. Clustering (Batch per sector ideally, but global for NIFTY100 is fine)
        cluster_features = ['revenue_growth_percentage', 'opm_percentage', 'debt_to_equity', 'cagr_3yr']
        df = self._safe_clustering(df, cluster_features)

        # 4. Iterate per company for Health Scoring and Forecasting
        results = []
        for company_id, group in df.groupby('company_id'):
            latest_data = group.sort_values('year_value', ascending=False).iloc[0].to_dict()
            
            # Health Score
            score, label = self.health_engine.compute_score(latest_data)
            
            # Label ID lookup (requires db query, but we can hardcode for performance or fetch once)
            label_id_map = self._get_label_ids()
            label_id = label_id_map.get(label, None)
            
            # Forecast Revenue (1yr and 3yr)
            forecasts, _ = self.forecaster.train_and_forecast(group, company_id, periods=3)
            f_1yr = forecasts[0] if len(forecasts) > 0 else 0
            f_3yr = forecasts[2] if len(forecasts) > 2 else 0
            
            # Collect results
            results.append({
                'company_id': company_id,
                'health_score': score,
                'label_id': label_id,
                'anomaly_flag': latest_data.get('anomaly_flag', False),
                'anomaly_score': latest_data.get('anomaly_score', 0.0),
                'forecasted_revenue_1yr': f_1yr,
                'forecasted_revenue_3yr': f_3yr
            })
            
        # 5. Persist Results
        self._persist_ml_scores(results)
        logger.info("ML Engine full pipeline completed.")

    def _fetch_warehouse_data(self) -> pd.DataFrame:
        query = """
            SELECT 
                c.company_id,
                y.year_value,
                s.sector_name,
                pl.revenue,
                pl.operating_profit,
                pl.opm_percentage,
                pl.net_profit,
                bs.debt_to_equity,
                cf.operating_cash_flow,
                fa.roce_percentage,
                fa.cagr_3yr,
                fa.sales_growth_percentage as revenue_growth_percentage,
                c.dividend_yield
            FROM dim_company c
            JOIN fact_profit_loss pl ON c.company_id = pl.company_id
            JOIN fact_balance_sheet bs ON c.company_id = bs.company_id AND pl.year_id = bs.year_id
            JOIN fact_cash_flow cf ON c.company_id = cf.company_id AND pl.year_id = cf.year_id
            JOIN fact_analysis fa ON c.company_id = fa.company_id AND pl.year_id = fa.year_id
            JOIN dim_year y ON pl.year_id = y.year_id
            LEFT JOIN dim_sector s ON c.sector_id = s.sector_id;
        """
        try:
            return pd.read_sql(query, connection)
        except Exception as e:
            logger.error(f"Failed to fetch warehouse data: {e}")
            return pd.DataFrame()

    def _get_label_ids(self) -> dict:
        try:
            df = pd.read_sql("SELECT label_id, label_name FROM dim_health_label", connection)
            return dict(zip(df.label_name, df.label_id))
        except:
            # Fallback based on schema initialization
            return {'EXCELLENT': 1, 'GOOD': 2, 'AVERAGE': 3, 'WEAK': 4, 'POOR': 5}

    def _safe_anomaly_detection(self, df, features):
        required = [f for f in features if f in df.columns]
        if required:
            return self.anomaly_engine.detect_anomalies(df, required)
        df['anomaly_flag'] = False
        df['anomaly_score'] = 0.0
        return df

    def _safe_clustering(self, df, features):
        required = [f for f in features if f in df.columns]
        if required:
            return self.clustering_engine.cluster_companies(df, required)
        df['cluster_id'] = -1
        return df

    @transaction.atomic
    def _persist_ml_scores(self, results: list):
        """Upserts results into `fact_ml_scores`."""
        if not results: return
        
        # Django bulk insert/update or raw SQL via psycopg2
        # Since we're inside Django and might not have models explicitly loaded here yet,
        # we can use cursor for raw upsert.
        query = """
            INSERT INTO fact_ml_scores 
            (company_id, health_score, label_id, anomaly_flag, anomaly_score, forecasted_revenue_1yr, forecasted_revenue_3yr)
            VALUES (%(company_id)s, %(health_score)s, %(label_id)s, %(anomaly_flag)s, %(anomaly_score)s, %(forecasted_revenue_1yr)s, %(forecasted_revenue_3yr)s)
            ON CONFLICT (company_id) DO UPDATE SET
                health_score = EXCLUDED.health_score,
                label_id = EXCLUDED.label_id,
                anomaly_flag = EXCLUDED.anomaly_flag,
                anomaly_score = EXCLUDED.anomaly_score,
                forecasted_revenue_1yr = EXCLUDED.forecasted_revenue_1yr,
                forecasted_revenue_3yr = EXCLUDED.forecasted_revenue_3yr,
                updated_at = CURRENT_TIMESTAMP;
        """
        try:
            with connection.cursor() as cursor:
                cursor.executemany(query, results)
            logger.info(f"Persisted {len(results)} ML score records.")
        except Exception as e:
            logger.error(f"Failed to persist ML scores: {e}")
            raise
