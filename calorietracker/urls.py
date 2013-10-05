from django.conf.urls import patterns, url

from calorietracker import views, import_old_db

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^test.json', views.test_json, name='test.json'),
                       url(r'^meals.json', views.meals_json, name='meals.json'),
                       url(r'^weeks.json', views.weeks_json, name='weeks.json'),
                       url(r'd3js.json', views.d3js_json, name='d3js.json'),
                       url(r'jstree.json', views.jstree_json, name='jstree.json'),
                       url(r'import_old_db', import_old_db.import_old_db, name='import_old_db')


)