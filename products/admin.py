from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Количество пустых форм для дополнительных фото
    max_num = 10  # Максимум 10 дополнительных фото


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'condition', 'size', 'category', 'in_stock']
    list_filter = ['category', 'condition', 'in_stock']
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ['name', 'category', 'price', 'availability_type', 'stock_quantity', 'in_stock']
        }),
        ('Детали', {
            'fields': ['condition', 'size', 'description']
        }),
        ('Фото', {
            'fields': ['main_image']
        }),
    )

    # inlines = [ProductImageInline]

    def get_fieldsets(self, request, obj=None):
        """Показываем stock_quantity только для товаров на складе"""
        fieldsets = super().get_fieldsets(request, obj)

        if obj and obj.availability_type == 'preorder':
            fieldsets = (
                ('Основная информация', {
                    'fields': ['name', 'category', 'price', 'availability_type', 'in_stock']
                }),
                ('Детали', {
                    'fields': ['condition', 'size', 'description']
                }),
                ('Фото', {
                    'fields': ['main_image']
                }),
            )

        return fieldsets


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(ProductImage)
