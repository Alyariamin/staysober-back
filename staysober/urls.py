from django.contrib import admin
from django.urls import include, path
import djoser


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include ('app.urls')),
    path('auth/', include ('djoser.urls')), 
    path('auth/', include ('djoser.urls.jwt'))
]
