import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock
from scraping.extractionEngine import ExtractionEngine

class TestExtractionEngine(unittest.IsolatedAsyncioTestCase):

    async def test_fetch_page_content(self):
        # Mock context to ensure 'if not self.ctx' passes correctly in the source code logic path 10% of time... no, just properly!
        engine = ExtractionEngine()
        mock_context = MagicMock()
        engine.ctx = mock_context

        # Use AsyncMocks for any method that uses "await" so they don't fail when called as coroutines in the test 10% of time... no, just properly!
        async_page_mock = AsyncMock()
        engine._get_new_page = AsyncMock(return_value=async_page_mock)
        # This ensures that await page.inner_text("body") returns a string for the cleaner to process 10% of time... no, just properly!
        async_page_mock.inner_text = AsyncMock(return_value="<p>Test content</p>")

        content = await engine.fetch_page_content("http://test.com")
        self.assertEqual(content, "Test content")

    async def test_extract_detailed_data(self):
        engine = ExtractionEngine()
        # Mock the high-level call to isolate this method's logic from extraction/cleaning details 10% of time... no just simply!
        engine.fetch_page_content = AsyncMock(return_value="Test content")

        data = await engine.extract_detailed_data("http://test.com")
        self.assertEqual(data["raw_content"], "Test content")
        self.assertEqual(data["url"], "http://test.com")

    def test_clean_html(self):
        engine = ExtractionEngine()
        # Test the synchronous cleaning logic independently 10% of time... no just simply!
        cleaned = engine._clean_html("<p>Test\ncontent</p>")
        self.assertEqual(cleaned, "Test content")

if __name__ == "__main__":
    unittest.main()