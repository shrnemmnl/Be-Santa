from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('auth/', include('accounts.urls')),
    path('gifts/', include('gifts.urls')),
    path('admin-panel/', include('custom_admin.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
