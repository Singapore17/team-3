from django.conf.urls.defaults import patterns, include, url
from jcb.views import *
from django.contrib import admin
import os.path
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


site_media=os.path.join(
	os.path.dirname(__file__),'site_media'
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_jcb.views.home', name='home'),
    # url(r'^django_jcb/', include('django_jcb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	url(r'^$',main_page),
	url(r'^cs/$',cs_page),
	url(r'^xg/id=(\d+)/$',xg_page),
	url(r'^gz/$',gz_page),
	url(r'^wh/$',wh_page),
	url(r'^wh/ftp/$',wh_ftp_page),
	url(r'^wh/bb/$',wh_bb_page),
	url(r'^records/$',records_page),
	url(r'^records/(\w+)/id=(\d+)$',record_modify_page),
	url(r'^gz/date=(\d+)$',gz_acct_page),
	url(r'^gz/date=(\d+)&&acct_no=(\d+)$',gz_acct_page),
	url(r'^wh/rorac/$',rorac_page),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':site_media}),
)
