from django.urls import path
from.import views

urlpatterns = [
    path('', views.index),
    path('signin', views.signin),
    path('register', views.register),
    path('newRegister', views.newRegister),
    path('newSignin', views.newSignin),
    path('dashboard', views.dashboard),
    path('signout', views.signout),
    path('user/new', views.newUser),
    path('profile', views.profile),
    path('profile/info', views.profile_info),
    path('profile/pass', views.profile_pass),
    path('profile/desc', views.profile_desc),
    path('users/edit/<int:num>', views.user_edit),
    path('user/info/<int:num>', views.user_info),
    path('user/pass/<int:num>', views.user_pass),
    path('user/remove/<int:num>', views.remove_verify),
    path('user/delete/<int:num>', views.delete_user),
    path('user/show/<int:num>', views.user_show),
    path('post_message/<int:num>', views.post_message),
    path('post_comment/<int:num>', views.post_comment)
]