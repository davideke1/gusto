# your_app/management/commands/populate_sports.py

from django.core.management.base import BaseCommand
from main.models import Sport

class Command(BaseCommand):
    help = 'Populate sports in the Sport model'

    def handle(self, *args, **options):
        sports_list = [
            "Badminton Singles M",
            "Badminton Singles W",
            "Badminton Doubles W",
            "Badminton Mixed",
            "Badminton Doubles M",
            "Cricket M",
            "Volleyball M",
            "Throwball W",
            "Football W",
            "Football M",
            "Powerlifting M",
            "Powerlifting W",
            "Kabaddi M",
            "Kabaddi W",
            "Chess",
            "Basketball M",
            "Basketball W",
            "Table Tennis Singles M",
            "Table Tennis Doubles M",
        ]

        for sport_name in sports_list:
            Sport.objects.get_or_create(name=sport_name)

        self.stdout.write(self.style.SUCCESS('Sports added successfully'))
