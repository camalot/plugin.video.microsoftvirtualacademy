import sys
import urllib
import os
import json
import xbmcgui
import xbmcplugin
import control
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
import http_request

url_root = "https://mva.microsoft.com/"
url_api = "https://api-mlxprod.microsoft.com/"
url_api_courses = "%ssdk/search/v1.0/5/courses?$skip=%i&$top=%i"
url_course = "en-us/training-courses/course-%s"

icon_folder = os.path.join(control.imagesPath, "folder.png")
icon_search = os.path.join(control.imagesPath, "search.png")
icon_next = os.path.join(control.imagesPath, "next-page.png")

ignore_sections = ["LCID", "Format"]
section_ids = [30201, 30202, 30203, 30204, 30205]


def add_video(title, thumbnail, plot, genre, video_url):
    list_item = control.item(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail, path=video_url)
    list_item.setInfo("video", {"Title": title, "Studio": "Microsoft Channel 9", "Plot": plot, "Genre": genre})
    list_item.setProperty("IsPlayable", "true")
    list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
    plugin_play_url = '%s?action=play&video_url=%s' % (sys.argv[0], urllib.quote_plus(video_url))
    control.addItem(handle=int(sys.argv[1]), url=plugin_play_url, listitem=list_item, isFolder=False)


def add_next_page(item_url, page):
    list_item = control.item("[B][UPPERCASE][COLOR green]%s[/COLOR][/UPPERCASE][/B]" % control.lang(30500) % page,
                             iconImage=icon_next, thumbnailImage=icon_next)
    control.addItem(handle=int(sys.argv[1]), url=item_url, listitem=list_item, isFolder=True)
    return


def create_select_criteria(section, topic):
    return {"SelectMatchOption": 2, "SelectOnField": section, "SelectTerm": topic}


def add_directory(text, icon, thumbnail, url):
    list_item = xbmcgui.ListItem(text, iconImage=icon, thumbnailImage=thumbnail)
    list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
    control.addItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=True)
    return


def get_course_data(select_criteria=[], skip=0, take=10):
    url = url_api_courses % (url_api, skip, take)
    payload = {"SelectCriteria": select_criteria, "DisplayFields": [],
               "SortOptions": [{"SortOnField": "Relevance", "SortOrder": 1}], "SearchKeyword": "",
               "UILangaugeCode": "1033", "UserLanguageCode": "1033"}
    result = http_request.post_json(url, payload)
    json_obj = json.loads(result)

    return json_obj["results"]


def get_course_meta(select_criteria=[]):
    url = url_api_courses % (url_api, 0, 1)

    # {"SelectCriteria":[],"DisplayFields":[],"SortOptions":[{"SortOnField":"Relevance","SortOrder":1}],"SearchKeyword":"","UILangaugeCode":"1033","UserLanguageCode":"1033"}
    payload = {"SelectCriteria": select_criteria, "DisplayFields": [],
               "SortOptions": [{"SortOnField": "Relevance", "SortOrder": 1}], "SearchKeyword": "",
               "UILangaugeCode": "1033", "UserLanguageCode": "1033"}

    result = http_request.post_json(url, payload)
    json_obj = json.loads(result)

    return {"sections": json_obj["narrowBySections"], "totalResultCount": json_obj["totalResultCount"] }


def set_no_sort():
    control.sort(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
    return


def get_banner(url):
    html_data = http_request.get(url)
    soup_strainer = SoupStrainer("head")
    beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)

    banner = beautiful_soup.find("meta", {"name": "msapplication-square310x310logo"})
    if banner is not None:
        return banner["content"]
    else:
        return None
