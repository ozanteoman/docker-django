from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from album.models import Album


class Command(BaseCommand):
    help = "add bulk album"

    def _create_albums(self, *args, **options):
        count = options.get("count") or 10
        for index in range(count):
            title = get_random_string()
            new_object = Album.objects.create(title=title)
            self.stdout.write(f"Created album name {new_object.title}")

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int)

    def handle(self, *args, **options):
        self.stdout.write("Started to Create Albums")
        self._create_albums(*args, **options)
        self.stdout.write("Finished to Create Albums")
