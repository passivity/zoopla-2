from csv import DictWriter

import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse
import pkgutil

h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 "
    "Safari/537.1"
}

t = 0


class ZooplaSpider(scrapy.Spider):
    name = "zoopla"

    def start_requests(self):
        data = pkgutil.get_data("zoopla", "resources/TS All addresses Updated 08 April_1.txt")

        for line in data.decode("utf-8").splitlines():
            try:
                yield scrapy.Request(url=line.rstrip(), headers=h, callback=self.parse)
            except Exception as e:
                self.log(f"{line.rstrip()} failed - {e.__cause__ or e} ({type(e)})")

    def parse(self, response: HtmlResponse, **kwargs):
        if response.status == 200:
            html = BeautifulSoup(response.text, "html.parser")

            listing_tag = html.find("span", {"data-testid": "listing-tag"})
            sale_description = list(listing_tag.parent.children)[-1]

            if listing_tag.text in ("Currently For Sale", "Currently For Rent") and sale_description.children:
                links = map(
                    lambda x: "https://www.zoopla.co.uk" + x["href"],
                    sale_description.find_all("a"),
                )

                if links:
                    title = html.find("h1", class_="ebcgyxg9").text
                    yield {"title": title, "links": "\n".join(list(links))}
            else:
                pass
        else:
            pass
