import logging
from OSINTProject.src.utils import filters
from OSINTProject.src.core.session_manager import SessionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtractionEngine:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def fetch_page_content(self, url: str) -> str:
        if not self.session_manager:
            logger.error("No Playwright context available for fetch_page_content")
            return ""

        page = await self.session_manager.get_new_context()

        try:
            content = await page.inner_text("body")
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

