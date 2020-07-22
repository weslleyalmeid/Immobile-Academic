# Scrapy settings for Guarapuava project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Guarapuava'

SPIDER_MODULES = ['Guarapuava.spiders']
NEWSPIDER_MODULE = 'Guarapuava.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#    'Accept-Encoding': 'gzip, deflate, br',
#    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
#    'Cache-Control': 'no-cache',
#    'Connection': 'keep-alive',
#    'Cookie': '_ga=GA1.3.1192687174.1595243548; _gid=GA1.3.1019081631.1595243548; __atuvc=10%7C30; laravel_session=eyJpdiI6IkpMVEFHZk1pVlZxMlFvbU83UEpTeGc9PSIsInZhbHVlIjoiTDVcL2VjeDZTN2QxYnB2ejhQb1pyS3lzc1lrTDZDMTVGa2FxdGs4aVZQTU5XbWdpNHdTUDN6eXRjRnlRclNNK0xzOVpZXC8yYlE0VHVNV2FJRXhMOUVwdz09IiwibWFjIjoiZGNjZWVmNmQ2NTE5ODg1ODNiMzVlY2ZlNDM0ODZkMzE4MDkzOTA3NWY4Yzg5ZTEwN2E4N2FiMmE1Zjk4NzVmNyJ9; _gat=1; _gat_gtag_UA_9335925_96=1',
#    'Host': 'www.imperiumimoveis.com.br',
#    'Pragma': 'no-cache',
#    'Sec-Fetch-Dest': 'document',
#    'Sec-Fetch-Mode':'navigate',
#    'Sec-Fetch-Site': ' none',
#    'Sec-Fetch-User':' ?1',
#    'Upgrade-Insecure-Requests':' 1',
#    'User-Agent':' Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Guarapuava.middlewares.GuarapuavaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Guarapuava.middlewares.GuarapuavaDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Guarapuava.pipelines.GuarapuavaPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
