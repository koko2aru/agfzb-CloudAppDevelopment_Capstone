from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['dealer_id']
    list_filter = ['type', 'year']

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']
    serch_fields = ['name']

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
