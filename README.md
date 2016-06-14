DBCP
===================

Files
------
####__DBCP.py__

Contains the basic function for controller placement problem.

The main function is the the function of "Find_Controller_Placement" has three parameters:
	1. graph_url is the file name of graph;
	2. avg_weight is the weight to select the placement according the objective function of average latency;
	3. max_weight is the weight to select the placement according the objective function of worst-case latency;
In this demo, we only consider average latency and worst-case latency.

####__test.py__

Help user to test the demo, you can change the graph and the tradeoff weight to get the comtroller placements.

####__archive.zip__

Contains all the test graphs. They are provided by The Internet Topology Zoo (http://www.topology-zoo.org)

Requirements
------------

Written using Python 2.7.3, networkx-1.11, and matplotlib
