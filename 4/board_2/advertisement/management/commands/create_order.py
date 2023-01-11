from django.core.management import BaseCommand
from django.contrib.auth.models import User
from advertisement.models import Order


class Command(BaseCommand):
    """Создание новых заказов"""
    def handle(self, *args, **options):
        self.stdout.write("Создаём новые заказы")
        user = User.objects.get(username="admin")
        order = Order.objects.get_or_create(
            delivery_address="ul Ibragimova, d 8",
            promocode="SALE123",
            user=user
        )
        self.stdout.write(f"Создан заказ {order}")