from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', include('new.urls'), name='core'),
                  path('adminbegi/', admin.site.urls),
                  path('old/', include('scetch.urls')),
                  path('accounts/', include('accounts.urls')),
                  path('admutrk/', include('adminka.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
