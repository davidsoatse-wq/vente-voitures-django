from django.contrib import admin
from django.urls import path
from inventory.views import home
from django.conf import settings # Ajoute ça
from django.conf.urls.static import static # Ajoute ça

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Ajoute cette ligne