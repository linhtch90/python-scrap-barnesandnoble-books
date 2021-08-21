import scrapy

class BNBooksSpiderHTML(scrapy.Spider):
    name = 'bn_book_spider_html'
    domain = 'https://www.barnesandnoble.com/'
    page_number = 1
    init_url = f'{domain}b/books/travel/_/N-1sZ29Z8q8Z1ary?Nrpp=20&Ns=P_Sales_Rank&page={page_number}'
    book_detail_url = 'https://www.barnesandnoble.com/w/road-trip-usa-jamie-jensen/1102216639;jsessionid=8C5713D058DC661BA7BDD599F4AD74F7.prodny_store01-atgap02?ean=9781640494473'
    start_urls = [
        book_detail_url,
    ]
    next_url = ''
    def parse(self, response):
        file_name = 'crawled_book_detail.html'
        with open(file_name, 'wb') as f:
            f.write(response.body)
