from django.urls import path
from users import views
urlpatterns = [
    # path('', views.user_list_api_view, name='user_list_api_view'),
    # path('<int:user_id>/', views.user_retrieve_api_view, name='user_retrieve_api_view'),
    # path('login/', views.login_api_view, name='login'),
    # path('logout/', views.logout_api_view, name='logout'),
    path('check-auth/', views.check_auth, name='check_auth'),
]

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns += router.urls
