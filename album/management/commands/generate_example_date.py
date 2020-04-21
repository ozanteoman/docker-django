from django.core.management import BaseCommand
from django.utils.crypto import get_random_string

from album.models import Song, Album, Artist


class Command(BaseCommand):
    help = "this manage command will generate the sampling data to use on working"
    bound = 100

    @staticmethod
    def _generate_random_first_name_and_last_name():
        return get_random_string(), get_random_string()

    @staticmethod
    def _generate_random_title_and_description():
        return get_random_string(), get_random_string()

    @staticmethod
    def _generate_random_song_name():
        return get_random_string()

    def _create_songs_of_album(self, album):
        for i in range(self.bound):
            name = self._generate_random_song_name()
            album.song.create(name=name)

    def _create_albums_of_artist(self, artist):
        for i in range(self.bound):
            title, description = self._generate_random_title_and_description()
            created_album = artist.album.create(**{'title': title, 'description': description})
            self._create_songs_of_album(created_album)

    def handle(self, *args, **options):
        print("it's time to run")
        # delete all of instances before execute the command
        Song.objects.all().delete()
        Album.objects.all().delete()
        Artist.objects.all().delete()

        for i in range(self.bound):
            first_name, last_name = self._generate_random_first_name_and_last_name()
            created_artist = Artist.objects.create(**{'first_name': first_name, 'last_name': last_name})
            self._create_albums_of_artist(created_artist)
            print(f"The artis is {created_artist}")

        print("it's time to sleep")
