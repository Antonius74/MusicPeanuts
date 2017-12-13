from bs4 import BeautifulSoup
import configparser
import pafy
import re
import json
import certifi
import urllib3

class YTSearchEngine:
    config = configparser.RawConfigParser()
    config.read('ConfigFile.properties')

    searchUrl = (config.get('YTConfig', 'YTConfig.YTQuery'))
    PLUrl = (config.get('YTConfig', 'YTConfig.YTPL'))
    playUrl = (config.get('YTConfig', 'YTConfig.PlayURL'))
    MapResultVideo = {}

    def __init__(self):
        None

    def getSoup(self, qString):
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        httpRequest = http.request('GET', qString)
        return BeautifulSoup(httpRequest.data, "html.parser")

    def getVideoInfo(self, soup):
        i=1
        for divTotal in soup.find_all("div"):
            listResult = divTotal.get("id")
            if listResult == 'results':
                for divResult in divTotal.find_all("div"):
                    ytClass = divResult.get('class')
                    if 'yt-lockup-video' in ytClass:
                        dataContextItem = divResult.get('data-context-item-id')
                        if dataContextItem != None:
                            for thumb in divResult.find_all("img"):
                                srcThumb = thumb.get("src")
                                if not re.search('^http', srcThumb):
                                    srcThumb = thumb.get("data-thumb")
                            for a in divResult.find_all("a"):
                                if a.get("title") != None and not re.search('^http', a.get("title")):
                                    title = a.get("title")
                            for span in divResult.find_all("span"):
                                if "video-time" in span.get("class"):
                                    vTime = span.contents[0]
                            MapContent = {"Title":title, "Type":"Video", "Source":"YT", "DataRef":dataContextItem, "Time":vTime, "VideoCount":None, "Thumb":srcThumb}
                            self.MapResultVideo.update({i:MapContent})
                            i = i + 1

                    elif 'yt-lockup-playlist' in ytClass:
                        try:
                            if divResult.div.div.a['href'] != None:
                                plHref = divResult.div.div.a['href']
                                if divResult.div.div.a.div.span.img['src'].startswith('http'):
                                    srcThumb = divResult.div.div.a.div.span.img['src']
                                else:
                                    srcThumb = divResult.div.div.a.div.span.img['data-thumb']
                                for div in divResult.div.find_all('div'):
                                    if "yt-lockup-content" in div.get("class"):
                                        title = div.a['title']
                                for div in divResult.div.div.a.find_all('div'):
                                    if "sidebar" in div.get("class"):
                                        countV = div.span.span.span.b.string
                                MapContent = {"Title": title, "Type": "PL", "Source":"YT", "DataRef": plHref, "Time": None, "VideoCount": countV, "Thumb": srcThumb}
                                self.MapResultVideo.update({i: MapContent})
                                i = i + 1

                        except Exception as e:
                            print(e)
        return json.dumps(self.MapResultVideo, ensure_ascii=False)


    def getPLdetails(self, pList):
        i = 1
        plurl = self.PLUrl + pList
        playlist = pafy.get_playlist(plurl)
        for items in playlist['items']:
            MapContent = {"Title": items['playlist_meta']['title'], "Type": "Video", "Source": "YT", "DataRef": items['playlist_meta']['encrypted_id'], "Time": items['playlist_meta']['duration'], "VideoCount": None, "Thumb": items['playlist_meta']['thumbnail']}
            self.MapResultVideo.update({i: MapContent})
            i = i + 1
        return json.dumps(self.MapResultVideo, ensure_ascii=False)

    def getVideoResult(self):
        return

    def main(self):
        qString = input("Enter qString:")
        se = YTSearchEngine()
        # print(se.getPLdetails(qString))
        qString = re.sub(' ', '+', qString)
        soup = se.getSoup(se.searchUrl + qString)
        print(se.getVideoInfo(soup))

if __name__ == '__main__':
    se = YTSearchEngine()
    se.main()




