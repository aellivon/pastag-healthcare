from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import CommonInfo

from decimal import Decimal


class HealthRecord(CommonInfo):
    """
        This is the model for the health records itself
    """

    record_types = {
        "blood_pressure": 0,
        "body_physique": 1
    }

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    details = models.TextField(max_length=255, null=True, blank=True)
    record_date = models.DateTimeField(null=True)
    key_words = models.TextField(max_length=1024, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # This adds record date now when submitted empty
        if not self.record_date:
            self.record_date = timezone.localtime(timezone.now())

        if not self.details:
            self.details = "No details available"

        # TODO: There must be a better way to search a date by string!
        record_date_with_time_zone = timezone.localtime(self.record_date).strftime('%B %d, %Y %I %M %I:%M %p')

        self.key_words = ""
        self.key_words += f'{record_date_with_time_zone} {self.state}'

        return super(HealthRecord, self).save(force_insert, force_update, using,
                                              update_fields)

    @property
    def formatted_record_date(self):
        # Custom format record to a readable format
        record_date_with_time_zone = timezone.localtime(self.record_date)
        return f"{record_date_with_time_zone.strftime('%B %d, %Y, %I:%M %p')}"

    @property
    def date(self):
        record_date_with_time_zone = timezone.localtime(self.record_date)
        return f"{record_date_with_time_zone.strftime('%B %d, %Y')}"

    @property
    def time(self):
        record_date_with_time_zone = timezone.localtime(self.record_date)
        return f"{record_date_with_time_zone.strftime('%I:%M %p')}"

    @property
    def state(self):
        # If the parent state is called, try to get type or return n/a
        # We need to define the type of record first

        if hasattr(self, 'bloodpressure'):
            return self.bloodpressure.state
        elif hasattr(self, 'bodyphysique'):
            return self.bodyphysique.state
        return "n/a"

    def get_record_type(self):
        # If the parent state is called, try to get type or return n/a
        # We need to define the type of record first

        if hasattr(self, 'bloodpressure'):
            return self.record_types.get("blood_pressure")
        elif hasattr(self, 'bodyphysique'):
            return self.record_types.get("body_physique")
        return "n/a"


class BloodPressure(HealthRecord):
    """
    This is the model for a bloodpressure record
    """

    states = {
        "normal": "Normal Blood Pressure",
        "elevated": "Elevated Hypertension",
        "high": "Hypertension Stage I (High)",
        "very_high": "Hypertension Stage II (Very High)",
        "risky": "Hypertension Crisis (Risky)",
        "low": "Alarmingly Low"
    }

    systolic_pressure = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
    diastolic_pressure = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])

    # NOTE: These are separated to use these constants more manageable
    #   epsecially useful in the paragraph feature!
    #   (Also more maintanable)

    # Note: The numbers should be increasing
    # SYSTOLIC PART

    BORDERLINE = {
        "LOW": {
            "SYSTOLIC": {
                "UPPER": 89
            },
            "DIASTOLIC": {
                "UPPER": 59
            }
        },
        "NORMAL": {
            "SYSTOLIC": {
                "LOWER": 90,
                "UPPER": 119
            },
            "DIASTOLIC": {
                "LOWER": 60,
                "UPPER": 79
            }
        },
        "ELEVATED": {
            "SYSTOLIC": {
                "LOWER": 120,
                "UPPER": 129
            },
            "DIASTOLIC": {
                "LOWER": 60,
                "UPPER": 79
            }
        },
        "HIGH": {
            "SYSTOLIC": {
                "LOWER": 130,
                "UPPER": 139
            },
            "DIASTOLIC": {
                "LOWER": 80,
                "UPPER": 89
            }
        },
        "VERY_HIGH": {
            "SYSTOLIC": {
                "LOWER": 140,
                "UPPER": 180
            },
            "DIASTOLIC": {
                "LOWER": 90,
                "UPPER": 120
            }
        },
        "RISKY": {
            "SYSTOLIC": {
                "LOWER": 181
            },
            "DIASTOLIC": {
                "LOWER": 121
            }
        }
    }

    def __str__(self):
        # TODO: change this
        return f"{self.user}"

    def is_systolic_okay(self):
        if (self.systolic_pressure >= self.BORDERLINE["NORMAL"]["SYSTOLIC"]["LOWER"] and
                self.systolic_pressure <= self.BORDERLINE["NORMAL"]["SYSTOLIC"]["UPPER"]):
            return True
        return False

    def is_diastolic_okay(self):
        if (self.diastolic_pressure >= self.BORDERLINE["NORMAL"]["DIASTOLIC"]["LOWER"] and
                self.diastolic_pressure <= self.BORDERLINE["NORMAL"]["DIASTOLIC"]["UPPER"]):
            return True
        return False

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
        # https://www.heart.org/en/health-topics/high-blood-pressure/the-facts-about-high-blood-pressure/low-blood-pressure-when-blood-pressure-is-too-low

        if ((self.systolic_pressure >= self.BORDERLINE["NORMAL"]["SYSTOLIC"]["LOWER"] and
                self.systolic_pressure <= self.BORDERLINE["NORMAL"]["SYSTOLIC"]["UPPER"]) and
            (self.diastolic_pressure >= self.BORDERLINE["NORMAL"]["DIASTOLIC"]["LOWER"] and
                self.diastolic_pressure <= self.BORDERLINE["NORMAL"]["DIASTOLIC"]["UPPER"])):
            # Range is 90 - 119
            # 60 - 79
            return self.states.get('normal')

        elif((self.systolic_pressure >= self.BORDERLINE["ELEVATED"]["SYSTOLIC"]["LOWER"] and
                self.systolic_pressure <= self.BORDERLINE["ELEVATED"]["SYSTOLIC"]["UPPER"]) and
             (self.diastolic_pressure >= self.BORDERLINE["ELEVATED"]["DIASTOLIC"]["LOWER"] and
                self.diastolic_pressure <= self.BORDERLINE["ELEVATED"]["DIASTOLIC"]["UPPER"])):
            # Range is 120 - 129 and 60 - 79
            return self.states.get('elevated')

        elif(self.systolic_pressure >= self.BORDERLINE["RISKY"]["SYSTOLIC"]["LOWER"] or
                self.diastolic_pressure >= self.BORDERLINE["RISKY"]["DIASTOLIC"]["LOWER"]):
            # Calculate the risky here since this one should override things
            # without constraints
            return self.states.get('risky')

        elif((self.systolic_pressure >= self.BORDERLINE["VERY_HIGH"]["SYSTOLIC"]["LOWER"] and
                self.systolic_pressure <= self.BORDERLINE["VERY_HIGH"]["SYSTOLIC"]["UPPER"]) or
             (self.diastolic_pressure >= self.BORDERLINE["VERY_HIGH"]["DIASTOLIC"]["LOWER"] and
                self.diastolic_pressure <= self.BORDERLINE["VERY_HIGH"]["DIASTOLIC"]["UPPER"])):
            return self.states.get('very_high')

        elif((self.systolic_pressure >= self.BORDERLINE["HIGH"]["SYSTOLIC"]["LOWER"] and
                self.systolic_pressure <= self.BORDERLINE["HIGH"]["SYSTOLIC"]["UPPER"]) or
             (self.diastolic_pressure >= self.BORDERLINE["HIGH"]["DIASTOLIC"]["LOWER"] and
                self.diastolic_pressure <= self.BORDERLINE["HIGH"]["DIASTOLIC"]["UPPER"])):
            # Range is 130 - 139 OR 80 - 89
            return self.states.get('high')

        elif (self.systolic_pressure <= self.BORDERLINE["LOW"]["SYSTOLIC"]["UPPER"] or
                self.diastolic_pressure <= self.BORDERLINE["LOW"]["DIASTOLIC"]["UPPER"]):
            # Range is 90 down and 60 down
            return self.states.get('low')


