from django.urls import path,re_path
from Bid.views import CreateController,DeleteController



app_name='Bid'
urlpatterns = [
    re_path(r'^$', CreateController, name='create'),
    re_path(r'^delete/$', DeleteController, name='delete' )
        
    ]