from bs4 import BeautifulSoup as bs
from requests import get

class Movie(object):
	"""docstring for Movie"""
	def __init__(self, the_title, the_ratings, the_year, the_boxoffice, in_the_theaters, the_id):
		self.the_title = the_title
		self.the_ratings = the_ratings
		self.the_year = the_year
		self.the_boxoffice = the_boxoffice
		self.in_the_theaters = in_the_theaters
		self.the_id = the_id

	@property
	def id(self):
		return self.the_id
	
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



class mp(object):
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
		rqst = get(mp.url, params=mp.parameters).json()
		json_wrap = []
		json_wrap.append(rqst)
		movie = json_wrap[0]
		title = movie['Title']
		ratings = movie['Ratings']
		year = movie['Year']
		box_office = movie["BoxOffice"]
		in_theaters = mp.in_theaters()
		the_id = movie["imdbID"]
		return Movie(title, ratings, year, 
					box_office, in_theaters, the_id)



	def search_title(self, info=False):
		# try:
		mp.parameters['t'] = self
		if info == True:
			movie = mp.requester().__dict__
			title, ratings, year, boxoffice, in_theaters, imdID = (
				movie["the_title"], movie["the_ratings"],
				movie["the_year"], movie["the_boxoffice"], 
				movie["in_the_theaters"], movie["the_id"])
			
			print('-'*60)
			print(f"{' '.join(title)}\n\nIMDBid: {imdID}\nBoxOffice: {boxoffice}\nYear: {year}\nRatings: ")
			for i in ratings:
				try:
					print(f'\t\t{i["Source"]} : {i["Value"]}')
				except KeyError:
					continue
			print('-'*60)

		else:
			return mp.requester()

	def search_id(self):
		mp.parameters['i'] = self
		return mp.requester()

	def search(self, key=""):
		mp.parameters['s'] = self
		rqst = get(mp.url, params=mp.parameters)
		movie = rqst.json()["Search"]
		
		
		if key == "":
			return movie
		items = []
		
		for i in movie:
			title, year, poster, the_id = i['Title'], i['Year'], i['Poster'], i["imdbID"]
			details = [title, year, poster, the_id]
			key = key.lower()
			
			if key == 'poster':
				items.append(poster)
			if key == 'title':
				items.append(title)
			if key == 'imdbid':
				items.append(the_id)
			if key == 'year':
				items.append(year)
		
		if not items:
			raise SystemExit(f'"{key}" is not an available key.\nTry: "Poster", "Title", "imdbID", or "Year"\n')
		return items

	def show(self, key=""):
		for i in self:
			try:
				movie = mp.search_title(i)
				title, year, ratings, boxoffice, = (
					movie.title, movie.year, 
					movie.ratings, movie.boxoffice)
			except KeyError:
				pass
			finally:
				key = key.lower()			
				if key == "":
					print(i)
				if key == "title":
					print(title)
				if key == "year":
					print(f'{title} : {year}')
				if key == "boxoffice":
					print(f'{title} : {boxoffice}')
				if key == "ratings":
					print('-'*60)
					print(f'\n{title}\n')
					for i in ratings:
						try:
							print(f'\t{i["Source"]} : {i["Value"]}')
						except KeyError:
							print("None")
							continue
					print('-'*60)
				if key == "all":
					print('-'*60)
					print(f'\n\t{" ".join(title)}\n')
					print(f'\tBox office: {boxoffice}')
					print(f'\tYear: {year}')
					print('\tRatings:')
					for i in ratings:
						try:
							
							print(f'\t\t{i["Source"]} : {i["Value"]}')
						except KeyError:
							print("s")
							continue
					print('-'*60)
