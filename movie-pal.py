from bs4 import BeautifulSoup as bs
from requests import get
import pprint


class Omdb(object):
	"""Main object for OMDB search"""
	pp = pprint.PrettyPrinter()
	url = 'http://www.omdbapi.com/'
	parameters = {'apikey' : ''}

	def __init__(self):
		pass
	
	def requester():
		r = get(Omdb.url, params=Omdb.parameters)
		return r.json()

	def search_title(self, printer=None):
		Omdb.parameters['t'] = self
		if printer == True:
			Omdb.pp.pprint(Omdb.requester())
		else:
			print(Omdb.requester())

Omdb.search_title('Batman Forever', printer=True)
