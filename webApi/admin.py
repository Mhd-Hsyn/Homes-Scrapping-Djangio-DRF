from django.contrib import admin
from .models import (
    Property_Type,
    Home,
    Home_Images,
    Price_History,
    Mortgage_History,
    Deed_History
)

class HomeAdmin(admin.ModelAdmin):
    search_fields = ['homelink', 'homeid','price', 'city', 'state', 'zip_code', 'address', 'estimated_payment', 'about', 'beds', 'baths', 'sqft', 'lot_size_sqft', 'price_per_sqft', 'days_on_market', 'year_built']
admin.site.register(Home, HomeAdmin)


class HomeImagesAdmin(admin.ModelAdmin):
    search_fields = ['image']
admin.site.register(Home_Images, HomeImagesAdmin)


admin.site.register(Property_Type)


class Price_HistoryAdmin(admin.ModelAdmin):
    search_fields = ['home__id']
admin.site.register(Price_History, Price_HistoryAdmin)



class Mortgage_HistoryAdmin(admin.ModelAdmin):
    search_fields = ['home__id']
admin.site.register(Mortgage_History, Mortgage_HistoryAdmin)



class Deed_HistoryAdmin(admin.ModelAdmin):
    search_fields = ['home__id']
admin.site.register(Deed_History, Deed_HistoryAdmin)

