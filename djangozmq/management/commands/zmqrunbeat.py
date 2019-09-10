from django.core.management.base import BaseCommand

from djangozmq.zmq import beat


class Command(BaseCommand):
    help = 'Runs beat for scheduled tasks'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Beat is running...'))
        beat.run()
