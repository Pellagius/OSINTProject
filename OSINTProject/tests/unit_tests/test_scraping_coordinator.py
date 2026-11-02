import unittest
from unittest.mock import AsyncMock, MagicMock
from src.scraping.scrapingCoordinator import ScrapingCoordinator
from src.api.models import SearchRequest
from src.scraping.discoveryEngine import DiscoveryEngine
from src.scraping.extractionEngine import ExtractionEngine
from src.core.session_manager import SessionManager

class TestScrapingCoordinator(unittest.IsolatedAsyncioTestCase):

    async def test_scrape(self):
        # Initialize with discoveryEngine and extractionEngine
        discovery_engine = DiscoveryEngine(session_manager=SessionManager())
        extraction_engine = ExtractionEngine(session_manager=SessionManager())
        coordinator = ScrapingCoordinator(discovery_engine, extraction_engine, max_concurrent_extractions=5)
        request = SearchRequest(subject_name="test", location="Brisbane")
        discovery_engine.discover_sources = AsyncMock(return_value=[{"url": "http://test.com"}])
        extraction_engine.extract_detailed_data = AsyncMock(return_value={"raw_content": "Test content", "url": "http://test.com"})

        results = await coordinator.scrape(request)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["url"], "http://test.com")

if __name__ == "__main__":
    unittest.main()