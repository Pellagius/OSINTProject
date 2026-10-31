import logging
from typing import List
from playwright.async_api import async_playwright, Browser, BrowserContext

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages the Playwright browser lifecycle and multiple execution contexts."""
    def __init__(self) -> None:
        self._playwright_context: (async_playwright.Playwright | None) = None
        self.browser: Browser | None = None
        self._contexts: List[BrowserContext] = []

    async def __aenter__(self) -> "SessionManager":
        logger.info("Initializing Playwright context.")
        self._playwright_context = await async_playwright().start()
        try:
            self.browser = await self._playwright_context.chromium.launch(headless=True)
            return self
        except Exception as e:
            logger.error(f"Failed to launch browser: {e}")
            if self._playwright_context:
                await self._playwright_context.stop()
            raise

    async def __aexit__(self, exc_type: any, exc_val: any, exc_tb: any) -> None:
        """Cleans up the browser and Playwright context."""
        if self.browser:
            await self.browser.close()
        if self._playwright_context:
            await self._playwright_context.stop()

    async def get_new_context(self) -> BrowserContext:
        """Creates a new browser context and adds it to the internal tracking list."""
        if not self.browser:
            raise RuntimeError("Browser not initialized. Call within an async 'with' block.")

        context = await self.browser.new_context()
        self._contexts.append(context)
        return context

    async def close_all_contexts(self) -> None:
        """Closes all managed contexts and clears the internal list."""
        for ctx in self._contexts:
            await ctx.close()
        self._contexts.clear()
