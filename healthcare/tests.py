from django.test import TestCase

from .models import BloodPressure

# View testcases

class ViewsTestCases(TestCase):

    def test_retrieving_dashboard(self):
        pass

    def test_retrieving_dashboard_with_unauthenticated_credentials(self):
        pass

    def test_retrieving_dashboard_of_with_invalid_credentials(self):
        pass

# Model testcases

class BloodPressureTestCases(TestCase):
    """
        Makes sures all calculation in blood pressure is accurate

        Always test the borderline. Usually mistakes comes from here
    """

    def test_upper_systolic_borderline_normal(self):

        to_test = BloodPressure(systolic_pressure=119,diastolic_pressure=70)
        self.assertEqual(to_test.state, BloodPressure.states.get('normal'))

    def test_lower_systolic_borderline_normal(self):

        to_test = BloodPressure(systolic_pressure=90,diastolic_pressure=70)
        self.assertEqual(to_test.state, BloodPressure.states.get('normal'))

    def test_upper_diastolic_borderline_normal(self):

        to_test = BloodPressure(systolic_pressure=90,diastolic_pressure=79)
        self.assertEqual(to_test.state, BloodPressure.states.get('normal'))

    def test_lower_diastolic_borderline_normal(self):

        to_test = BloodPressure(systolic_pressure=90,diastolic_pressure=60)
        self.assertEqual(to_test.state, BloodPressure.states.get('normal'))

    def test_upper_systolic_borderline_elevated(self):

        to_test = BloodPressure(systolic_pressure=129,diastolic_pressure=79)
        self.assertEqual(to_test.state, BloodPressure.states.get('elevated'))

    def test_lower_systolic_borderline_elevated(self):
        to_test = BloodPressure(systolic_pressure=120,diastolic_pressure=79)
        self.assertEqual(to_test.state, BloodPressure.states.get('elevated'))

    def test_upper_systolic_borderline_high(self):
        to_test = BloodPressure(systolic_pressure=139,diastolic_pressure=70)
        self.assertEqual(to_test.state, BloodPressure.states.get('high'))

    def test_lower_systolic_borderline_high(self):
        to_test = BloodPressure(systolic_pressure=130,diastolic_pressure=70)
        self.assertEqual(to_test.state, BloodPressure.states.get('high'))

    def test_upper_diastolic_borderline_high(self):
        to_test = BloodPressure(systolic_pressure=90,diastolic_pressure=89)
        self.assertEqual(to_test.state, BloodPressure.states.get('high'))

    def test_lower_diastolic_borderline_high(self):
        to_test = BloodPressure(systolic_pressure=90,diastolic_pressure=80)
        self.assertEqual(to_test.state, BloodPressure.states.get('high'))

    def test_lower_systolic_borderline_very_high(self):
        to_test = BloodPressure(systolic_pressure=140,diastolic_pressure=70)
        self.assertEqual(to_test.state, BloodPressure.states.get('very_high'))

    def test_lower_diastolic_borderline_very_high(self):
        to_test = BloodPressure(systolic_pressure=119,diastolic_pressure=90)
        self.assertEqual(to_test.state, BloodPressure.states.get('very_high'))

    def test_upper_systolic_borderline_very_high(self):
        to_test = BloodPressure(systolic_pressure=180,diastolic_pressure=70)
        self.assertEqual(to_test.state, BloodPressure.states.get('very_high'))

    def test_upper_diastolic_borderline_very_high(self):
        to_test = BloodPressure(systolic_pressure=119,diastolic_pressure=120)
        self.assertEqual(to_test.state, BloodPressure.states.get('very_high'))

    def test_lower_systolic_borderline_very_risky(self):
        to_test = BloodPressure(systolic_pressure=181,diastolic_pressure=90)
        self.assertEqual(to_test.state, BloodPressure.states.get('risky'))

    def test_lower_diastolic_borderline_very_risky(self):
        to_test = BloodPressure(systolic_pressure=119,diastolic_pressure=121)
        self.assertEqual(to_test.state, BloodPressure.states.get('risky'))

    def test_upper_systolic_borderline_very_low(self):
        to_test = BloodPressure(systolic_pressure=89,diastolic_pressure=70)
        self.assertEqual(to_test.state, BloodPressure.states.get('low'))

    def test_upper_diastolic_borderline_very_low(self):
        to_test = BloodPressure(systolic_pressure=100,diastolic_pressure=59)
        self.assertEqual(to_test.state, BloodPressure.states.get('low'))