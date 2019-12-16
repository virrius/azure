from django.urls import path
from node_front.views import mainView, statusView

urlpatterns = [
    path('', mainView, name='main'),
    path('status', statusView, name='status'),
]