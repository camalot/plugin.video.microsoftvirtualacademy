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
        self.section = urllib.unquote_plus(params.get("section", ""))
        self.group = urllib.unquote_plus(params.get("group", ""))
        self.current_page = int(urllib.unquote_plus(params.get("page", "1")))
        self.per_page = 10
        self.search_term = urllib.unquote_plus(params.get("query", ""))

        if self.section != "":
            self.icon = os.path.join(control.imagesPath, "%s.png" % self.section)
        else:
            self.icon = os.path.join(control.imagesPath, "unknown.png")

        utils.set_no_sort()
        if self.action == 'search':
            self.search()
        return

    def search(self):

        if self.search_term is None or self.search_term == '':
            t = control.lang(30201).encode('utf-8')
            k = control.keyboard('', t)
            k.doModal()
            self.search_term = k.getText() if k.isConfirmed() else None

        if self.search_term is None or self.search_term == '':
            return

        skip = (self.current_page-1) * self.per_page
        take = self.per_page
        select_filter = utils.create_filter_criteria(self.section, self.group, self.search_term)
        results_count = utils.get_course_meta(select_filter)["totalResultCount"]
        courses = utils.get_course_data(select_filter, skip, take)

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
            next_url = "%s?action=search&group=%s&section=%s&page=%i&query=%s" % (
                sys.argv[0], urllib.quote_plus(self.group, safe=':/'), urllib.quote_plus(self.section, safe=':/'),
                self.current_page + 1, self.search_term)
            utils.add_next_page(next_url, self.current_page + 1)
        control.directory_end(False)
        return
