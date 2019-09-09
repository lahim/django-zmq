from django.core.management.base import BaseCommand

from djangozmq.zmq import master


class Command(BaseCommand):
    help = 'Runs ZMQ master'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Master is running...'))
        master.run()
