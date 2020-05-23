from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('create/', views.UserCreateView.as_view(), name="create"),
    path('index/', views.indexview, name="index"),
    path('output/', views.outputview, name="output"),
    path('list/', views.listview, name="list"),
    path('list_index/', views.list_indexview, name="list_index"),
    path('reset/', views.reset_view, name='reset'),
    path('out/', views.outview, name='out'),

]
