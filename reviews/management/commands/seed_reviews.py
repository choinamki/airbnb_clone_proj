from django.core.management.base import BaseCommand
from reviews.models import Review


class Command(BaseCommand):

    help = 'This command creates Reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', type=int, default=1, help='How many reviews do you want to create'
        )


    def handle(self, *args, **options):


        self.stdout.write(self.style.SUCCESS('Reviews created!'))