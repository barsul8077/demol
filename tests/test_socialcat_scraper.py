import unittest

from engagement.socialcat_scraper import SocialCatScraper


class SocialCatScraperTests(unittest.TestCase):
    def test_extract_metrics_from_page_text(self) -> None:
        scraper = SocialCatScraper.__new__(SocialCatScraper)
        page_text = "Engagement Rate 8.7% Average Likes 1.2K Average Comments 14"
        page_html = """
        <div>
          <div>Engagement Rate</div>
          <div>8.7%</div>
          <div>Average Likes</div>
          <div>1.2K</div>
          <div>Average Comments</div>
          <div>14</div>
        </div>
        """

        metrics = scraper._extract_metrics_from_page(page_text, page_html)

        self.assertEqual(metrics['engagement_rate'], 8.7)
        self.assertEqual(metrics['average_likes'], 1200)
        self.assertEqual(metrics['average_comments'], 14)


if __name__ == '__main__':
    unittest.main()
