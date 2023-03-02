from django.test import TestCase
from .utils import add_two_numbers
from django.urls import reverse, reverse_lazy
from string import ascii_letters
from random import choices
from advertisement.models import Product, Order
from django.contrib.auth.models import User, Permission
from django.conf import settings


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="user_test", password="qwerty")
        permission = Permission.objects.get(codename="view_order")
        cls.user.user_permissions.add(permission)


    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.products = Product.objects.create(
            name="Tablet_7",
            created_by=self.user
        )
        self.order = Order.objects.create(
            user=self.user,
            delivery_address="ul. Komarova, d. 12",
            promocode="abc",
        )
        self.order.products.add(self.products)

    def tearDown(self) -> None:
        self.order.delete()
        self.products.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse(
                "order_details",
                kwargs={"pk": self.order.pk}
            ),
        )
        self.assertContains(response, self.order.promocode)
        self.assertContains(response, self.order.delivery_address)
        self.assertEqual(response.context['object'].pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='Test_name',
            password='qwrerty1234!',
            is_staff=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_order_export(self):
        fixtures = ['order-fixtures.json']
        response = self.client.get(reverse('orders_export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user,
                'products': [
                    product for product in order.products
                ]
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(orders_data['orders'], expected_data)


class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'product-fixtures.json'
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse("products_export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,
        )


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="user_test", password="qwerty")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUP(self) -> None:
        self.client.force_login(self.user)

    def test_orders_view(self):
        self.client.login(username="user_test", password="qwerty")
        response = self.client.get(
            reverse("orders_list")
        )
        self.assertContains(response, "Список заказов")


    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(
            reverse("orders_list")
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class ProductsListViewTestCase(TestCase):
    fixtures = [
        'products-fixtures.json',
    ]
    def test_products(self):
        response = self.client.get(
            reverse("products_list")
        )
        self.assertQuerysetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=[p.pk for p in response.context["product"]],
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'advertisement/products-list.html')


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="Best Product", created_by_id="1")

    # def setUp(self) -> None:
    #     self.product = Product.objects.create(name="Best Product", created_by_id="1")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    # def tearDown(self) -> None:
    #     self.product.delete()

    def test_get_product(self):
        response = self.client.get(reverse("product_details", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("product_details", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="user_test", password="qwerty")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        # self.client.force_login(user="admin")
        # self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        self.product_name = "".join(choices(ascii_letters, k=10))
        self.client.login(username="user_test", password="qwerty")
        response = self.client.post(reverse("create_product"), {
            "name": self.product_name,
            "price": "123.45",
            "description": "A good table",
            "discount": "10",
            "created_by": "admin",
        })
        self.assertRedirects(response, reverse("products_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_number(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)