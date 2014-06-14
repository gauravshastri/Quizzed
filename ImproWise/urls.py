from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ImproWise.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
        (r'^Login/', include('Login.urls')),
        (r'^quiz/$', 'Quiz.views.index'),
        (r'^quiz/category/$', 'Quiz.views.category_quiz'),
        (r'^quiz/result$', 'Quiz.views.result'),
        (r'^quiz/challenge/$', 'Quiz.views.challenge'),
        (r'^quiz/start_quiz/$', 'Quiz.views.start_quiz'),
    url(r'^admin/', include(admin.site.urls)),
)
