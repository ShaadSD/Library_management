"""
URL configuration for Library_Management_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import Home,BookDetaiView,ProfileView,return_book
urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('Book.urls')),
    path('book/', include('transactions.urls')),
    path('', Home.as_view(), name='home'),
    path('book/<int:pk>/', BookDetaiView.as_view(), name='book_detail'),
    path('book/<slug:slug>/', Home.as_view(), name='Categorywise'),
    path('profile/',ProfileView.as_view(),name='profile'),
     path('return/<int:pk>/', return_book, name='return_book'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)