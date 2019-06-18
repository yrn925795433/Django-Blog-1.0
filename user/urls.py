from django.conf.urls import url
from .views import reg,show,login

urlpatterns = [
    url(r'^reg$',reg),
    url(r'^show$',show),
    url(r'^login$',login),

]