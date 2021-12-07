from plexapi.server import PlexServer
from scr.Album import album
from configparser import ConfigParser
import datetime
import csv


def main():
    config = ConfigParser()
    config.read('src/Config/config.ini')
    plexconfig = config['PLEX']
    baseurl = plexconfig.get('URL')
    token = plexconfig.get('TOKEN')
    plex = PlexServer(baseurl, token)
    # get_albums_released_today(plex)
    get_all_alblums_released_dates(plex)


def get_all_alblums_released_dates(plex):
    albums = []
    music = plex.library.section(f"Music")
    for plexalbum in music.search(libtype="album"):
        if plexalbum.originallyAvailableAt is not None:
            albums.append(album(plexalbum.parentTitle, plexalbum.title, plexalbum.originallyAvailableAt))

    write_to_csv(albums)


def get_albums_released_today(plex):
    albums = []
    dt = datetime.datetime.today()
    music = plex.library.section(f"Music")
    for plexalbum in music.search(libtype="album"):
        if (plexalbum.originallyAvailableAt is not None
                and plexalbum.originallyAvailableAt.month == dt.month
                and plexalbum.originallyAvailableAt.day == dt.day):
            albums.append(album(plexalbum.parentTitle, plexalbum.title, plexalbum.originallyAvailableAt))

    print_and_write(albums)


def print_and_write(albums):
    albums.sort(key=lambda x: x.age, reverse=True)

    for a in albums:
        a.print_album()


def write_to_csv(albums):
    albums.sort(key=lambda x: (x.year, x.month, x.day), reverse=True)

    pathtosave = get_path_config()
    with open(pathtosave, mode='w', encoding="utf-8", newline='') as csv_file:
        fieldnames = ['title', 'artist', 'year', 'month', 'day']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for album in albums:
            writer.writerow({'title': album.title, 'artist': album.artist, 'year': album.year, 'month': album.month,
                             'day': album.day})


def get_path_config():
    config = ConfigParser()
    config.read('scr/Config/config.ini')
    pathconfig = config['PATHS']
    return pathconfig.get('CSVLOCATION')


if __name__ == "__main__":
    main()
