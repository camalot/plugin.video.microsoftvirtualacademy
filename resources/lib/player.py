import re, sys, json, time, xbmc

import control
import bookmarks


class player(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.totalTime = 0
        self.loadingTime = 0
        self.currentTime = 0
        self.title = ""
        self.year = 2015
        self.offset = '0'
        self.dbid = 0

    def run(self, meta):

        # if control.window.getProperty('PseudoTVRunning') == 'True':
        #    return control.player.play(url, control.item(path=url))

        self.getVideoInfo(meta)
        if meta["thumb"] is None:
            meta["thumb"] = "DefaultVideo.png"
        item = control.item(path=meta["url"], iconImage=meta["thumb"], thumbnailImage=meta["thumb"])
        item.setInfo(type='Video', infoLabels={"Title": self.title, "Plot": meta["plot"], "Genre": meta["genre"]})

        item.setProperty('Video', 'true')
        # item.setProperty('IsPlayable', 'true')
        item.setProperty("ListItem.IsResumable", "true")
        item.setProperty("ListItem.EndTime", meta["endTime"])
        item.setProperty("totaltime", meta["endTime"])

        control.player.play(meta["url"], item)

        for i in range(0, 240):
            if self.isPlayingVideo(): break
            xbmc.sleep(1000)
        while self.isPlayingVideo():
            try:
                self.totalTime = self.getTotalTime()
            except Exception, e:
                print str(e)
                pass
            try:
                self.currentTime = self.getTime()
            except Exception, e:
                print str(e)
                pass
            xbmc.sleep(1000)
        time.sleep(5)

    def getVideoInfo(self, meta):
        try:
            self.loadingTime = time.time()
            self.totalTime = meta["endTime"]
            self.currentTime = 0
            self.title = meta["title"]
            self.year = meta["year"]
            self.dbid = meta["dbid"]
        except Exception, e:
            print str(e)
            pass

        try:
            # if control.setting('resume_playback') == 'true':
            self.offset = bookmarks.getBookmark(self.title, meta["id"])
            if self.offset == '0': raise Exception()

            minutes, seconds = divmod(float(self.offset), 60);
            hours, minutes = divmod(minutes, 60)
            yes = control.yesnoDialog(
                '%s %02d:%02d:%02d' % (control.lang(30461).encode('utf-8'), hours, minutes, seconds), '', '',
                self.title, control.lang(30463).encode('utf-8'), control.lang(30462).encode('utf-8'))

            if yes:
                self.offset = '0'
        except Exception, e:
            print str(e)
            pass


    def setWatchedStatus(self):
        return
        # if self.content == 'episode':
        #    try:
        #        control.jsonrpc(
        #            '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(
        #                self.DBID))
        #        if not self.folderPath.startswith('plugin://'): control.refresh()
        #    except:
        #        pass

        #    try:
        #        from metahandler import metahandlers
        #        metaget = metahandlers.MetaData(preparezip=False)
        #        metaget.get_meta('tvshow', self.tvshowtitle, imdb_id=self.imdb)
        #        metaget.get_episode_meta(self.tvshowtitle, self.imdb, self.season, self.episode)
        #        metaget.change_watched(self.content, '', self.imdb, season=self.season, episode=self.episode, year='',
        #                               watched=7)
        #    except:
        #        pass

    def onPlayBackStarted(self):
        for i in range(0, 200):
            if control.condVisibility('Window.IsActive(busydialog)') == 1:
                control.idle()
            else:
                break
            control.sleep(100)

        if control.setting('playback_info') == 'true':
            elapsedTime = '%s %s %s' % (control.lang(30464).encode('utf-8'), int((time.time() - self.loadingTime)),
                                        control.lang(30465).encode('utf-8'))
            control.infoDialog(elapsedTime, heading=self.title)

        try:
            if self.offset == '0':
                raise Exception()
            self.seekTime(float(self.offset))
        except Exception, e:
            print str(e)
            pass

    def onPlayBackStopped(self):
        try:
            bookmarks.deleteBookmark(self.title, self.dbid)
            ok = int(self.currentTime) > 180 and (self.currentTime / self.totalTime) <= .92
            if ok:
                print "adding bookmark: %s : %s" % (self.currentTime, self.dbid)
                bookmarks.addBookmark(self.currentTime, self.title, self.dbid)
        except Exception, e:
            print str(e)
            pass
        try:
            ok = self.currentTime / self.totalTime >= .9
            if ok: self.setWatchedStatus()
        except Exception, e:
            print str(e)
            pass

    def onPlayBackEnded(self):
        self.onPlayBackStopped()
