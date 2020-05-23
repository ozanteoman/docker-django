from django.core.management.base import BaseCommand

from album.models import Song, Category


class Command(BaseCommand):
    help = "add bulk album"

    def handle(self, *args, **options):
        self.stdout.write("Started to Add Categories To Songs")
        all_category_ids = list(Category.objects.all().values_list('pk', flat=True))
        for song in Song.objects.all():
            song.category.add(*all_category_ids)

        self.stdout.write("Finished to Add Categories To Songs")
