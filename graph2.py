#import graphviz 
from graphviz import Digraph
from graphviz import Graph
#import lpsolver function in multilayer.py
from multilayer import multilayer_solver
#below are imports for layered graph
# import networkx as nx
# import pygraphviz as pgv # pygraphviz should be available

dot = Digraph(comment='Mesh network',format='png')
dot2 = Digraph(comment='Mesh network',format='png')

k = 3 #number of layers
l = [1,10,10] # number of nodes in each layer
X,Weights,E = multilayer_solver(k,l)
n = sum(l)


#to generate input graph with given data
for i in range(1,n+1):
    for j in range(1,n+1):
            r = Weights.get("x"+'_'+str(i)+'_'+str(j))
            if(r!=None):
                if(i!=j):
                    dot.attr('edge',color='red',label = str(Weights["x"+'_'+str(i)+'_'+str(j)]))
                    dot.edge(str(i),str(j))

#to generate output based on answers of lpsolver
for i in X.keys():
    if(X[i]==1.0):
        r = Weights.get("_".join(i.split('_')[:-1]))
        if(r!=None):
            dot2.attr('edge',color='green',label = str(Weights["_".join(i.split('_')[:-1])]))
            dot2.edge(i.split('_')[1],i.split('_')[2])

dot.render('mesh2.gv', view=True)
dot2.render('meshclean.gv',view=True)

#below is to generate layered graph of input
# G = nx.DiGraph()
# for i in Weights.keys():
#     if(i.split('_')[1]!=i.split('_')[2]):
#         G.add_edge(i.split('_')[1],i.split('_')[2],color='red',label = Weights[i])


# A = nx.nx_agraph.to_agraph(G)
# p = 1
# for i in range(1,k+1):
#     a = []
#     for j in range(p,p+l[i-1]):
#         a.append(str(j))
#     A.add_subgraph(a,rank='same')
#     p = p+l[i-1]
    
# A.draw('example.png', prog='dot')

