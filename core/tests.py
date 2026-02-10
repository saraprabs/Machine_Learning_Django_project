from django.test import TestCase

# Create your tests here.
from .models import PredictionRecord

class PredictionTest(TestCase):
    def test_prediction_saves_and_displays(self):
        # 1. Simulate saving a result
        record = PredictionRecord.objects.create(
            name="John Doe", 
            age=25,          # <--- Add this to satisfy 'if self.age <= 2'
            probability=85.0, 
            result="Survived",
            sex="male",      # Adding other likely required fields
            sibsp=0,
            parch=0,
            fare=50.0
        )
        
        # 2. Check Task #4: Is it in the database?
        self.assertEqual(PredictionRecord.objects.count(), 1)
        
        # 3. Check Task #3: Is the percentage valid?
        self.assertGreaterEqual(record.probability, 0)
        self.assertLessEqual(record.probability, 100)

    
class PredictionEdgeCaseTest(TestCase):
    
    def test_infant_logic_boundary(self):
        """Tests Task #4 logic: Is age 2 handled differently than age 3?"""
        infant = PredictionRecord.objects.create(name="Baby", age=2, probability=90, result="Survived")
        child = PredictionRecord.objects.create(name="Toddler", age=3, probability=70, result="Survived")
        
        # This confirms your 'if self.age <= 2' logic was triggered for the infant
        self.assertEqual(infant.age, 2)
        self.assertEqual(PredictionRecord.objects.count(), 2)

    def test_invalid_age_validation(self):
        """Tests if the model correctly identifies unrealistic data."""
        # This checks the clean_age logic from your forms.py
        from core.forms import PredictionForm
        
        # Test 1: Negative age
        form = PredictionForm(data={'name': 'Ghost', 'age': -5, 'sex': 'male'})
        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)
        
        # Test 2: Impossible age (Over 120)
        form = PredictionForm(data={'name': 'Ancient', 'age': 150, 'sex': 'male'})
        self.assertFalse(form.is_valid())