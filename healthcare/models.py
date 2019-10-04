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