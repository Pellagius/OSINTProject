import logging
from src.api.models import SearchRequest
from src.scraping.twitterScraper import TwitterScraper
from src.core.session_manager import SessionManager
from src.utils.filters import filter_high_value

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscoveryEngine:
    def __init__(self, session_manager: SessionManager, twitter_scraper: TwitterScraper = TwitterScraper()):
        self._session_manager = session_manager
        self._twitter_scraper = twitter_scraper

    async def discover_sources(self, request: SearchRequest) -> list[dict]:
        results = []
        logger.info(f"Performing discovery for: {request.subject_name} in {request.location}")
        findings = await self._perform_multi_platform_search(request.subject_name)
        results.extend(findings)

        # Deduplicate and filter high-value targets
        results = filter_high_value(results)
        
        unique_results = {res['url']: res for res in results if 'url' in res}.values()
        return list(unique_results) 

    async def _perform_multi_platform_search(self, term: str) -> list[dict]:
        results = []

        # Step 1: Check social media providers specifically first as requested
        social_media_findings = await self._discover_social_media(term)
        results.extend(social_media_findings)

        # Step 2: Broad web search for general results (e.g., news, blogs, official pages)
        web_search_findings = await self._perform_general_web_discovery(term)
        results.extend(web_search_findings)

        return results

    async def _perform_general_web_discovery(self, term: str) -> list[dict]:
        logger.info(f"Performing broader web discovery for terms related to: {term}")

        results = []
        try:
            raw_links = await self._fetch_serp_data(term) 
            logger.info("SERP Fetch complete.")
            for link in raw_links:
                if "sponsored" not in link['title'].lower() and "ad" not in link['url'].lower():
                    results.append({
                        "url": link["url"],
			            "source_type": "web",
                        "confidence_score": 1.0  # Preliminary score before detailed analysis/me    ing by LLM logic
                    })
        except Exception as e:
            logger.error(f"Failed to perform broader web discovery for {term}: {e}")

        return list({res['url']: res for res in results if 'url' in res}.values())

    async def _fetch_serp_data(self, term: str) -> list[dict]:
        logger.info(f"Fetching SERP context for: {term}")
        
        context = await self._session_manager.get_new_context()
        page = await context.new_page()
        try:
            logger.info(f"Fetching SERP data for: {term}")
            print(f"search url: https://www.google.com/search?q={term}")
            await page.goto(f"https://www.google.com/search?q={term}")
            
            await page.wait_for_selector("div.g")

            results = await page.eval_on_selector_all("div.g", "elements => elements.map(el => ({url: el.querySelector('a')?.href || '', title: el.querySelector('h3')?.innerText || ''}))")
            
            return results
        except Exception as e:
            logger.error(f"Failed to fetch SERP data for {term}: {e}")
            return []
        finally:
            await page.close()

    async def _discover_social_media(self, term: str) -> list[dict]:
        logger.info(f"Searching specifically across social media platform types for: {term}")
        results = []
    
        if not term or len(term) < 2:
            return []

        potential_urls = self._twitter_scraper.generate_social_media_variants(term)
        for url in potential_urls:
            results.append({
                "url": url,
                "source_type": "social",
                "platform": "x_twitter",
                "confidence_score": 1.0
            })

        return results