from urllib.parse import urlparse
from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    path('typingtest',views.test,name="typingtest"),
    path('signup',views.handlesignup,name="signup"),
    path('login',views.handlelogin,name="login"),
    path('logout',views.handlelogout,name="logout"),
]