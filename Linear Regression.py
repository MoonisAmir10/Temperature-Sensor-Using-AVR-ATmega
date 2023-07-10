# Importing scikit-learn library and LinearRegression class
from sklearn.linear_model import LinearRegression
import numpy as np

# Create two arrays that hold 20 values each for x and y
x = [24, 26, 23, 35, 50, 25, 28] # sensor data voltage in volts
y = [26.2, 27.4, 23, 36.9, 53.1, 26.9, 28.9] # temperature reading in degrees Celsius

# Reshape x array to a 2D array with one column
x = np.array(x).reshape(-1,1)

# Creating an instance of the LinearReg class and fitting it to the x and y arrays
reg = LinearRegression().fit(x,y)

# Print the coefficients and intercept of the fitted model
print("The coefficient is", reg.coef_[0])
print("The intercept is", reg.intercept_)

# Print the equation of the graph using the coefficients and intercept
print("The equation of the graph is y =", reg.coef_[0], "* x +", reg.intercept_)
