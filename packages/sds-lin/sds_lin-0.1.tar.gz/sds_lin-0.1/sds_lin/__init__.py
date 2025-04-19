import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
data = {
    'Height': [151, 174, 138, 186, 128, 136, 179, 163, 152],
    'Weight': [63, 81, 56, 91, 47, 57, 76, 72, 62]
}
df = pd.DataFrame(data)
X = df[['Height']]
y = df['Weight']
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
df['Predicted_Weight'] = y_pred
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)
intercept = model.intercept_
coefficient = model.coef_
print("Dataset with Predictions:\n")
print(df)
print("\nMean Squared Error:", mse)
print("R-squared:", r2)
print("Intercept:", intercept)
print("Coefficient:", coefficient)

