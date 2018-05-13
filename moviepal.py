from bs4 import BeautifulSoup as bs
from requests import get
from re import findall
from json import loads

class mp():
    url = 'http://www.omdbapi.com/'
    parameters = {'apikey': ''}

    def __init__(self):
        pass

    def rotten():
        source = get('''https://www.rottentomatoes.com/browse/in-theaters?minTomato=0
                    &maxTomato=100
                    &minPopcorn=0
                    &maxPopcorn=100
                    &genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=release''').text
        soup = bs(source, 'lxml')
        js_source = soup.find_all("script")[38].prettify()
        final_json = findall('\[{.*}\]', js_source)
        final_json = loads(final_json[0])
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
                    elif printer == True:
                        print(movie)
                    elif printer == False and key != "":
                        try:
                            items.append(movie[key])
                        except KeyError:
                            pass
                    else:
                        items.append(movie)

            if printer == False:
                return items
        else:
            raise SystemExit("Please use a [ list ] or { set }!")

    def query(key="", the_site=""):
        the_query = mp.display(mp.in_theaters(site=the_site), key=key)
        return the_query
