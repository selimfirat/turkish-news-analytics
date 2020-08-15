import scrapy
from scrapy import Request
from datetime import datetime

from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule
import datetime

from news_entry import NewsEntry
from newsplease import NewsPlease
import tldextract

class NewsSpider(scrapy.Spider):

    name = "news"
    custom_settings = {
        "ITEM_PIPELINES": {
            'data_store_pipeline.DataStorePipeline': 300,
        }
    }

    start_urls = []
    allowed_domains = []

    targets = [
        "http://aa.com.tr/",
        "https://www.ajanshaber.com/",
        "https://www.yenisafak.com/",
        "http://www.turkiyegazetesi.com.tr/",
        "http://www.star.com.tr/"
        "https://www.ulusal.com.tr/",
        "https://odatv.com/",
        "http://www.oncevatan.com.tr/",
        "http://sol.org.tr/",
        "http://www.internethaber.com/",
        "https://www.cnnturk.com/",
        "https://www.sozcu.com.tr/",
        "http://www.ensonhaber.com/",
        "http://www.yenicaggazetesi.com.tr/",
        "http://www.oncevatan.com.tr/",
        "https://tr.sputniknews.com/",
        "http://www.internethaber.com/",
        "https://www.cnnturk.com"
    ]

    def __init__(self, target=None, *args, **kwargs):
        if target is not None:
            targets = [target]

        for target in self.targets:
            ext = tldextract.extract(target)
            domain = '{uri.domain}.{uri.suffix}'.format(uri=ext)


            self.allowed_domains.append(domain)
            self.start_urls.append(target)

        super(NewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        now = datetime.datetime.now()

        article = NewsPlease.from_html(response.text, response.url)
        if article.date_publish is not None and article.text is not None:
            yield NewsEntry(
                full_url=response.url,
                source_domain = article.source_domain,
                date_publish = article.date_publish,
                date_download = str(now),
                title = article.title,
                description = article.description,
                text = article.text,
            #    dont_filter=True
            )

        for link in LxmlLinkExtractor(allow=self.allowed_domains).extract_links(response):
            yield Request(link.url, self.parse)
