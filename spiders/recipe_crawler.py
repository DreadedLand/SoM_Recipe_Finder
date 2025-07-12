# can use scrapy or BeautifulSoup
# this can only scrape html websites
# for javascript websites I can use selenium but too much work
import sqlite3
import scrapy
import re

from urllib.parse import urlparse

from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from twisted.internet.defer import Deferred

from parsers._parse_dx import get_recipe_data
from parsers._parse_dx import DOMAINS
from parsers._version import __version__

skip_words = [
    # "top", "best", "roundup", "list", "collection", "gallery", "deals", "author",
    "news", "trends", "celebrity", "grocery", "tips", "cuisine", "everyday", "magazine", "youtube",
    "snapchat", "facebook", "watch", "video", "article", "about", "story", "archive"
]

# USE REGEX PATTERN TO CRAWL BLOGS ONLY.
class RecipeSpider(scrapy.Spider):
    custom_settings = {
        "DEPTH_LIMIT": 3,
        "CLOSESPIDER_PAGECOUNT": 60,  # how many websites the spider should scrape before closing
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS": 7,
        "ROBOTSTXT_OBEY": False,
        "USER_AGENT": f"Mozilla/5.0 (compatible; WINDOWS NT 10.0; Win64; x64; rv:{__version__}) spiders/{__version__}",  # avoid bot
        "DEPTH_PRIORITY": 1,
        "SCHEDULER_DISK_QUEUE": "scrapy.squeues.PickleFifoDiskQueue",
        "SCHEDULER_MEMORY_QUEUE": "scrapy.squeues.FifoMemoryQueue",
        "LOG_LEVEL": "DEBUG",
        "REDIRECT_ENABLED": True
    }

    name = "recipe_crawler"
    # seed urls:
    start_urls = [
        "https://www.allrecipes.com",
        "https://www.foodnetwork.com",
        # "https://www.food.com", uses javascript (ew)
        # "https://www.seriouseats.com", logic not implemented yet
        "https://www.bonappetit.com",
        "https://www.epicurious.com"
    ]

    def __init__(self):
        self.conn = sqlite3.connect("../recipes.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('DROP TABLE IF EXISTS recipes')
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS recipes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        ingredients TEXT,
                        rating TEXT,
                        url TEXT UNIQUE
                    )
                ''')

    def parse(self, response):
        '''shallow = response.meta.get("shallow", 0)  # 0: full, 1: shallow, 2: very shallow, 3: just don't crawl atp
        max_links = max(1, 10 - shallow * 3)  # if shallow, then crawl fewer links fr (help me why doesn't my script js work)
        count = 0'''
        for link in response.css("a::attr(href)").getall():
            # if count >= max_links:
                # break
            if not link or not link.startswith("http"):
                continue

            url = link.lower().strip().split("#")[0]
            parsed = urlparse(url)
            domain = parsed.netloc.replace("www.", "").lower()
            path = parsed.path

            if not any(domain.endswith(site) for site in DOMAINS):
                continue

            for site, (func, recipe_pattern, blog_pattern) in DOMAINS.items():
                if domain.endswith(site):
                    if re.fullmatch(recipe_pattern, path):
                        self.log(f"Following recipe link: {url}")
                        yield response.follow(link, self.parseRecipe, dont_filter=True, errback=self.parse_error, priority=10)
                    elif re.search(blog_pattern, path):
                        self.log(f"Crawling through blog link: {url}")
                        yield response.follow(link, self.parse, dont_filter=True)

    def parse_error(self, failure):
        self.log(f"Parse recipe request failed: {failure.value}")

    def parseRecipe(self, response):
        print(">>>>>>>>>>>> ENTERED THE PARSE RECIPE FUNCTION")
        self.log(f"*** ENTERED parseRecipe: {response.url}")
        self.log(f"STATUS CODE: {response.status} for {response.url}")
        self.log(f"Trying to parse recipe from: {response.url}")
        try:
            data = get_recipe_data(response)
            self.log(f"Got data from: {response.url}")
            if not data:
                self.log(f"Skipped: No data found for {response.url}")
                return

            self.log(f"There is data for: {response.url}")

            self.cursor.execute('''
                        INSERT OR IGNORE INTO recipes (title, ingredients, rating, url) VALUES (?, ?, ?, ?)
                    ''', (data["title"], ", ".join(data["ingredients"]), data["rating"], response.url))

            self.log(f"Inserted into db from: {response.url}.")
            self.conn.commit()  # save to db and commit
            self.log(f"Committed db from: {response.url}")

            self.log(f"Saved recipe: {data['title']}\n from {response.url}.")
        except Exception as e:
            self.log(f"Failed parsing {response.url}: {e}")

    def close(self, reason: str) -> Deferred[None] | None:
        self.conn.close()
        self.log(f"Connection closed. Reason {reason}.")


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(RecipeSpider)
    process.start()
