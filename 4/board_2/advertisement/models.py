from django.db import models
from django.contrib.auth.models import User


def product_preview_directory_path(instanse: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(pk=instanse.pk, filename=filename)


def product_images_directory_path(instanse: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(pk=instanse.product.pk, filename=filename)


class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]
        #db_table = "tech_products" Обращение к другой таблице
        #verbose_name_plural = "products"

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2) #Для цен, длинна 8, после занятой 2
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"

    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     else:
    #         return self.description[:48] + "..."


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
    receipt = models.FileField(null=True, upload_to='orders/receipts/')


class Advertisement(models.Model):
    title = models.CharField(max_length=1500)
    description = models.TextField(max_length=1000, default='', verbose_name='описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.FloatField(verbose_name='цена', default=0)
    views_count = models.IntegerField(verbose_name='количество просмотров', default=0)
    status = models.ForeignKey('AdvertisementStatus', default=None, null=True, on_delete=models.CASCADE,
                               related_name='advertisement')
    adv_type = models.ForeignKey('AdvertisementType', default=None, null=True, on_delete=models.CASCADE,
                                 related_name='advertisement')

    def __str__(self):
        return self.title


class AdvertisementStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AdvertisementType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name