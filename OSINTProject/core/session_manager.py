# core/session_manager.py

import logging
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self):
        self._browser = None
        self._contexts = []

    async def start(self):
        if self._browser is None:
            logger.info("Starting Playwright engine...")
            self._playwright_instance = await async_playwright().start()
            self._browser = await self._playwright_instance.chromium.launch(headless=True)
        return self

    async def close(self):
        if not self._browser:
            pass 

        try: 
            for ctx in list(self._contexts):
                await ctx.close()
            self._contexts = []

            if self._browser:
                await self._browser.close()
            if self._playwright_instance:
                await self.playwright.stop()

        finally:
            if not self._playwright_instance and not self._browser is None and len(self._contexts) > 0:
                logger.info("Shutdown failed, retrying...")
                self._contexts = []
                await self._playwright.stop()
                await self._browser.stop()

    async def get_new_context(self):
        """Creates a new browser context for isolation."""
        if not self._browser:
            raise RuntimeError("Browser not initialized. Call within an async 'with' block.")
        context = await self._browser.new_context()
        self._contexts.append(context)
        return context

    async def close_all_contexts(self):
        """Closes all active contexts to free resources."""
        for ctx in self._contexts:
            await ctx.close()
        self._contexts = []