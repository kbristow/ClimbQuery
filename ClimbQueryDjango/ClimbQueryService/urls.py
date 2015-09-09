"""ClimbProjectTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, url

import v_climbingarea, v_crags, v_routes, v_load_routes

urlpatterns = patterns('',
    url(r'^ClimbingArea/', v_climbingarea.GetClimbingAreas.as_view()),
    url(r'^Crag/', v_crags.Crags.as_view()),
    url(r'^Route/', v_routes.GetRoutes.as_view()),
    url(r'^LoadRoutes/Bronkies', v_load_routes.LoadBronkies.as_view()),
    url(r'^LoadRoutes/Boven', v_load_routes.LoadBoven.as_view())
)
