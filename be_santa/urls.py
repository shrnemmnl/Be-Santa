from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('auth/', include('accounts.urls')),
    path('admin-panel/', include('custom_admin.urls')),
]
