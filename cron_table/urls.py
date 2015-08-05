from django.conf.urls import include, url
from django.contrib import admin
from cron_table import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'dj_sandbox.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'create', views.create),
    url(r'save', views.save),
    url(r'show/(?P<cron_hash>[^/]+)', views.show),
    url(r'^', views.index),

]
