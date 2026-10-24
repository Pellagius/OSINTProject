import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtractionEngine:
    def __init__(self, session_manager):
        self.session_manager = session_manager

    async def fetch_page_content(self, url: str) -> str:
        if not self.session_manager:
            logger.error("No Playwright context available for fetch_page_content")
            return ""

        page = await self.session_manager.get_new_page()
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
        cleaned = html.replace('\\n', ' ').replace('\\n', '').replace('\\r\\n', '')
        cleaned = re.sub(r'<[^<]+?>', '', cleaned) 
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned	

