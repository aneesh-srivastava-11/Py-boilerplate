from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")
        # Add your factory/seeding logic here
        self.stdout.write(self.style.SUCCESS("Successfully seeded data!"))
