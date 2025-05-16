BOT_NAME = "vne"

SPIDER_MODULES = ["vne.spiders"]
NEWSPIDER_MODULE = "vne.spiders"


###MAC DINH KHI CHAY SE SINH RA 2 FILE CSV, JSON
FEEDS = {
    'data.json' : {'format' : 'json', 'overwrite' : True},
    'data.csv' : {'format' : 'csv', 'overwrite' : True}
}


###QUY DINH HIEN THI CAC TRUONG
FEED_EXPORT_FIELDS = [
    'url', 'category', 'title', 'author', 'date', 'lead', 'main_content'
]

ROBOTSTXT_OBEY = True


###THAY ANH MUON TEST THI THAY DOI THONG TIN DATABASE O DAY
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Leduytung041a@'
MYSQL_DATABASE = 'vne'


ITEM_PIPELINES = {
    'vne.pipelines.VnePipeline': 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
