from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group
from .models import Advertisement, Product, Order, ProductImage
from random import randint
from .forms import ProductForm, OrderForm, GroupForm
from timeit import default_timer
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser


class OrderCreateView(CreateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy("orders_list")


class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ["advertisement.change_order", ]
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse("order_details", kwargs={
            "pk": self.object.pk
        })


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ["advertisement.view_order"]
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("orders_list")


class OrdersExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [
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
        return JsonResponse({'orders': orders_data})


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """ ???? ?????????? ?????????????????? ???????????????? ?????????? ?? ???????????? form.is_valid() """
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    permission_required = ["advertisement.add_product", ]
    model = Product
    fields = "name", "price", "description", "discount", "created_by", "preview"
    # form_class = ProductForm
    success_url = reverse_lazy("products_list")


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        self.object = self.get_object()
        has_edit_perm = self.request.user.has_perm("advertisement.change_product")
        created_by_current_user = self.object.created_by == self.request.user
        return has_edit_perm and created_by_current_user

    model = Product
    # fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    form_class = ProductForm

    def get_success_url(self):
        return reverse("product_details",
                       kwargs={
             "pk": self.object.pk
        })

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductsListView(ListView):
    template_name = 'advertisement/products-list.html'
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = "products"


class ProductDetailsView(DetailView):
    template_name = 'advertisement/products-details.html'
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by("pk").all()
        products_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": product.price,
                "archived": product.archived,
            }
            for product in products
        ]
        return JsonResponse({"products": products_data})



def advertisement_list(request, *args, **kwargs) -> HttpResponse:
    advertisements = Advertisement.objects.all()
    rnd_adv = Advertisement.objects.all()[randint(0, 5)]
    return render(request, 'advertisement/advertisements.html', {'advertisements': advertisements, 'rnd_adv': rnd_adv})


def categories(request, *args, **kwargs) -> HttpResponse:
    categories_list = ['???????????? ????????', '??????????????????', '??????????', '??????????']
    return render(request, 'advertisement/categories.html', {'categories_list': categories_list})


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
        regions_list = ['????????????', '???????????????????? ??????????????', '???????????????????? ??????????', '?????????????????????? ??????????????']
        return render(request, 'advertisement/regions.html', {'regions_list': regions_list})

    def post(self, request) -> HttpResponse:
        return HttpResponse('???????????? ?????????????? ????????????')


class AdvertisementList(View):
    def get(self, request):
        with open('./advertisement/templates/count.txt', 'r') as file:
            count = int(file.read())
        with open('./advertisement/templates/count.txt', 'w') as file:
            file.write(str(int(count) + 1))
        lst_2 = ['????????????????', '??????????????', '??????????????', '??????????????']
        lst_3 = ['??????????????', '??????????', '????????????']
        lst_1 = ['????????????????????', '??????????????????', '????????']
        return render(request, 'advertisement/advertisement_list.html', {'lst_1': lst_1, 'lst_2': lst_2,
                                                                         'lst_3': lst_3, 'count': count})
    def post(self, request):
        with open('./advertisement/templates/count.txt', 'r') as file:
            count = int(file.read())
        with open('./advertisement/templates/count.txt', 'w') as file:
            file.write(str(int(count) + 1))
        return HttpResponse('???????????? ???? ???????????????? ?????????? ???????????? ?????????????? ????????????????')


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
        context['name'] = '???????????????????? ????????????????????'
        context['description'] = '???????????????????? ???????????????????? ?? ?????????? ????????????!'
        return context


class MainPage(TemplateView):
    template_name = 'advertisement/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = ['????????????????', '??????????????', '??????????????', '??????????????', '??????????????', '??????????', '????????????']
        context['regions_list'] = ['????????????', '???????????????????? ??????????????', '???????????????????? ??????????', '?????????????????????? ??????????????']
        return context


