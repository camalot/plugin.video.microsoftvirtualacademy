import sys
import control
import utils
import urllib
import os

# Main class
class Main:
    def __init__(self):
        # params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        # self.action = params.get("action", None)
        utils.set_no_sort()

        meta = utils.get_course_meta()["sections"]
        for m in meta:
            header = m["header"]
            title = header
            if title in utils.ignore_sections:
                continue

            for sid in utils.section_ids:
                if title == control.lang(sid):
                    title = control.lang(sid + 100)
            icon = os.path.join(control.imagesPath, "%s.png" % header)
            utils.add_directory(title, icon, icon,
                                "%s?action=browse-section&section=%s" % (sys.argv[0], urllib.quote_plus(header)))

        control.directory_end()
        return
