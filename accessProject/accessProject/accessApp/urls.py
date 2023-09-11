from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('apis/view/', views.view_api, name='view_api'),
    path('apis/add/', views.add_api, name='add_api'),
    path('apis/update/<int:api_id>/', views.update_api, name='update_api'),
    path('apis/remove/<int:api_id>/', views.remove_api, name='remove_api'),
    path('users/view/', views.view_user, name='view_user'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/remove/<int:user_id>/', views.remove_user, name='remove_user'),
    path('add_users/', views.addUser, name='addUser'),
    path('view_users/', views.viewUser, name='viewUser'),
    path('get_user/<int:user_id>/', views.getUser, name='getUser'),
    path('update_users/<int:user_id>/', views.updateUser, name='updateUser'),
    # path('update_users_form/<int:user_id>/', views.updateUserForm, name='updateUserForm'),
    path('remove_users/', views.removeUser, name='removeUser'),
    path('view_apis/', views.viewAPI, name='viewAPI'),
    path('add_apis/', views.addAPI, name='addAPI'),
    path('remove_apis/', views.removeAPI, name='removeAPI'),
    path('get_api/<int:api_id>/', views.getApi, name='getApi'),
    path('update_apis/<int:api_id>/', views.updateAPI, name='updateAPI'),
    # path('update_apis_form/<int:api_id>/', views.updateAPIForm, name='updateAPIForm'),
    path('map_api_to_users/<int:api_id>/', views.map_api_to_users, name='map_api_to_users'),
    path('map_page/', views.map_page, name='map_page'),
    path('map_input_page/<int:api_id>/', views.map_input_page, name='map_input_page'),
]