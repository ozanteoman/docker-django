from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Ekrana Hello World yazdıran komut"

    def handle(self, *args, **options):
        self.stdout.write("Hello World")
