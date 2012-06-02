from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth import views as auth_views
from django_webauth.views import LogoutView

from humfrey.desc import views as desc_views
from humfrey.images import views as images_views
from humfrey.misc import views as misc_views

from dataox.equipment import views as equipment_views
from dataox.equipment.resource import resource_registry

from humfrey.misc.views import SimpleView

mapping_kwargs = {'id_mapping': (('https://data.ox.ac.uk/id/equipment/', 'https://www.research-facilities.ox.ac.uk/view/', True),),
                  'doc_view': ('equipment', 'doc-generic'),
                  'desc_view': ('equipment', 'desc'),
                  'resource_registry': resource_registry}

urlpatterns = patterns('',
    url(r'^search/$', equipment_views.SearchView.as_view(**mapping_kwargs), name='search'),

    url(r'^view/$', equipment_views.DocView.as_view(**mapping_kwargs), name='doc-generic'),
    url(r'^view.+$', equipment_views.DocView.as_view(**mapping_kwargs), name='doc'),
    url(r'^desc/$', equipment_views.DescView.as_view(**mapping_kwargs), name='desc'),

    url(r'^browse/(?:(?P<notation>[a-z\-\d\/]+)/)?$', equipment_views.BrowseView.as_view(**mapping_kwargs), name='browse'),

    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^webauth/', include('django_webauth.urls', 'webauth')),

    url(r'^$', misc_views.SimpleView.as_view(template_name="equipment/index"), name='index'),
    url(r'^about/$', misc_views.SimpleView.as_view(template_name="equipment/about"), name='about'),
    url(r'^contact/$', misc_views.SimpleView.as_view(template_name="equipment/contact"), name='contact'),
    url(r'^legal-and-privacy/$', misc_views.SimpleView.as_view(template_name='legal'), name='legal'),
    url(r'^thumbnail/$', images_views.ResizedImageView.as_view(), name='resized-image'),
    
) + staticfiles_urlpatterns()

handler404 = SimpleView.as_view(template_name='404-main', context={'status_code':404})
handler500 = SimpleView.as_view(template_name='500', context={'status_code':500})
