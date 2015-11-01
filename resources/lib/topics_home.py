import sys
import control
import utils
import urllib
import re
import http_request
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup


# Main class
class Main:
    def __init__(self):
        #params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        #self.action = params.get("action", None)
        utils.set_no_sort()

        url = utils.url_root
        html_data = http_request.get(url)
        soup_strainer = SoupStrainer("div", {"class": "tilesArticles"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        articles = beautiful_soup.findAll("article")
        keys = {}
        for article in articles:
            anchor = article.find("a")
            div_container = anchor.find("div", {"class": "imageContainer"})
            if div_container is None:
                continue
            img = div_container.find("img")
            thumb = img["src"]
            title = anchor["title"]
            url = anchor["href"]

            if re.match('^https?:', url):
                url = url[len(utils.url_root):]

            if url not in keys:
                utils.add_directory(title, thumb, thumb,
                                    "%s?action=browse-topic&url=%s" % (sys.argv[0], urllib.quote_plus(url)))
                keys[url] = title

        control.directory_end()
        return
