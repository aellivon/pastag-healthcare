 
from datetime import datetime
from django.utils import timezone

from pastagcore.shortcuts import get_object_or_403

from .models import BloodPressure, BodyPhysique, HealthRecord

class OwnerRecordRequiredMixin(object):
    """
        Get if the one accessing the record is the owner
        If not board member, throw bad request.
    """
    # error_board = "boards/error_member.html"
    def dispatch(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        # Permission Denied if it does not exist
        get_object_or_403(HealthRecord.active_objects, pk=id, user=self.request.user)

        return super().dispatch(request, *args, **kwargs)

class ApiDateRangeMixin(object):
    """
        Common code for extracting from date and until date on
        graph api
    """

    def extract_from_date_and_until_date(self, *args, **kwargs):
        today_date = timezone.localtime()
        last_month = self.get_last_month(today_date)
        from_date = self.request.GET.get("from_date", None)
        until_date = self.request.GET.get("until_date", None)

        if from_date:
            from_date = timezone.localtime(timezone.make_aware(datetime.strptime(from_date, "%Y-%m-%d")))
        else:
            from_date = last_month

        if until_date:
            until_date = timezone.localtime(timezone.make_aware(datetime.strptime(until_date, "%Y-%m-%d")))
            until_date = until_date.replace(hour=23, minute=59, second=59)
        else:
            until_date = today_date

        return from_date, until_date

    def get_last_month(self, today_date):
        """
            Gets last month without losing the timezone
        """
        last_full_month = today_date
        last_month = today_date.month - 1

        if last_month == 0:
            last_month = 1

        invalid = True
        to_substract = 0
        while invalid and to_substract < 33:
            try:
                last_full_month = today_date.replace(month=last_month, day=today_date.day - to_substract)
                invalid = False
            except ValueError as e:
                print(e)
                to_substract += 1

        return last_full_month

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

        latest = BloodPressure.active_objects.filter(user=user).order_by('record_date').last()

        if latest:
            return latest
        # Else return n/a string
        return None

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