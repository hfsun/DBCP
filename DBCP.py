import networkx as nx
import matplotlib.pyplot as plt
import time


cc_map = [  
    'red',  
    'darkblue',  
    'darkcyan',  
    'black',  
    'darkred',  
    'darkmagenta',  
    'brown', #dark yellow  
    'blue',  
    'green',  
    'cyan',  
    'darkgreen',  
    'm',
    'brown', #dark yellow  
    'blue',  
    'green',  
    'cyan',  
    'black',  
    'm'
    ] 

#remove the single nodes in a graph.
def Remove_Single_Node(graph):
    for node in graph.nodes():
        if nx.is_isolate(graph,node):
            graph.remove_node(node)
    return graph

#given a graph location to read the graph, graphml style only.
def Read(graph_url):
    G = nx.read_graphml(graph_url)
    G = Remove_Single_Node(G)   #remove the single nodes in a graph.
    return G    

#given a dc value according to the diameter.
def Find_DC(graph):
    dia = nx.diameter(graph)
    dc = (dia+2)/3
    if dc == 0:
        return 1
    return dc


#draw the graph after 
def Draw_Graph(graph,colors='r',shapes=200):
    nx.draw_networkx(graph,node_color=colors,node_size=shapes)
    plt.show()

#get the neighbors within the dc value for the given node
def NeighborsWithinDC(node,dc,graph,neighbors=[]):
    if len(neighbors) == 0:
        neighbors.append(node)
    if dc == 0:
        return neighbors
    dc -= 1
    for nd in graph.neighbors(node):
        if nd not in neighbors:
            neighbors.append(nd)
        neighbors = NeighborsWithinDC(nd,dc,graph,neighbors)
    return neighbors

#get the density for the given node
def Density(node,dc,graph):
    li = NeighborsWithinDC(node,dc,graph,[])
    li.remove(node)
    return len(li)

#find the most close node with higher density
def Find_Close_Higher_Node(node,densities,graph,uplevenodes=[],distance=0):
    hnode = ''
    hden = densities[node]
    distance +=1
    
    if uplevenodes==[]:
        downlevenodes = graph.neighbors(node)
        for nd in downlevenodes:
            if densities[node]<densities[nd]:
                hnode = nd
                hden=densities[nd]
        if hnode != '':
            return hnode,distance
    else:
        downlevenodes = []
        for upnd in uplevenodes:
            for nd in graph.neighbors(upnd):
                downlevenodes.append(nd)
                if densities[node]<densities[nd]:
                    hnode = nd
                    hden = densities[nd]
        if hnode != '':
            return hnode, distance
    if distance < 3:
        hnode,distance = Find_Close_Higher_Node(node,densities,graph,downlevenodes,distance)
        return hnode,distance
    else: 
        return hnode,distance

def subGraph(graph,colors):
    nodeset = {}
    subG = []
    for i in xrange(len(colors)):
        indexofcluster = cc_map.index(colors[i])
        if indexofcluster not in nodeset.keys():
            nodeset[indexofcluster] = []
        nodeset[indexofcluster].append(graph.nodes()[i])
    for subset in nodeset.keys():
        subG.append(graph.subgraph(nodeset[subset]))
    return subG

def CombineSubGraph(graph,colors):
    subG = subGraph(graph,colors)
    change = False
    for subg in subG:
        if subg.number_of_nodes() == 1:
            node = subg.nodes()[0]
            print node
            for nd in graph.neighbors(node):  
            #assign the node to neighber cluster with more than 1 node
                indexnode = G.nodes().index(nd)
                color_nd = colors[indexnode]
                for nnd in graph.neighbors(nd):
                    if colors[G.nodes().index(nnd)] == color_nd:
                        colors[G.nodes().index(node)] = colors[G.nodes().index(nnd)]
                        
                        change = True
                        break
    if change:
        subG = subGraph(graph,colors)
    return subG

#Used to change the tradeoff metric for select the best placement based on the tradeoff
def tradeoff_function(avglat,avg_weight,maxlat,max_weight):
    return avg_weight*avglat+max_weight*maxlat

#For worst case latecy
def Bestplacement(graph, colors,avg_weight,max_weight):
    subG = subGraph(graph,colors)              

    controllers = []
    for subg in subG:
        controllerplace = ''
        mintl = -1
        for node in subg:
            lenghts = nx.single_source_shortest_path_length(subg,node)

            mx = -1
            ag = 0.0
            for l in lenghts:
                if lenghts[l]>mx:
                    mx = lenghts[l]
                ag += lenghts[l]
            tl = tradeoff_function(ag/nx.number_of_nodes(subg),avg_weight,mx,max_weight)
            #tl = avg_weight*(ag/nx.number_of_nodes(subg))+max_weight*mx
            if mintl < 0:
                mintl = tl
                controllerplace = node
            elif tl < mintl:
                mintl = tl
                controllerplace = node
        controllers.append(controllerplace)
    return controllers

def Find_Controller_Placement(graph_name,avg_weight=1.0,max_weight=0.0):    
    
    g_name = graph_name
    G = Read(g_name)
    #Draw_Graph(G)
    dc = Find_DC(G)

    densities = {}
    belongs = {}

    start = time.clock()

    for node in G.nodes():
        densities[node]=Density(node,dc,G)
    numofc=0
    numofnodes = nx.number_of_nodes(G)

    colors = ['w' for i in xrange(numofnodes)]

    for node in G.nodes():
        cnode,cdis = Find_Close_Higher_Node(node,densities,G,uplevenodes=[],distance=0)

        if cdis > 1:
            colors[G.nodes().index(node)]=cc_map[numofc]
            numofc+=1
        else:
            belongs[node]=cnode

    end = time.clock()

    for node in G.nodes():
        indexcurnode = G.nodes().index(node)
        if colors[indexcurnode] is 'w':
            indexbelnode = G.nodes().index(belongs[node])
            while colors[indexbelnode] is 'w':
                indexbelnode = G.nodes().index(belongs[G.nodes()[indexbelnode]])
            colors[indexcurnode] = colors[indexbelnode]

    controllerlist = Bestplacement(G,colors,avg_weight,max_weight)

    shapes = [200 for i in xrange(numofnodes)]
    for controller in controllerlist:
        shapes[G.nodes().index(controller)]=1000
    print "total time consumption: %f s" % (end - start)
    Draw_Graph(G,colors,shapes)