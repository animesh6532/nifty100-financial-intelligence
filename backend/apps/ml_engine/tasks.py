import logging
from celery import shared_task
from .services import MLEngineService

logger = logging.getLogger(__name__)

@shared_task
def run_full_ml_pipeline():
    """
    Celery task to run the full machine learning pipeline.
    This includes anomaly detection, clustering, health scoring, and forecasting.
    Results are persisted back to the database.
    """
    logger.info("Starting scheduled ML pipeline run.")
    try:
        service = MLEngineService()
        service.run_pipeline_for_all()
        logger.info("Scheduled ML pipeline run completed successfully.")
        return {"status": "success", "message": "ML pipeline executed successfully."}
    except Exception as e:
        logger.error(f"Scheduled ML pipeline run failed: {e}")
        return {"status": "error", "message": str(e)}

@shared_task
def retrain_forecast_model(company_id: int):
    """
    Celery task to specifically retrain a forecast model for a single company.
    (Useful if new quarterly data arrives).
    """
    logger.info(f"Retraining forecast model for company_id: {company_id}")
    try:
        service = MLEngineService()
        df = service._fetch_warehouse_data()
        
        # Filter for company
        company_df = df[df['company_id'] == company_id]
        if not company_df.empty:
            forecasts, _ = service.forecaster.train_and_forecast(company_df, company_id, periods=3)
            logger.info(f"Retrained forecast successfully. New 1yr forecast: {forecasts[0]}")
            
            # Note: We would ideally update fact_ml_scores here as well, 
            # but usually the full pipeline runs and updates everything.
            return {"status": "success", "forecasts": forecasts}
        else:
            return {"status": "skipped", "message": "No data found for company."}
    except Exception as e:
        logger.error(f"Retraining forecast model failed: {e}")
        return {"status": "error", "message": str(e)}
