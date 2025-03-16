from django.core.management.base import BaseCommand
from scetch.utils import reset_daily_slots

class Command(BaseCommand):
    help = "Сбрасывает бронирование всех слотов на текущий день"

    def handle(self, *args, **kwargs):
        result = reset_daily_slots()
        self.stdout.write(self.style.SUCCESS(result))
