import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtractionEngine:
    def __init__(self, context=None):
        # The "ctx" can be any object that provides page creation/management, allowing us to swap in mocks easily during unit tests.
        self.ctx = context

    async def fetch_page_content(self, url: str) -> str:
        if not self.ctx:
            logger.error("No Playwright context available for fetch_page_content")
            return ""

        # In our DI model, 'self.ctx' is a helper that provides page objects from the shared session/browser manager.
        page = await self._get_new_page()
        try:
            content = await page.inner_text("body")
            return self._clean_html(content)
        except Exception as e:
            logger.error(f"Failed to fetch content from {url}: {e}")
            return ""
        finally:
            await page.close()

    # Extract
    async def extract_detailed_data(self, url: str) -> dict:
        content = await self.fetch_page_content(url)
        if not content:
            return {}

        data = {
            "raw_content": content,
            "url": url,
            "source_type": "social" if "twitter.com/x.com" in url else "generic", 
        }

        return data

    # Refine
    def _clean_html(self, html: str) -> str:
        # Remove non-breaking spaces or other entities that might clutter LLM context
        cleaned = html.replace('\\n', ' ').replace('\n', '').replace('\\r\\n', '') 
        # Collapse multiple whitespaces into one to ensure clean input for the analysis engine
        cleaned = re.sub(r'\\s+', ' ', cleaned).strip()
        return cleaned

    async def _get_new_page(self) -> object:
         """Helper method used by fetch_page_content; logic depends on your specific session manager."""
         pass
