import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ser = serial.Serial('COM5', 4800, timeout=1) #open serial port
ser.bytesize = serial.EIGHTBITS #set data size
ser.parity = serial.PARITY_NONE #set parity
ser.stopbits = serial.STOPBITS_ONE #set stop bits
ser.encoding = 'ascii' #set encoding
ser.newline = '\n' #set line ending

temp_list = [] #list to store temperature values

fig = plt.figure() #create a figure object
ax = fig.add_subplot(1, 1, 1) #create an axes object

def animate(i): #define a function to update the plot
    data = ser.readline() #read one line from serial port
    if data: #if data is not empty
        temp = int(data) #convert data to integer
        temp_list.append(temp) #append temp to list
        ax.clear() #clear the axes
        print("Temperature in celcius: ", temp) #print temp to console
        ax.plot(temp_list) #plot list

ani = animation.FuncAnimation(fig, animate, interval=1000) #create an animation object that calls animate function every 1000 ms
plt.show() #show plot
