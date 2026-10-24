import unittest
from unittest.mock import AsyncMock, MagicMock
from scraping.discoveryEngine import DiscoveryEngine
from api.models import SearchRequest

class TestScrapingEngine(unittest.IsolatedAsyncioTestCase):

    async def test_discover_sources(self):
        engine = DiscoveryEngine()
        request = SearchRequest(subject_name="test", location="Brisbane")
        engine._perform_multi_platform_search = AsyncMock(return_value=[{"url": "http://test.com"}])
        engine._filter_high_value = MagicMock(return_value=[{"url": "http://test.com"}])

        results = await engine.discover_sources(request)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["url"], "http://test.com")

    async def test_perform_multi_platform_search(self):
        engine = DiscoveryEngine()
        engine._discover_social_media = AsyncMock(return_value=[{"url": "http://social.com"}])
        engine._perform_general_web_discovery = AsyncMock(return_value=[{"url": "http://web.com"}])

        results = await engine._perform_multi_platform_search("test")
        self.assertEqual(len(results), 2)

    async def test_perform_general_web_discovery(self):
        engine = DiscoveryEngine()
        engine._fetch_serp_data = AsyncMock(return_value=[{"url": "http://web.com", "title": "Test"}])

        results = await engine._perform_general_web_discovery("test")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["url"], "http://web.com")

    async def test_discover_social_media(self):
        engine = DiscoveryEngine()
        from scraping.twitterScraper import TwitterScraper
        TwitterScraper.generate_social_media_variants = MagicMock(return_value=["http://twitter.com/test"])

        results = await engine._discover_social_media("test")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["url"], "http://twitter.com/test")

    def test_filter_high_value(self):
        engine = DiscoveryEngine()
        results = [{"url": "http://test.com"}, {"url": "http://login.com"}]
        filtered = engine._filter_high_value(results)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["url"], "http://test.com")

if __name__ == "__main__":
    unittest.main()