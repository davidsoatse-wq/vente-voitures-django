from django.contrib import admin
from django.urls import path,include
from inventory.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', home, name='home'),
    path('', include('inventory.urls'))
# dire au projet d'aller regarder le dossier inventor pour le visuel
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)