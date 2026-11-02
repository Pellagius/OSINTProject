import asyncio
import logging
from src.core.session_manager import SessionManager
from src.scraping.discoveryEngine import DiscoveryEngine
from src.scraping.extractionEngine import ExtractionEngine
from src.scraping.scrapingCoordinator import ScrapingCoordinator
from src.scraping.twitterScraper import TwitterScraper

logger = logging.getLogger(__name__)

class DependencyGraph:
    def __init__(self):
        self._session_manager = None
        self._scraping_coordinator = None
        self._discovery_engine = None
        self._extraction_engine = None
        self._twitter_scraper = None

    async def initialize(self):
        self_session_manager = SessionManager()
        await self_session_manager.__aenter__()
        self._twitter_scraper = TwitterScraper()
        self._discovery_engine = DiscoveryEngine(self_session_manager, self._twitter_scraper)
        self._extraction_engine = ExtractionEngine( self_session_manager)
        self._scraping_coordinator = ScrapingCoordinator(self._discovery_engine, self._extraction_engine)
        
    def get_coordinator(self):
        return self._scraping_coordinator

    async def shutdown(self):
        if self._session_manager:
            await self._session_manager.close()

# Example usage
async def main():
    graph = DependencyGraph()
    await graph.initialize()

    _ = graph.get_coordinator()

if __name__ == "__main__":
    asyncio.run(main())