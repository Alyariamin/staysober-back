from django.contrib import admin
from django.urls import include, path
import djoser
from django.urls import path

from core.views import ChangePasswordView
# from core/views import ChangePasswordView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include ('app.urls')),
    path('auth/', include ('djoser.urls')), 
    path('auth/', include ('djoser.urls.jwt')),
   path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
]

