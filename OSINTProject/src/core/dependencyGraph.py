import asyncio
from OSINTProject.src.core.session_manager import SessionManager
from OSINTProject.src.scraping.discoveryEngine import DiscoveryEngine
from OSINTProject.src.scraping.extractionEngine import ExtractionEngine
from OSINTProject.src.scraping.scrapingCoordinator import ScrapingCoordinator
from OSINTProject.src.scraping.twitterScraper import TwitterScraper

class DependencyGraph:
    def __init__(self):
        self._session_manager = None
        self._scraping_coordinator = None
        self._discovery_engine = None
        self._extraction_engine = None
        self._twitter_scraper = None

    async def initialize(self):
        self._session_manager = SessionManager()
        self._twitter_scraper = TwitterScraper()
        await self._session_manager.start()
        self._discovery_engine = DiscoveryEngine(self._session_manager, self._twitter_scraper)
        self._extraction_engine = ExtractionEngine(self._session_manager)
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