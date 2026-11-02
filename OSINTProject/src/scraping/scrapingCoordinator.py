import asyncio
import logging
from src.api.models import SearchRequest
from typing import List, Dict
from src.scraping.discoveryEngine import DiscoveryEngine
from src.scraping.extractionEngine import ExtractionEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScrapingCoordinator:
    def __init__(self, discoveryEngine: DiscoveryEngine, extractionEngine: ExtractionEngine, max_concurrent_extractions: int = 5):
        self._semaphore = asyncio.Semaphore(max_concurrent_extractions)
        self._discovery_engine = discoveryEngine
        self._extraction_engine = extractionEngine

    async def scrape(self, request: SearchRequest) -> List[Dict]:
        all_results = []
        
        logger.info(f"Executing discovery phase for terms related to: {request.subject_name}")
        found = await self._discovery_engine.discover_sources(request)
        all_results.extend(found)

        unique_items = [res for res in all_results if 'url' in res] 
        logger.info(f"Discovered {len(unique_items)} unique candidates to process.")
   
        async def _wrapped_extraction(item):
            async with self._semaphore: # Respect the max concurrent limit (e.g., Playwright pages open at once)
                try:
                    result = await self._extraction_engine.extract_detailed_data(item['url'])
                    print(f"Extracted data for {item['url']}: {result}")
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

