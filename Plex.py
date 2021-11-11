from plexapi.server import PlexServer
import datetime
from AlbumInfo import album
from configparser import ConfigParser

def main():
    config = ConfigParser()
    config.read('Config/config.ini')
    plexconfig = config['PLEX']
    baseurl = plexconfig.get('URL')
    token = plexconfig.get('TOKEN')
    plex = PlexServer(baseurl, token)
    getalbumsreleasedtoday(plex)


def getalbumsreleasedtoday(plex):
    albums = []
    dt = datetime.datetime.today()
    music = plex.library.section(f"Music")
    for plexalbum in music.search(libtype="album"):
        if (plexalbum.originallyAvailableAt != None
                and plexalbum.originallyAvailableAt.month == dt.month
                and plexalbum.originallyAvailableAt.day == dt.day):
            age = dt.year - plexalbum.originallyAvailableAt.year
            albums.append(album(plexalbum.parentTitle, plexalbum.title, age))

    printandwrite(albums)


def printandwrite(albums):
    dt = datetime.datetime.today()
    albums.sort(key=lambda x: x.age, reverse=True)

    for a in albums:
        stringBulider = f'{a.artist} - {a.title} - {a.age} years ago'
        print(stringBulider)

if __name__ == "__main__":
    main()