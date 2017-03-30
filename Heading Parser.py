# Lab 8 - Murtaza Meerza

from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin

class HeadingParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.lst1 = []
        self.Headings = False
        
    def handle_starttag(self,tag,attrs):
        if tag in ['h1','h2','h3','h4','h5','h6']:
            self.Headings = True
               
    def handle_endtag(self,tag):
        if tag in ['h1','h2','h3','h4','h5','h6']:
            self.Headings = False
     
    def handle_data(self,data):
        if self.Headings == True:
            data = data.strip()
            if data != '':
                self.lst1.append(data)            
        
    def getHeading(self):
        return self.lst1


def testHP(url):
    lc = HeadingParser()
    lc.feed( urlopen(url).read().decode() )

    return lc.getHeading()
    

if __name__=='__main__':
    import doctest
    print( doctest.testfile( 'lab8TEST.py' ))    
      
