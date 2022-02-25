from plexapi.server import PlexServer
from scr.Album import album
from configparser import ConfigParser
import datetime
import csv
from scr.Enums import SortType, PrintType


def main():
    print("1. Get Albums Released Today")
    print("2. Get All Albums Released Dates")
    print("3. Get Albums Play Count")
    print("q. (Q)uit")

    ustring = input("Please enter input: ")

    if ustring.lower() == "q":
        quit()

    config = ConfigParser()
    config.read('scr/Config/config.ini')
    plex = get_plex_server(config)

    if ustring == "1":
        get_albums_released_today(plex)
    elif ustring == "2":
        get_all_albums_released_dates(plex)
    elif ustring == "3":
        get_album_play_count(plex)


def get_plex_server(config):
    plex_config = config['PLEX']
    baseurl = plex_config.get('URL')
    token = plex_config.get('TOKEN')
    return PlexServer(baseurl, token)


def get_all_albums_released_dates(plex):
    albums = []
    music = plex.library.section(f"Music")
    for plex_album in music.search(libtype="album"):
        if plex_album.originallyAvailableAt is not None:
            albums.append(album(plex_album, plex_album.parentTitle, plex_album.title, plex_album.originallyAvailableAt))

    write_age_to_csv(albums)


def get_album_play_count(plex):
    albums = []
    music = plex.library.section(f"Music")
    for plex_album in music.search(libtype="album"):
        if plex_album.originallyAvailableAt is not None:
            albums.append(album(plex_album, plex_album.parentTitle, plex_album.title, plex_album.originallyAvailableAt,
                                plex_album.viewedLeafCount, plex_album.leafCount))

    print_and_write(albums, SortType.artist, PrintType.playCount, False)


def get_albums_released_today(plex):
    albums = []
    dt = datetime.datetime.today()
    music = plex.library.section(f"Music")

    for plex_album in music.search(libtype="album"):
        if (plex_album.originallyAvailableAt is not None
                and plex_album.originallyAvailableAt.month == dt.month
                and plex_album.originallyAvailableAt.day == dt.day):
            albums.append(album(plex_album, plex_album.parentTitle, plex_album.title, plex_album.originallyAvailableAt))

    print("1. Add to playlist")
    print("2. print")
    print("3. Both")
    print("q. (Q)uit")

    ustring = input("Please enter input: ")

    if ustring.lower() == "q":
        quit()

    if ustring == "1":
        add_to_playlist(plex, "Released Today", albums)
    elif ustring == "2":
        print_and_write(albums, SortType.date, PrintType.age)
    elif ustring == "3":
        add_to_playlist(plex, "Released Today", albums)
        print_and_write(albums, SortType.date, PrintType.age)


def print_and_write(albums, order_type=SortType.date, print_type=PrintType.age, to_print=True):
    if order_type == SortType.date:
        albums.sort(key=lambda x: x.age, reverse=True)
    elif order_type == SortType.artist:
        albums.sort(key=lambda x: x.artist, reverse=True)

    if to_print:
        for a in albums:
            if print_type == PrintType.age:
                a.print_album_age()
            elif print_type == PrintType.playCount:
                a.print_album_with_count()
    else:
        write_count_to_csv(albums)


def add_to_playlist(plex, playlist_name, albums, remove_item=True, order_type=SortType.date, ):
    playlist = plex.playlist(playlist_name)

    if remove_item:
        playlist.removeItems(playlist.items())

    if order_type == SortType.date:
        albums.sort(key=lambda x: x.age, reverse=True)
    elif order_type == SortType.artist:
        albums.sort(key=lambda x: x.artist, reverse=True)

    for a in albums:
        playlist.addItems(a.plex_album.tracks())


def write_age_to_csv(albums):
    albums.sort(key=lambda x: (x.year, x.month, x.day), reverse=True)

    path_to_save = get_path_config()
    with open(path_to_save, mode='w', encoding="utf-8", newline='') as csv_file:
        fieldnames = ['title', 'artist', 'year', 'month', 'day']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for a in albums:
            writer.writerow({'title': a.title, 'artist': a.artist, 'year': a.year, 'month': a.month, 'day': a.day})


def write_count_to_csv(albums):
    albums.sort(key=lambda x: x.artist, reverse=False)

    path_to_save = get_path_config()
    with open(path_to_save, mode='w', encoding="utf-8", newline='') as csv_file:
        fieldnames = ['title', 'artist', 'count', 'total']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for a in albums:
            writer.writerow({'title': a.title, 'artist': a.artist, 'count': a.viewedLeafCount, 'total': a.leafCount})


def get_path_config():
    config = ConfigParser()
    config.read('scr/Config/config.ini')
    pathconfig = config['PATHS']
    return pathconfig.get('CSV-LOCATION')


if __name__ == "__main__":
    main()
