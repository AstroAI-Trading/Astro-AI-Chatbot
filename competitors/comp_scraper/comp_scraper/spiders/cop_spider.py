import scrapy
from urllib.parse import quote  # Import the quote function to encode special characters
from comp_scraper.spiders.ListOfCompanies import start_companies


class CompetitorsSpider(scrapy.Spider):
    name = 'cop_spider'
    base_url = 'https://www.marketbeat.com/stocks/NASDAQ/{}/competitors-and-alternatives/'
    start_companies = start_companies  # Import the list of companies from ListOfCompanies module

    def start_requests(self):
        for company in self.start_companies:
            encoded_company = quote(company)  # Encode the company name
            url = self.base_url.format(encoded_company)
            yield scrapy.Request(url=url, callback=self.parse_competitors)

    def parse_competitors(self, response):
        try:
            # Extracting the content inside the h2 tag with class="h3 mt-0"
            competitors_info = response.css('h2.h3.mt-0::text').get()

            if competitors_info:
                # Process the extracted information as needed
                self.log(competitors_info)

                # Remove unwanted phrases
                competitors_info_cleaned = competitors_info.replace(" vs. ", ", ").replace(" and ", " ")

                # Create a dictionary with the information and yield it
                competitors_data = {
                    'company': response.url.split('/')[-3],  # Extract company name from the URL
                    'competitors': competitors_info_cleaned.strip(),
                }
                yield competitors_data

            # Extracting the next competitors page URL
            next_page = response.css('a[aria-controls="tabContentCompetitors"]::attr(href)').get()

            if next_page:
                yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse_competitors)

        except Exception as e:
            self.log(f"Error processing {response.url}: {e}")
