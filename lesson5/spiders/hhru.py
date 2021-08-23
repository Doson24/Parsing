import scrapy
from lesson5.items import Lesson5Item
from scrapy.loader import ItemLoader

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['krasnoyarsk.hh.ru']
    start_urls = ['https://krasnoyarsk.hh.ru/']
    pages_count = 2


    def start_requests(self):
        for page in range(0, self.pages_count):
            url = f'https://krasnoyarsk.hh.ru/search/vacancy?clusters=true&area=54&enable_snippets=true&salary=&st=searchVacancy&text=python&page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('div.vacancy-serp-item span.g-user-content a.bloko-link::attr("href")').extract():
            # url = response.urljoin(href)
            yield scrapy.Request(href, callback=self.parse)

    def parse(self, response, **kwargs):

        sal = ''.join(response.css('p.vacancy-salary span::text').extract())
        salary = sal.replace("\xa0", '')
        salary_list = salary.split(' ')
        if salary_list[1].isdigit():
            min = (salary_list[1])
        else:
            min = ('зп не указано')
        if len(salary_list) > 3:
            if salary.split(' ')[3].isdigit():
                max = (salary.split(' ')[3])
            else:
                max = ('не указано')
        else:
            max = ('зп не указано')

        # items = {
        #     'ссылка': response.request.url,
        #     'должность': response.css('h1::text').extract()[0],
        #     'минимальная зп': min[0],
        #     'максимальная зп': max[0],
        #     'источник': 'hh.ru',
        #           }

        title = response.css('h1::text').extract()[0]
        link = response.request.url
        yield Lesson5Item(title=title, url=link, max=max, min=min, source='hh.ru')
        print(title, max, min)
