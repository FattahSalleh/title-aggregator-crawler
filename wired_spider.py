import scrapy
import json


class WiredSpider(scrapy.Spider):
    name = "wired"
    start_urls = [
        "https://www.wired.com/",
    ]
    url_prefix = "https://www.wired.com"

    def __init__(self):
        super().__init__()
        self.articles = []

    def parse(self, response):
        for article in response.css("div.summary-item__content"):
            title = article.css("a.summary-item-tracking__hed-link > ::text").get()
            url = article.css("a.summary-item-tracking__hed-link::attr(href)").get()

            if title and url:
                # Check if the URL already starts with the prefix
                if not url.startswith(self.url_prefix):
                    # If not, add prefix to the URL
                    url = self.url_prefix + url

                # Follow the article URL to extract the published date
                yield scrapy.Request(
                    url, callback=self.parse_article, meta={"title": title, "url": url}
                )
            else:
                print("URL or title not found")

    def parse_article(self, response):
        title = response.meta["title"]
        url = response.meta["url"]
        publication_date = response.css(
            "time[data-testid='ContentHeaderPublishDate']::attr(datetime)"
        ).get()

        if publication_date:
            self.articles.append(
                {"title": title, "url": url, "publication_date": publication_date}
            )
        else:
            print("Published date not found for article:", title)

        # Save scraped data to a JSON file
        with open("wired_articles.json", "w") as f:
            json.dump(self.articles, f, indent=4)
