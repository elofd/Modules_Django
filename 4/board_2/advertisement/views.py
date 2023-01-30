from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import Group
from .models import Advertisement, Product, Order
from random import randint
from .forms import ProductForm, OderForm, GroupForm
from timeit import default_timer
from django.urls import reverse_lazy


def advertisement_list(request, *args, **kwargs) -> HttpResponse:
    advertisements = Advertisement.objects.all()
    rnd_adv = Advertisement.objects.all()[randint(0, 5)]
    return render(request, 'advertisement/advertisements.html', {'advertisements': advertisements, 'rnd_adv': rnd_adv})


def categories(request, *args, **kwargs) -> HttpResponse:
    categories_list = ['личные вещи', 'транспорт', 'хобби', 'отдых']
    return render(request, 'advertisement/categories.html', {'categories_list': categories_list})


class OrdersListView(ListView):
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )


class OrderDetailView(DetailView):
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )


class OrderCreateView(CreateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy("orders_list")


class OrderUpdateView(UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("order_details", kwargs={
            "pk": self.object.pk
        })


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("orders_list")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("product_details",
                       kwargs={
             "pk": self.object.pk
        })


class ProductCreateView(CreateView):
    """ Не нужно создавать отдельно форму и делать form.is_valid() """
    model = Product
    fields = "name", "price", "description", "discount"
    # form_class = ProductForm
    success_url = reverse_lazy("products_list")


class ProductsListView(ListView):
    template_name = 'advertisement/products-list.html'
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = "products"


class ProductDetailsView(DetailView):
    template_name = 'advertisement/products-details.html'
    model = Product
    context_object_name = "product"


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'advertisement/groups.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        # return self.render(request)
        return redirect(request.path)


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        return render(request, 'advertisement/shop-index.html', context=context)


class Regions(View):
    def get(self, request) -> HttpResponse:
        regions_list = ['Москва', 'Московская область', 'республика Алтай', 'Вологодская область']
        return render(request, 'advertisement/regions.html', {'regions_list': regions_list})

    def post(self, request) -> HttpResponse:
        return HttpResponse('Регион успешно создан')


class AdvertisementList(View):
    def get(self, request):
        with open('./advertisement/templates/count.txt', 'r') as file:
            count = int(file.read())
        with open('./advertisement/templates/count.txt', 'w') as file:
            file.write(str(int(count) + 1))
        lst_2 = ['Приворот', 'Отворот', 'Поворот', 'Гадание']
        lst_3 = ['Пончики', 'Пицца', 'Шаурма']
        lst_1 = ['Автомобили', 'Снегоходы', 'Яхты']
        return render(request, 'advertisement/advertisement_list.html', {'lst_1': lst_1, 'lst_2': lst_2,
                                                                         'lst_3': lst_3, 'count': count})
    def post(self, request):
        with open('./advertisement/templates/count.txt', 'r') as file:
            count = int(file.read())
        with open('./advertisement/templates/count.txt', 'w') as file:
            file.write(str(int(count) + 1))
        return HttpResponse('Запрос на создание новой записи успешно выполнен')


class Contacts(TemplateView):
    template_name = 'advertisement/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tel'] = '8-800-708-19-45'
        context['mail'] = 'sales@company.com'
        return context


class About(TemplateView):
    template_name = 'advertisement/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Бесплатные объявления'
        context['description'] = 'Бесплатные объявления в вашем городе!'
        return context


class MainPage(TemplateView):
    template_name = 'advertisement/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = ['Приворот', 'Отворот', 'Поворот', 'Гадание', 'Пончики', 'Пицца', 'Шаурма']
        context['regions_list'] = ['Москва', 'Московская область', 'республика Алтай', 'Вологодская область']
        return context
