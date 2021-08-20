import scrapy

class BNBooksSpiderHTML(scrapy.Spider):
    name = 'bn_book_spider_html'
    domain = 'https://www.barnesandnoble.com/'
    page_number = 1
    init_url = f'{domain}b/books/travel/_/N-1sZ29Z8q8Z1ary?Nrpp=20&Ns=P_Sales_Rank&page={page_number}'
    start_urls = [
        init_url,
    ]
    next_url = ''
    def parse(self, response):
        print('*** This is parse function ***')
        file_name = 'crawled_html.html'
        with open(file_name, 'wb') as f:
            f.write(response.body)
