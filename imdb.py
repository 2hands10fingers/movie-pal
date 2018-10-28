from bs4 import BeautifulSoup as bs
from requests import get
class imdb():
	def imdb():
        source = get(
            'http://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth_1').text
        soup = bs(source, 'lxml')
        titles = soup.find_all('td', {"class": "overview-top"})
        titles = [i.h4.a.text[:-7].lstrip() for i in titles]
        return titles