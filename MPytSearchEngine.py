from bs4 import BeautifulSoup
import re
import requests
import json
from collections import namedtuple

searchUrl = ("https://www.youtube.com/results?search_query=")
playUrl = ("https://www.youtube.com")
MapResult = {}

def getSoup():
    httpRequest  = requests.get(searchUrl+qString)
    flatData = httpRequest.text
    return BeautifulSoup(flatData, "html.parser")
    
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
                        MapResult.update({i:MapContent})


def getVideoResult():
    return

print ("Enter qString:")
qString = input()
qString = re.sub(' ', '+', qString)
soup = getSoup()
getVideoInfo(soup)
jSonMap = json.dumps(MapResult, ensure_ascii=False)
print (jSonMap)
#print (json.loads(str(MapResult)))
#print(json.dump(str(MapResult)))
#j=print(json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4))
#print(j)