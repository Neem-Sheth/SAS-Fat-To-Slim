from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin

admin.site.site_header = 'SAS:FTF Admin'
admin.site.site_title = 'SAS:FTF Admin'
admin.site.index_title= 'SAS: Fat To Slim Administration'

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', include('foodtracker.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
