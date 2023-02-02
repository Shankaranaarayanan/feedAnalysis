from django.contrib import admin
from feed_app.models import Stock,StockRecord,Formula

# Register your models here.
admin.site.register(Stock)
admin.site.register(StockRecord)
admin.site.register(Formula)