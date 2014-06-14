from django.conf.urls import patterns, include, url


urlpatterns = patterns('Login.views',
	(r'^index/$', 'index'),
	(r'^home/$', 'login_success'),
	(r'^register/$', 'register'),
	(r'^logout/$', 'logout'),
	(r'^friends/$', 'friends'),
	(r'^messages/$', 'messages'),
	(r'^features/$', 'features'),
	(r'^contact/$', 'contact'),
#    #(r'^Info/$', 'details'),
	#(r'^home/(?P<pid>\d+)/$', 'login_success'),
#    #(r'^Form/(?P<pID>\d+)/$', 'person_form'),
)
