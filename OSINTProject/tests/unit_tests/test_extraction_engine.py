import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock
from src.scraping.extractionEngine import ExtractionEngine
from src.core.session_manager import SessionManager

class TestExtractionEngine(unittest.IsolatedAsyncioTestCase):

    async def test_fetch_page_content(self):
        session_manager = AsyncMock(spec=SessionManager)
        engine = ExtractionEngine(session_manager=session_manager)
        async_page_mock = AsyncMock()
        async_page_mock.inner_text = AsyncMock(return_value="<p>Test content</p>")
        async_page_mock.close = AsyncMock(return_value=None)
        async_context_mock = AsyncMock()
        async_context_mock.new_page = AsyncMock(return_value=async_page_mock)
        session_manager.get_new_context = AsyncMock(return_value=async_context_mock)
        content = await engine.fetch_page_content("http://test.com")
        self.assertEqual(content, "Test content")

    async def test_fetch_page_content_get_new_context_failure(self):
        # Initialize with a session manager
        session_manager = SessionManager()
        engine = ExtractionEngine(session_manager=session_manager)
        engine.session_manager.get_new_context = AsyncMock(side_effect=Exception("Failed to get new context"))

        with self.assertRaises(Exception):
            await engine.fetch_page_content("http://test.com")

    async def test_fetch_page_content_inner_text_failure(self):
        # Initialize with a session manager
        session_manager = SessionManager()
        engine = ExtractionEngine(session_manager=session_manager)
        session_manager.get_new_context = AsyncMock(side_effect=Exception("Failed to get inner text"))

        with self.assertRaises(Exception):
            await engine.fetch_page_content("http://test.com")

    async def test_extract_detailed_data(self):
        # Initialize with a session manager
        session_manager = SessionManager()
        engine = ExtractionEngine(session_manager=session_manager)
        engine.fetch_page_content = AsyncMock(return_value="Test content")

        data = await engine.extract_detailed_data("http://test.com")
        self.assertEqual(data["raw_content"], "Test content")
        self.assertEqual(data["url"], "http://test.com")
        self.assertEqual(data["source_type"], "generic")

    async def test_extract_detailed_data_empty_content(self):
        # Initialize with a session manager
        session_manager = SessionManager()
        engine = ExtractionEngine(session_manager=session_manager)
        engine.fetch_page_content = AsyncMock(return_value="")

        data = await engine.extract_detailed_data("http://test.com")
        self.assertEqual(data, {})

    async def test_extract_detailed_data_twitter_url(self):
        # Initialize with a session manager
        session_manager = SessionManager()
        engine = ExtractionEngine(session_manager=session_manager)
        engine.fetch_page_content = AsyncMock(return_value="Test content")

        data = await engine.extract_detailed_data("https://twitter.com/user")
        self.assertEqual(data["raw_content"], "Test content")
        self.assertEqual(data["url"], "https://twitter.com/user")
        self.assertEqual(data["source_type"], "social")

if __name__ == "__main__":
    unittest.main()