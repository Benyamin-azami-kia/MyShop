from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from tags.models import TaggedItem
from .models import *


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name='inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields=['collection']
    prepopulated_fields={
        'slug':['title']
    }
    actions=['clear_inventory']
    list_display=['title','unit_price','inventory_status','collection_title']
    list_editable=['unit_price']
    list_select_related = ['collection']
    list_per_page=10
    list_filter=['collection','last_update', InventoryFilter]
    search_fields=['title__istartswith','description__icontains']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request,f'{updated_count} products were successfully updated!'
                            ,messages.ERROR)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership']
    list_editable=['membership']
    list_select_related=['user']
    ordering=['user__first_name','user__last_name']
    search_fields=['user__first_name__istartswith','user__last_name__istartswith']


class OrderItemInline(admin.TabularInline):
    model=OrderItem
    extra=0
    min_num=1
    autocomplete_fields=['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemInline]
    list_display=['id','placed_at','customer']
    autocomplete_fields=['customer']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields=['title']
    list_display=['title','product_count']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = (reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
                    'collection__id' : collection.id
                }))
        return format_html('<a href="{}">{}</a>',url ,collection.product_count) 
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('products'))