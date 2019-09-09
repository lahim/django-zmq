from django.core.management.base import BaseCommand

from djangozmq.zmq import slave


class Command(BaseCommand):
    help = 'Runs ZMQ slave'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Slave is running...'))
        slave.run()
