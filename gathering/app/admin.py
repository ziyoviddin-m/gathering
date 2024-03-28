from django.contrib import admin

from .models import Payment, Collect


admin.site.register(Collect)
admin.site.register(Payment)