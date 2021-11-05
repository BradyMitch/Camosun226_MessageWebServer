from django.urls import path
from . import views

urlpatterns = [
        path('get/<str:key>', views.get_message, name='get_message'),
        path('update/<pk>', views.update_message.as_view(), name='update_message'),
        path('create', views.create_message.as_view(), name='create_message'),
        path('', views.get_all_messages, name='get_all_messages'),
]
