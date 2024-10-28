from django.urls import path
from .views import RegisterView,LoginView
from . import views
urlpatterns = [
   path('register/',RegisterView.as_view(),name='register'),
   path('logout/',views.user_logout,name='logout'),
   path('login/',LoginView.as_view(),name='login'),
   path('borrow/<int:pk>/', views.borrow_book, name='borrow_book'),
] 