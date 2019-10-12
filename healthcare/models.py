from django.db import models
from django.contrib.auth import get_user_model

class ActiveManager(models.Manager):
    """
        This class defines a new default query set so the project can always
            filter data that is active
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class CommonInfo(models.Model):
    """
        This class is the parent class for all the models
    """
    is_active = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # This allows me to escape to default django query set if 
    #   later in the project I need it
    objects = models.Manager()
    
    # for active query set
    active_objects =ActiveManager()

    class Meta:
        abstract = True


class HealthRecordCommonInfo(CommonInfo):
    """
        This is the model for the health records itself
    """
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    details = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True

# NOTE: We are putting the models here since this could be extendable
# in the near future! 

class BloodPressure(HealthRecordCommonInfo):
    """
        This is the model for a bloodpressure record
    """

    states = {
        "normal":"Normal Blood Pressure",
        "elevated": "Elevated Hypertension",
        "high": "Hypertension Stage I",
        "very_high": "Hypertension Stage II",
        "risky": "Hypertension Crisis",
        "low": "Hypotension"
    }

    systolic_pressure = models.IntegerField()
    diastolic_pressure = models.IntegerField()

    def __str__(self):
        return f"{self.user}"

    @property
    def pressure(self):
        """
            A more readable format for blood pressure
        """
        return f"{self.systolic_pressure}/{self.diastolic_pressure}"

    @property
    def state(self):
        # Based on
        # https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings

        if ((self.systolic_pressure >= 90 and self.systolic_pressure < 120) and
            (self.diastolic_pressure >= 60 and self.diastolic_pressure < 80)):
            # Range is 90 - 119
            # 60 - 79
            return self.states.get('normal')
        elif((self.systolic_pressure >= 120 and self.systolic_pressure < 130) and
            (self.diastolic_pressure >= 60 and self.diastolic_pressure < 80)):
            # Range is 120 - 129 and 60 - 79
            return self.states.get('elevated')
        elif(self.systolic_pressure > 180 or self.diastolic_pressure > 120):
            # Calculate the risky here since this one should override things
            # without constraints
            return self.states.get('risky')
        elif(self.systolic_pressure >= 140 or self.diastolic_pressure >= 90):
            return self.states.get('very_high')
        elif ((self.systolic_pressure >= 130 and self.systolic_pressure < 140) or
              (self.diastolic_pressure >= 80 and self.diastolic_pressure < 90)):
            # Range is 130 - 139 OR 80 - 89
            return self.states.get('high')
        elif (self.systolic_pressure < 90 or self.diastolic_pressure < 60):
            # Range is 90 down and 60 down
            return self.states.get('low')

class BodyPhysique(HealthRecordCommonInfo):
    """
        This is the model for a the user's body physique record
    """

    states = {
        "under":"Underweight",
        "normal": "Normal weight",
        "over": "Overweight",
        "obese": "Obesity"
    }

    # Weight
    weight_in_kilograms = models.IntegerField()
    # Height
    height_in_centimeters = models.IntegerField()

    def __str__(self):
        return f"{self.user}"

    def _calculate_bmi(self):
        """
            Calculates bmi for interpratation
            Based on:
            https://www.cdc.gov/healthyweight/assessing/bmi/childrens_bmi/childrens_bmi_formula.html
        """
        return self.weight_in_kilograms / (self.height_in_meters**2)

    @property
    def height_in_meters(self):
        """
            Convert height height_in_centimeters to height_in_meters
        """
        return self.height_in_centimeters * 0.01

    @property
    def bmi_state(self):
        """
            Underweight = <18.5.
            Normal weight = 18.5–24.9.
            Overweight = 25–29.9.
            Obesity = BMI of 30 or greater.
        """
        bmi = self._calculate_bmi()
        if bmi < 18.5:
            return self.states.get('under')
        elif bmi >= 18.5 and  bmi < 25:
            return self.states.get('normal')
        elif bmi >= 25 and bmi < 30:
            return self.states.get('over')
        elif bmi > 30:
            return self.states.get('obese')

    def calculate_penalty(self):
        """
            Calculates the penalty the bmi state.
            This is directly connected to the face that is in the gui.
        """
        if not self.bmi_state == self.states.get('normal'):
            # only calculate penalty if normal
            if (self.bmi_state == self.states.get('over') or
                self.bmi_state == self.states.get('obese')):
                # Group higher states to make it's baseline 30

                # TODO: Test this
                import math
                return math.floor(30 - self._calculate_bmi)

        return 0
