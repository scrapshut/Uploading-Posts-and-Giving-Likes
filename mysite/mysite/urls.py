"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.post_list, name="post_list"),
    url(r'^posts/(?P<id>\d+)/(?P<slug>[\w-]+)/$',views.post_detail, name="post_detail"),
    url(r'post_create/$', views.post_create, name="post_create"),
    url(r'login/$', views.user_login, name="user_login"),
    url(r'logout/$', views.user_logout, name="user_logout"),
    url(r'register/$', views.register, name="register"),
    url(r'like_post/$', views.like_post, name="like_post"),


    #url(r'^password-reset/$', auth_views.password_reset, name="password_reset"),
    #url(r'^password-reset/done/$', auth_views.password_reset_done, name="password_reset_done"),
    #url(r'^password-reset/confirm/(?P<uidb64>[w\-]+)/(?P<token>[w\-]+)/$', auth_views.password_reset_confirm, name="password_reset_confirm"),
    #url(r'^password-reset/complete/$', auth_views.password_reset_complete, name="password_reset_complete"),

    url(r'^password-reset/$',
        auth_views.PasswordResetView.as_view(template_name="posts/password_reset_form.html"),
        name='password_reset'),
    url(r'^password-reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name="posts/password_reset_done.html"),
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="posts/password_reset_confirm.html"),
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name="posts/password_reset_complete.html"),
        name='password_reset_complete'),

]
