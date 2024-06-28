from django.urls import path
from posts import views

urlpatterns = [
    path('', views.post_list_api_view, name='post_list_api_view'),
    path('<int:post_id>/', views.post_retrieve_api_view, name='post_retrieve_api_view'),
    path('likes/<int:post_id>/', views.post_like_api_view, name='post_like_api_view'),
]
