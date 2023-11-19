import csv
import itertools
import networkx as nx
import pickle
import random
import time
#----------------------- Load Pickle file ----------------------------------
def random_numbers(low, high, n): # generates random order for edge selection
# ------------- Define seed---------------
    random.seed = 123
    return random.sample(range(low, high), n)

#--------------------create graph from parsed obo file-------------------
def create_graph(filename):
    relations = open(filename,'r')
    edges = []
    for rel in relations:
        nodes = rel.strip('\n').split('|')
        edges.append((nodes[0],nodes[2]))
    gtg = nx.Graph()
    gtg.add_edges_from(edges)
    return gtg

# ------------- Create a sub-graph for each of connected components ---------------
def robustness(graph):
    subGraphs=[graph.subgraph(c) for c in nx.connected_components(graph) if len(c) > 3] # select subgraphs with number of nodes > 3
    print(type(subGraphs))
    finalInformation = [] # stores the final results. Pattern: (target Graph/ Number of removed edges/ removed target edge/ Betweenness of target edge)
    graphIndexCounter = -1 # holds index of each graph
    # ------------------------ Iterate over each graph -------------------------------
    for g in subGraphs[1:]:

        tempGraph = nx.Graph(g) # make an unfrozen temp graph to be able to remove edges
        edgeList = list(tempGraph.edges) # list of edges of a subgraph
        numberOfNodes = len(tempGraph.nodes)
        numberOfEdges = len(tempGraph.edges)
        graphIndexCounter += 1

        edgeCounter = 0 # counter of removed edges
        orderIndex=[]
        orderIndex = random_numbers(0, len(edgeList), len(edgeList)) #random order to select edges

        for e in orderIndex:

            tempGraph.remove_edges_from([edgeList[e]]) # remove one random edge
            edgeCounter +=1

            if nx.is_connected(tempGraph): # if the graph stills connected

                continue

            else: # if the graph is divided into two parts

                sizeFlag = True # check  whether there is a subgraph with size 1 or not

                for i in nx.connected_components(tempGraph):

                    if len(i) >= 2: # if the subgraph has more than 1 node

                        continue

                    elif len(i) == 1: # if the subgraph is an isolated node

                        sizeFlag = False
                        removedNode = list(itertools.chain(i))[0] # stores the isolated node ID
                        break

                if sizeFlag == True: # if there is not any component with size 1

                    tempGraph.add_edges_from([edgeList[e]]) # add the latest deleted node to graph
                    edgeBetweenness = nx.edge_betweenness_centrality(tempGraph, k=None, normalized=True, weight=None, seed=None) # calculates edge betweenness for the graph
                    finalInformation.append((graphIndexCounter,numberOfNodes,numberOfEdges,edgeCounter,edgeList[e],edgeBetweenness[edgeList[e]]))
                    break

                elif sizeFlag == False: # if there is a component with size 1

                    tempGraph.remove_node(removedNode) # removes the isolated node from graph
                    if len(tempGraph.nodes) == 2: # if two nodes are remained in the graph (2 nodes, 1 edge)
                        finalInformation.append((graphIndexCounter, numberOfNodes, numberOfEdges, numberOfEdges,edgeList[orderIndex[len(orderIndex)-1]], "NAN"))
                        break
    return finalInformation



# -----------------------pickle creator------------------
def pickle_creator(finalInformation):
    with open('./finalResults1.pickle', 'wb') as f:
        pickle.dump(finalInformation, f)


# ------------------csv creator---------------------------
def csv_creator(finalInformation):
    header = ['Graph Index','Nodes','Edges','number of removed edges','Last removed edge','Betweenness']
    with open('csv/FinalResults.csv', 'w') as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerow(header)
        writer.writerows(finalInformation)

    
# -----------------------main function----------------------
def main():
    start_time = time.time()
    g = create_graph('text/out_doid.txt')
    edge_removal_result = robustness(g)
    pickle_creator(edge_removal_result)
    csv_creator(edge_removal_result)
    print("--- Total Execution time %s seconds ---" % (time.time() - start_time))

# -------------------------------if name----------------------
if __name__ == "__main__":
    main()

