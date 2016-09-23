import networkx as nx
import matplotlib.pyplot as plt
import time

#remove the single nodes in a graph.
def Remove_Single_Node(graph):
    for node in graph.nodes():
        if nx.is_isolate(graph,node):
            graph.remove_node(node)
    return graph
    
#given a graph location to read the graph, graphml style only.
def Read(graph_url):
    graph = nx.read_graphml(graph_url)
    graph = Remove_Single_Node(graph)   #remove the single nodes in a graph.
    return graph 

#assign all the switch to the nearest controller.
def AssignSwitchToController(controller_list,graph):
    switch2controller = []  #the list to store the assignment of the switches.
    for i in xrange(nx.number_of_nodes(graph)):#calculate the neareat controller for each switch.
        node = graph.nodes()[i]
        path_length = -1
        ctl = 0
        for controller in controller_list:
            length = nx.shortest_path_length(graph,node,controller)
            if path_length > length or path_length == -1:
                ctl = controller
                path_length = length
        switch2controller.append(ctl)
    return switch2controller

#calculate the latency for a new flow from a source switch to a target switch.
def EndtoEndComm(graph,source,target,switch2controller):
    path = nx.shortest_path(graph,source,target)
    
    #domain_controller = switch2controller[graph.nodes().index(source)]
    domain_controller = switch2controller[graph.nodes().index(source)]
    l_s2c = nx.shortest_path_length(graph,source,domain_controller)#calculate the latency of the package-in package delivery, which is sent from source switch to controller.
    l_c2s = 0
    #calculate the worst-case latency of the combinition of 2 parts:controller to controller latency and controller to switch latency.
    for node in path:
        #calculate the latency of inter-controller communication
        c2c = nx.shortest_path_length(graph,domain_controller,switch2controller[graph.nodes().index(node)])
        #calculate the latency of the rule delivery, which is sent from controller to the switch.
        c2s = nx.shortest_path_length(graph,switch2controller[graph.nodes().index(node)],node)
        l_c2s = c2c+c2s if l_c2s < c2c+c2s else l_c2s
    return l_s2c+l_c2s    

def Avg_latency_of_end_to_end(graph_name,controller_list):
    graph = Read(graph_name)
    switch2controller = AssignSwitchToController(controller_list,graph)
    latency = 0.0   #count the sum of the latency
    num = 0.0   #count the number of the condidate conditions
    #traverse all the condidate source and target conditions.
    for nd1 in graph:
        for nd2 in graph:
            if nd1 != nd2:
                latency += EndtoEndComm(graph,nd1,nd2,switch2controller)
                num += 1
    avg_latency = latency/num
    return avg_latency

def Avg_latency_of_inter_controller(graph_name,controller_list):
    graph = Read(graph_name)
    switch2controller = AssignSwitchToController(controller_list,graph)
    latency = 0.0   #count the sum of the latency
    num = 0.0   #count the number of the condidate conditions
    #traverse all the condidate source and target conditions.
    for nd1 in controller_list:
        for nd2 in controller_list:
            if nd1 != nd2:
                latency += nx.shortest_path_length(graph,nd1,nd2)
                num += 1
    avg_latency = latency/num
    return avg_latency
    
def Worst_latency_of_controller_to_switch(graph_name,controller_list):
    graph = Read(graph_name)
    switch2controller = AssignSwitchToController(controller_list,graph)
    latency = 0.0   #save the worst-case of the latency
    #traverse all the condidate source and target conditions.
    for sw in graph.nodes():
        cur_latency = nx.shortest_path_length(graph,sw,switch2controller[graph.nodes().index(sw)])
        if cur_latency>latency:
            latency = cur_latency
    return latency