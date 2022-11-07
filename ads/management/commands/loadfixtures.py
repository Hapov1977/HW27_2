import os
import subprocess

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Loads fixtures from dataset dir"
    fixtures_dir = 'datasets'
    convert_data_command = subprocess.Popen(["python", os.path.join(fixtures_dir, "convert_csv_to_json.py")])
    loadfixtures_command = 'loaddata'
    filenames = [
        "location.json",
        "category.json",
        "user.json",
        "ad.json",
    ]

    def handle(self, *args, **options):
        for fixture_filename in self.filenames:
            if self.convert_data_command.poll():
                self.convert_data_command.terminate()
            call_command(self.loadfixtures_command, os.path.join(self.fixtures_dir, fixture_filename))
            print(f'Fixture {fixture_filename} loaded into database')
