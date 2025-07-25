from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/',views.login_view,name="login"),
    path('testing/',views.testing_view,name="testing"),
    path('profile/',views.profile_create,name="profile"),
    path('logout/',views.logout_view,name="logout"),
]
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()