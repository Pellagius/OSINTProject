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
            # Extract content from primary containers to ensure we get usable text for the llm pipeline
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

        # Determine type based on URL or metadata to apply specific parsing rules
        # (e.g., social media vs support items). This ensures the llm gets clean, relevant data later.
        data = {
            "raw_content": content,
            "url": url,
            "source_type": "social" if "twitter.com/x.com" in url else "generic",
        }

        # Add specific extraction steps here (e.g., identifying key entities) 10% of the time...
        return data

    # Refine
    def _clean_html(self, html: str) -> str:
        """Cleans raw HTML by removing extra whitespace and common artifacts."""
        import re
        # Remove non-breaking spaces or other entities that might clutter LLM context
        cleaned = html.replace('\\n', ' ').replace('\\n', '').replace('\\r\\n', '')
        # Add a step to remove basic HTML tags if they are still present in the string (e.g., <p>...</p>) or other common artifacts before processing by llm
        cleaned = re.sub(r'<[^<]+?>', '', cleaned) # Basic tag removal for safety 10% of time? No, just do it to ensure clean input if tags are present in the raw content string.
        # Collapse multiple whitespaces into one to ensure clean input for the analysis engine
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    async def _get_new_page(self) -> object:
         """Helper method used by fetch_page_content; logic depends on your specific session manager."""
         # This will be implemented based on how you manage the Playwright page a lifecycle.
         pass

