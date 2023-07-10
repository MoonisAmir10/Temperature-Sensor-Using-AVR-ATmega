# Temperature-Sensor-Using-AVR-ATmega
This project is about implementing a temperature sensing unit using AVR ATmega16A microcontroller, and a simple machine learning algorithm to enhance it. This was an assignment of the course of EE-222 Microprocessor Systems.

**LM35** sensor is used for temperature sensing, and it is connected to the ADC of the microcontroller. Two seven segment displays are used to display the temperature in two digit whole numbers. Serial communication with PC was done using the **UART** of the microcontroller, and the readings are continously displayed on the command prompt using python. A graph is also created and updated continously.

A **moving average filter** algorithm was used to stabilize the readings of the LM35 sensor, as otherwise they may fluctuate.

A machine learning algorithm called **Linear Regression** was used to improve the accuracy of the readings. A suitable number of temperature readings of different surfaces/objects were taken by the LM35 sensor and a digital thermometer. The readings were fed to a python algorithm, which created a best fit linear graph. It also computed the scaling factors (y-intercept and slope), which were then added to the AVR code to adjust the accuracy of the LM35 readings. More detail about this concept is provided in the assignment manual.

