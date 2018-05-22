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

args = parser.parse_args()


def main():
    print("Processing arguments...")
    if args.key is None:
        args.key = ''
    if args.search:
        print(mp.search(args.search, key=args.key))
    if args.search_title:
        movie = mp.search_title(args.search_title, key=args.key)
        if args.key == '':
            mp.sorter(movie)
        else:
            print(movie)

    if args.search_id:
        movie = mp.search_id(args.search_id, key=args.key)
        if args.key == '':
            mp.sorter(movie)
        else:
            print(movie)
    if args.generate:
        import htmlgen
    if args.rotten_score:
        mp.sorter(mp.rotten_scraper(args.rotten_score, the_year=args.key))
    if args.rotten_search:
        print(mp.rotten_search(args.rotten_search))


if __name__ == '__main__':
    main()
