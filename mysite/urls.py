from django.conf.urls import patterns, include, url
from django.contrib import admin

from rtrack import views

# TODO: Once the modal forms / ajax views are reliable, we need to pull out the old separate page forms

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/login/$', views.user_login, name='login'),
                       url(r'^accounts/logout/$', views.user_logout, name='logout'),
                       # url(r'^password_change/$', views.change_password, name='password_change'),
                       url(r'accounts/change_password', 'django.contrib.auth.views.password_change',
                           {'post_change_redirect': 'password_changed'}, name='password_change'),
                       url(r'^accounts/password_changed/$', views.password_changed, name='password_changed'),
                       url(r'report/(?P<report_id>\d+)/$', views.reportview, name='report'),
                       url(r'report/(?P<report_id>\d+)/createassociation/$',
                           views.create_association, name='createassociation'),
                       url(r'report/(?P<report_id>\d+)/createassociationajax/$', views.create_association_ajax,
                           name='createassociationajax'),
                       url(r'report/(?P<report_id>\d+)/deleteassociation/(?P<user_name>\w+)/$',
                           views.remove_user_link, name='remove_user_link'),
                       url(r'report/(?P<report_id>\d+)/urlink/$', views.create_url_link, name='create_url_link'),
                       url(r'report/(?P<report_id>\d+)/urlinkajax/$', views.create_url_link_ajax,
                           name='create_url_link_ajax'),
                       url(r'report/(?P<report_id>\d+)/notelink/$', views.create_note_link, name='create_note_link'),
                       url(r'report/(?P<report_id>\d+)/notelinkajax/$', views.create_note_link_ajax,
                           name='create_note_link_ajax'),
                       url(r'createreport/$', views.createreport, name='createreport'),
                       url(r'search/$', views.search, name='search'),
                       url(r'user/(?P<user_name>\w+)/$', views.user_page, name='user_page'),
                       url(r'user/(?P<user_name>\w+)/createnote/$', views.user_add_note, name='create_user_note'),
                       url(r'user/(?P<user_name>\w+)/modmail_link/$', views.create_modmail_link, name='create_modmail_link'),
                       url(r'create_user/$', views.add_user, name='create_user'),
                       url(r'about/$', views.about, name='about'),
                       )
