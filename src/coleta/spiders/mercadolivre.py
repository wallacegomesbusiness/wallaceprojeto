import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]

    def parse(self, response):
        products = response.css('div.ui-search-result__content') # 54 itens

        for produto in products:
            prices = produto.css('span.andes-money-amount__fraction::text').getall()
            cents = produto.css('span.andes-money-amount__cents::text').getall()
            
            yield {
            'brand': produto.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
            'name': produto.css('h2.ui-search-item__title::text').get(),
            'old_prices_reais': prices[0] if len(prices) > 0 else None,
            'old_prices_centavos': cents[0] if len(cents) > 0 else None,
            'new_prices_reais': prices[1] if len(prices) > 1 else None,
            'new_prices_centavos': cents[1] if len(cents) > 1 else None,
            'reviews_rating_number': produto.css('span.ui-search-reviews__rating-number::text').get(),
            'reviews_amount': produto.css('span.ui-search-reviews__amount::text').get()
            }