import seaborn as sns
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
iris = sns.load_dataset('iris')
X = iris[['petal_length']] 
y = iris['petal_width']     
model = LinearRegression()
model.fit(X, y)
intercept = model.intercept_
coefficient = model.coef_[0]
print(f"Intercept: {intercept}")
print(f"Coefficient: {coefficient}")
iris['predicted_petal_width'] = model.predict(X)
print("\nSample Predictions:\n", iris[['petal_length', 'petal_width', 'predicted_petal_width']].head())
plt.figure(figsize=(8, 5))
plt.scatter(iris['petal_length'], iris['petal_width'], color='blue', label='Actual')
plt.plot(iris['petal_length'], iris['predicted_petal_width'], color='red', label='Regression Line')
plt.xlabel('Petal Length (cm)')
plt.ylabel('Petal Width (cm)')
plt.title('Linear Regression: Petal Width vs. Petal Length')
plt.legend()
plt.grid(True)
plt.show()
