from bs4 import BeautifulSoup as bs
from requests import get
from re import findall
from json import loads, load
class rotten_tomatoes():

	def rotten_search(movie, key="", printer=False):
        url = f'https://www.rottentomatoes.com/search/?search={movie}'
        source = get(url).text
        soup = bs(source, 'lxml')
        rotten_results = soup.find_all('script')
        for i in rotten_results:
            scraped_json = i.text.rstrip().lstrip()
            if scraped_json.startswith(
                    ("require(['jquery', 'globals', 'search-results',",
                        "'bootstrap'], function($, RT, mount)")):
                movies = findall('({.*})', scraped_json)[0]
                movies = loads(movies)

                if key == 'print':
                    printer = True

                if key == 'verbose':
                    links = [i["url"] for i in movies["movies"]]
                    for url in links:
                        rotten_scraper(url, key='slug')

                if printer == True:
                    return super_sort(movies)
                return movies

    def rotten_scraper(entry, the_year='', key=''):
        rotten_link = 'https://www.rottentomatoes.com{}{}{}'

        def link_mangler(entry):
            return entry.lower().replace(" ", "_")

        def the_url(year):
            if key == 'slug':
                link = rotten_link.format('/m/', entry, '')
            else:
                link = rotten_link.format('/m/', link_mangler(entry), year)
            return link

        def perform(source):
            the_page = source.text
            soup = bs(the_page, 'lxml')
            audience_review = ''
            rotten_rating = ''

            print('-' * 20)
            print(f'Page Title: "{soup.find("title").text}"\n')

            try:
                audience_review = soup.find(
                    'div',
                    {'class': 'audience-score'}).find(
                    'div',
                    {'class': 'meter-value'}).span.text
            except AttributeError:
                audience_review = soup.find(
                    'div', {'class': 'audience-score'}).find(
                        'div', {'class': 'noScore'}).text

            titles = soup.find('script', {'id': 'jsonLdSchema'}).text
            titles = loads(titles.encode('ascii', 'ignore').decode('ascii'))
            try:
                rotten_rating = str(
                    titles["aggregateRating"]["ratingValue"]) + "%"
            except KeyError:
                rotten_rating = 'Tomatometer Not Available'

            the_ratings = {"AudienceRating": audience_review,
                           "AverageRating": rotten_rating}
            if key == '':
                return the_ratings
            sorter(the_ratings)
            print()

        def get_this(year):
            if year == '':
                return get(the_url(year))
            return get(the_url(f'_{year}'))

        if get_this(the_year).status_code == 404:
            raise SystemExit(
                "404 ERROR: \nThat didn't seem to work. Try entering a year or a different title.")
        return perform(get_this(the_year))

    def super_sort(data, dict_key="movies"):
        for movie in data[dict_key]:
            print('-' * 20)
            for k, v in movie.items():
                if isinstance(movie[k], list):
                    if k == 'castItems':
                        print('Cast:')
                    else:
                        print(f'{k}:')
                    for x in movie[k]:
                        if isinstance(x, dict):
                            for key, value in x.items():
                                if key == "url":
                                    print(f'\t\t{key}: https://rottentomatoes.com{value}')
                                else:
                                    print(f'\t{key}: {value}')
                else:
                    print(f'{k}: {v}')

	def sorter(self):
        keys = list(self)
        for i in keys:
            print(f'{i}: {self[i]}')


	def rotten():
        source = get('''https://www.rottentomatoes.com/
                    browse/in-theaters?minTomato=0
                    &maxTomato=100
                    &minPopcorn=0
                    &maxPopcorn=100
                    &genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=release''').text
        soup = bs(source, 'lxml')
        js_source = soup.find_all("script")[38].prettify()
        final_json = findall('\[{.*}\]', js_source)
        try:
            final_json = loads(final_json[0])
        except IndexError:
            SystemExit('Error fetching data. Please retry.')
        finally:
            final_json = [i['title'] for i in final_json]
        return final_json

    def sorter(self):
        keys = list(self)
        for i in keys:
            print(f'{i}: {self[i]}')