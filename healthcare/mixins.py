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

        latest_body_physique = BodyPhysique.active_objects.filter(user=user).last()

        if latest_body_physique:
            return latest_body_physique
        # Else return n/a string
        return None

    def get_my_latest_weight(self):
        """
            if latest recored exists. return weight_in_kilograms
            else return 'n/a'
        """
        physique = self.get_my_latest_body_physique()
        if physique:
            return physique.weight_in_kilograms
        return 'n/a'

    def get_my_latest_height(self):
        """
            if latest recored exists. return centimeters
            else return 'n/a'
        """
        physique = self.get_my_latest_body_physique()
        if physique:
            return physique.height_in_centimeters
        return 'n/a'