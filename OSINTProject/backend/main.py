from fastapi import FastAPI
from core.config import settings
from services.burn_service import burn_subject_data
from services.analysis_service import analyzer
from api.models import SearchRequest
from core.dependencyGraph import DependencyGraph

app = FastAPI(title="OSINT Intelligence System")

dependency_graph = DependencyGraph()

async def startup():
    await dependency_graph.initialize()

async def shutdown():
    print("Shutting down DependencyGraph...")
    await dependency_graph.shutdown()

@app.post("/search")
async def search(request: SearchRequest):
    discovery_engine = dependency_graph.get_discovery_engine()
    extraction_engine = dependency_graph.get_extraction_engine()

    # Discover
    try:
        discovery_results = await discovery_engine.discover_sources(request)

    except Exception as e:
         return {"status": "error", "message": f"Discovery failed for {request.subject_name}: {str(e)}"}

    # Extract
    extracted_data = []
    for url in discovery_results.get("urls", []): 
        page_content = await extraction_engine.extract_detailed_data(url)
        extracted_data.append({
            "source": url,
            "raw_text": page_content
        })
    
    # Analyse
    # TODO: Anaylse extracted_data
    
    return {
        "status": "success",
        "data": "analysed data repsonse object" 

    }

@app.post("/burn/{subject_id}")
async def burn_subject(subject_id: int):
    success = burn_subject_data(subject_id)
    if success:
        return {"message": f"Successfully burned all data for subject {subject_id}"}
    return {"error": "Failed to burn data"}


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
