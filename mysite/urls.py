"""rtrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from rtrack import views

# TODO: Once the modal forms / ajax views are reliable, we need to pull out the old separate page forms

urlpatterns = [
                    url(r'^$', views.index, name='index'),
                    url(r'^admin/', include(admin.site.urls)),
                    url(r'^accounts/login/$', views.user_login, name='login'),
                    url(r'^accounts/logout/$', views.user_logout, name='logout'),
                    url(r'accounts/change-password/$', auth_views.password_change,
                        {'template_name': 'registration/password_change_form.html'}, name='password_change'),
                    url(r'accounts/password_changed/$', views.password_changed,
                        {'template_name': 'registration/password_change_done.html'}, name='password_changed'),
                    url(r'report/(?P<report_id>\d+)/$', views.reportview, name='report'),
                    url(r'report/(?P<report_id>\d+)/createassociationajax/$', views.create_association_ajax, name='createassociationajax'),
                    url(r'report/(?P<report_id>\d+)/deleteassociation/(?P<user_name>[-\w]+)/$', views.remove_user_link, name='remove_user_link'),
                    url(r'report/(?P<report_id>\d+)/urlink/$', views.create_url_link, name='create_url_link'),
                    url(r'report/(?P<report_id>\d+)/urlinkajax/$', views.create_url_link_ajax, name='create_url_link_ajax'),
                    url(r'report/(?P<report_id>\d+)/notelink/$', views.create_note_link, name='create_note_link'),
                    url(r'report/(?P<report_id>\d+)/notelinkajax/$', views.create_note_link_ajax, name='create_note_link_ajax'),
                    url(r'report/(?P<report_id>\d+)/readonly/$', views.readonly, name='readonly'),
                    url(r'createreport/$', views.createreport, name='createreport'),
                    url(r'search/$', views.search, name='search'),
                    url(r'user/(?P<user_name>[-\w]+)/$', views.user_page, name='user_page'),
                    url(r'user/(?P<user_name>[-\w]+)/createnote/$', views.user_add_note, name='create_user_note'),
                    url(r'user/(?P<user_name>[-\w]+)/createnote/$', views.user_add_note_ajax, name='create_user_note_ajax'),
                    url(r'user/(?P<user_name>[-\w]+)/modmail_link/$', views.create_modmail_link, name='create_modmail_link'),
                    url(r'user/(?P<user_name>[-\w]+)/modmail_link/$', views.create_modmail_link_ajax, name='create_modmail_link_ajax'),
                    url(r'create_user/$', views.add_user, name='create_user'),
                    url(r'about/$', views.about, name='about'),
]
