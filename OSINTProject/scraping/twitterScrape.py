import re

class TwitterScraper:
    def __init__(self):
        pass

    @staticmethod
    def generate_social_media_variants(term: str) -> list[str]:
        """
        Generates a set of potential social media URLs based on common naming conventions 
        to ensure high recall across different naming conventions.
        """
        if not term or len(term) < 2:
            return []

        # Basic cleaning and variations for Twitter/X handle logic
        base_clean = "".join(c for c in term if c.isalnum()).lower() # e.g., "Joe Bloggs" -> "joebloggs"
        underscore_variant = term.replace(" ", "_").replace("-", "_")  # e.g., "Joe Bloggs" -> "joe_blogs"

        potential_urls = set()
        if base_clean: 
            potential_urls.add(f"https://twitter.com/{base_clean}")
        if underscore_variant and underscore_variant != base_clean: 
            potential_urls.add(f"https://twitter.com/{underscore_variant}")

        # Additional variants for high-recall discovery (e.g., jdoe, joed)
        parts = [p for p in re.split(r'[\s_-]', term) if p]
        if len(parts) >= 2:
            first_init = parts[0][0].lower()
            last_name = parts[-1].lower()
            # Add "jdoe" style (First initial + last name)
            potential_urls.add(f"https://twitter.com/{first_init}{last_name}")

        if len(parts) >= 2:
             # Adding a variant that joins the first part with only the last character of second word/part if it exists (e.g., joed)
            full_first = parts[0].lower()
            try:
                last_init = parts[-1][0] # This is safe because we checked len(parts)>=2 and filters out empty strings above
                potential_urls.add(f"https://twitter.com/{full_first}{last_init}")
            except IndexError: 
                 pass

        return list(potential_urls)

    @staticmethod
    def identify_source_type(url: str) -> str:
        """Determines the type of content based on its URL structure."""
        if "twitter.com/x.com" in url or "twitter.com/" in url: 
            return "social"
        return "generic"

# Support for legacy-style calls during transition, primarily used by modules requiring specific Twitter handling.
def discover_twitter(term: str) -> list[dict]:
    import logging # Ensure logger is available if called directly as a standalone function
    logger = logging.getLogger(__name__)

    logger.info(f"Performing discovery for social media terms (Twitter/X): {term}")
    potential_urls = TwitterScraper.generate_social_media_variants(term)

    results = []
    for url in potential_urls:
        results.append({
            "url": url,
            "source_type": "social",
            "platform": "x_twitter", # Specific identifier to help downstream logic select correct parsers/models later
            "confidence_score": 1.0  # Placeholder for pre-fetch validation check before full extraction pipeline starts
        })

    return results