import requests
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url , timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getTags(html):
    tag_title = dict()
    soup = BeautifulSoup(html,"html.parser")
    tag_title_wrappers = soup.find_all("a",{"class":"tag-title-wrapper"})
    # tagCols = soup.find_all("table", {"class": "tagCol"})
    for tag_title_wrapper in tag_title_wrappers:
        tagList = []
        tagCol = tag_title_wrapper.find_next_sibling()
        tags = tagCol.find_all("a")
        for tag in tags:
            tagList.append(tag.string)
        tag_title[tag_title_wrapper['name']] = tagList
    return tag_title

def printTagList(tagList):
    with open('tags.dat','a') as f:
        f.write(str(tagList))

if __name__ == '__main__':
    url = 'https://movie.douban.com/tag/'
    html = getHTMLText(url)
    tagList = getTags(html)
    printTagList(tagList)
