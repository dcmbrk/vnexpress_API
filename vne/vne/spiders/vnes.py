import scrapy
import json
from vne.items import VneItem
from datetime import datetime

class VnesSpider(scrapy.Spider):
    name = "vnes"
    allowed_domains = ["vnexpress.net"]

    # Danh sách chuyên mục
    CATEGORIES = {
        'Thời Sự': '1001005',
        'Thế giới': '1001002',
        'Kinh doanh': '1003159',
        'Khoa học công nghệ': '1002592',
        'Góc nhìn': '1003450',
        'Bất động sản': '1005628',
        'Sức khỏe': '1003784',
        'Thể thao': '1002568',
        'Giải trí': '1003520',
        'Pháp luật': '1001007',
        'Giáo dục': '1005955',
        'Đời sống': '1005110',
        'Xe': '1005285',
        'Du lịch': '1004402',
        'Ý kiến': '1004528',
        'Tâm sự': '1001014',
        'Thư giãn': '1001011'
    }

    def start_requests(self):
        for name, cid in self.CATEGORIES.items():
            url = self.getUrlByCat(cat_id=cid, limit=1, page=1)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                cb_kwargs={'cat_name': name, 'cat_id': cid}
            )

    def parse(self, response, cat_name, cat_id):
        # Chuyển response JSON sang dict
        data = json.loads(response.text)
        items = data['data'][cat_id]['data']

        for a in items:
            info = self.get_article_info(a, cat_name)
            share_url = a.get('share_url', '')
            yield scrapy.Request(
                url=share_url,
                callback=self.parse_full_article,
                meta=info
            )

    def parse_full_article(self, response):
        item = VneItem()
        item['url'] = response.url
        item['category'] = response.meta['category']
        item['title'] = response.meta['title']
        item['lead'] = response.meta['lead']
        item['date'] = self.get_art_date(response)
        item['main_content'] = response.css('.Normal::text').getall()
        item['author'] = self.get_author(response)
        yield item

    def getUrlByCat(self, cat_id, limit, page):
        return (
            f'https://gw.vnexpress.net/ar/get_rule_1?'
            f'category_id={cat_id}&limit={limit}&page={page}&data_select=title,lead,share_url,publish_time'
        )

    def get_author(self, response):
        authors = response.xpath(
            '//p[@class="Normal" and contains(@style, "text-align:right")]/strong/text()'
        ).getall()
        author = authors[-1].strip() if authors else ''
        if not author:
            author = response.xpath(
                '//article[@class="fck_detail "]//p[strong][last()]/strong/text()'
            ).get(default='').strip()
        return author

    def get_article_info(self, data, cat_name):
        return {
            'category': cat_name,
            'title': data.get('title', ''),
            'lead': data.get('lead', ''),
            'publish_time': data.get('publish_time')
        }

    def get_art_date(self, response):
        epoch = response.meta['publish_time']
        return datetime.fromtimestamp(epoch).strftime('%Y-%m-%d')
