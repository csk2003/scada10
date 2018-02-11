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
		if not Raspbery_Health.state_suspended:
			self.is_enabled = False
			Alarm.objects.create(pole_id=self.id,verbiage='raspbery_suspended') 
		elif  not Raspbery_Health.wind_sensor_chk:
			self.is_enabled = False
			Alarm.objects.create(pole_id=self.id,verbiage='wind_sensor_fail')
		elif not Raspbery_Health.humidity_sensor_chk: 
			self.is_enabled = False
			Alarm.objects.create(pole_id=self.id,verbiage='humidity_sensor_fail')
		elif not Raspbery_Health.water_debit_chk:
			self.is_enabled = False
			Alarm.objects.create(pole_id=self.id,verbiage='water_debit_fail')
		elif not Raspbery_Health.thermometer_chk:
			self.is_enabled = False
			Alarm.objects.create(pole_id=self.id,verbiage='thermo_fail')

#the pole cone of influence. Weather data

class Cone(models.Model):
	temperature = models.FloatField(default=0)
	humidity = models.FloatField(default=0)
	wind_speed = models.PositiveIntegerField(default=0)
	water_debit = models.PositiveIntegerField(default=0)
	size_of_cone = models.PositiveIntegerField(default=0) 
	pole = models.OneToOneField(
        Pole,
        on_delete=models.SET_NULL
    )

#alarm class. if pole sensor missing or values out of boundry or if colision of cone

class Alarm(models.Model):
	pole = models.ForeignKey(Pole)
	verbiage = models.TextField(blank=True)

	#raise alarm if pole is affected
	def log_alarm(self):
		ALARM_VERBATIM = {'raspbery_suspended': "General Failure Detected, RPI is suspended",
		'wind_sensor_fail': "Check wind sensor", 
		'humidity_sensor_fail': "Check humidity sensor"
		'water_debit_fail': "Check water debit sensor"
		'thermo_fail': "Thermometer failure"
		 }

		 failure_verbiage = ALARM_VERBATIM.get(self.verbiage, default='Alarm not found!')
		 return failure_verbiage

#raspbery model

class Raspbery_Health(models.Model):
	name = models.TextField(max_length=20)
	state_suspended = models.BooleanField(initial=True)
	wind_sensor_chk = models.BooleanField(initial=True)
	humidity_sensor_chk = models.BooleanField(initial=True)
	water_debit_chk = models.BooleanField(initial=True)
	thermometer_chk = models.BooleanField(initial=True)


