import DBCP as dp

#the function of "Find_Controller_Placement" has three parameters:
#1. graph_url is the file name of graph;
#2. avg_weight is the weight to select the placement according the objective function of average latency;
#3. max_weight is the weight to select the placement according the objective function of worst-case latency;
#In this demo, we only consider average latency and worst-case latency.

dp.Find_Controller_Placement('Arnes.graphml',avg_weight=1.0,max_weight=0.0)
