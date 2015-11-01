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
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.action = params.get("action", 'browse-topic')
        self.sort_method = params.get("sort", '')
        self.topic_url = urllib.unquote_plus(params.get("url", ''))

        utils.set_no_sort()
        self.browse()
        return

    def browse(self):

        url = "%s%s" % (utils.url_root, self.topic_url)
        print "url: %s" % url
        html_data = http_request.get(url)
        soup_strainer = SoupStrainer("div", {"id": "main_content"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)

        div_topic_header = beautiful_soup.find("header", {"class": "topic-header"})
        div_image = div_topic_header.find("div", {"class": "image"})
        if div_image is not None:
            img = div_image.find("img", {"class": "topicImage"})
            thumbnail = img["src"]

        div_topic_detail = beautiful_soup.find("section", {"class": "topic-detail"})
        articles = div_topic_detail.findAll("article")

        for article in articles:
            div_image = article.find("div", {"class": "image"})
            img = div_image.find("img")
            if img is not None:
                thumbnail = img["src"]

            div_title = article.find("div", {"class": "title"})
            a_link = div_title.find("a")
            course_url = a_link["href"]
            if re.match('^https?:', course_url):
                course_url = course_url[len(utils.url_root):]

            title = a_link.string

            utils.add_directory(title, thumbnail, thumbnail,
                                "%s?action=view-course&url=%s" % (sys.argv[0], urllib.quote_plus(course_url)))
        control.directory_end(False)
        return
