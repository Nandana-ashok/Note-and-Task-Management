"""
URL configuration for Note_Management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from notes_app import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.RegistrationView.as_view()),
    path('login/',obtain_auth_token),
    path('notes/',views.NotesListCreateView.as_view()),
    path('notes/<int:id>/',views.NotesRetrieveUpdateDeleteView.as_view()),
    path('logout/',views.LogOutView.as_view()),
    path('jwt_login/',TokenObtainPairView.as_view()),
    path('tasks/',views.TaskCreateListView.as_view()),
    path('jwt_refresh/',TokenRefreshView.as_view()),
    path('tasks/<int:task_id>/',views.TaskRetrieveUpdateDeleteView.as_view()),
    path('jwt_logout/',views.JWT_LogOut.as_view()),
    
]
