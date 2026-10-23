import asyncio
import logging
from api.models import SearchRequest
from typing import List, Dict
from scraping.discoveryEngine import DiscoveryEngine
from scraping.extractionEngine import ExtractionEngine
from core.session_manager import SessionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScrapingCoordinator:
    def __init__(self, max_concurrent_extractions: int = 5):
        self._semaphore = asyncio.Semaphore(max_concurrent_extractions)
        self._session_manager = SessionManager(max_pages=max_concurrent_extractions)

    async def process_discovery_results(self, request: SearchRequest) -> List[Dict]:
        # 1. Discovery Phase (Gathering candidates)

        discoverer = DiscoveryEngine(session_mgr)
        all_results = []
        
        logger.info(f"Executing discovery phase for terms related to: {request.subject_name}")
        found = await discoverer.discover_sources(request)
        all_results.extend(found)

        # Deduplicate results (though discoveryEngine should already handle this based on our previous discussion).
        unique_items = [res for res in all_results if 'url' in res] 
        logger.info(f"Discovered {len(unique_items)} unique candidates to process.") 

        # 2. Extraction Phase (Getting content from the discovered URLs)
        extractor = ExtractionEngine(session_mgr)
        processed_results = []
   
        async def _wrapped_extraction(item):
            async with self._semaphore: # Respect the max concurrent limit (e.g., Playwright pages open at once)
                try:
                    result = await extractor.extract_detailed_data(item['url'])
                    if result and 'raw_content' in result:  # Only add if extraction was successful
                        return result
                except Exception as e:
                    logger.error(f"Failed to extract content from {item.get('url')}: {e}")
            return None

        tasks = [asyncio.create_task(_wrapped_extraction(item)) for item in unique_items]
        results = await asyncio.gather(*tasks)
        processed_results = [r for r in results if r is not None]

        logger.info(f"Successfully processed {len(processed_results)} items.")
        return processed_results


