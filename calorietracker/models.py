from django.db import models
import math


class Food(models.Model):
    name = models.CharField(max_length=50, unique=True)
    kcal_per_100g = models.IntegerField()
    grams = models.IntegerField()
    hidden = models.BooleanField()

    @property
    def total_kcal(self):
        return int(math.floor(self.kcal_per_100g * self.grams / 100.0))

    def __unicode__(self):
        return self.name


class Meal(models.Model):
    food = models.ForeignKey(Food)
    date = models.DateTimeField()

    def __unicode__(self):
        return '%s | %s | %s' % (self.date.strftime('%H:%M'), self.food.name, self.food.total_kcal)


class Weight(models.Model):
    date = models.DateField(unique=True)
    kg = models.DecimalField(decimal_places=1, max_digits=4)
    fat = models.DecimalField(decimal_places=1, max_digits=4)
    water = models.DecimalField(decimal_places=1, max_digits=4)
    muscles = models.DecimalField(decimal_places=1, max_digits=4)
    bone_kg = models.DecimalField(decimal_places=1, max_digits=4)
    bmr = models.PositiveIntegerField()
    amr = models.PositiveIntegerField()

    def __unicode__(self):
        return '%s | %s' % (self.date.strftime('%Y-%m-%d %H:%M'), self.kg)
