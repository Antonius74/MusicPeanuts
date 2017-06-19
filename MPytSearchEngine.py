from bs4 import BeautifulSoup
import configparser
import re
import json
import certifi
import urllib3

config = configparser.RawConfigParser()
config.read('ConfigFile.properties')

searchUrl = (config.get('YTConfig', 'YTConfig.YTQuery'))
playUrl = (config.get('YTConfig', 'YTConfig.PlayURL'))
MapResultVideo = {}

def getSoup():
    print (searchUrl+qString)
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    httpRequest = http.request('GET', searchUrl+qString)
    return BeautifulSoup(httpRequest.data, "html.parser")
    
def getVideoInfo(soup):
    i=0
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
                        i=i+1
                        MapContent = {"Title":title, "Type":"Video", "Source":"YT", "DataRef":dataContextItem, "Time":vTime, "VideoCount":None, "Thumb":srcThumb}
                        MapResultVideo.update({i:MapContent})
                elif 'yt-lockup-playlist' in ytClass:
                    try:
                        if divResult.div.div.a['href'] != None:
                            plHref = divResult.div.div.a['href']
                            if divResult.div.div.a.div.span.img['src'].startswith('http'):
                                srcthumb = divResult.div.div.a.div.span.img['src']
                            else:
                                srcthumb = divResult.div.div.a.div.span.img['data-thumb']
                            for div in divResult.div.find_all('div'):
                                if "yt-lockup-content" in div.get("class"):
                                    title = div.a['title']
                            for div in divResult.div.div.a.find_all('div'):
                                if "sidebar" in div.get("class"):
                                    countV = div.span.span.span.b.string
                            i = i + 1
                            MapContent = {"Title": title, "Type": "PL", "Source":"YT", "DataRef": plHref, "Time": None, "VideoCount": countV, "Thumb": srcThumb}
                            MapResultVideo.update({i: MapContent})


                    except Exception as e:
                        print(e)


def getPLDetails(plList):
    return

def getVideoResult():
    return

print ("Enter qString:")
qString = input()
qString = re.sub(' ', '+', qString)
soup = getSoup()
getVideoInfo(soup)
jSonMapYT = json.dumps(MapResultVideo, ensure_ascii=False)
print (jSonMapYT)