class BodyPhysique(HealthRecord):
    """
    This is the model for a the user's body physique record
    """
    states = {
        "under": "Underweight",
        "normal": "Normal Weight",
        "over": "Overweight",
        "obese": "Obesity"
    }

    # Weight
    weight_in_kilograms = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Weight (kg)",
                                              validators=[MinValueValidator(1), MaxValueValidator(999)])
    # Height
    height_in_centimeters = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Height (cm)",
                                                validators=[MinValueValidator(1), MaxValueValidator(999)])

    # Borderline constants
    BORDERLINE = {
        "UNDER": {
            "UPPER": 18.49
        },
        "NORMAL": {
            "LOWER": 18.5,
            "UPPER": 24.99
        },
        "OVER": {
            "LOWER": 25,
            "UPPER": 29.99
        },
        "OBESE": {
            "LOWER": 30
        }
    }

    def __str__(self):
        return f"{self.user}"

    def _strip_zero(self, num):
        if num == num.to_integral():
            return num.to_integral()
        return num.normalize()

    @property
    def height(self):
        # Trims zeroes, should only be used on displaying numbers
        return self._strip_zero(self.height_in_centimeters)

    @property
    def weight(self):
        # Trims zeroes, should only be used on displaying numbers
        return self._strip_zero(self.weight_in_kilograms)

    @property
    def height_weight_and_bmi(self):
        return f"({self.height}cm  & {self.weight}kg)"

    @property
    def bmi(self):
        """
            Calculates bmi for interpratation
            Based on:
            https://www.cdc.gov/healthyweight/assessing/bmi/childrens_bmi/childrens_bmi_formula.html
        """
        return round(self.weight_in_kilograms / (self.height_in_meters**2), 2)

    @property
    def height_in_meters(self):
        """
            Convert height height_in_centimeters to height_in_meters
        """
        return self.height_in_centimeters * Decimal(0.01)

    @property
    def state(self):
        """
            Return the bmi state here too, do not merge bmi state and state.
            We might have multiple state on a body physique
        """
        return self.bmi_state

    @property
    def bmi_state(self):
        """
            Underweight = <18.5.
            Normal weight = 18.5–24.99
            Overweight = 25–29.99
            Obesity = BMI of 30 or greater.
        """
        if self.bmi <= self.BORDERLINE["UNDER"]["UPPER"]:
            return self.states.get('under')
        elif self.bmi >= self.BORDERLINE["NORMAL"]["LOWER"] and self.bmi <= self.BORDERLINE["NORMAL"]["UPPER"]:
            return self.states.get('normal')
        elif self.bmi >= self.BORDERLINE["OVER"]["LOWER"] and self.bmi <= self.BORDERLINE["OVER"]["UPPER"]:
            return self.states.get('over')
        elif self.bmi >= self.BORDERLINE["OBESE"]["LOWER"]:
            return self.states.get('obese')

        def is_bmi_normal(self):
            """
                Checks if the bmi is normal
            """
            if self.bmi >= self.BORDERLINE["NORMAL"]["LOWER"] and self.bmi <= self.BORDERLINE["NORMAL"]["UPPER"]:
                return True
            return False

    def calculate_penalty(self):
        """
            Calculates the penalty the bmi state.
            This is directly connected to the evaluation on gui.
        """
        if not self.bmi_state == self.states.get('normal'):
            # only calculate penalty if normal
            if (self.bmi_state == self.states.get('over') or
                    self.bmi_state == self.states.get('obese')):

                # Group higher states to make it's baseline 30
                # TODO: Test this
                import math
                return math.floor(30 - self.bmi)

        return 0
