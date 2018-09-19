from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

   # url = "https://www.google.co.in/search?q="+word+"&oq="+word+"&aqs=chrome.0.69i59.8573j1j8&sourceid=chrome&ie=UTF-8"

# class ElectronicsSpider(CrawlSpider):
#         name = "electronics"
#         allowed_domains = ["www.olx.com.pk"]
#         start_urls = [
#             "https://www.google.co.in/search?q="+"quora"+"&oq="+"quora"+"&aqs=chrome.0.69i59.8573j1j8&sourceid=chrome&ie=UTF-8",
#
#         ]
#
#
#
#         def parse_item(self, response):
#             print('Processing..' + response.url)
#             print(response.body)
import requests
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

url = "https://www.google.co.in/search?q="+"quora"+"&oq="+"quora"+"&aqs=chrome.0.69i59.8573j1j8&sourceid=chrome&ie=UTF-8"
r=requests.get(url,headers=headers)
print(r.text)