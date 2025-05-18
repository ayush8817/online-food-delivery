from django.contrib import admin
from .models import Restaurant, Category, MenuItem, Order, OrderItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('name', 'category', 'price', 'is_available')
    show_change_link = True

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'rating', 'is_active')
    list_filter = ('is_active', 'rating')
    search_fields = ('name', 'address', 'phone')
    inlines = [MenuItemInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone')
        }),
        ('Status', {
            'fields': ('rating', 'is_active')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'category', 'price', 'is_available')
    list_filter = ('restaurant', 'category', 'is_available')
    search_fields = ('name', 'description', 'restaurant__name')
    list_select_related = ('restaurant', 'category')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('menu_item', 'quantity', 'price')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'restaurant', 'created_at')
    search_fields = ('user__username', 'restaurant__name', 'delivery_address')
    readonly_fields = ('user', 'restaurant', 'total_amount', 'created_at')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'restaurant', 'status', 'total_amount', 'created_at')
        }),
        ('Delivery Information', {
            'fields': ('delivery_address',)
        }),
    ) 