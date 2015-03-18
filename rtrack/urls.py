from django.conf.urls import patterns, url, include

from rtrack import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url('^accounts/login/$', views.user_login, name='login'),
                       url('^accounts/logout/$', views.user_logout, name='logout'),
                       url(r'report/(?P<report_id>\d+)/$', views.reportview, name='report'),
                       url(r'report/(?P<report_id>\d+)/createassociation/$', views.create_association, name='createassociation'),
                       url(r'report/(?P<report_id>\d+)/urlink/$', views.create_url_link, name='create_url_link'),
                       url(r'report/(?P<report_id>\d+)/notelink/$', views.create_note_link, name='create_note_link'),
                       url(r'createreport/$', views.createreport, name='createreport'),
                       url(r'search/$', views.user_search, name='search'),
                       url(r'user/(?P<user_name>\w+)/$', views.user_page, name='user_page'),
                       url(r'user/(?P<user_name>\w+)/createnote/$', views.user_add_note, name='create_user_note'),
                       url(r'user/(?P<user_name>\w+)/modmail_link/$', views.create_modmail_link, name='create_modmail_link'),
                       url(r'create_user/$', views.add_user, name='create_user'),
                       )