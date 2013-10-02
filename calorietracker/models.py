from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=50, unique=True)
    kcal_per_100g = models.IntegerField()
    grams = models.IntegerField()
    hidden = models.BooleanField()

    @property
    def total_kcal(self):
        return self.kcal_per_100g * self.grams / 100.0

    def __unicode__(self):
        return self.name


class Meal(models.Model):
    food = models.ForeignKey(Food)
    date = models.DateTimeField()

    def __unicode__(self):
        return '%s | %s | %s' % (self.date.strftime('%H:%M'), self.food.name, self.food.total_kcal)