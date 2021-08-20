import scrapy

class BNBooksSpider(scrapy.Spider):
    name = 'bn_book_spider'
    domain = 'https://www.barnesandnoble.com/'
    page_number = 1
    init_url = f'{domain}b/books/travel/_/N-1sZ29Z8q8Z1ary?Nrpp=20&Ns=P_Sales_Rank&page={page_number}'
    start_urls = [
        init_url,
    ]
    next_url = ''
    
    def parse(self, response):
        print('*** This is parse function ***')
        
        css_book_title = 'div.product-shelf-image a.pImageLink::attr(title)'
        css_book_image = 'div.product-shelf-image a.pImageLink img.full-shadow:not(.Resolve.lp-lazy)::attr(src)'
        css_book_detail = 'div.product-shelf-image a.pImageLink::attr(href)'
        css_book_author = 'div.product-shelf-author.pt-0 a::text'
        css_book_price = 'div.quick-add a.btn-quick-add::attr(data-price)'
        
        book_titles = response.css(css_book_title).getall()
        book_image_urls = response.css(css_book_image).getall()
        book_detail_urls = response.css(css_book_detail).getall()
        book_authors = response.css(css_book_author).getall()
        book_prices = response.css(css_book_price).getall()

        # Remove last 4 zero chars from book price
        for i in range(len(book_prices)):
            price = str(book_prices[i])
            book_prices[i] = price[:len(price) - 4]

        # Yield data
        for i in range(len(book_titles)):
            yield {
                'title': book_titles[i],
                'author': book_authors[i],
                'price': book_prices[i],
                'image_src': book_image_urls[i],
                'book_detail_src': f'{self.domain}{book_detail_urls[i]}', 
            }

        # Move to next page
        self.page_number += 1
        if self.page_number < 12:
            self.next_url = f'{self.domain}b/books/travel/_/N-1sZ29Z8q8Z1ary?Nrpp=20&Ns=P_Sales_Rank&page={self.page_number}'
            yield scrapy.Request(self.next_url, callback=self.parse)
            
        
        
       

    
    

