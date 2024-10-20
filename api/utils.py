import torch
import pandas as pd
import numpy as np
from model import SalaryPredictor
from dataset import SalaryDataset

EDUCATION_MAPPING = {
    0: "High School",
    1: "Bachelor's",
    2: "Master's",
    3: "PhD",
    4: "Associate's",
    5: "Some College",
    6: "Professional Degree",
    7: "Other"
}

REVERSE_EDUCATION_MAPPING = {v: k for k, v in EDUCATION_MAPPING.items()}

def predict_salary(
    age,
    gender,
    education_level,
    job_title,
    years_experience,
):
    input_size = 206 
    model = SalaryPredictor(input_size)
    model.load_state_dict(torch.load("./classifiers/model.pth", map_location=torch.device('cpu')))
    model.eval()
    
    dataset_instance = SalaryDataset("./data/Salary_Data.csv")
    
    if education_level not in REVERSE_EDUCATION_MAPPING:
        raise ValueError(f"Invalid education level. Must be one of: {list(REVERSE_EDUCATION_MAPPING.keys())}")
    
    education_code = REVERSE_EDUCATION_MAPPING[education_level]
    
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [gender],
        'Education Level': [education_code],
        'Job Title': [job_title],
        'Years of Experience': [years_experience],
    })
    
    input_data['Experience_Education'] = (
        input_data['Years of Experience'] * 
        input_data['Education Level']
    )
    
    X_numeric = input_data[['Age', 'Years of Experience', 'Experience_Education']].values
    X_categorical = input_data[['Gender', 'Education Level', 'Job Title']]
    
    X_numeric_scaled = dataset_instance.numeric_transformer.transform(X_numeric)
    X_categorical_encoded = dataset_instance.categorical_transformer.transform(X_categorical)
    
    X = np.hstack([X_numeric_scaled, X_categorical_encoded])
    X = X.astype(np.float32)
    
    input_tensor = torch.FloatTensor(X)
    
    with torch.no_grad():
        prediction = model(input_tensor)
        
    predicted_salary = dataset_instance.inverse_transform_salary(prediction.numpy())
    
    return float(predicted_salary[0][0])

def get_feature_info():
    dataset = SalaryDataset("./data/Salary_Data.csv")
    return {
        "education_levels": list(EDUCATION_MAPPING.values()), 
        "job_titles": dataset.data['Job Title'].unique().tolist(),
        "gender_categories": dataset.data['Gender'].unique().tolist(),
        "age_range": {
            "min": int(dataset.data['Age'].min()),
            "max": int(dataset.data['Age'].max())
        },
        "experience_range": {
            "min": float(dataset.data['Years of Experience'].min()),
            "max": float(dataset.data['Years of Experience'].max())
        }
    }