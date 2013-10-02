from django.conf.urls import patterns, url

from calorietracker import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^test.json',views.test_json,name='test.json'),
    url(r'^meals.json',views.meals_json,name='meals.json'),
    url(r'^weeks.json',views.weeks_json,name='weeks.json'),
    url(r'flare.json',views.flare_json,name='flare.json'),
    url(r'd3js.json',views.d3js_json,name='d3js.json'),



)