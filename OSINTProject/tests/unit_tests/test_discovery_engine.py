import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from OSINTProject.src.scraping.discoveryEngine import DiscoveryEngine
from OSINTProject.src.api.models import SearchRequest
from OSINTProject.src.core.session_manager import SessionManager
from OSINTProject.src.scraping.twitterScraper import TwitterScraper

class TestScrapingEngine(unittest.IsolatedAsyncioTestCase):

    async def test_discover_sources(self):
        engine = DiscoveryEngine(session_manager=SessionManager())
        request = SearchRequest(subject_name="test", location="Brisbane")
        
        # Mock _perform_multi_platform_search to return some initial results
        engine._perform_multi_platform_search = AsyncMock(return_value=[
            {"url": "http://test.com", "source_type": "web"},
            {"url": "http://social.com", "source_type": "social"}
        ])
        
        # Mock _filter_high_value to return only high-value results
        # Assuming high-value results are those with "social" as source_type
        with patch('OSINTProject.src.utils.filters.filter_high_value') as mock_filter_high_value:
            mock_filter_high_value.return_value = [
                {"url": "http://social.com", "source_type": "social"}
            ]

            results = await engine.discover_sources(request)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["url"], "http://social.com")

    async def test_discover_sources_no_results(self):
        engine = DiscoveryEngine(session_manager=SessionManager())
        request = SearchRequest(subject_name="test", location="Brisbane")
        engine._perform_multi_platform_search = AsyncMock(return_value=[])
        
        # Mock _filter_high_value to return an empty list
        with patch('OSINTProject.src.utils.filters.filter_high_value') as mock_filter_high_value:
            mock_filter_high_value.return_value = []

            results = await engine.discover_sources(request)
            self.assertEqual(len(results), 0)

    async def test_discover_sources_mixed_results(self):
        engine = DiscoveryEngine(session_manager=SessionManager())
        request = SearchRequest(subject_name="test", location="Brisbane")
        engine._perform_multi_platform_search = AsyncMock(return_value=[
            {"url": "http://social.com", "source_type": "social"},
            {"url": "http://web.com", "source_type": "web"}
        ])
        
        # Mock _filter_high_value to return only high-value results
        with patch('OSINTProject.src.utils.filters.filter_high_value') as mock_filter_high_value:
            mock_filter_high_value.return_value = [
                {"url": "http://social.com", "source_type": "social"}
            ]

            results = await engine.discover_sources(request)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["url"], "http://social.com")

    async def test_perform_multi_platform_search(self):
        engine = DiscoveryEngine(session_manager=SessionManager())
        engine._discover_social_media = AsyncMock(return_value=[{"url": "http://social.com"}])
        engine._perform_general_web_discovery = AsyncMock(return_value=[{"url": "http://web.com"}])

        results = await engine._perform_multi_platform_search("test")
        self.assertEqual(len(results), 2)

    async def test_perform_multi_platform_search_empty_input(self):
        engine = DiscoveryEngine(session_manager=SessionManager())
        engine._discover_social_media = AsyncMock(return_value=[])
        engine._perform_general_web_discovery = AsyncMock(return_value=[])

        results = await engine._perform_multi_platform_search("")
        self.assertEqual(len(results), 0)

    async def test_perform_general_web_discovery(self):
        engine = DiscoveryEngine(session_manager=SessionManager())
        engine._fetch_serp_data = AsyncMock(return_value=[
            {"url": "http://web.com", "title": "Test"},
            {"url": "http://sponsored.com", "title": "Sponsored Link"}
        ])

        results = await engine._perform_general_web_discovery("test")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["url"], "http://web.com")

    async def test_perform_general_web_discovery_empty_input(self):
        engine = DiscoveryEngine(session_manager=SessionManager())
        engine._fetch_serp_data = AsyncMock(return_value=[])

        results = await engine._perform_general_web_discovery("")
        self.assertEqual(len(results), 0)

    async def test_perform_general_web_discovery_with_sponsored_links(self):
        engine = DiscoveryEngine(session_manager=SessionManager())
        engine._fetch_serp_data = AsyncMock(return_value=[
            {"url": "http://sponsored.com", "title": "Sponsored Link"},
            {"url": "http://web.com", "title": "Test"}
        ])

        results = await engine._perform_general_web_discovery("test")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["url"], "http://web.com")

    async def test_discover_social_media(self):
       
        twitterScraper = TwitterScraper()
        twitterScraper.generate_social_media_variants = MagicMock(return_value=[
            "http://twitter.com/joebloggs",
            "http://twitter.com/joebloggs_",
            "http://twitter.com/joe_bloggs"
        ])
        engine = DiscoveryEngine(session_manager=SessionManager(), twitter_scraper=twitterScraper)
        results = await engine._discover_social_media("Joe Bloggs")
        self.assertEqual(len(results), 3)
        self.assertIn("http://twitter.com/joebloggs", results[0]["url"])
        self.assertIn("http://twitter.com/joebloggs_", results[1]["url"])
        self.assertIn("http://twitter.com/joe_bloggs", results[2]["url"])

    async def test_discover_social_media_empty_input(self):
        engine = DiscoveryEngine(session_manager=SessionManager())
        twitterScraper = TwitterScraper()
        twitterScraper.generate_social_media_variants = MagicMock(return_value=[])

        results = await engine._discover_social_media("")
        self.assertEqual(len(results), 0)

    async def test_filter_high_value_with_high_value_results(self):
        with patch('OSINTProject.src.utils.filters.filter_high_value') as mock_filter_high_value:
            mock_filter_high_value.return_value = [
                {"url": "http://social.com", "source_type": "social"}
            ]
            results = mock_filter_high_value([
                {"url": "http://social.com", "source_type": "social"},
                {"url": "http://web.com", "source_type": "web"}
            ])
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["url"], "http://social.com")

    async def test_filter_high_value_no_high_value_results(self):
        with patch('OSINTProject.src.utils.filters.filter_high_value') as mock_filter_high_value:
            mock_filter_high_value.return_value = []
            results = mock_filter_high_value([
                {"url": "http://test.com", "source_type": "web"}
            ])
            self.assertEqual(len(results), 0)

if __name__ == "__main__":
    unittest.main()