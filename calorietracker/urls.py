from django.conf.urls import patterns, url

from calorietracker import views, import_old_db

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^jstree.json$', views.jstree_json, name='jstree.json'),
                       url(r'^import_old_db$', import_old_db.import_old_db, name='import_old_db'),
                       url(r'^calories.json$', views.calories_json, name='calories.json'),
                       url(r'^invalidate_cache$', views.invalidate_cache, name='invalidate_cache'),
                       url(r'^food.json$', views.food_json, name='food.json'),
                       url(r'^calorie_graph.js$', views.calorie_graph_js, name='calorie_graph.js'),
                       url(r'^meal_tree.js$', views.meal_tree_js, name='meal_tree.js'),
                       url(r'^add_meal$', views.add_meal, name='add_meal'),
                       url(r'^delete_meal$', views.delete_meal, name='delete_meal'),
                       url(r'^weights.json$', views.weights_json, name='weights.json'),
                       url(r'^weight_graph.js$', views.weight_graph_js, name='weight_graph.js'),
                       url(r'^add_weight', views.add_weight, name='add_weight'),
                       url(r'^mobile',views.mobile,name='mobile'),

)