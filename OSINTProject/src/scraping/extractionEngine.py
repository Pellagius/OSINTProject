import logging
from src.utils import filters
from src.core.session_manager import SessionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtractionEngine:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def fetch_page_content(self, url: str) -> str:
        if not self.session_manager:
            logger.error("No Playwright context available for fetch_page_content")
            return ""

        context = await self.session_manager.get_new_context()
        page = await context.new_page()

        try:
            content = await page.inner_text("body")
            print(f"Fetched content from {url}: {content[:100]}...")  
            return filters.clean_html(content)
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
            "source_type": "social" if "twitter.com" in url else "generic",
        }

        return data

