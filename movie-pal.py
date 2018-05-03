from bs4 import BeautifulSoup as bs
from requests import get
import pprint

class Movie(object):
	"""docstring for Movie"""
	def __init__(self, the_title, the_ratings, the_year, 
		     the_boxoffice, in_the_theaters):
		
		self.the_title = the_title
		self.the_ratings = the_ratings
		self.the_year = the_year
		self.the_boxoffice = the_boxoffice
		self.in_the_theaters = in_the_theaters

	@property
	def in_theaters(self):
		return self.in_the_theaters

	@property
	def boxoffice(self):
		return self.the_boxoffice

	@property
	def year(self):
		return self.the_year

	@property
	def ratings(self):
		return self.the_ratings
	
	@property
	def title(self):
		return self.the_title



class omdb(object):
	"""Main object for OMDB search"""
	
	url = 'http://www.omdbapi.com/'
	parameters = {'apikey' : ''}

	def __init__(self):
		pass

	def in_theaters():
		source = get('http://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth_1').text
		soup = bs(source, 'lxml')
		titles = soup.find_all('td', { "class" : "overview-top" })
		titles = [i.h4.a.text[:-7].lstrip() for i in titles]
		return titles

	def requester():
		rqst = get(omdb.url, params=omdb.parameters).json()
		json_wrap = []
		json_wrap.append(rqst)
		movie = json_wrap[0]
		title = movie['Title']
		ratings = movie['Ratings']
		year = movie['Year']
		box_office = movie["BoxOffice"]
		in_theaters = omdb.in_theaters()
		
		return Movie(title, ratings, year, 
			     box_office, in_theaters )

	def search_title(self):
		omdb.parameters['t'] = self
		return omdb.requester()
