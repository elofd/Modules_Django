from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import Group
from .models import Advertisement, Product, Order
from random import randint


def orders_list(request: HttpRequest, *args, **kwargs):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }
    return render(request, "advertisement/orders-list.html", context=context)


def products_list(request: HttpRequest, *args, **kwargs):
    context = {
        "products": Product.objects.all(),
    }
    return render(request, 'advertisement/products-list.html', context=context)


def groups_list(request: HttpRequest, *args, **kwargs):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'advertisement/groups.html', context=context)


def advertisement_list(request, *args, **kwargs):
    advertisements = Advertisement.objects.all()
    rnd_adv = Advertisement.objects.all()[randint(0, 5)]
    return render(request, 'advertisement/advertisements.html', {'advertisements': advertisements, 'rnd_adv': rnd_adv})


def categories(request, *args, **kwargs):
    categories_list = ['личные вещи', 'транспорт', 'хобби', 'отдых']
    return render(request, 'advertisement/categories.html', {'categories_list': categories_list})


class Regions(View):
    def get(self, request):
        regions_list = ['Москва', 'Московская область', 'республика Алтай', 'Вологодская область']
        return render(request, 'advertisement/regions.html', {'regions_list': regions_list})

    def post(self, request):
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
