import scrapy
from lesson5.items import Lesson5Item
from scrapy.loader import ItemLoader

class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['krasnoyarsk.leroymerlin.ru']
    start_urls = ['http://krasnoyarsk.leroymerlin.ru/']
    # num_page = range(1, 3)
    num_page = 4

    # def count_pages(self, response):
    #     количество страниц
    #     a = response.css('div a').xpath('@data-qa-pagination-item').getall()
    #     self.num_page = a

    def start_requests(self, **kwargs):


        for page in range(1, self.num_page +1):
            url = f"https://krasnoyarsk.leroymerlin.ru/catalogue/potolochnye-svetodiodnye-svetilniki/?21514=30~&22088=Потолочная+люстра&02419=Hi+-+Tech&03160=Управление+яркостью+освещения&page={page}"
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('div.phytpj4_plp a::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)


    def parse(self, response,**kwargs):
        link = response.request.url
        l = ItemLoader(item=Lesson5Item(), response=response)
        l.add_xpath('name', "//h1/text()")
        l.add_xpath('terms', "//dt/text()")
        l.add_xpath('definitions', "//dd/text()")
        # p = response.xpath("//meta[@itemprop='price']/@content")[0]
        # l.add_value('price', p)
        l.add_xpath('price', "//meta[@itemprop='price']/@content")
        l.add_xpath('photos', "//source[@media=' only screen and (min-width: 1024px)']/@srcset")
        l.add_value('link', link)
        p = l.load_item()
        # print(p)
        return p
        # yield Lesson5Item(url=link)
