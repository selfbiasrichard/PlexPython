import datetime

class album:
    def __init__(self, artist, title, originallyAvailableAt):
        self.artist = artist
        self.title = title
        self.originallyAvailableAt = originallyAvailableAt
        self.day = originallyAvailableAt.day
        self.month = originallyAvailableAt.month
        self.year = originallyAvailableAt.year
        self.age = self.getAge()

    def printAlbum(self):
        print(f'{self.artist} - {self.title} - {self.age} years ago')

    def getAge(self):
        dt = datetime.datetime.today()
        return dt.year - self.originallyAvailableAt.year