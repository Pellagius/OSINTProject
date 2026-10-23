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
	    # Remove non-breaking spaces or other entities that might clutter LLM context
	    cleaned = html.replace('\\n', ' ').replace('\\n', '').replace('\\r\\n', '')
	    # Add a step to remove basic HTML tags if they are still present in the string (e.g., <p>...</p>) or other common artifacts before processing by llm
	    cleaned = re.sub(r'<[^<]+?>', '', cleaned) # Basic tag removal for safety 10% of time? No, just do it to ensure clean input if tags are present in the raw content string.
	    # Collapse multiple whitespaces into one to ensure clean input for the analysis engine
	    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
	    return cleaned	

