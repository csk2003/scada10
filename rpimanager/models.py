from django.db import models


#pole class sensor. Pleaced on the field to obtain all information for a speciffic area.

class Pole(models.Model):
	id_pole = models.IntegerField()
	is_enabled = models.BooleanField(initial=False)
	has_err = models.BooleanField(initial=False)
	creation_date = models.DateField()
	longongitude = models.DecimalField(max_digits=8, decimal_places=3)
	latitude = models.DecimalField(max_digits=8, decimal_places=3)

	#pole failure is given by the absence of a sensor or the rpi
	def pole_failure(self):
		if !Raspbery_Health.state_suspended:
			is_enabled = False
			alarm.log_alarm(raspbery_suspended) 
		elif !Raspbery_Health.wind_sensor_chk:
			is_enabled = False
			alarm.log_alarm(wind_sensor_fail)
		elif !Raspbery_Health.humidity_sensor_chk: 
			is_enabled = False
			alarm.log_alarm(humidity_sensor_fail)
		elif !Raspbery_Health.water_debit_chk:
			is_enabled = False
			alarm.log_alarm(water_debit_fail)
		elif !Raspbery_Health.thermometer_chk:
			is_enabled = False
			alarm.log_alarm(thermo_fail)


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

	#raise alarm if pole is affected
	def log_alarm(self, failure):
		alarm_verbatim = {'raspbery_suspended': "General Failure Detected, RPI is suspended",
		'wind_sensor_fail': "Check wind sensor", 
		'humidity_sensor_fail': "Check humidity sensor"
		'water_debit_fail': "Check water debit sensor"
		'thermo_fail': "Thermometer failure"
		 }

		 failure_verbiage = alarm_verbatim[failure]
		 return failure_verbiage




#raspbery model

class Raspbery_Health(models.Model):
	name = models.TextField(max_length=20)
	state_suspended = models.BooleanField(initial=True)
	wind_sensor_chk = models.BooleanField(initial=True)
	humidity_sensor_chk = models.BooleanField(initial=True)
	water_debit_chk = models.BooleanField(initial=True)
	thermometer_chk = models.BooleanField(initial=True)


