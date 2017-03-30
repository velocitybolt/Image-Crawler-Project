# web.py


##### html crash course #####

# create sample.html

'''
html - hypertext markup language

text document with content "marked up"
for display in a browser

editors:
    text editor
    wysiwyg editor

creates sample.html
    - tags
    - attributes

<a href=http://www.cnn.com/ target=_blank> CNN </a>

<a> is opening tag
</a> is closing tag
CNN is "data", what is marked up betweeen opening and closing tags
opening tags may or may not have some attribute=value pairs
for example, these are attribute=value pairs
    href=http://www.cnn.com/
    target=_blank

some tags will only have opening tags: <br>

'''

##### using Python to retreive documents #####

'''
html documents are really text documents

if file on local computer, use open()

for remote documents, need urllib.request

>>> open('sample.html').read()[:100]
'<html>\n<head>\n<title>\nSample HTML document\n</title>\n</head>\n\n<body>\n<h1> Sample HTML document </h1>\n'
>>> 
>>> 
>>> 
>>> from urllib.request import *
>>> response = urlopen( 'http://cnn.com')
>>> html = response.read().decode()
>>> html[:150]
'<!DOCTYPE html><html class="no-js"><head><meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"><meta charset="utf-8"><meta content="text/html"'
>>> # how many links
>>> html.count('<a>')
0
>>> html.count('</a>')
191
>>> 
>>> 
>>> # retrieve and save files

>>> urlretrieve('http://lifehacklane.com/img_posts/2016-09-02-14-20-10.jpg','newshark.jpg')
Traceback (most recent call last):
  File "<pyshell#16>", line 1, in <module>
...
raise HTTPError(req.full_url, code, msg, hdrs, fp)
urllib.error.HTTPError: HTTP Error 403: Forbidden
>>> urlretrieve('http://kids.nationalgeographic.com/content/dam/kids/photos/animals/Fish/A-G/great-white-shark-teeth.jpg.adapt.945.1.jpg','newshark.jpg')
('newshark.jpg', <http.client.HTTPMessage object at 0x032A8AF0>)
>>> 

'''

##### HTMLParser ####

'''
HTMLParser - parses (breaks up)
an html document into usable pieces.
When you 'feed' the parser, it
automatically calls three methods
as the items are encountered

    handle_starttag
    handle_data
    handle_endtag

in HTMLParser, these methods are "stubs"
(i.e. implementation is pass)
we get the behaviour we want
by subclssing (inheriting from)
HTMLParser and overriding these methods

'''

from html.parser import HTMLParser

class PrintParser(HTMLParser):

    # feed method inherited
    # eats a str (html doc)

    def handle_starttag(self,tag,attrs):
        print('handle_starttag',tag,attrs)
    def handle_data(self,data):
        print('handle_data',data)
    def handle_endtag(self,tag):
        print('handle_endtag',tag)

'''
>>> p = PrintParser()
>>> p.feed( open('sample.html').read() )
handle_starttag html []
...
handle_starttag img [('height', '200'), ('src', 'http://s.hswstatic.com/gif/shark-sam-7.jpg')]
handle_data 
...
handle_starttag a [('href', 'doc.html')]
...
>>> 
'''

#### # urljoin #####

'''
when we collect links, we want to
collect them in absolute form

urljoin turns relative links
into absolute links

>>> from urllib.parse import urljoin
>>> urljoin('http://cnn.com','shark.jpg')
'http://cnn.com/shark.jpg'

'''

##### LinkCollector #####

from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin

class LinkCollector(HTMLParser):
    ''' when given a url, LinkCollector
collects all the links found at that url.
You can retrive separately (all in absolute form):

1) relative links
2) absolute links
3) all links = 1) + 2)'''

    def __init__(self,url):
        # do I need this?
        HTMLParser.__init__(self)
        self.url = url
        self.absoluteLinks = set()
        self.relativeLinks = set()

    def handle_starttag(self,tag,attrs):
        if tag=='a':
            for attr,val in attrs:
                if attr=='href': # collect
                    if val[:4]=='http': # absolute
                        self.absoluteLinks.add( val )
                    else:  # relative
                        self.relativeLinks.add( urljoin(self.url, val) )

    def getRelatives(self):
        return self.relativeLinks
    def getAbsolutes(self):
        return self.absoluteLinks
    def getLinks(self):
        return self.relativeLinks.union( self.absoluteLinks )
                        
def scrapeLinks(url, filename):
    ''' create a local html file named filename
containing all links found at url'''
    # colllect links
    lc = LinkCollector(url)
    lc.feed( urlopen(url).read().decode() )

    # write them to a file
    file = open(filename,'w')
    file.write( '<html><body>\n')
    for link in lc.getLinks():
        file.write( '<a href={}> {} </a><br>\n'.format(link,link))
    file.write('</body></html>')
    file.close()

##### Crawler #####
'''
want this to work:
>>> c = Crawler()
>>> c.crawl( 'http://cnn.com', 2, True)
... recursively crawl all relative (True)
links found at cnn up to a depth of 2 ...
>>> c.getCrawled()
... return a set of urls that were
crawled (read) ...
>>> c.getFound()
... return a set of urls that were found
(but not necessarily crawled) ...
>>> c.getDead()
... return a set of urls that could not be read ...
'''

from urllib.error import URLError

# based on text version, but with some changes
class Crawler():

    def __init__(self):
        self.crawled = set()
        self.found = set()
        self.dead = set()

    # recursive method
    def crawl(self,url,depth=0,relativeOnly=True):

        # read html at url
        # collect links found there
        lc = LinkCollector(url)
        try:
            lc.feed( urlopen(url).read().decode()  )
        except (UnicodeDecodeError, URLError):
            self.dead.add( url )
        
        # mark current url as crawled
        self.crawled.add( url )

        # depending on depth
        # recursive crawl links that were found
        if relativeOnly:
            found = lc.getRelatives()
        else:
            found = lc.getLinks()
        self.found.update( found )
        # recursive crawl, empty base case
        if depth>0:
            for link in found:
                if link not in self.crawled:
                    self.crawl(link,depth-1,relativeOnly)
        
        

    def getCrawled(self):
        return self.crawled
    def getFound(self):
        return self.found
    def getDead(self):
        return self.dead




        

    














