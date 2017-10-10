from xml.sax import make_parser, handler
from xml.sax.saxutils import escape

class wikiHandler(handler.ContentHandler):
    def __init__(self):
        #self.title = set()
        self.current_content = ""
        self.cw=0 #counter for wikiarticles
        self.ca=0 #counter for wikiarticles starting with A
        self.b1=0 #boolian if article is redirect (0) or not (1)
        self.b2=0 #boolian to check if it is the first id tag of an article
        self.ns=0 #save ns to figure out if it is an article
        self.out1=open('wikiA.txt','w',encoding="utf8") #file for article starting with A
        self.out2=open('wikiCat.txt','w',encoding="utf8") #file for Cat article
        self.out3=open('wikiPedia.txt','w',encoding="utf8") #file for all articles
        self.out4=open('articleIDs.txt','w',encoding='utf8')
        self.current_title="" #keep track of current title
        self.current_id="" #keep track of current ID

    def startElement(self, name, attrs):
        self.current_content = ""

    def characters(self, content):
        self.current_content += content.strip()

    def endElement(self, name):
        if (name=="ns"):
            self.ns=int(self.current_content)
        if (name == "id")&(self.b2):
            self.current_id=self.current_content
            self.b2=0
        if name == "title":
            self.current_title=self.current_content
            self.b1=1
            self.b2=1
        if name == "redirect": # a 'redirect' tag is located between the 'title' tag and the 'text' tag - if it exists
            self.b1=0
        if (name == "text") & (self.b1 == 1) & (self.ns==0):  # if it's not a redirect and if it is an article
            s = escape(self.current_content,{"'":"&apos;","\"":"&quot;"})    #get text with original entities
            if (s[0:9]!='#REDIRECT'):
                self.cw = self.cw + 1  # increase counter
                if self.cw % 10000 == 0:
                    print(self.cw)
                id = self.current_id
                self.out4.write(id)
                self.out4.write('\n')
                s = s.replace('\n', ' ')    #replace newlines
                s = s.lower()               #replace capital letters
                self.out3.write(s)          #write it in a line in wikiPedia.txt
                self.out3.write('\n')       #make a newline
                self.out3.flush()
                if self.current_title=="Cat":   #if it's cat do the same, write in extra file
                    self.out2.write(s)
                    self.out2.write('\n')
                    self.out2.flush()
                if self.current_title:
                    if (self.current_title[0]=="A") | (self.current_title[0]=="a"): # if the title starts with A do the same write in extra file
                        self.ca = self.ca + 1
                        self.out1.write(s)
                        self.out1.write('\n')
                        self.out1.flush()


parser = make_parser()
b = wikiHandler()
parser.setContentHandler(b)
parser.parse("enwiki-20170820-pages-articles-multistream.xml")
