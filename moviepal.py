#!/usr/bin/python3
import re
import webbrowser
import json
from re import findall
from time import sleep

from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd


class EarningsCell():
    def __init__(self, match):
        self.daily_gross = match['daily_gross']
        self.percent_change = match['percent_change']
        self.average = match['average']
        self.total_gross = match['total_gross']
        self.day_number = match['day_number']

    def __str__(self):
        return f'Daily:{self.daily_gross} Change:{self.percent_change} Average:{self.average} Total:{self.total_gross} Day:{self.day_number}'

class mp():
    url = 'http://www.omdbapi.com/'
    parameters = {'apikey': ''}

    # TODO setting the pandas options here is really gross.
    # TODO consider not printing right from the dataframe in boxoffice (or elsewhere)
    pd.set_option('display.height', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_colwidth', 500)

    def __init__(self):
        pass

    def api(self):
        with open('config.json', 'r') as keyfile:
            apikey = json.load(keyfile)["omdb_api_key"]
            site = 'http://www.omdbapi.com/apikey.aspx'
            if apikey in ["KEYHERE", ""]:
                sitevisit = input(
                    f"API Key not found in 'config.json'.\nIt is currently: '{apikey}'.\nWoud you like to visit the site to obtain one (Y/N)? ")
                if sitevisit in ['Yes', 'Y', 'y', 'yes', 'Of Course']:
                    webbrowser.open(site)
                else:
                    raise SystemExit(f'\nERROR: OMDB API Key Missing.\nPlease visit: {site}')

            mp.parameters['apikey'] = apikey

    def _convert_title(self, content):
        match = re.match(r'(?P<title>[A-Z0-9\.\?\-",\(\)\s:]+)[A-Z]{1}.*', content)
        return match['title'].title() if match else content

    def _convert_earnings_cell(self, content):
        match = re.match(
            r'(?P<daily_gross>\$[\S]*) (?P<percent_change>--|[+-].*%) / (?P<average>\$[^\$]+)(?P<total_gross>\$[^\$]+) / (?P<day_number>\d{1,3})',
            content)
        return EarningsCell(match) if match else content

    def _convert_date_col_header(self, content):
        match = re.match(r'.*(?P<date>\d\d?/\d\d?).*', content)
        return match['date'] if match else content


    def boxoffice(self):
        # TODO stop hard coding the URL
        url = 'http://www.boxofficemojo.com/daily/chart/?view=7day&sortdate=2018-05-25&p=.htm'
        converters = {
            1: self._convert_title,
            2: self._convert_earnings_cell,
            3: self._convert_earnings_cell,
            4: self._convert_earnings_cell,
            5: self._convert_earnings_cell,
            6: self._convert_earnings_cell,
            7: self._convert_earnings_cell,
            8: self._convert_earnings_cell
        }

        df = pd.read_html(io=url,
                          header=0,
                          match='Rank\*',
                          skiprows=3,
                          converters=converters)[0][:-1]

        df.fillna('Not Available', inplace=True)

        # Rename the column headers.
        df.rename(mapper=self._convert_date_col_header,
                  axis='columns',
                  inplace=True)

        # TODO decide if you want to print out more than just the current day's results
        # TODO perhaps consider returning the dataframe or the string version of it instead of printing
        print(df.iloc[:, :3])


    def rotten(self):
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
            final_json = json.loads(final_json[0])
        except IndexError:
            SystemExit('Error fetching data. Please retry.')
        finally:
            final_json = [i['title'] for i in final_json]
        return final_json

    def imdb(self):
        source = get(
            'http://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth_1').text
        soup = bs(source, 'lxml')
        titles = soup.find_all('td', {"class": "overview-top"})
        titles = [i.h4.a.text[:-7].lstrip() for i in titles]
        return titles

    def metac(self):
        ua_one = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
        ua_two = 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        headers = {'User-Agent': ua_one + ua_two}
        source = get(
            'http://www.metacritic.com/browse/movies/release-date/theaters/metascore', headers=headers).text
        soup = bs(source, 'lxml')
        imdb_movies = soup.find_all(
            'div', {'class': 'browse_list_wrapper wide'})

        titles_list = []
        for i in imdb_movies:
            scraped_titles = i.find_all('div', {'class': 'title'})
            titles = [title.text.rstrip().lstrip() for title in scraped_titles]
            titles_list.append(titles)
        return sum(titles_list, [])

    def in_theaters(self, key=""):
        key = key.lower()
        if key == "imdb":
            return mp.imdb()
        if key in ["rt", "rottentomatoes", "rotten tomatoes"]:
            return mp.rotten()
        if key in ['meta', 'metac', 'metacritic', 'mtc']:
            return mp.metac()
        all_titles = mp.merged_titles()
        print(f'Requesting {len(all_titles)} items...')
        return

    def requester(self, key=""):
        rqst = get(mp.url, params=mp.parameters).json()
        print(rqst)
        print()
        sleep(0.05)
        movie = rqst
        if key == "":
            return movie
        try:
            return movie[key]
        except KeyError:
            raise SystemExit(f'That key doesn\'t seem available.\n Try any of these keys:\n\n{list(movie.keys())}')

    def merged_titles(self):
        tomatoes = mp.rotten()
        for i in mp.imdb():
            tomatoes.append(i)
        for i in mp.metac():
            tomatoes.append(i)
        return set(tomatoes)

    def search_title(self, search_term, key=""):
        mp.parameters['t'] = self
        return mp.requester(key)

    def search_id(self, search_term, key=""):
        mp.parameters['i'] = self
        return mp.requester(key)

    def rotten_search(movie, search_term, key="", printer=False):

        source = get(
            f'https://www.rottentomatoes.com/search/?search={movie}').text
        soup = bs(source, 'lxml')
        rotten_results = soup.find_all('script')
        for i in rotten_results:
            scraped_json = i.text.rstrip().lstrip()
            if scraped_json.startswith(
                    ("require(['jquery', 'globals', 'search-results',",
                     "'bootstrap'], function($, RT, mount)")):
                movies = findall('({.*})', scraped_json)[0]
                movies = json.loads(movies)

                if key == 'print':
                    printer = True

                if key == 'verbose':
                    links = [i["url"] for i in movies["movies"]]
                    for url in links:
                        mp.rotten_scraper(url, key='slug')

                if printer == True:
                    return mp.super_sort(movies)
                return movies

    def rotten_scraper(self, entry, the_year='', key=''):
        rotten_link = 'https://www.rottentomatoes.com{}{}{}'

        def link_mangler(entry):
            return entry.lower().replace(" ", "_")

        def the_url(year):

            if key == 'slug':
                link = rotten_link.format(entry, '', '')
            else:
                link = rotten_link.format('/', link_mangler(entry), year)
            return link

        def perform(source):
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
                    'div', {'class': 'audience-score'}).find(
                    'div', {'class': 'noScore'}).text

            titles = soup.find('script', {'id': 'jsonLdSchema'}).text
            titles = json.loads(titles.encode('ascii', 'ignore').decode('ascii'))
            try:
                rotten_rating = str(
                    titles["aggregateRating"]["ratingValue"]) + "%"
            except KeyError:
                rotten_rating = 'Tomatometer Not Available'

            the_ratings = {"AudienceRating": audience_review,
                           "AverageRating": rotten_rating}
            if key == '':
                return the_ratings
            mp.sorter(the_ratings)
            print()

        def get_this(year):
            if year == '':
                return get(the_url(year))
            return get(the_url(f'_{year}'))

        if get_this(the_year).status_code == 404:
            raise SystemExit(
                "404 ERROR: \nThat didn't seem to work. Try entering a year or a different title.")
        return perform(get_this(the_year))

    def search(self, search_term, key=""):
        mp.parameters['s'] = self
        rqst = get(mp.url, params=mp.parameters)
        movie = rqst.json()["Search"]

        if key == "":
            return mp.key_loop(movie)

        items = []
        for i in movie:
            try:
                items.append(i[key])
            except KeyError:
                raise SystemExit(f'"{key}" is not an available key.',
                                 '\nTry: "Poster", "Title", "imdbID", or "Year"\n')
        return mp.looper(items)

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
                        print(str(movie).encode(
                            'ASCII', "ignore").decode('ascii'))
                        print()
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

    def query(self, key="", the_site=""):
        if key == "":
            raise SystemExit('query() requires a key')
        the_query = mp.display(mp.in_theaters(key=key), key=key)
        return the_query

    def sorter(self, iterable_to_be_sorted):
        # TODO this doesn't sort anything??
        keys = list(iterable_to_be_sorted)
        for i in keys:
            print(f'{i}: {iterable_to_be_sorted[i]}')

    def looper(self, iterable_to_be_looped_over):
        for i in iterable_to_be_looped_over:
            if isinstance(i, dict):
                mp.key_loop(i)
            else:
                print(i)

    def key_loop(self, dict_to_be_looped_over):
        for i in dict_to_be_looped_over:
            for key, value in i.items():
                print(f'{key}: {value}')
            print()

    def super_sort(self, data, dict_key="movies"):
        # TODO this doesn't sort anything??
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


