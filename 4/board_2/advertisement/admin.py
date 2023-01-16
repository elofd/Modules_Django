from django.contrib import admin
from .models import Product, Order
from django.http import HttpRequest
from django.db.models import QuerySet
from .admin_mixins import ExportAsCSVMixin


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="UnArchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
    ]
    # list_display = "pk", "name", "description", "price", "discount"
    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    list_display_links = "pk", "name"
    ordering = "-name", "pk"
    search_fields = "name", "description", "price"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide", "collapse"),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": ("Extra options. Field 'archived' is for soft delete.")
        })
    ]

    def description_short(self, object: Product) -> str:
        if len(object.description) < 48:
            return object.description
        else:
            return object.description[:48] + "..."


# class ProductInline(admin.TabularInline):
class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    search_fields = "delivery_address",
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"
    fieldsets = [
        (None, {
            "fields": ("delivery_address",),
        }),
        ("descriptions", {
            "fields": ("promocode",),
        }),
        ("author", {
            "fields": ("user",),
        })
    ]

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

