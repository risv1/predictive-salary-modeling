# Salary Estimation

## Description

This is a project for our BDE course for predicting job salaries using different classification algorithms and neural networks for regressive estimated prediction of salary based on employee's/applicant's details like education, experience, etc.

## Tools

- HDFS
- Spark
- PyTorch
- Scikit-Learn

## Used

These are the models we used...

### Classifiers

```python
models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(),
    'Random Forest': RandomForestRegressor(),
    'Lasso Regression': Lasso(),
    'LightGBM': lgb.LGBMRegressor()
}
```

### FF Network

A feedforward neural network with residual connections and batch normalization, and applying Kaiming normalization to initialise weights with ReLU.
