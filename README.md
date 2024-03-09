# Probabilistic-Road-Map-Visualization
A visualization of the Probabilistic road map generation using pygame library.

## Theory

Probabilistic Roap Map (PRM) method starts by creating a free space with 'n' sample nodes. If any obstacles are present, a check is done to ensure the nodes are not colliding with them.
This generated node is then connected with the nearby nodes with a straight line.
The system checks whether the line lies in free space or not. A graph is constructed in the end taking into consideration the start and goal points.

![PRM](https://github.com/harrisonseby/Probabilistic-Road-Map/assets/69869649/b88a8a24-cdbc-4ea7-8f9c-4a73914eec0f)

## Drawbacks of this code

This code only constructs the graph for the PRM. The next step is run a search algorithm like the A* or Dijkstra algorith.
The code will be updated once it is complete.

## How to run this program

Prior to running this script, make sure you have installed **numpy**, **pygame** and **scipy** libraries.

Once the script is run, you will see a window with random nodes created. 
Press 'i' on the keyboard and click a point on the window to set the start location.
Similarly, press 'f' on the keyboard and click a point on the window to set the final/goal location.
Press 'Enter' to see the PRM graph visualization
