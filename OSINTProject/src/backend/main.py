from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.services.burn_service import burn_subject_data
from src.services.analysis_service import analyzer
from src.core.dependencyGraph import DependencyGraph
from src.api.models import SearchRequest
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up...")
    await dependency_graph.initialize()
    
    yield 
    
    print("Application is shutting down...")
    await dependency_graph.shutdown()

app = FastAPI(title="OSINT Intelligence System", lifespan=lifespan)
dependency_graph = DependencyGraph()

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
    analysis = analyzer.analyze_content(results)

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
