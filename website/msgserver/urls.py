from django.urls import path
from . import views

urlpatterns = [
        path('/message/<str:key>', views.get_message, name='get_message'),
]
