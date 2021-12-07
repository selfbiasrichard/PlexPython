from plexapi.server import PlexServer
from scr.Album import album
from configparser import ConfigParser
import datetime
import csv

def main():
    config = ConfigParser()
    config.read('scr/Config/config.ini')
    plexconfig = config['PLEX']
    baseurl = plexconfig.get('URL')
    token = plexconfig.get('TOKEN')
    plex = PlexServer(baseurl, token)
    #getalbumsreleasedtoday(plex)
    getallalblumsreleaseddates(plex)

def getallalblumsreleaseddates(plex):
    albums = []
    music = plex.library.section(f"Music")
    for plexalbum in music.search(libtype="album"):
        if (plexalbum.originallyAvailableAt != None):
            albums.append(album(plexalbum.parentTitle, plexalbum.title, plexalbum.originallyAvailableAt))

    writetocsv(albums)

def getalbumsreleasedtoday(plex):
    albums = []
    dt = datetime.datetime.today()
    music = plex.library.section(f"Music")
    for plexalbum in music.search(libtype="album"):
        if (plexalbum.originallyAvailableAt != None
                and plexalbum.originallyAvailableAt.month == dt.month
                and plexalbum.originallyAvailableAt.day == dt.day):
            albums.append(album(plexalbum.parentTitle, plexalbum.title, plexalbum.originallyAvailableAt))

    printandwrite(albums)

def printandwrite(albums):
    dt = datetime.datetime.today()
    albums.sort(key=lambda x: x.age, reverse=True)

    for a in albums:
        a.printAlbum()

def writetocsv(albums):
    albums.sort(key=lambda x: (x.year, x.month, x.day), reverse=True)

    pathtosave = getpathconfig()
    with open(pathtosave, mode='w', encoding="utf-8", newline='') as csv_file:
        fieldnames = ['title', 'artist', 'year', 'month', 'day']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for album in albums:
            writer.writerow({'title': album.title, 'artist': album.artist, 'year': album.year, 'month': album.month, 'day': album.day})

def getpathconfig():
    config = ConfigParser()
    config.read('scr/Config/config.ini')
    pathconfig = config['PATHS']
    return pathconfig.get('CSVLOCATION')

if __name__ == "__main__":
    main()