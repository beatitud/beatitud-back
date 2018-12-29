from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mail(
            'Subject here',
            'Here is the message.',
            'mailing-list@beatitud.io',
            ['antoine_rose@hotmail.fr'],
            fail_silently=False,
        )
