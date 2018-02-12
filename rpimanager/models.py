from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from math import sin, cos, sqrt, atan2, radians


#pole class sensor. Pleaced on the field to obtain all information for a speciffic area.

class Pole(models.Model):
    is_enabled = models.BooleanField(default=False)
    has_err = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now_add=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=3)
    latitude = models.DecimalField(max_digits=8, decimal_places=3)

    #pole failure is given by the absence of a sensor or the rpi
    def pole_failure(self):
        if not Raspbery_Health.state_suspended:
            self.is_enabled = False
            Alarm.objects.create(pole_id=self.id,verbiage='raspbery_suspended') 
        elif not Raspbery_Health.wind_sensor_chk:
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

    def has_raspberry(self):
        try:
            rasp = self.raspbery
        except Raspbery.DoesNotExist:
            return False
        else:
            return True

    def colision(self):
    	r=6373000 #radius of earth in m
    	#curret long and latitude
    	c_log = radians(self.longitude)
    	c_lat = radians(self.latitude)
    	c_id = self.id
    	for e in pole.objects.all():
    		#each long and lat
    		elongit = radians(e.longitude)
    		elatit = radians(e.latitude)
    		dlon = elongit-c_log
    		dlat = elatit-c_lat
    		a = sin(dlat/2)**2+cos(c_lat)*sin(dlon/2)**2
    		c = 2*asin(sqrt(a))
    		dist = c * r
    		if e.id == c_id:
    			pass
    		else
    			if dist <= 20:
    				Alarm.objects.create(pole_id=c_id,verbiage='colision')




class Cone(models.Model):
    temperature = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    wind_speed = models.PositiveIntegerField(default=0)
    water_debit = models.PositiveIntegerField(default=0)
    size_of_cone = models.PositiveIntegerField(default=0) 
    pole = models.OneToOneField(
        Pole,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


#TODO de facut calculul de debit petru aspersor


#alarm class. if pole sensor missing or values out of boundry or if colision of cone

class Alarm(models.Model):
    pole = models.ForeignKey(
        Pole,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    verbiage = models.TextField(blank=True)

    #raise alarm if pole is affected
    def log_alarm(self):
        ALARM_VERBATIM = {
            'raspbery_suspended': "General Failure Detected, RPI is suspended",
            'wind_sensor_fail': "Check wind sensor", 
            'humidity_sensor_fail': "Check humidity sensor",
            'water_debit_fail': "Check water debit sensor",
            'thermo_fail': "Thermometer failure",
            'colision': "Colision move poles further apart"
        }

        failure_verbiage = ALARM_VERBATIM.get(self.verbiage, default='Alarm not found!')
        return failure_verbiage

#raspbery model

class Raspbery(models.Model):
    name = models.TextField(max_length=20)
    state_suspended = models.BooleanField(default=True)
    wind_sensor_chk = models.BooleanField(default=True)
    humidity_sensor_chk = models.BooleanField(default=True)
    water_debit_chk = models.BooleanField(default=True)
    thermometer_chk = models.BooleanField(default=True)
    ping_probe = models.BooleanField(default=True)
    pole = models.OneToOneField(
        Pole,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

#post save of rpi if it is attached to pole ad if so if we got colision of cones
@receiver(post_save, sender=Raspbery)
def attach_cone(sender, instance, created, **kwargs):
    if not created:
        if instance.pole:
            if instance.pole.has_raspberry():
                Cone.objects.create(pole=instance.pole)
                #if colision create alarm