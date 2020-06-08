from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', views.logout, name='logout'),
    path('get_code', views.get_code, name='get_code'),
]
