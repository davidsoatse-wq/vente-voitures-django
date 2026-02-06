from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # <--- C'est "urls" et non "id_index"
    path('', include('inventory.urls')),
]