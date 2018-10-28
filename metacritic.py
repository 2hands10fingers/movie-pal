from bs4 import BeautifulSoup as bs
from requests import get
from headers import headers
class metacritic():
	def headers():
        ua_one = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
        ua_two = 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        headers = {'User-Agent': ua_one + ua_two}
        return headers

	def metac():
        source = get(
            'http://www.metacritic.com/browse/movies/release-date/theaters/metascore', headers=headers.headers()).text
        soup = bs(source, 'lxml')
        imdb_movies = soup.find_all(
            'div', {'class': 'browse_list_wrapper wide'})

        titles_list = []
        for i in imdb_movies:
            scraped_titles = i.find_all('div', {'class': 'title'})
            titles = [title.text.rstrip().lstrip() for title in scraped_titles]
            titles_list.append(titles)
        return sum(titles_list, [])