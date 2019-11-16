from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('buscar.urls')),
    path('admin/', admin.site.urls),
    path('oi/', include('buscar.urls')),
]