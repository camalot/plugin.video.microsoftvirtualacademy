import sys
import urllib
import re
import xbmc
import xbmcgui
import xbmcaddon
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
import http_request
import control
import utils


class Main:
    def __init__(self):
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.video_url = urllib.unquote_plus(params["video_url"])
        self.play_video()

    def play_video(self):
        # Get current list item details...
        title = unicode(xbmc.getInfoLabel("ListItem.Title"), "utf-8")
        thumbnail = xbmc.getInfoImage("ListItem.Thumb")
        studio = unicode(xbmc.getInfoLabel("ListItem.Studio"), "utf-8")
        plot = unicode(xbmc.getInfoLabel("ListItem.Plot"), "utf-8")
        genre = unicode(xbmc.getInfoLabel("ListItem.Genre"), "utf-8")

        # Show wait dialog while parsing data...
        dialog_wait = xbmcgui.DialogProgress()
        dialog_wait.create(control.lang(30504), title)

        if self.video_url is None:
            # Close wait dialog...
            dialog_wait.close()
            del dialog_wait

            # Message...
            xbmcgui.Dialog().ok(control.lang(30000), control.lang(30505))
            return

        # Play video...
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()

        list_item = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        list_item.setInfo("video", {"Title": title, "Studio": studio, "Plot": plot, "Genre": genre})
        playlist.add(self.video_url, list_item)

        # Close wait dialog...
        dialog_wait.close()
        del dialog_wait

        # Play video...
        xbmc_player = xbmc.Player()
        xbmc_player.play(playlist)
        return