# Probabilistic-Road-Map-Visualization
A visualization of the Probabilistic road map generation using pygame library.

## Theory

Probabilistic Roap Map (PRM) method starts by creating a free space with 'n' sample nodes. If any obstacles are present, a check is done to ensure the nodes are not colliding with them.
This generated node is then connected with the nearby nodes with a straight line.
The system checks whether the line lies in free space or not. A graph is constructed in the end taking into consideration the start and goal points.

![pygamewindow2024-03-1311-57-01-ezgif com-crop](https://github.com/harrisonseby/Probabilistic-Road-Map/assets/69869649/1e87fd48-4eb6-4b69-aba2-1366c5787c57)

## Drawbacks of this code

This code only constructs the graph for the PRM in the absence of obstacles.
The next step is to include obstacles in the PRM graph construction and also run a search algorithm like the A* or Dijkstra algorith.
The code will be updated once it is complete.

## How to run this program

Prior to running this script, make sure you have installed **numpy**, **pygame** and **scipy** libraries.

Once the script is run, you will see a window with random nodes created. 
Press 'i' on the keyboard and click a point on the window to set the start location.
Similarly, press 'f' on the keyboard and click a point on the window to set the final/goal location.
Press 'Enter' to see the PRM graph visualization
