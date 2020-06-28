from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.RecipeListView.as_view(), name='recipe_list'),
    path('detail/recipe/<int:pk>', views.RecipeDetailView.as_view(), name='detail'),
    path('detail/calender/<int:pk>', views.MyCalenderDetailView.as_view(), name='calender_detail'),
    path('delete/recipe/<int:pk>', views.RecipeDelete.as_view(), name='delete'),
    path('delete/calender/', views.deletecalender, name='calender_delete'),
    path('change/<int:year>/<int:month>/<int:day>/', views.ChangeDay.as_view(), name='change'),
    path('change/plot', views.get_svg, name="img2"),
    path('cahnge/calnder', views.changecalender, name='calender_change'),
    path('create/recipe/', views.newrecipe, name='recipe_create'),
    path('create/calender', views.newcalender, name='calender_create'),
    path('update/recipe/<int:pk>', views.RecipeUpdateView.as_view(), name='update'),
    path('update/calender/<int:pk>', views.MyCalenderUpdateView.as_view(), name='calender_update'),
    path('myshohi/', views.myshohiview, name='myshohi'),
    path('allshohi/', views.allshohiview, name='allshohi'),
    path('recipe/', views.recipeview, name='recipe'),
    path('week/', views.WeekCalendar.as_view(), name='week'),
    path('week/<int:year>/<int:month>/<int:day>/', views.WeekCalendar.as_view(), name='week'),

]
