import time
from django.db import connection, reset_queries

from album.models import Song


class UsingSelectRelated(object):

    @staticmethod
    def _starting_count_of_queries():
        print("------START---------")
        # reset the queries before running
        reset_queries()

        # should return 0
        start_queries_count = len(connection.queries)
        print(f"in start the count of the queries is equal to {start_queries_count}")

    @staticmethod
    def _fetched_count_of_queries():
        fetched_queries_count = len(connection.queries)
        print(f"fetched count of queries is equal to {fetched_queries_count}")
        print("---------END------------")

    def _append_songs_to_list(self, all_songs):
        self._starting_count_of_queries()
        # start the timing
        start = time.perf_counter()

        songs = []
        for song in all_songs[:1000]:
            songs.append({"song_name": song.name, "album_name": song.album.title, "artist_name": song.album.artist.first_name})
        end = time.perf_counter()

        print(f"Finished in : {(end - start):.2f}s")
        self._fetched_count_of_queries()

    def example_one(self):
        self._starting_count_of_queries()
        # hit the database
        song = Song.objects.get(id=20)

        # hit the database again to get album's instance that related to song
        album = song.album
        print(album.title)

        self._fetched_count_of_queries()

    def example_two(self):
        self._starting_count_of_queries()
        # hit the database
        song = Song.objects.select_related('album').get(id=21)

        # does not hit the database because song.album has been prepopulated
        # in the previous query
        album = song.album
        print(album.title)

        self._fetched_count_of_queries()

    def example_three(self):
        def _example_three_one():
            list_of_song_name = []
            album_id = 2
            self._starting_count_of_queries()

            all_songs_without_select_related = Song.objects.filter(album_id=album_id)
            for song in all_songs_without_select_related:
                # will hit the database for each of song's album
                list_of_song_name.append(song.album.title)

            self._fetched_count_of_queries()

        def _example_three_two():
            list_of_song_name = []
            album_id = 2
            self._starting_count_of_queries()
            all_songs_without_select_related = Song.objects.filter(album_id=album_id).select_related('album')
            for song in all_songs_without_select_related:
                list_of_song_name.append(song.album.title)

            self._fetched_count_of_queries()

        _example_three_one()
        _example_three_two()

    def example_four(self):
        # it doesn't matter where are the order of filter and select_related
        # result is the same.
        self._starting_count_of_queries()

        songs = Song.objects.select_related('album').filter(id=21)

        for song in songs:
            print(song.name, song.album.title)

        self._fetched_count_of_queries()

        ######
        self._starting_count_of_queries()
        songs = Song.objects.filter(id=21).select_related('album')
        for song in songs:
            print(song.name, song.album.title)

        self._fetched_count_of_queries()

    def example_five(self):
        def _example_five_without_select_related():
            self._starting_count_of_queries()
            song = Song.objects.get(id=5)  # hit the database one time
            album = song.album  # hit the database one more time
            artist = album.artist  # hit the database one more time
            print(artist.first_name, album.title, song.name)
            self._fetched_count_of_queries()

        def _example_five_with_select_related():
            self._starting_count_of_queries()
            song = Song.objects.select_related('album__artist').get(id=6)  # hit once
            album = song.album  # does not hit the database
            artist = album.artist  # does not hit the database
            print(artist.first_name, album.title, song.name)
            self._fetched_count_of_queries()

        _example_five_with_select_related()
        _example_five_without_select_related()

    def example_six(self):
        self._starting_count_of_queries()
        # using of select_related without keyword
        songs = Song.objects.select_related().all()
        print(songs.first().name)
        # prevent needless using of select_related
        songs_without_select_related = songs.select_related(None)
        print(songs_without_select_related.first().name)
        print(self._fetched_count_of_queries())

    def example_seven(self):
        all_songs = Song.objects.all()
        self._append_songs_to_list(all_songs)

    def example_eight(self):
        all_songs = Song.objects.all().select_related('album__artist')
        self._append_songs_to_list(all_songs)
