from django.conf.urls import include, url
from django.contrib import admin
from cron_table import urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'dj_sandbox.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^cron_table/', include('cron_table.urls')),
]
