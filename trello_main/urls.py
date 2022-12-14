from django.urls import path  
from .views import signup, activate
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [  
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('signup', signup, name = 'signup'),  
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        activate, name='activate'),  
]  