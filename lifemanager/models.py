from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=50)
    kcal_per_100g = models.IntegerField()
    grams = models.IntegerField()
    hidden = models.BooleanField()

    @property
    def total_kcal(self):
        return self.kcalper100g / 100.0 * self.grams

    def __unicode__(self):
        return self.name


class Meal(models.Model):
    food = models.ForeignKey(Food)
    date = models.DateTimeField()

    def __unicode__(self):
        return str(self.food) + ' ' + str(self.date)
