from scrapy.item import Item, Field


class NewsEntry(Item):
    full_url = Field()
    source_domain = Field()
    date_publish = Field()
    title = Field()
    description = Field()
    date_download = Field()
    text = Field()