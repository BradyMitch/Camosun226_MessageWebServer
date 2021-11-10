from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
        path('get/<str:key>', views.get_message, name='get_message'),
        path('update/<pk>', views.update_message.as_view(), name='update_message'),
        path('create', csrf_exempt(views.create_message.as_view()), name='create_message'),
        path('', views.get_all_messages, name='get_all_messages'),
]
