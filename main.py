import tornado.ioloop
import tornado.web
import re
import urllib2

from wordcloud import WordCloud
import matplotlib as plt
# Force matplotlib to not use any Xwindows backend.
plt.use('Agg')
import pylab as pl
import io

    """
    #This class has been used only to start with Tornado
    class MainHandler(tornado.web.RequestHandler):
    def get(self):
    self.write("Test...it works!")
    """

class FormHandler(tornado.web.RequestHandler):#form HTML for receiving an URL as input
    def get(self):
        self.write('<html><body>Dear Visitor, please add an url here: <br /><br /><form action="/backend" method="POST">'
                   '<input type="text" name="url">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
    
    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_body_argument("message"))


class PostHandler(tornado.web.RequestHandler):
	def post(self):
		url = self.get_argument('url', '')#receive post url
		full_url = "http://"+url#add http, here I should add a filter to recognize when users use http://
		req = urllib2.Request(full_url)#
		response = urllib2.urlopen(req)
		the_page = response.read()#get text from website indicated in the url
		wordList = re.sub("[^\w]", " ",  the_page).split()#take words from text
		one_hundred = top_words(wordList)#select most frequent words
		final_value = "  ".join(one_hundred)#generate a random sentence to be used for the image library
		image = genImage(final_value)#generate the image
		self.set_header('Content-type', 'image/png')
		self.set_header('Content-length', len(image))
		self.write(image)#save the image as words.png



class FrontHandler(tornado.web.RequestHandler):#this class just shows the resulting image to the user
	def get(self):
		self.write('<html><body><img src="words.png" /></body></html>')





def top_words(list_of_words):#find the 100 most frequent words in the list
    
	list_words = []
	nr_words = len(list_of_words)
	x=0
	while x < nr_words:
		list_words.append(list_of_words[x])
		x+=1
    
	top_words_list = []
	
	word_counter = {}
	for sword in list_words:
	    if sword in word_counter:
	        word_counter[sword] += 1
	    else:
	        word_counter[sword] = 1
	
	m_popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
	
	
	
	
	return m_popular_words[:100]



def genImage(list_w):#generate the image with wordcloud
	
    wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(list_w)
    
    
    pl.Figure()
    pl.imshow(wordcloud)
    
    memdata = io.BytesIO()
    pl.axis("off")
    pl.savefig(memdata, format='png')
    image = memdata.getvalue()
    
    return image




def make_app():
    return tornado.web.Application([
                                    (r"/", FormHandler),(r"/backend", PostHandler),(r"/words.png", PostHandler),(r"/result", FrontHandler),
                                    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
