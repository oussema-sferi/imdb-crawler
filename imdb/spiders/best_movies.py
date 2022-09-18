import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    
    # link for Thriller movies
    # start_urls = ['']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?genres=thriller&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=5CYKHKCH0RXGE3J9XFX3&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_3', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"), process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        #
        yield {
            'title': response.xpath("//div[@class='sc-80d4314-1 fbQftq']/h1/text()").get(),
            'year': response.xpath("//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt']/li[1]/a/text()").get(),
            # 'duration': response.xpath("//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt']/li[3]/text()[1]").get(),
            'genre': response.xpath("//div[@class='ipc-chip-list--baseAlt ipc-chip-list sc-16ede01-4 bMBIRz']/div[2]/a/span/text()").get(),
            'rating': response.xpath("(//span[@class='sc-7ab21ed2-1 jGRxWM'])[1]/text()").get(),
            'movie_url': response.url,
            #'user_agent': response.request.headers['User-Agent']
        }
