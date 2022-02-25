import datetime

class album:
    def __init__(self, pa, artist, title, originallyAvailableAt, viewedLeafCount = 0, leafCount = 0):
        self.artist = artist
        self.title = title
        self.originallyAvailableAt = originallyAvailableAt
        self.day = originallyAvailableAt.day
        self.month = originallyAvailableAt.month
        self.year = originallyAvailableAt.year
        self.leafCount = leafCount
        self.viewedLeafCount = viewedLeafCount
        self.age = self.get_age()
        self.plex_album = pa

    def print_album_age(self):
        print(f'{self.artist} - {self.title} - {self.age} years ago')

    def print_album_with_count(self):
        print(f'{self.artist} - {self.title} - {self.viewedLeafCount}/{self.leafCount}')

    def get_age(self):
        dt = datetime.datetime.today()
        return dt.year - self.originallyAvailableAt.year