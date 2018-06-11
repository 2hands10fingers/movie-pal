#!/usr/bin/python3
from moviepal import mp
import webbrowser
import os


class HtmlGen():
    """Generates necessary HTML when called upon"""

    def __init__(self):
        pass

    def ascii_clean(self):
        return self.encode('ascii', 'ignore').decoode('ascii')

    def imgcheck(image, title):
        if image == 'N/A':
            return (f'<img src="img/popcorn.png" alt="{title}">')
        return (f'<img src="{image}" alt="{title}">')

    with open('ui/index.html', 'w') as file:
        print('Creating HTML Header')
        file.write(f'''
        <html>
            <head>
                <title>🎥 Movie Pal</title>
                <script
                    src="https://code.jquery.com/jquery-3.3.1.min.js"
                    integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
                    crossorigin="anonymous">
                </script>
                <script 
                    src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" 
                    integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" 
                    crossorigin="anonymous">
                </script>
                <script 
                    type="text/javascript" 
                    src="../ui/js/SheetClip.js"></script>
                <script
                    type="text/javascript"
                    src="../ui/js/copydata.js"
                    ></script>
                <link
                    href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css"
                    rel="stylesheet"
                    integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB"
                    crossorigin="anonymous">
                <link
                    rel="stylesheet"
                    href="https://use.fontawesome.com/releases/v5.0.13/css/all.css"
                    integrity="sha384-DNOHZ68U8hZfKXOrtjWvjxusGo9WQnrNx2sqG0tfsghAvtVlRW3tvkXWZh58N9jp"
                    crossorigin="anonymous">
                <link
                    href="https://fonts.googleapis.com/css?family=Source+Sans+Pro"
                    rel="stylesheet">
                <link
                    rel="stylesheet"
                    href="styles/main.css">
            </head>
            <body>
                <div class="movies--wrapper">
                  <div data-toggle="modal" data-target="#myModal" class="nav-mp">Search</div>
                    <div class="movies--container container">
                        ''')
        print('Gathering film titles...')
        movies = mp.display(mp.query(key="Title"))
        print('Creating film entities...')
        for movie in movies:
            try:
                (title, ratings, boxoffice, genre,
                 _type, poster, runtime, plot, imdbid) = (
                    movie["Title"],
                    movie["Ratings"],
                    movie["BoxOffice"],
                    movie["Genre"],
                    movie["Type"],
                    movie["Poster"],
                    movie["Runtime"],
                    str(movie["Plot"]),
                    movie["imdbID"]

                )
                rotten, imdb, mtc = '', '', ''
                try:
                    file.write(f'''<div class="movie--container">
                                <a target="_blank" href="https://imdb.com/title/{imdbid}">
                                    <h3>{title}</h3>
                                </a>
                                <div class="movie--data">
                                    <div class="movie--left">
                                        <a target="_blank" href="https://imdb.com/title/{imdbid}">
                                        {imgcheck(poster, title)}
                                        </a>
                                    </div>
                                <div class="movie--right">
                                <div class="boxoffice">
                                        <span class="boxoffice--icon far fa-money-bill-alt"></span>
                                        <span class="boxoffice--result">{boxoffice}</span>
                                    </div>''')
                except UnicodeEncodeError:
                    pass

                for i in ratings:

                    if i['Source'] == 'Rotten Tomatoes':
                        value, rotten = i["Value"], i["Value"]

                        file.write(f'''<div class="review--rt">
                                        <span class="review--rt-icon"><img src="img/tomato.png"></span>
                                        <span class="review--rt-result">{value}</span>
                                      </div>''')
                    elif i['Source'] == 'Metacritic':
                        value, mtc = i["Value"], i["Value"]

                        file.write(f'''<div class="review--metac">
                                        <span class="review--metac-icon"><img src="img/mtc-icon.png"></span>
                                        <span class="review--metac-result">{value}</span>
                                    </div>''')
                    elif i['Source'] == 'Internet Movie Database':
                        value, imdb = i["Value"], i["Value"]

                        file.write(f'''<div class="review--imdb">
                                        <span class="review--imdb-icon fab fa-imdb"></span>
                                        <span class="review--imdb-result">{value}</span>
                                    </div>''')

                file.write(f''' </div>
                            </div>
                        <div class="plot--container">
                            <p>{plot}</p>
                        </div>
                        <div class="link--wrapper">
                            <a href="#">Copy Data</a>
                            <textarea 
                                class="datarow"
                                data-plot='{plot.replace("'", " ")}'
                                data-rotten="{rotten}"
                                data-imdb="{imdb}"
                                data-mtc="{mtc}"
                                data-boxoffice="{boxoffice}"
                                data-genre="{genre}"
                                data-runtime="{runtime}"
                                data-title="{title}"
                                >
                            </textarea>
                        </div>
                        </div>''')
            except KeyError:
                pass
            except UnicodeEncodeError:
                pass

        file.write(f'''</div></div>
                        <div class="copy-all">
                        <span>Copy All</span>
                        </div>
                        <div class="modal" id="myModal" tabindex="-1" role="dialog">
                            <div class="modal-dialog modal-dialog-centered" role="document">
                                <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Get Film Info</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div class="modal-body">
                                    
                                    <input id="search">
                                    <button type="button" onclick="inputGrabber()"><i class="fas fa-search"></i></button>
                                    <input class="searchinput" type="checkbox"><span class="discover">Discover</span></radio>
                                
                                    
                                    <script src="../config.js"></script>
                                    <script src="js/search.js" type="text/javascript"></script>
                                
                                    </input>
                                
                                    <div class="data">
                                    <!-- data here -->
                                    </div>
                                </div>
                                <div class="modal-footer">
                                   <div class="footer-deco"></div>
                                </div>
                                </div>
                            </div>
                            </div>
        </body></html>''')

print('Enjoy!')
webbrowser.open('file://' + os.path.abspath('ui/index.html'))
