from fastapi import FastAPI
from OSINTProject.src.core.config import settings
from OSINTProject.src.services.burn_service import burn_subject_data
from OSINTProject.src.services.analysis_service import analyzer
from OSINTProject.src.core.dependencyGraph import DependencyGraph
from OSINTProject.src.api.models import SearchRequest

app = FastAPI(title="OSINT Intelligence System")

dependency_graph = DependencyGraph()

async def startup():
    await dependency_graph.initialize()

async def shutdown():
    await dependency_graph.shutdown()

@app.post("/search")
async def search(request: SearchRequest):

    # Discover and Extract
    coordinator = dependency_graph.get_coordinator()
    results = await coordinator.scrape(request)

    if not results:
        return {
            "status": "success", 
            "data": None 
        }
    
    # Analyse
    analysis = analyzer.process(results)
    
    return {
        "status": "success",
        "data": analysis  

    }

@app.post("/burn/{subject_id}")
async def burn_subject(subject_id: int):
    success = burn_subject_data(subject_id)
    if success:
        return {"message": f"Successfully burned all data for subject {subject_id}"}
    return {"error": "Failed to burn data"}


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
