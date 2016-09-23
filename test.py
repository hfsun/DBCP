import DBCP as dp
import Evaluation as eva

#the function of "Find_Controller_Placement" has three parameters:
#1. graph_url is the file name of graph;
#2. avg_weight is the weight to select the placement according to the objective function of average controller-to-switch latency;
#3. max_weight is the weight to select the placement according to the objective function of worst-case controller-to-switch latency;
#4. inter_weight is the weight to select the placement according to the objective function of average inter-controller latency;
#In this demo, we only consider average latency and worst-case latency.

#the eva class has three function can be used. They are:
#1. Avg_latency_of_end_to_end(graph_name,controller_list), it can measure the average latency of end-to-end communications;
#2. Avg_latency_of_inter_controller(graph_name,controller_list), it can measure the average latency of inter-controller communications;
#3. Worst_latency_of_controller_to_switch(graph_name,controller_list), it can measure the worst-case controller-to-switch communciations.

graph_name = 'archive/Biznet.graphml'
ctl_list = dp.Find_Controller_Placement(graph_name,avg_weight=1.0,max_weight=1.0,inter_weight=1.0)

avgL = eva.Avg_latency_of_end_to_end(graph_name,ctl_list)
print 'the average latency of end-to-end communications is',avgL