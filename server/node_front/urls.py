from django.urls import path
from node_front.views import mainView

urlpatterns = [
    path('index', mainView, name='main'),
]