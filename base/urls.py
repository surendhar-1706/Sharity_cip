from .views import *
from django.urls import path
urlpatterns = [
    path('', home, name='home'),
    path('signup/', Signup, name='signup'),
    path('login/', Login, name='login'),
    path('logout/', Logout_fun, name='logout'),
    path('profile/', Profile_fun, name='profile'),
    path('updateprofile/', Updateprofile, name='updateprofile'),
    path('post', Postlist, name="post"),
    path('createpost', Postcreate, name='createpost'),
    path('viewprofile/<str:user_name>/', Viewprofile, name='viewprofile'),
    path('makepayments/<str:user_name>', Makepayments, name='makepayments'),


]
