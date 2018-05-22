#!/usr/bin/python3
from bs4 import BeautifulSoup as bs
from requests import get
from re import findall
from json import loads


class mp():
    url = 'http://www.omdbapi.com/'
    parameters = {'apikey': '7256b64c'}

    def __init__(self):
        pass

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

    def imdb():
        source = get(
            'http://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth_1').text
        soup = bs(source, 'lxml')
        titles = soup.find_all('td', {"class": "overview-top"})
        titles = [i.h4.a.text[:-7].lstrip() for i in titles]
        return titles

    def in_theaters(site=""):
        site = site.lower()
        if site == "imdb":
            return mp.imdb()
        if site in ["rt", "rottentomatoes", "rotten tomatoes"]:
            return mp.rotten()

        return mp.merged_titles()

    def requester(key=""):
        rqst = get(mp.url, params=mp.parameters).json()
        movie = rqst
        if key == "":
            return movie
        return movie[key]

    def merged_titles():
        tomatoes = mp.rotten()
        for i in mp.imdb():
            tomatoes.append(i)
        return set(tomatoes)

    def search_title(self, key=""):
        mp.parameters['t'] = self
        return mp.requester(key)

    def search_id(self, key=""):
        mp.parameters['i'] = self
        return mp.requester(key)

    def rotten_search(movie, key=""):
        source = get(
            f'https://www.rottentomatoes.com/search/?search={movie}').text
        soup = bs(source, 'lxml')
        rotten_results = soup.find_all('script')
        for i in rotten_results:
            stuff = i.text.rstrip().lstrip()
            if stuff.startswith(
                    "require(['jquery', 'globals', 'search-results', 'bootstrap'], function($, RT, mount)"):
                x = findall('({.*})', stuff)[0]
                movies = loads(x)
                return [movie["name"] for movie in movies["movies"]]

    def rotten_scraper(entry, the_year=''):
        rotten_link = 'https://www.rottentomatoes.com/m/{}{}'

        def link_mangler(entry):
            return entry.lower().replace(" ", "_")

        def the_url(year):
            link = rotten_link.format(link_mangler(entry), year)
            return link

        def perform(source):
            print('Connecting...')
            the_page = source.text
            soup = bs(the_page, 'lxml')
            print(f'Page Title: "{soup.find("title").text}"')
            audience_review = ''
            rotten_rating = ''
            try:
                audience_review = soup.find(
                    'div',
                    {'class': 'audience-score'}).find(
                    'div',
                    {'class': 'meter-value'}).span.text
            except AttributeError:
                audience_review = soup.find(
                    'div', {'class': 'audience-score'}).find('div', {'class': 'noScore'}).text
            titles = soup.find('script', {'id': 'jsonLdSchema'}).text
            titles = loads(titles.encode('ascii', 'ignore').decode('ascii'))
            try:
                rotten_rating = str(titles["aggregateRating"][
                                    "ratingValue"]) + "%"
            except KeyError:
                rotten_rating = 'Tomatomete Not Available'
            return {"AudienceRating": audience_review, "AverageRating": rotten_rating}

        def get_this(year):
            if year == '':
                return get(the_url(year))
            return get(the_url(f'_{year}'))

        if get_this(the_year).status_code == 404:
            raise SystemExit(
                "That didn't seem to work. Try entering a year or a different title.")
        return perform(get_this(the_year))

    def search(self, key=""):
        mp.parameters['s'] = self
        rqst = get(mp.url, params=mp.parameters)
        movie = rqst.json()["Search"]

        if key == "":
            return movie

        items = []
        for i in movie:
            try:
                items.append(i[key])
            except KeyError:
                raise SystemExit(f'"{key}" is not an available key.',
                                 '\nTry: "Poster", "Title", "imdbID", or "Year"\n')
        return items

    def display(self, printer=False, key=""):
        if isinstance(self, (list, set)):
            items = []
            for i in self:
                try:
                    movie = mp.search_title(i)
                except KeyError:
                    pass
                finally:
                    if movie["Response"] == 'False':
                        pass
                    if printer == True and key != "":
                        try:
                            print(movie[key])
                        except KeyError:
                            pass
                        except TypeError:
                            pass
                    elif printer == True:
                        print(str(movie).encode('ASCII', "ignore"))
                    elif printer == False and key != "":
                        try:
                            items.append(movie[key])
                        except KeyError:
                            pass
                        except TypeError:
                            pass
                    else:
                        items.append(movie)

            if printer == False:
                return items
        else:
            raise SystemExit("Please use a [ list ] or { set }!")

    def query(key="", the_site=""):
        if key == "":
            raise SystemExit('query() requires a key')
        the_query = mp.display(mp.in_theaters(site=the_site), key=key)
        return the_query

    def sorter(data):
        keys = list(data)
        for i in keys:
            print(f'{i}: {data[i]}')
