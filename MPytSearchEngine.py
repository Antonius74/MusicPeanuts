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
                        MapContent = {"Title":title, "Type":"Video", "YTRef":dataContextItem, "Time":vTime, "Thumb":srcThumb}
                        MapResultVideo.update({i:MapContent})
                elif 'yt-lockup-playlist' in ytClass:
                    try:
                        if divResult.div.div.a['href'] != None:
                            print (divResult.div.div.a['href'])
                            print(divResult.div.div.a.div.span.img)
                            print()
                        elif divResult.div.div.a['href'] != None:
                            print (divResult.div.div.a['href'])
                            print(divResult.div.div.a.div.span.img)
                            print()
                    except:
                        None
#                    for span in divResult.find_all('span'):
#                        print(span.div.div.a)
#                        classInSpan = span.get("class")
#                        if classInSpan != None:
#                            if 'yt-thumb-simple' in classInSpan:
#                                print (classInSpan)
#                                for img in span.find_all("img"):
#                                    print (span)
                                #    print (img.get("src"))




def getVideoResult():
    return

print ("Enter qString:")
qString = input()
qString = re.sub(' ', '+', qString)
soup = getSoup()
getVideoInfo(soup)
jSonMap = json.dumps(MapResultVideo, ensure_ascii=False)
#print (jSonMap)
