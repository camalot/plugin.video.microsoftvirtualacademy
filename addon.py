
##############################################################################
#
# Microsoft Virtual Academy plugin for Kodi
# https://mva.microsoft.com
#
# Version 1.0
#
#
# https://github.com/camalot/plugin.video.microsoftvirtualacademy
#
#

__addon__ = "Microsoft Virtual Academy"
__author__ = "Ryan Conrad"
__url__ = "https://github.com/camalot/plugin.video.microsoftvirtualacademy"
__date__ = "10/27/2015"
__version__ = "1.0"

import os
import sys
import urlparse
import xbmc
import xbmcaddon

addon_path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path'))
lib_path = xbmc.translatePath(os.path.join(addon_path, 'resources', 'lib'))
sys.path.append(lib_path)

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
action = params.get('action', 'home')

if action is None or action == '':
    print "no action found: triggering default"
    action = 'home'

if action == 'home':
    import home as plugin
elif action == 'view-course':
    import course as plugin
elif action == "browse-section":
    import section as plugin
elif action == "browse-group":
    import section as plugin
elif action == "search":
    import searcher as plugin
elif action == 'play':
    import play as plugin
elif action == 'settings':
    import settings as plugin
else:
    import home as plugin

plugin.Main()
