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
icon_settings = os.path.join(control.imagesPath, "settings.png")

text_green = "[B][COLOR green][UPPERCASE]%s[/UPPERCASE][/COLOR][/B]"

ignore_sections = ["LCID", "Format"]
section_ids = [30201, 30202, 30203, 30204, 30205]
default_filter = {"SelectCriteria": [], "DisplayFields": [],
               "SortOptions": [{"SortOnField": "Relevance", "SortOrder": 1}], "SearchKeyword": "",
               "UILangaugeCode": "1033", "UserLanguageCode": "1033"}
default_lanugage = {"SelectOnField": "LCID", "SelectTerm": "1033", "SelectMatchOption": 2}

def add_video(title, thumbnail, plot, genre, video_url):
    list_item = control.item(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    list_item.setInfo("video", {"Title": title, "Studio": "Microsoft Channel 9", "Plot": plot, "Genre": genre})
    list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
    plugin_play_url = '%s?action=play&video_url=%s' % (sys.argv[0], urllib.quote_plus(video_url))
    control.addItem(handle=int(sys.argv[1]), url=plugin_play_url, listitem=list_item, isFolder=False)


def add_next_page(item_url, page):
    list_item = control.item(text_green % (control.lang(30500) % page),
                             iconImage=icon_next, thumbnailImage=icon_next)
    control.addItem(handle=int(sys.argv[1]), url=item_url, listitem=list_item, isFolder=True)
    return


def language_filter():
    # {SelectOnField: "LCID", SelectTerm: "1045", SelectMatchOption: 2}
    result = []
    setting_lang_items = control.lang(30600).split(",")
    for lang_item in setting_lang_items:
        lang_enabled = control.setting(lang_item)
        if lang_enabled == "true":
            result.append({"SelectOnField": "LCID", "SelectTerm": "%s" % lang_item, "SelectMatchOption": 2})

    if not result:
        return default_lanugage

    return result


def create_filter_criteria(section, topic, search_term=None):
    if section == "" or topic == "":
        select_criteria = []
    else:
        select_criteria = [{"SelectMatchOption": 2, "SelectOnField": section, "SelectTerm": topic}]
    for lfilter in language_filter():
        select_criteria.append(lfilter)
    if search_term is None:
        search_term = ""
    payload = {"SelectCriteria": select_criteria, "DisplayFields": [],
           "SortOptions": [{"SortOnField": "Relevance", "SortOrder": 1}], "SearchKeyword": search_term,
           "UILangaugeCode": "1033", "UserLanguageCode": "1033"}
    return payload


def add_directory(text, icon, thumbnail, url):
    list_item = xbmcgui.ListItem(text, iconImage=icon, thumbnailImage=thumbnail)
    list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
    control.addItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=True)
    return


def get_course_data(filter_payload, skip=0, take=10):
    url = url_api_courses % (url_api, skip, take)
    result = http_request.post_json(url, filter_payload)
    json_obj = json.loads(result)

    return json_obj["results"]


def get_course_meta(filter_payload=None):
    url = url_api_courses % (url_api, 0, 1)

    # {"SelectCriteria":[],"DisplayFields":[],"SortOptions":[{"SortOnField":"Relevance","SortOrder":1}],"SearchKeyword":"","UILangaugeCode":"1033","UserLanguageCode":"1033"}

    if filter_payload is None:
        filter_payload = default_filter
        for lfilter in language_filter():
            filter_payload["SelectCriteria"].append(lfilter)

    result = http_request.post_json(url, filter_payload)
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
