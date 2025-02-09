# Salary Prediction Model

This project aims to predict salaries based on various attributes using machine learning models. The dataset contains information on various factors like experience, education, job title, and more, which are used to predict the salary of an individual.

## Tools

- HDFS
- Spark
- PyTorch
- Scikit-Learn

## Classifiers

```python
models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(),
    'Random Forest': RandomForestRegressor(),
    'Lasso Regression': Lasso(),
    'LightGBM': lgb.LGBMRegressor()
}
```

## Models Tested

1. **Random Forest Regressor**
   - **R-squared Score**: 0.971
   - **Mean Squared Error (MSE)**: 81,133,639.07
   - **Mean Absolute Error (MAE)**: 3,480.71
   - **Summary**: The Random Forest model demonstrated the highest predictive performance among all models tested, achieving the best R-squared score and the lowest error metrics. This makes it the most suitable model for salary prediction in this dataset.

2. **Decision Tree Regressor**
   - **R-squared Score**: 0.961
   - **Mean Squared Error (MSE)**: 109,463,767.14
   - **Mean Absolute Error (MAE)**: 3,505.79
   - **Summary**: The Decision Tree model also performed well, but it had higher error metrics compared to the Random Forest model, indicating slightly less accuracy.

3. **LightGBM**
   - **R-squared Score**: 0.964
   - **Mean Squared Error (MSE)**: 103,256,579.09
   - **Mean Absolute Error (MAE)**: 5,826.86
   - **Summary**: LightGBM performed decently but was not as accurate as Random Forest. However, it still offered solid performance.

4. **Lasso Regression**
   - **R-squared Score**: 0.674
   - **Mean Squared Error (MSE)**: 926,579,620.73
   - **Mean Absolute Error (MAE)**: 23,945.09
   - **Summary**: The Lasso Regression model had the lowest R-squared score and significantly higher error metrics, indicating that it is less effective in capturing the patterns in the dataset.

5. **Linear Regression**
   - **R-squared Score**: 0.674
   - **Mean Squared Error (MSE)**: 926,576,326.70
   - **Mean Absolute Error (MAE)**: 23,944.85
   - **Summary**: The Linear Regression model performed similarly to Lasso Regression, with a poor fit to the data.

## Feature Importance Analysis
The Random Forest Regressor model's feature importances were visualized to identify which attributes contribute most to predicting salary. The top 10 most important features are plotted in a horizontal bar chart.

```python
feature_importances = models['Random Forest'].feature_importances_
feature_names = list(X_train.columns)
sorted_indices = np.argsort(feature_importances)[::-1]
sorted_feature_importances = [feature_importances[i] for i in sorted_indices]
sorted_feature_names = [feature_names[i] for i in sorted_indices]

plt.figure(figsize=(12, 8))
plt.barh(sorted_feature_names[:10], sorted_feature_importances[:10], color='skyblue')
plt.xlabel('Feature Importance')
plt.title('Most Important Features in Predicting Salary')
plt.gca().invert_yaxis() 
plt.show()
```

## Actual vs. Predicted Salary
A scatter plot comparing the actual vs. predicted salaries for the Random Forest model has been created, along with a diagonal line representing perfect predictions (i.e., where actual equals predicted).

```python
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_rf, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')  # Diagonal line
plt.xlabel('Actual Salary')
plt.ylabel('Predicted Salary')
plt.title('Actual vs. Predicted Salaries (Random Forest)')
plt.grid()
plt.show()
```


## Residuals Analysis
A Q-Q plot was generated to check the residuals for normality, ensuring the model's assumptions are met. The plot should show the residuals closely following a normal distribution along the diagonal line. 
```python
# Q-Q plot of residuals code
plt.figure(figsize=(10, 6))
sm.qqplot(residuals_rf, line='s')
plt.title('Q-Q Plot of Residuals (Random Forest)')
plt.grid()
plt.show()
```

## Conclusion
Based on the R-squared scores and error metrics, Random Forest Regressor is the best model for salary prediction in this dataset. It offers the highest accuracy with the lowest MSE and MAE. Further optimization and fine-tuning of the Random Forest model could potentially yield even better results.

For future work:
- Hyperparameter Tuning: Further fine-tune the Random Forest model using techniques like GridSearchCV or RandomizedSearchCV.
- Cross-Validation: Implement cross-validation to ensure the model’s robustness and stability.
