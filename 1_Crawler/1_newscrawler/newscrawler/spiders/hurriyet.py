from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class HurriyetSpider(CrawlSpider):
    name = "hurriyet"
    allowed_domains = ["hurriyet.com.tr"]
    collection_name = 'hurriyet'

    def __init__(self, *args, **kwargs):
        super(HurriyetSpider, self).__init__(*args, **kwargs)
       # begin_date = pd.Timestamp(yearmonth + "-01")
       # end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
       # date_inds  = [d.date().isoformat().replace("-","") for d in pd.date_range(begin_date,end_date)]
        urls = ["http://www.hurriyet.com.tr/arama/#/?page=%s" % d for d in range(1,230)]
        start_url = []
        for links in urls:
            start_url.append(links+"&key=yapay%20zeka&where=/&how=Article,Column&platform=/&isDetail=false")
	self.start_urls = start_url
        rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="news"]/div[@class="desc"]//a',)), callback="parse_items", follow= False),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="special-author-loop author-items"]/div[@class="author"]//a',)), callback="parse_items", follow= False),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="paging"]/a',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        new_content = hxs.xpath("//div[@class='news-box']/p/text()").extract()
        if new_content:
            yield self.parse_news(response)
        else:
            yield self.parse_column(response)

    def parse_news(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "tr"
        item["source"] = "hurriyet"
        category     = hxs.xpath("//div[@class='col-md-12']/div[@class='breadcrumb-body clr']/span//text()").extract()
        author       = hxs.xpath("//div[@class='author-info-content']/div[@class='name']//a/text()").extract()
        date_time    = hxs.xpath("//span[@class='modify-date']/text()").extract()
        item["author"]   = '|'.join(author)
        title            = hxs.xpath("//h1[@class='news-detail-title selectionShareable']/text()").extract()
        intro            = hxs.xpath("//div[@class='news-detail-spot news-detail-spot-margin']/h2/text()").extract()
        new_content      = hxs.xpath("//div[@class='news-box']/p/text()").extract()
        #
        # Processing outputs
        item["intro"]      = ' '.join(intro)
        item["title"]      = ' '.join(title)
        new_content        = ' '.join(new_content)
        new_content        = re.sub('\n',' ',new_content)
        item["content"]    = re.sub('\s{2,}',' ',new_content)
        category           = category[1:-1]
        category           = [c for c in category if not c==">"]
        item["category"]   = '|'.join(category)
        item["date_time"]  = " ".join(date_time)
        return(item)

    
    def parse_column(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"]         = response.request.url
        item["lang"]        = "tr"
        item["source"]    = "hurriyet"
        category             = ["koseyazisi"]
        date_time           = hxs.xpath("//div[@class='article-date']/text()").extract()
        author                = hxs.xpath("//div[@class='author-info-content']/div[@class='name']//a/text()").extract()
        title                     = hxs.xpath("//h1[@class='article-title']/text()").extract()
        intro                    = hxs.xpath("//div[@class='article-content news-description']/p/text()").extract()
        new_content       = hxs.xpath("//div[@class='article-content news-text']/p/text()").extract()
        new_content         = ' '.join(new_content)
        new_content         = re.sub('\n',' ',new_content)
        if not new_content:
            new_content       = hxs.xpath("//div[@class='article-content news-text']//text()").extract()
            new_content         = ' '.join(new_content)
            new_content         = re.sub('\n',' ',new_content)

        #
        # Processing outputs
        item["intro"]      = ' '.join(intro)
        item["title"]           = ' '.join(title)
        item["content"]     = re.sub('\s{2,}',' ',new_content)
        item["category"]    = '|'.join(category)
        item["date_time"]  = " ".join(date_time)
        item["author"]       = " ".join(author)
        return(item)


