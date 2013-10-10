from django.http import HttpResponse
from calorietracker.models import Meal, Food
from django.core import serializers
from datetime import datetime, timedelta
import json
from django.template import RequestContext, loader
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import patch_cache_control
from functools import wraps
from django.core.cache import cache


def index(request):
    template = loader.get_template('calorietracker.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def add_meal(request):
    if request.method == "POST":
        try:
            if 'food_id' in request.POST:
                food_id = request.POST['food_id']
                food = Food.objects.get(pk=food_id)
                meal = Meal(food=food, date=datetime.now())
                meal.save()
                #clear the cache so the client can get the new data
                cache.clear()
                output = "Success"
            else:
                output = "Error food_id was not supplied"
        except Exception as e:
            output = "Error"
    else:
        output = "Method not supported"
    return HttpResponse(output)

def calorie_graph(request):
    template = loader.get_template('calorie_graph.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def calorie_graph_js(request):
    template = loader.get_template('calorie_graph.js')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def meal_tree(request):
    template = loader.get_template('meal_tree.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def meal_tree_js(request):
    template = loader.get_template('meal_tree.js')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def meals_json(request):
    meals = Meal.objects.order_by('date')
    output = serializers.serialize('json', meals, indent=2, use_natural_keys=True, )
    return HttpResponse(output, content_type='application/json')


def test_json(request):
    return HttpResponse("")


def test(request):
    template = loader.get_template('test.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def weeks_json(request):
    weeks = get_weeks()

    output = json.dumps(weeks, indent=2, cls=MyEncoder)
    return HttpResponse(output, content_type='application/json')


def get_weeks():
    meals = Meal.objects.order_by('date')

    firstdt = meals[0].date if meals.count() > 0 else datetime.now()
    firstdt = firstdt - timedelta(days=firstdt.weekday(), hours=firstdt.hour,
                                  minutes=firstdt.minute, seconds=firstdt.second)

    lastdt = meals[meals.count() - 1].date if meals.count() > 0 else datetime.now()
    lastdt = lastdt - timedelta(hours=lastdt.hour,
                                minutes=lastdt.minute, seconds=lastdt.second)
    lastdt = lastdt + timedelta(days=(6 - lastdt.weekday()), hours=23, minutes=59, seconds=59)

    weeks = []
    dt = firstdt
    while dt < lastdt:
        week = Week(dt)
        for day in week.days:
            day.meals = [meal for meal in meals if day.contains(meal.date)]
        weeks.append(week)
        dt = dt + timedelta(days=7)
    return weeks


def no_client_cache(decorated_function):
    """Like Django @never_cache but sets more valid cache disabling headers.

    @never_cache only sets Cache-Control:max-age=0 which is not
    enough. For example, with max-age=0 Firefox returns cached results
    of GET calls when it is restarted.
    """

    @wraps(decorated_function)
    def wrapper(*args, **kwargs):
        response = decorated_function(*args, **kwargs)
        patch_cache_control(
            response, no_cache=True, no_store=True, must_revalidate=True,
            max_age=0)
        return response

    return wrapper


def food_json(request):
    data = []
    for food in Food.objects.all().order_by('name'):
        data.append([food.id, food.name, food.total_kcal])
    d = {'aaData': data}
    output = json.dumps(d, indent=2)
    return HttpResponse(output, content_type='application/json')


@no_client_cache
@cache_page(60 * 15)
def jstree_json(request):
    weeks = get_weeks()
    d = []
    for week in weeks:
        d3week = {'data': str(week), 'children': [],
                  'attr': {'class': 'week', 'jstree_color': 'red' if week.total_kcal > 1500 * 7 else 'green'}}
        for day in week.days:
            d3day = {'data': str(day), 'children': [],
                     'attr': {'class': 'day', 'jstree_color': 'red' if day.total_kcal > 1500 else 'green'}}
            for meal in day.meals:
                d3meal = {'data': str(meal), 'attr': {'class': 'meal', 'meal_id': meal.id}}
                d3day['children'].append(d3meal)

            #don't allow empty children lists
            if len(d3day['children']) == 0:
                del d3day['children']

            #expand current day by default
            if 'children' in d3day and day.contains(datetime.now()):
                d3day['state'] = 'open'
            d3week['children'].append(d3day)

        #expand current week by default
        if week.contains(datetime.now()):
            d3week['state'] = 'open'

        d.append(d3week)
    d = d[::-1]

    output = json.dumps(d, indent=2, cls=MyEncoder)
    response = HttpResponse(output, content_type='application/json')
    return response


@no_client_cache
@cache_page(60 * 15)
def plot_json(request):
    weeks = get_weeks()
    datapoints = []
    for week in weeks:
        for day in week.days:
            if datetime.now() >= day.begin:
                datapoints.append({"date": day.begin.strftime("%Y-%m-%d"), "kcal": day.total_kcal})
    output = json.dumps(datapoints, indent=2, cls=MyEncoder)
    return HttpResponse(output, content_type='application/json')


def invalidate_cache(request):
    from django.core.cache import cache

    output = cache.clear()
    return HttpResponse(str(output))


class Week():
    def __init__(self, begin):
        self.begin = begin
        self.end = begin + timedelta(days=6, hours=23, minutes=59, seconds=59)
        self.days = [Day(begin + timedelta(days=i)) for i in range(0, 7)]

    @property
    def total_kcal(self):
        return sum([day.total_kcal for day in self.days])

    def contains(self, date):
        return self.begin <= date <= self.end

    def __unicode__(self):
        return '%s-%s | %s' % (self.begin.strftime('%Y.%m.%d'), self.end.strftime('%d'), str(self.total_kcal))

    def __str__(self):
        return unicode(self).encode('utf-8')


class Day():
    def __init__(self, begin):
        self.begin = begin
        self.end = begin + timedelta(hours=23, minutes=59, seconds=59)
        self.meals = []

    @property
    def total_kcal(self):
        return sum([meal.food.total_kcal for meal in self.meals])

    def contains(self, date):
        return self.begin <= date <= self.end

    def __unicode__(self):
        return '%s | %s' % (self.begin.strftime('%Y.%m.%d'), str(self.total_kcal))

    def __str__(self):
        return unicode(self).encode('utf-8')


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Week):
            return {'begin': obj.begin, 'end': obj.end, 'days': obj.days, 'total_kcal': obj.total_kcal}
        if isinstance(obj, Day):
            return {'begin': obj.begin, 'end': obj.end, 'meals': obj.meals, 'total_kcal': obj.total_kcal}

        if isinstance(obj, Meal):
            d = instance_dict(obj)
            d['total_kcal'] = obj.food.total_kcal
            d['food']['total_kcal'] = obj.food.total_kcal
            return d
        if isinstance(obj, Food):
            pass

        return json.JSONEncoder.default(self, obj)


def instance_dict(instance, key_format=None):
    """Returns a dictionary containing field names and values for the given instance"""
    from django.db.models.fields.related import ForeignKey

    if key_format:
        assert '%s' in key_format, 'key_format must contain a %s'
    key = lambda key: key_format and key_format % key or key

    d = {}
    for field in instance._meta.fields:
        attr = field.name
        value = getattr(instance, attr)
        if value is not None and isinstance(field, ForeignKey):
            value = value._get_pk_val()
            if isinstance(instance, Meal):
                value = instance_dict(Food.objects.get(pk=value))

        d[key(attr)] = value
    for field in instance._meta.many_to_many:
        d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
    return d
