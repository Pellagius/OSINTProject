import unittest
from unittest.mock import AsyncMock, MagicMock
from scraping.scrapingCoordinator import ScrapingCoordinator
from api.models import SearchRequest

class TestScrapingCoordinator(unittest.IsolatedAsyncioTestCase):

    async def test_process_discovery_results(self):
        coordinator = ScrapingCoordinator()
        request = SearchRequest(subject_name="test", location="Brisbane")
        discoverer = MagicMock()
        discoverer.discover_sources = AsyncMock(return_value=[{"url": "http://test.com"}])

        results = await coordinator.process_discovery_results(request)
        print(f"RESULTS: { results }")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["url"], "http://test.com")

if __name__ == "__main__":
    unittest.main()