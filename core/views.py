from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import joblib
import numpy as np
import pandas as pd
import os

model_path = os.path.join(settings.BASE_DIR, 'ML', 'titanic_model_pipeline.pkl')
# Load your model globaly so it doesn't reload on every click
model = joblib.load(model_path)
def get_importances(model, cols):
    # Extract the classifier from the pipeline
    rf_model = model.named_steps['model']
    importances = rf_model.feature_importances_
    
    # Create a list of dictionaries for the template
    data = []
    for i in range(len(cols)):
        data.append({
            'name': cols[i],
            'value': round(importances[i] * 100, 2)
        })
    # Sort by importance value
    return sorted(data, key=lambda x: x['value'], reverse=True)

def predict_view(request):
    error = None
    survival_prob = 0
    if request.method == 'POST':
        try:
        # Get data from form
            pclass = int(request.POST.get('pclass'))
            if pclass not in [1, 2, 3]:
                raise ValueError("Pclass must be 1, 2, or 3.")
            sex = 1 if request.POST.get('sex') == 'male' else 0
            age = float(request.POST.get('age'))
            if age < 0 or age > 110:
                raise ValueError("Age must be between 0 and 110.")
            sibsp = int(request.POST.get('sibsp', 0))
            parch = int(request.POST.get('parch', 0))
            fare = float(request.POST.get('fare', 32.0))
            if fare < 0:
                raise ValueError("Fare cannot be a negative number.")
            embarked_map = {'S': 0, 'C': 1, 'Q': 2}
            embarked = embarked_map.get(request.POST.get('embarked'), 0)

            # --- Derived Features (Feature Engineering) ---
            family_size = sibsp + parch + 1
            age_class = age * pclass
            # ... add other features (SibSp, Parch, Fare)

            # Create feature array
            features = [[
                pclass, sex, age, sibsp, parch, fare, family_size,
                embarked, age_class
            ]]
            cols = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'FamilySize','Embarked',  'Age_Class']
            features_df = pd.DataFrame(features, columns=cols)
            prediction = model.predict(features_df)
        
            # Optional: Get probability if your model supports it
            try:
                prob = round(model.predict_proba(features_df)[0][1] * 100, 2)
            except:
                prob = "N/A"

            # context = {
            #     'result': "Survived" if prediction[0] == 1 else "Did Not Survive",
            #     'probability': prob,
            #     'input_data': request.POST
            #     }
            result = "Survived" if prediction[0] == 1 else "Did Not Survive"
            return render(request, 'result.html', {
                'result': result,
                'probability': prob,
                'importances': get_importances(model, cols) # Optional helper function
            })
        except (ValueError, TypeError) as e:
            return render(request, 'index.html', {
                'error': f"Invalid input: {str(e)}",
                'previous_data': request.POST # Helps user keep their other entries
            })

    return render(request, 'index.html')

# def predict_survival(request):
#     if request.method == 'POST':
#         # ... (all your data collection and prediction logic from before) ...
        
#         prediction = model.predict(features)
        
#         # Create a dictionary of context to send to the HTML
#         context = {
#             'result': "Survived" if prediction[0] == 1 else "Did Not Survive",
#             'probability': round(model.predict_proba(features)[0][1] * 100, 2), # Optional: % chance
#             'input_data': request.POST # Send back the inputs so the user sees what they typed
#         }
        
#         return render(request, 'result.html', context)