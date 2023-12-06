from flask import Flask, render_template, request
import pandas as pd
import re
app = Flask(__name__)

class MedicationSearch:
    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)
        self.medical_conditions = self.df['medical_condition'].unique()

    def get_all_medical_conditions(self):
        return self.medical_conditions

    def search_medication(self, medical_condition):
        condition_pattern = re.compile(f'.*{medical_condition}.*', re.IGNORECASE)
        condition_drugs = self.df[self.df["medical_condition"].str.contains(condition_pattern, na=False)]

        if condition_drugs.empty:
            return []

        result = []
        for index, row in condition_drugs.iterrows():
            drug_name = row["drug_name"]
            side_effects = row["side_effects"]

            primary_side_effects = ["fever", "nausea", "headache", "fatigue", "upset stomach", "dizziness",
                                    "darkened skin color", "skin rash or itching", "vaginal itching or discharge",
                                    'skin rash', 'hives']

            if any(effect in side_effects for effect in primary_side_effects):
                result.append(drug_name)

        return result

searcher = MedicationSearch("project.csv")

@app.route('/')
def index():
    all_conditions = searcher.get_all_medical_conditions()
    return render_template('index.html', conditions=all_conditions)

@app.route('/search', methods=['POST'])
def search():
    medical_condition = request.form['condition']
    search_result = searcher.search_medication(medical_condition)

    if search_result:
        return render_template('result.html', condition=medical_condition, medications=search_result)
    else:
        return render_template('no_result.html', condition=medical_condition)

if __name__ == '__main__':
    app.run(debug=True)
