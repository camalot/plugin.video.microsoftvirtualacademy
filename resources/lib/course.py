import sys
import control
import utils
import urllib
import re
import json
import http_request
import xml.etree.ElementTree
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup


# Main class
class Main:
    def __init__(self):
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.action = params.get("action", 'view-course')
        self.sort_method = params.get("sort", '')
        self.topic_url = urllib.unquote_plus(params.get("url", ''))
        self.course_id = urllib.unquote_plus(params.get("id", None))
        utils.set_no_sort()
        self.browse()
        return

    def browse(self):
        url = "%s%s" % (utils.url_root, self.topic_url)
        print "url: %s" % url
        if self.course_id is None:
            if not re.match("-(\d+)$", url):
                html_data = http_request.get(url)
                soup_strainer = SoupStrainer("head")
                beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)

                share_url = beautiful_soup.find("meta", {"id": "ctl00_ctl00_metaShareUrl"})
                course_code = re.findall("-(\d+)$", share_url["content"])[0]
            else:
                course_code = re.findall("-(\d+)$", url)[0]
        else:
            course_code = self.course_id

        print "code: %s" % course_code
        data_url = "%sservices/products/anonymous/%s?version=1.0.0.0&isTranscript=false&languageId=12" % (
            utils.url_api, course_code)
        json_data = http_request.get(data_url)

        # "https:\/\/cp-mlxprod-static.microsoft.com\/012044-1000\/en-us"
        scorm_data_url = json.loads(json_data).replace("\\/", "/")

        manifest_url = "%s/imsmanifestlite.json" % scorm_data_url
        thumbnail = "%s/thumbnail.png" % scorm_data_url

        course_details_url = "%s/coursedetails.xml?v=1446384003349" % scorm_data_url
        course_details_data = http_request.get(course_details_url)
        course_details_xml = xml.etree.ElementTree.XML(course_details_data)
        print course_details_xml
        # course_details_root = course_details_xml.getroot()
        course_level = course_details_xml.findall(".//Level")[0].text
        description = course_details_xml.findall('.//Introduction')[0].text

        json_data = http_request.get(manifest_url)
        manifest_data = json.loads(json_data)

        print manifest_data
        manifest = manifest_data["manifest"]
        organizations = manifest["organizations"]

        for org in organizations["organization"]:
            for item in org["item"]:
                try:
                    first_item = item["item"][0]
                    # identifier = item["@identifier"]
                    title = item["title"]
                    resource = first_item["resource"]
                    href = resource["@href"]
                    settings_url = href.split("=")[1]

                    video_settings_url = "%s/%s/videosettings.xml?v=1" % (scorm_data_url, settings_url)

                    video_settings_data = http_request.get(video_settings_url)
                    video_settings = xml.etree.ElementTree.XML(video_settings_data)
                    # video_settings_root = video_settings.getroot()

                    media_sources = video_settings.findall('.//MediaSources')
                    for source in media_sources:
                        if source.attrib["videoType"] == "progressive":
                            progressives = source.findall(".//MediaSource")
                            for prog in progressives:
                                if prog.attrib["default"] == "true":
                                    default_media = prog.text
                                    break
                            continue
                    utils.add_video(title, thumbnail, description, "Level %s" % course_level, default_media)
                except Exception, e:
                    print str(e)

        control.directory_end()
        return
