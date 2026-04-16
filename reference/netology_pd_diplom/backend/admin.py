from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, \
    Contact, ConfirmEmailToken


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Панель управления пользователями
    """
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'company', 'position')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """ Список магазинов """
    list_display = ('name', 'user', 'url', 'state')
    list_filter = ('name', 'state')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Список категорий """
    list_display = ('name',)#, 'shops')
    list_filter = ('name', 'shops')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Список продуктов """
    list_display = ('name', 'category')
    list_filter = ('name', 'category')


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    """ Информационный список о продуктах """
    list_display = ('model', 'product', 'external_id', 'shop', 'quantity', 'price', 'price_rrc')
    list_filter = ('model', 'product', 'external_id', 'shop', 'quantity', 'price', 'price_rrc')


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    """ Список имен параметров """
    list_display = ('name',)
    list_filter = ('name',)


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    """ Список параметров """
    list_display = ('product_info', 'parameter', 'value')
    list_filter = ('parameter', 'value')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'dt')
    list_filter = ('state','dt')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """ Список заказанных позиций """
    list_display = ('order', 'product_info', 'quantity')
    list_filter = ('order', 'quantity')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """ Список контактов пользователя """
    list_display = ('user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone')
    list_filter = ('user', 'city', 'phone')


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at',)
