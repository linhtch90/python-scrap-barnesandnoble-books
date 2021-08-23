import scrapy
import random


class BNBooksSpider(scrapy.Spider):
    name = "bn_book_spider"
    domain = "https://www.barnesandnoble.com"
    page_number = 1
    init_url = f"{domain}/b/books/travel/_/N-1sZ29Z8q8Z1ary?Nrpp=20&Ns=P_Sales_Rank&page={page_number}"
    next_url = ""
    start_urls = [
        init_url,
    ]

    book_titles = ''
    book_image_urls = ''
    book_detail_urls = ''
    book_authors = ''
    book_prices = ''
    global_index = 0

    def parse(self, response):
        css_book_title = "div.product-shelf-image a.pImageLink::attr(title)"
        css_book_image = "div.product-shelf-image a.pImageLink img.full-shadow:not(.Resolve.lp-lazy)::attr(src)"
        css_book_detail = "div.product-shelf-image a.pImageLink::attr(href)"
        css_book_author = "div.product-shelf-author.pt-0 a::text"
        css_book_price = "div.quick-add a.btn-quick-add::attr(data-price)"

        self.book_titles = response.css(css_book_title).getall()
        self.book_image_urls = response.css(css_book_image).getall()
        self.book_detail_urls = response.css(css_book_detail).getall()
        self.book_authors = response.css(css_book_author).getall()
        self.book_prices = response.css(css_book_price).getall()

        # Remove last 4 zero chars from book price
        for i in range(len(self.book_prices)):
            price = str(self.book_prices[i])
            self.book_prices[i] = price[: len(price) - 4]

        # Yield data
        for i in range(len(self.book_titles)):
            book_detail_url = f'{self.domain}{self.book_detail_urls[i]}'
            print(book_detail_url)

            # yield {
            #     "title": self.book_titles[i],
            #     "author": self.book_authors[i],
            #     "price": self.book_prices[i],
            #     "image_src": self.book_image_urls[i],
            #     "book_detail_src": f"https://www.barnesandnoble.com{self.book_detail_urls[i]}",                
            # }

            yield scrapy.Request(url=book_detail_url, callback=self.book_detail_parse)            

        # Move to next page - for testing with limited number of pages
        # self.page_number += 1
        # max_page_number = 2
        # if self.page_number < max_page_number:
        #     self.next_url = f'{self.domain}/b/books/travel/_/N-1sZ29Z8q8Z1ary?Nrpp=20&Ns=P_Sales_Rank&page={self.page_number}'
        #     yield scrapy.Request(self.next_url, callback=self.parse)

        # Move till the last page
        css_next_page = "li.pagination__next a.next-button::attr(href)"
        next_page = response.css(css_next_page).get()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse)
    
    def book_detail_parse(self, response):
        css_isbn_13 = 'div#ProductDetailsTab table.plain.centered tbody tr:nth-child(1) td::text'
        css_publisher = 'div#ProductDetailsTab table.plain.centered tbody tr:nth-child(2) td a span::text'
        css_publish_date = 'div#ProductDetailsTab table.plain.centered tbody tr:nth-child(3) td::text'
        css_pages = 'div#ProductDetailsTab table.plain.centered tbody tr:nth-child(6) td::text'

        book_isbn_13 = response.css(css_isbn_13).get()
        book_publisher = response.css(css_publisher).get()
        book_publish_date = response.css(css_publish_date).get()
        book_pages = response.css(css_pages).get()        

        if self.global_index < 12:
            try:
                int(book_pages)
            except:
                book_pages = random.randint(200, 1500)

            yield {
                "title": self.book_titles[self.global_index],
                "author": self.book_authors[self.global_index],
                "price": float(self.book_prices[self.global_index]),
                "image_src": self.book_image_urls[self.global_index],
                "book_detail_src": f"https://www.barnesandnoble.com{self.book_detail_urls[self.global_index]}",
                "isbn_13": book_isbn_13,
                "publisher": book_publisher,
                "publish_date": book_publish_date,
                "pages": int(book_pages),                
            }
            
            if self.global_index == 11:
                self.global_index = 0
            else:
                self.global_index += 1
