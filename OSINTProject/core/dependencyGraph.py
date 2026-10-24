import asyncio
from core.session_manager import SessionManager
from scraping.discoveryEngine import DiscoveryEngine
from scraping.extractionEngine import ExtractionEngine

class DependencyGraph:
    def __init__(self):
        self._session_manager = None
        self._discovery_engine = None
        self._extraction_engine = None

    async def initialize(self):
        self._session_manager = SessionManager()
        await self._session_manager.start()

        self._discovery_engine = DiscoveryEngine(self._session_manager)
        self._extraction_engine = ExtractionEngine(self._session_manager)

    def get_discovery_engine(self):
        return self._discovery_engine

    def get_extraction_engine(self):
        return self._extraction_engine
    
    async def shutdown(self):
        if self._session_manager:
            await self._session_manager.close()

# Example usage
async def main():
    graph = DependencyGraph()
    await graph.initialize()

    discovery_engine = graph.get_discovery_engine()
    extraction_engine = graph.get_extraction_engine()

if __name__ == "__main__":
    asyncio.run(main())