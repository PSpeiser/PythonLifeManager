from django.conf.urls import patterns, url

from calorietracker import views, import_old_db

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^test.json$', views.test_json, name='test.json'),
                       url(r'^meals.json$', views.meals_json, name='meals.json'),
                       url(r'^weeks.json$', views.weeks_json, name='weeks.json'),
                       url(r'^jstree.json$', views.jstree_json, name='jstree.json'),
                       url(r'^import_old_db$', import_old_db.import_old_db, name='import_old_db'),
                       url(r'^plot.json$', views.plot_json, name='plot.json'),
                       url(r'^invalidate_cache$', views.invalidate_cache, name='invalidate_cache'),
                       url(r'^food.json$', views.food_json, name='food.json'),
                       url(r'^test$', views.test, name='test'),
                       url(r'^calorie_graph$', views.calorie_graph, name='calorie_graph'),
                       url(r'^calorie_graph.js$',views.calorie_graph_js,name='calorie_graph.js'),
                       url(r'^meal_tree$', views.meal_tree, name='meal_tree'),
                       url(r'^meal_tree.js$',views.meal_tree_js,name='meal_tree.js'),
                       url(r'^add_meal$',views.add_meal,name='add_meal'),



)