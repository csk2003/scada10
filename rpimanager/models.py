from django.db import models


#pole class sensor. Pleaced on the field to obtain all information for a speciffic area.

class Pole(models.Model):
	id_pole = models.IntegerField()
	is_enabled = models.BooleanField(initial=False)
	has_err = models.BooleanField(initial=False)
	creation_date = models.DateField()
	longongitude = models.DecimalField(max_digits=8, decimal_places=3)
	latitude = models.DecimalField(max_digits=8, decimal_places=3)

#the pole cone of influence. Weather data

class Cone(models.Model):
	temperature = models.FloatField()
	humidity = models.FloatField()
	wind_speed = models.IntegerField()
	water_debit = models.IntegerField()
	size_of_cone = models.IntegerField() 

#alarm class. if pole sensor missing or values out of boundry or if colision of cone

class Alarm(models.Model):
	index = models.IntegerField()
	id_alarm = models.IntegerField()
	alarm_id_pole = models.ForeignKey(id_pole)
	verbiage = models.TextField(blank=True)

