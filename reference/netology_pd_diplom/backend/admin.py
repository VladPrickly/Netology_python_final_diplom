from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, \
    Contact, ConfirmEmailToken


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """ Список пользователей """
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'company', 'position')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'company', 'type', 'is_staff')
    list_editable = ('first_name', 'last_name', 'company')
    list_per_page = 20


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """ Список магазинов """
    list_display = ('name', 'user', 'url', 'state')
    list_filter = ('name', 'user', 'state')
    ordering = ['name']
    search_fields = ['name', 'url']
    list_per_page = 15


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Список категорий """
    list_display = ('name', )
    list_filter = ('name', 'shops')
    search_fields = ['name']
    list_per_page = 15


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Список продуктов """
    list_display = ('name', 'category')
    list_filter = ('category',)
    ordering = ['-name']
    search_fields = ['category']
    list_editable = ['category']
    list_per_page = 10


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    """ Информационный список о продуктах """
    list_display = ('product', 'model', 'external_id', 'shop', 'quantity', 'price', 'price_rrc')
    list_filter = ('shop', 'quantity', 'price')
    ordering = ['product']
    search_fields = ['product', 'model']
    list_display_links = ('product', 'model')
    list_editable = ('quantity', 'price', 'price_rrc')
    list_per_page = 10

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    """ Список имен параметров """
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ['name']
    list_per_page = 15


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    """ Список параметров """
    list_display = ('product_info__product', 'parameter', 'value')
    list_filter = ('parameter', 'value')
    search_fields = ['product_info__product', 'parameter', 'value']
    ordering = ['product_info__product']
    list_per_page = 20


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Список заказов """
    list_display = ('user', 'state', 'dt')
    list_filter = ('state','dt')
    list_editable = ('state',)
    list_per_page = 10


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """ Список заказанных позиций """
    list_display = ('order', 'product_info', 'quantity')
    list_filter = ('order', )
    list_editable = ('quantity', )
    list_per_page = 10


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """ Список контактов пользователя """
    list_display = ('user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone')
    list_filter = ('city', 'street', 'house')
    list_editable = ('city', 'street', 'house', 'structure', 'building', 'apartment', 'phone')
    list_display_links = ('user',)
    search_fields = ('user', 'city')
    list_per_page = 15

@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    """ Токен подтверждения Email """
    list_display = ('user', 'key', 'created_at',)
