# Murtaza Meerza - HW6
from web import *
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import URLError

class ImageCollector(HTMLParser):
    def __init__(self,url):
        HTMLParser.__init__(self)
        self.url = url
        self.absoluteLinks = set()
        self.relativeLinks = set()

    def handle_starttag(self,tag,attrs):
        if tag=='img':
            for attr,val in attrs:
                if attr=='src': 
                    if val[:4]=='http': 
                        self.absoluteLinks.add(val)
                    else:  
                        self.relativeLinks.add(urljoin(self.url, val))

    def getImages(self):
        return self.relativeLinks.union(self.absoluteLinks)

  
class ImageCrawler(Crawler):
    def __init__(self):
        Crawler.__init__(self)
        self.Images = set()
        self.Crawled = set()
        self.Dead = set()

    def crawl(self,url,depth=0,relativeOnly=True):
        ic = ImageCollector(url)
        try:
            ic.feed(urlopen(url).read().decode())
        except (UnicodeDecodeError, URLError):
            self.Dead.add(url)
            
        # mark that its been crawled
        self.crawled.add(url)

        # recursively crawl image links
        if relativeOnly:
            images = ic.getImages()
        self.Images.update(images)

        # empty base case crawl
        if depth>0:
            for link in images:
                if link not in self.crawled:
                    # hint from class
                    Crawler.crawl(self,url,depth,relativeOnly)

    def getImages(self):
        return self.Images

    def getCrawled(self):
        return self.Crawled
   
    def getDead(self):
        return self.Dead

def scrapeImages(url,filename,depth,relativeOnly):
    c = ImageCrawler()
    c.crawl(url,depth,relativeOnly)

    file = open(filename,'w')
    file.write('<html><body>\n')
    for i in c.getImages():
        file.write('<img src={}>'.format(i))
    file.write('</body></html>')
    file.close()
        

if __name__=='__main__':
    import doctest
    print(doctest.testfile('hw6TEST.py'))          
         
            
