from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
# from .views import BaseRegisterView
from .views import *


urlpatterns = [

   path('', PostList.as_view(), name= 'post_list'),
   path('<int:pk>', PostDetail.as_view(), name = 'post_detail'),
   path('create/', PostCreate.as_view(), name = 'post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostSearcher.as_view(), name='post_search'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
   path('login/', LoginView.as_view(template_name='login.html'), name='login'),
   path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
   path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
   path('index/', IndexView.as_view(template_name = 'index.html')),
   path('upgrade/', upgrade_me, name = 'upgrade')

]


