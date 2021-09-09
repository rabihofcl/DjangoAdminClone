from django.urls import path
from . import views

import accounts.views


urlpatterns = [
    path('', views.ad_signin, name='ad_signin'),
    path('ad_signin', views.ad_signin, name='ad_signin'),
    path('ad_home', views.ad_home, name='ad_home'),
    path('ad_signout', views.ad_signout, name='ad_signout'),
    path('user_edit/<user_id>', views.user_edit, name='user_edit'),
    path('update_user/<user_id>', views.update_user, name='update_user'),
    path('cancel_edit', views.cancel_edit, name='cancel_edit'),
    path('user_delete/<user_id>', views.user_delete, name='user_delete'),
    path('ad_signup', views.ad_signup, name='ad_signup'),
]