from django.urls import path, include

urlpatterns = [
    path('v1/accounts/', include('apps.accounts.urls')),
    path('v1/core/', include('apps.core.urls')),
]
