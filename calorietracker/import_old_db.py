from django.http import HttpResponse
from calorietracker.models import Meal, Food
import sqlite3


def import_old_db(request):
    delete_current_db()
    conn = sqlite3.connect("C:/Users/Doskir/Dropbox/CalorieTracker/caloriedb.s3db")
    c = conn.cursor()
    c.execute("SELECT * FROM food")
    foods = c.fetchall()
    for food in foods:
        f = Food(id=food[0], name=food[1], kcal_per_100g=food[2], grams=food[3], hidden=bool(food[4]))
        f.save()
    c.execute("SELECT * FROM meals")
    meals = c.fetchall()
    for meal in meals:
        m = Meal(id=meal[0], food=Food.objects.get(pk=meal[1]), date=meal[2].split('.')[0])
        m.save()
    c.close()
    conn.close()
    return HttpResponse("Imported %d foods, %d meals" % (Food.objects.count(), Meal.objects.Count()))


def delete_current_db():
    for meal in Meal.objects.all():
        meal.delete()
    for food in Food.objects.all():
        food.delete()
