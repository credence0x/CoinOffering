from django.urls import path,re_path
from Users.views import SignUpController,SignInController,HomePageController,LogOutController



app_name='Users'
urlpatterns = [
    re_path(r'^sign-in/$', SignInController, name='sign-in'),
    re_path(r'^sign-up/$', SignUpController, name='sign-up' ),
    re_path(r'^home-page/$',  HomePageController, name='home-page'),
    re_path(r'^log-out/$',  LogOutController, name='log-out'),

    
    ]