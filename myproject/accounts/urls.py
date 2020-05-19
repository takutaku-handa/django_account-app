from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('create/', views.UserCreateView.as_view(), name="create"),
    path('index/', views.indexview, name="index"),
    path('index/output/', views.outputview, name="output"),
    path('list/', views.listview, name="list"),
]
