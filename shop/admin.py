from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, path
from django.utils.safestring import mark_safe

from shop.models import Product, Order, OrderLine


@admin.register(Product)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "created", "modified", "add_to_cart")
    list_display_links = ("id",)
    search_fields = ("name",)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "add_to_cart/<path:product_id>",
                self.admin_site.admin_view(self.add_product_to_cart),
                name="shop_product_add  _to_cart",
            )
        ]
        return urls + custom_urls

    @staticmethod
    def add_to_cart(item):
        return mark_safe(f"<a href='add_to_cart/{item.id}'>Add to cart</a>")

    @staticmethod
    def add_product_to_cart(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        order = (
            Order.objects.filter(customer=request.user, shipped=False)
            .order_by("-modified")
            .first()
        )
        if order:
            try:
                order_line = OrderLine.objects.get(order=order, product=product)
                order_line.quantity += 1
                order_line.save()
                messages.success(
                    request, "Product already in the cart, one more unit was added"
                )
            except Exception:
                OrderLine.objects.create(order=order, product=product)
                messages.success(request, "Product added to your cart")
        else:
            order = Order.objects.create(customer=request.user)
            OrderLine.objects.create(order=order, product=product)
            messages.success(request, "Product added to your cart")
        return redirect(reverse("admin:shop_order_change", args=(order.id,)))


class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    readonly_fields = ("total_amount",)


@admin.register(Order)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "shipped", "created", "modified")
    list_display_links = ("id",)
    list_filter = ("shipped",)
    search_fields = (
        "name",
        "customer__username",
        "customer__first_name",
        "customer__lastname",
    )
    inlines = (OrderLineInLine,)
    change_form_template = "order_changeform.html"

    def save_model(self, request, obj, form, change):
        if request.POST.get("_ship"):
            obj.ship()
            messages.success(
                request, "Order has been shipped! You'll receive an email soon"
            )
        else:
            return super().save_model(request, obj, form, change)
