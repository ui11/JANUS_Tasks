import pandas as pd #I used this library for reading, handling and utilising the data from given in the .csv file.
import matplotlib # I used this library for plotting and animating the graphs
matplotlib.use('TkAgg') # I used this package because my animation wasn’t working without it.
                        # I found this fix on Stack Overflow (link in README).
                        # I just applied it to make the animation run.
import matplotlib.pyplot as plt #I used this plot my graph
from matplotlib.animation import FuncAnimation #I used this to animate my graph

data = pd.read_csv('FlightData.csv') # I used this to load and read the .csv file in the code
data = data.interpolate()  #I used this  fill any missing or blank values in the dataset
                           # because of sensor errors by interpolating between known values

data['Time'] = data.index # Since time wasn't given, I used this to create the Time column
                          # assuming that each reading in the rows of Pressure column is 1 second apart

data['Altitude'] = 44330 * (1 - (data['Pressure'] / 101327.401) ** (1 / 5.255))
# I used this to convert the pressure data into altitude using the barometric formula
# The formula I used is :- Altitude = 44330 * (1 - (P / P0) ^ (1/5.255))
# where P0 is pressure at the ground level and P is the pressure at a given point.
# I used the ground level pressure as 101327.401 pascals, because the problem task
# It was given to assume the object was launched from the ground, and it was first data in the Pressure column.
data['Altitude'] = data['Altitude'].rolling(window=3).mean()
# I used this to smooth out noise (ups and downs) in the altitude values, to make the graph look cleaner
# This syntax works by reading n values (here, n=3) from the sensor readings calculate their average



data['Velocity'] = data['Altitude'].diff() / data['Time'].diff()
# I used this to calculate velocity as change in altitude over change in time (v = (delta)h / (delta)t)
# here, (delta)t = 1 second, since we have take each reading to be one second apart.
data['Velocity'] = data['Velocity'].rolling(window=3).mean()
#As stated above, I used this syntax to smoothen out the velocity data.

fig, ax = plt.subplots(1,2)
# I used above syntax to create 2 graphs
# one for Altitude vs Time, one for Velocity vs Time (1 row, 2 columns)
line, = ax[0].plot([], [], color='red')   # I used this to create plot the points in Altitude vs Time graph
                                          # which will be updated after every regular time intervals.
                                          # I learned to use this syntax in a YouTube video (link in README).
line2, = ax[1].plot([], [], color='blue') #I used this to do the same thing with Velocity vs Time graph

ax[0].set_xlabel('Time')
ax[0].set_ylabel('Altitude')
ax[0].set_title('Altitude vs Time')
# I used this syntax to label x and y axes and set the title for the Altitude vs Time graph
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Velocity')
ax[1].set_title('Velocity vs Time')
# I used this syntax to label x and y axes and set the title for the Velocity vs Time graph

ax[0].set_xlim(data['Time'].min(), data['Time'].max())
ax[0].set_ylim(data['Altitude'].min(), data['Altitude'].max())
#I used this syntax to set the limits for the Altitude vs Time graph
# without using it, my graph animation was not working.
ax[1].set_xlim(data['Time'].min(), data['Time'].max())
ax[1].set_ylim(data['Velocity'].min(), data['Velocity'].max())
#I used this syntax to set the limits for the Velocity vs Time graph
#for the same reason as stated above.

ax[0].grid()
ax[1].grid()
#I used this syntax to add grid lines to both graphs for better readability.

def update(frame):
    #Here, I am defining a function, which will be called by FuncAnimation
    # to plot the graph from starting till the frame that is called at that time.
    x = data['Time'][:frame]
    y = data['Altitude'][:frame]
    #Above syntax will help us update Altitude graph data up to the current frame or time step.
    line.set_data(x, y) # Here, I am assigning the coordinates to Time and Altitude.

    p = data['Velocity'][:frame]
    q = data['Time'][:frame]
    # Above syntax will help us update Velocity graph data up to the current frame or time step.
    line2.set_data(q, p) # Here, I am assigning coordinates to Velocity and Time.
    return line, line2

# Here, I am using FuncAnimation to animate my graph
animation = FuncAnimation(fig, update, frames=len(data), interval=40)
'''Here, the function update will be called after each interval to update the plot for each frame
 (from starting to that frame number, if len(data)=n, then update(0).....update(n-1) will be called after a designated interval )
len(data) assigns number to frame acc to the number of rows in Pressure entry, this is also the number of times
update function will be called by FuncAnimation.'''
#Here, interval= n means after much time interval (40ms here), between calling of each update function

#Here, I used the syntax to finally show the plot.
plt.show()
'''So, Here's the code of Task-2, I don't know if it's best one you've seen yet,
 but it is definitely the best one I could come up with, for now:)'''