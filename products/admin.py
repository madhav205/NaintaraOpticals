from django.contrib import admin
from .models import Product, Order, OrderHistory, Wishlist, Address
from django.utils.html import format_html

@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'user', 'quantity', 'price', 'delivery_city', 'colored_status')
    list_filter = ('status',)
    search_fields = ('product_name', 'user__username', 'delivery_city')
    ordering = ('-id',)

    fields = (
        'user', 'product_name', 'price', 'quantity',
        'delivery_name', 'delivery_mobile',
        'delivery_house', 'delivery_street',
        'delivery_city', 'delivery_state', 'delivery_pincode',
        'status', 'cancel_reason'
    )

    def colored_status(self, obj):
        colors = {
            'Pending': '#856404',
            'Delivered': '#065f46',
            'Cancelled': '#991b1b',
            'Out of Stock': '#7c3aed',
        }
        backgrounds = {
            'Pending': '#fff3cd',
            'Delivered': '#d1fae5',
            'Cancelled': '#fee2e2',
            'Out of Stock': '#ede9fe',
        }
        color = colors.get(obj.status, '#000')
        bg = backgrounds.get(obj.status, '#eee')
        return format_html(
            '<span style="background:{};color:{};padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;">{}</span>',
            bg, color, obj.status
        )
    colored_status.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        if obj.status in ['Cancelled', 'Out of Stock']:
            if not obj.cancel_reason:
                obj.cancel_reason = "Cancelled by admin."
        super().save_model(request, obj, form, change)

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    list_editable = ('stock',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'quantity')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'city', 'state', 'is_default')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('product', 'user')