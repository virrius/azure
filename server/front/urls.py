
from django.contrib import admin
from django.urls import path, include
from node_front.views import mainView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('node_front.urls')),
    
]
