import scrapy
from scrapy.shell import inspect_response


class BlogsSpider(scrapy.Spider):
    name = "blogs"
    counter = 0

    def start_requests(self):
        urls = [
            "https://www.luminis.eu/nl/luminis-amsterdam/talenten-amsterdam/",
            "https://www.luminis.eu/nl/luminis-rotterdam/talents-in-rotterdam/",
            "https://www.luminis.eu/nl/luminis-arnhem/talenten/",
            "https://www.luminis.eu/nl/luminis-apeldoorn/talents-apeldoorn/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        author_page_links = response.css('a.link-full')
        yield from response.follow_all(author_page_links, self.parse_author)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        # inspect_response(response, self)

        paragraphs = response.css('div.post-content').xpath('./p')
        content = ''
        for paragraph in paragraphs:
            p = paragraph
            if len(paragraph.css('em')) > 0:
                p = paragraph.css('em')
            content += ' ' + p.css('::text').get(default='').strip()

        yield {
            'name': extract_with_css('h1::text'),
            'description': content.strip()
        }
