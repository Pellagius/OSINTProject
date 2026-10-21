from fastapi import FastAPI
from core.config import settings
from services.burn_service import burn_subject_data
from services.analysis_service import analyzer
from api.models import SearchRequest

app = FastAPI(title="OSINT Intelligence System")



@app.post("/search")
async def search(request: SearchRequest):
    # The search logic will be implemented here, 
    # utilizing ScrapingEngine and the analyzer.
    # For now, we will simulate the link between the request and the engine.
    # In a full implementation, we would use a mapping service to turn 
    # search criteria into a list of URLs to scrape.
    
    # Example of how the integration will flow:
    # 1. Determine URLs based on request.subject_name and request.location
    # 2. Pass URLs to ScrapingEngine
    # 3. Pass resulting text to analyzer
    
    # For this step, we are making the link between the request and the processing pipeline.
    result = {
        "status": "success",
        "message": f"Processing search for {request.subject_name} in {request.location}",
        "data": request.model_dump()
    }
    return result

@app.post("/burn/{subject_id}")
async def burn_subject(subject_id: int):
    success = burn_subject_data(subject_id)
    if success:
        return {"message": f"Successfully burned all data for subject {subject_id}"}
    return {"error": "Failed to burn data"}
