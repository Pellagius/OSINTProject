import unittest
from OSINTProject.src.scraping.twitterScraper import TwitterScraper

class TestTwitterScraper(unittest.TestCase):

    def test_generate_social_media_variants(self):
        scraper = TwitterScraper()
        variants = scraper.generate_social_media_variants("Joe Bloggs")
        self.assertIn("https://twitter.com/joebloggs", variants)
        self.assertIn("https://twitter.com/joe_bloggs", variants)
        self.assertIn("https://twitter.com/jbloggs", variants)
        self.assertIn("https://twitter.com/joeb", variants)

    def test_identify_source_type(self):
        scraper = TwitterScraper()
        self.assertEqual(scraper.identify_source_type("https://twitter.com/joebloggs"), "social")
        self.assertEqual(scraper.identify_source_type("https://example.com"), "generic")

if __name__ == "__main__":
    unittest.main()