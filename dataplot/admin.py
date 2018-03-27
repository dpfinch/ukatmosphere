from django.contrib import admin
from .models import measurement_data, site_info, measurement_info
# Register your models here.
admin.site.register(measurement_data)
admin.site.register(site_info)
admin.site.register(measurement_info)
