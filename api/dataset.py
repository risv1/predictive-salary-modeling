import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.preprocessing import RobustScaler, OneHotEncoder

class SalaryDataset:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        print("Initial data shape:", self.data.shape)
        print("Initial salary range:", self.data['Salary'].min(), "-", self.data['Salary'].max())
        
        self.preprocess_data()
        
    def preprocess_data(self):
        print("\nMissing values before cleaning:")
        print(self.data.isnull().sum())
        
        numeric_columns = ['Age', 'Years of Experience', 'Salary']
        categorical_columns = ['Gender', 'Education Level', 'Job Title']
        
        for col in numeric_columns:
            self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
            self.data[col] = self.data[col].fillna(self.data[col].median())
        
        for col in categorical_columns:
            self.data[col] = self.data[col].astype(str)
            self.data[col] = self.data[col].fillna(self.data[col].mode()[0])
        
        print("\nMissing values after cleaning:")
        print(self.data.isnull().sum())

        self.data['Education Level'] = pd.Categorical(self.data['Education Level']).codes
        self.data['Experience_Education'] = (
            self.data['Years of Experience'] * 
            self.data['Education Level']
        )
        
        Q1 = self.data['Salary'].quantile(0.25)
        Q3 = self.data['Salary'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        self.data = self.data[
            (self.data['Salary'] >= lower_bound) & 
            (self.data['Salary'] <= upper_bound)
        ]
        
        X_numeric = self.data[['Age', 'Years of Experience', 'Experience_Education']].values
        X_categorical = self.data[categorical_columns]
        
        self.numeric_transformer = RobustScaler(quantile_range=(1, 99))
        self.categorical_transformer = OneHotEncoder(
            drop='first', 
            sparse_output=False, 
            handle_unknown='ignore'
        )
        
        X_numeric_scaled = self.numeric_transformer.fit_transform(X_numeric)
        
        X_categorical_encoded = self.categorical_transformer.fit_transform(X_categorical)
        
        self.X = np.hstack([X_numeric_scaled, X_categorical_encoded])
        
        self.salary_scaler = RobustScaler(quantile_range=(1, 99))
        self.y = self.salary_scaler.fit_transform(
            self.data['Salary'].values.reshape(-1, 1)
        ).ravel()
        
        self.X = self.X.astype(np.float32)
        self.y = self.y.astype(np.float32)
        
        print("\nProcessed data information:")
        print("Features shape:", self.X.shape)
        print("Target shape:", self.y.shape)
        
        if np.any(np.isnan(self.X)) or np.any(np.isnan(self.y)):
            raise ValueError("NaN values found in processed data")
    
    def get_data(self):
        return torch.FloatTensor(self.X), torch.FloatTensor(self.y)
    
    def inverse_transform_salary(self, scaled_salary):
        return self.salary_scaler.inverse_transform(scaled_salary.reshape(-1, 1))
    
    def get_categorical_features(self):
        return self.data[['Gender', 'Education Level', 'Job Title']]
    
    def get_numerical_features(self):
        return self.data[['Age', 'Years of Experience']]