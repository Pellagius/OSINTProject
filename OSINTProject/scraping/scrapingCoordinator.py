import asyncio
import logging
from api.models import SearchRequest
from typing import List, Dict
from discoveryEngine import ScrapingEngine

try:
    from extractionEngine import ExtractionEngine
except ImportError:
    from extractionEngine import ExtractionEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScrapingCoordinator:
    def __init__(self, max_concurrent_extractions: int = 5):
        self._semaphore = asyncio.Semaphore(max_concurrent_extractions)

    async def process_discovery_results(self, request: SearchRequest) -> List[Dict]:
        # 1. Discovery Phase (Gathering candidates)
        discoverer = ScrapingEngine()  # If using DI for context, pass it here: ScrapingEngine(context=self_shared_ctx)

        all_results = []
        
        logger.info(f"Executing discovery phase for terms related to: {request.subject_name}")
        found = await discoverer.discover_sources(request)
        all_results.extend(found)

        # Deduplicate results (though discoveryEngine should already handle this based on our previous discussion).
        unique_items = [res for res in all_results if 'url' in res] 
        logger.info(f"Discovered {len(unique_items)} unique candidates to process.") 

   