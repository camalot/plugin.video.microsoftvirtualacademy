import sys
import control
import utils
import urllib
import os


# Main class
class Main:
    def __init__(self):
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.action = params.get("action", None)
        self.section = urllib.unquote_plus(params.get("section", ''))
        self.group = urllib.unquote_plus(params.get("group", ""))
        self.current_page = int(urllib.unquote_plus(params.get("page", "1")))
        self.per_page = 10

        self.icon = os.path.join(control.imagesPath, "%s.png" % self.section)

        utils.set_no_sort()
        if self.action == 'browse-section':
            self.browse_section()
        elif self.action == "browse-group":
            self.browse_group()
        return

    def browse_section(self):
        meta = utils.get_course_meta()
        utils.add_directory(utils.text_green % control.lang(30501), utils.icon_search, utils.icon_search,
                            "%s?action=search&section=%s" % (sys.argv[0], self.section))

        for m in meta["sections"]:
            header = m["header"]
            if header == self.section:
                infos = m["narrowByInfos"]
                for info in infos:
                    count = info["count"]
                    name = info["name"].encode('utf-8')
                    utils.add_directory("%s (%i)" % (name, count), self.icon, self.icon,
                                        "%s?action=browse-group&group=%s&section=%s&page=1" % (
                                            sys.argv[0], urllib.quote_plus(name, safe=':/'),
                                            urllib.quote_plus(self.section, safe=':/')))
        control.directory_end(False)
        return

    def browse_group(self):

        skip = (self.current_page - 1) * self.per_page
        take = self.per_page
        select_filter = utils.create_filter_criteria(self.section, self.group)
        results_count = utils.get_course_meta(select_filter)["totalResultCount"]
        courses = utils.get_course_data(select_filter, skip, take)

        utils.add_directory(utils.text_green % control.lang(30501), utils.icon_search, utils.icon_search,
                            "%s?action=search&section=%s&group=%s" % (sys.argv[0], self.section, self.group))

        for course in courses:
            name = course["courseName"].encode('utf-8')
            thumb = course["courseImage"]
            if thumb is None or thumb == '':
                thumb = self.icon
            cid = course["id"]
            utils.add_directory(name, thumb, thumb,
                                "%s?action=view-course&id=%s&url=%s" % (sys.argv[0], cid, utils.url_course % cid))
        has_more = (results_count - (skip+self.per_page)) > 0
        if has_more:
            next_url = "%s?action=browse-group&group=%s&section=%s&page=%i" % (
                sys.argv[0], urllib.quote_plus(self.group, safe=':/'), urllib.quote_plus(self.section, safe=':/'),
                self.current_page + 1)
            utils.add_next_page(next_url, self.current_page + 1)
        control.directory_end(False)
        return
