"""billiardmate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    #path('', include('django.contrib.auth.urls')),
    path('change-password/', auth_views.PasswordChangeView.as_view()),
    path('player_registration/', PlayerRegistrationView.as_view(), name="Player_registraion"),
    path('club_registration/', ClubRegistrationView.as_view(), name="club_registration"),
    path('<int:pk>/', ProfileDetail.as_view(), name='user_profile'),
    path('<int:pk>/update/', ProfileUpdateView.as_view(), name='user_update'),
    # path('tournament/upcoming', UpcomingTournament.as_view(), name='upcoming_tournament')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
