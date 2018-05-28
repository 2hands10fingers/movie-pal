#!/usr/bin/python3
import argparse
from moviepal import mp

parser = argparse.ArgumentParser(
    description="CLI for generating moviea data from IMDB and Rotten Tomatoes")
parser.add_argument("-s", "--search", type=str,
                    help="""Search any movie title.
                    Add a 'key' argument to find specific datapoint i.e. Ratings, Title, Plot, etc.""")
parser.add_argument("-k", "--key",
                    type=str, help="Use this to search for a specific datapoint when searching")
parser.add_argument("-t", "--search_title", type=str,
                    help="Search the API for a title")
parser.add_argument("-id", "--search_id", type=str,
                    help="Search the API by IMDB ID")
parser.add_argument("-ui", "--generate", action="store_true",
                    help="Search the API by IMDB ID")

parser.add_argument("-rtscore", "--rotten_score", type=str,
                    help="Tries to scrapes a Rotten Tomatoes page for a given title")
parser.add_argument("-rtn", '--rotten_search', type=str,
                    help="Search Rotten Tomatoes to see available titles")
parser.add_argument("-it", "--in_theaters", action="store_true",
                    help=("Displays information about all movies in theaters.",
                          " Limit it to the site by setting key to rt, imdb, or meta"))
parser.add_argument("-box", "--boxoffice", action="store_true",
                    help=("Displays boxoffice numbers for all movies in theaters."))

args = parser.parse_args()


def main():
    movie_pal = mp()
    print("Processing arguments...\n")
    if args.key is None:
        args.key = ''
    if args.search:
        movie_pal.search(args.search, key=args.key)
    if args.search_title:
        movie = movie_pal.search_title(args.search_title, key=args.key)
        if args.key == '':
            movie_pal.sorter(movie)
        else:
            print(movie)

    if args.search_id:
        movie = movie_pal.search_id(args.search_id, key=args.key)
        if args.key == '':
            movie_pal.sorter(movie)
        else:
            print(movie)
    if args.generate:
        import htmlgen
    if args.rotten_score:
        movie_pal.sorter(movie_pal.rotten_scraper(args.rotten_score, the_year=args.key))
    if args.rotten_search:
        movie_pal.rotten_search(args.rotten_search, key=args.key, printer=False)
        print('\nSearch Complete!')
    if args.in_theaters:
        x = movie_pal.display(movie_pal.in_theaters(key=args.key))
        movie_pal.key_loop(x)
    if args.boxoffice:
        movie_pal.boxoffice()


if __name__ == '__main__':
    main()
