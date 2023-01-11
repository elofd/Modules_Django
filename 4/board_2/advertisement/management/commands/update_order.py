from django.core.management import BaseCommand
from advertisement.models import Product, Order

class Command(BaseCommand):
    """Добавляем продукты в заказ"""
    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write("Заказ не найден")
            return
        products = Product.objects.all()
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(self.style.SUCCESS(f"Добавили продукты {order.products.all()} в заказ {order}"))