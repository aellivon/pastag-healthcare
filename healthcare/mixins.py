 
from datetime import datetime
from django.utils import timezone

from pastagcore.shortcuts import get_object_or_403

from .models import BloodPressure, BodyPhysique

class BloodPressureMixin(object):
    """
        Blood pressure mixin
    """

    def get_my_latest_blood_pressure(self):
        """
            Gets the logged in user's latest blood pressure
        """
        return self.get_user_latest_blood_pressure(self.request.user)

    def get_user_latest_blood_pressure(self, user):
        """
            Gets a user's latest blood pressure
        """

        latest_blood_pressure = BloodPressure.active_objects.filter(user=user).last()

        if latest_blood_pressure:
            return latest_blood_pressure
        # Else return n/a string
        return 'n/a'

class BodyPhysiqueMixin(object):
    """
        BodyPhysique mixin
    """

    def get_my_latest_body_physique(self):
        """
            Gets the logged in user's body_physique
        """
        return self.get_user_latest_body_physique(self.request.user)

    def get_user_latest_body_physique(self, user):
        """
            Gets a user's latest body_physique
        """

        latest = BodyPhysique.active_objects.filter(user=user).order_by('record_date').last()

        if latest:
            return latest
        # Else return n/a string
        return None

    def get_my_latest_height(self, user):
        """
            Gets the user latest height
        """
        body_physique = self.get_user_latest_body_physique(self.request.user)
        if body_physique:
            return body_physique.height_in_centimeters
        return None