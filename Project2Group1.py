# import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
import scipy.stats as stats


# reading data
data = pd.read_csv('./winequality-white.csv', sep=';')
# Separate features and target variable
X = data.drop('quality', axis=1)
y = data['quality']
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# point estimation for parameters:

# Fit the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)
# Point estimation
coefficients = model.coef_
intercept = model.intercept_

print("-----------------------------------------------------------------------------------")
print("Point Estimation")
print("-----------------------------------------------------------------------------------")

print("Estimation for coefficients for (x_1, x_2,...., x_11):\n", coefficients)
print("\nEstimation for intercept term:\n", intercept)



# interval estimation for parameters (alpha = 0.05):

X_train = sm.add_constant(X_train)  # adding a constant
model_sm = sm.OLS(y_train, X_train).fit()
# confidence intervals
confidence_intervals = model_sm.conf_int()
print("-----------------------------------------------------------------------------------")
print("Interval Estimation")
print("-----------------------------------------------------------------------------------")
print("\nInterval Estimation of the parameters \n", confidence_intervals)



# Hypothesis Testing: Test for Significance of Regression
# Want to test the hypothesis if there is a linear relationship between the response y and any of the regressor x1, · · · , xn
# Add a constant to the features for the intercept term
summary = model_sm.summary()
# Extract Prob (F-statistic)
f_statistic = float(summary.tables[0].data[2][-1])
df_regression = 11
n = len(data)
df_residual = n-11-1
f_critical  = float(stats.f.ppf(1 - 0.05, df_regression, df_residual))
print("-----------------------------------------------------------------------------------")
print("Test for Significance of Regression")
print("-----------------------------------------------------------------------------------")
print(f"F-statistic: {f_statistic}")
print(f"critcal f value: {f_critical}")
if f_statistic > f_critical:
    print("Reject null hypothesis\nindicating that at least one independent variable is contributing to the explanation of the dependent variable.")
else:
    print("Fail to reject null hypothesis")


print("-----------------------------------------------------------------------------------")
print("Residual Analysis")
print("-----------------------------------------------------------------------------------")
predicted_values = model.predict(X_test)
# Calculate residuals
residuals = y_test - predicted_values
# Residual plot
plt.figure(figsize=(10, 6))
plt.scatter(predicted_values, residuals)
plt.axhline(y=0, color='r', linestyle='-')
plt.title('Residual Plot')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.show()
# Histogram of residuals
plt.figure(figsize=(10, 6))
plt.hist(residuals, bins=30, edgecolor='k', alpha=0.7)
plt.title('Histogram of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()
# Generate Q-Q plot
fig, ax = plt.subplots(figsize=(8, 6))
sm.qqplot(residuals, line ='q', ax=ax)
ax.set_title('Q-Q Plot of Residuals')
ax.set_xlabel('Theoretical Quantiles')
ax.set_ylabel('Sample Quantiles')
plt.show()
print("graphs as been plotted")

print("-----------------------------------------------------------------------------------")
print(f"Adjusted R^2: {float(summary.tables[0].data[1][-1])}")
print("-----------------------------------------------------------------------------------")



print("-----------------------------------------------------------------------------------")
print("Forward Selection")
print("-----------------------------------------------------------------------------------")
X = data.drop('quality', axis=1)
y = data['quality']
def forward_selection(X, y):
    features = list(X.columns)
    selected_features = []
    best_model = None
    best_aic = np.inf
    
    for _ in range(len(features)):
        aic_values = []
        for feature in features:
            model_features = selected_features + [feature]
            X_temp = X[model_features]
            X_temp = sm.add_constant(X_temp)
            model = sm.OLS(y, X_temp).fit()
            aic_values.append((feature, model.aic))
        
        best_feature, best_aic_value = min(aic_values, key=lambda x: x[1])
        
        if best_aic_value < best_aic:
            best_aic = best_aic_value
            selected_features.append(best_feature)
            features.remove(best_feature)
            best_model = model
        
    return selected_features, best_model

selected_features_forward, best_model_forward = forward_selection(X, y)
print("Selected Features (Forward Selection):", selected_features_forward)



print("-----------------------------------------------------------------------------------")
print("Backward Selection")
print("-----------------------------------------------------------------------------------")
def backward_elimination(X, y):
    features = list(X.columns)
    best_model = None
    best_aic = np.inf
    
    iter = 0
    while len(features) > 0 and iter <= 100:
        aic_values = []
        for feature in features:
            model_features = features.copy()
            model_features.remove(feature)
            X_temp = X[model_features]
            X_temp = sm.add_constant(X_temp)
            model = sm.OLS(y, X_temp).fit()
            aic_values.append((feature, model.aic))
        
        best_feature, best_aic_value = min(aic_values, key=lambda x: x[1])
        
        if best_aic_value < best_aic:
            best_aic = best_aic_value
            features.remove(best_feature)
            best_model = model
        iter = iter + 1
        
    selected_features = features
    
    return selected_features, best_model

selected_features_backward, best_model_backward = backward_elimination(X, y)
print("Selected Features (Backward Elimination):", selected_features_backward)


print("-----------------------------------------------------------------------------------")
print("Stepwise Selection")
print("-----------------------------------------------------------------------------------")
def stepwise_selection(X, y):
    features = list(X.columns)
    selected_features = []
    best_model = None
    best_aic = np.inf
    iter = 0
    while len(features) > 0 and iter <= 100:
        aic_values = []
        for feature in features:
            model_features = selected_features + [feature]
            X_temp = X[model_features]
            X_temp = sm.add_constant(X_temp)
            model = sm.OLS(y, X_temp).fit()
            aic_values.append((feature, model.aic))
        
        best_feature, best_aic_value = min(aic_values, key=lambda x: x[1])
        
        if best_aic_value < best_aic:
            best_aic = best_aic_value
            selected_features.append(best_feature)
            features.remove(best_feature)
            best_model = model
        iter = iter + 1
        
    return selected_features, best_model

selected_features_stepwise, best_model_stepwise = stepwise_selection(X, y)
print("Selected Features (Stepwise Selection):", selected_features_stepwise)
