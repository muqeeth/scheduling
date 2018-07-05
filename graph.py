from graphviz import Digraph
from graphviz import Graph
from sc1 import ILP

dot = Digraph(comment='Mesh network',format='png')

n = None
try:
	n = raw_input("enter n value(assume max of 2 hops): ")
except:
	n = 5

n = int(n)
d,C = ILP(n)


for i in range(2,n+1):
    for j in range(1,n+1):
        if(i!=j):
            if(d["x"+str(i)+str(j)]==1.0):
                dot.attr('edge',color='green',label = str(C["x"+str(i)+str(j)]))
                # if(j!=1):
                #     dot.attr('edge',constraint='false')
                dot.edge(str(i),str(j))
            else:
                dot.attr('edge',color='red',label = str(C["x"+str(i)+str(j)]))
                # if(j!=1):
                #     dot.attr('edge',constraint='false')
                dot.edge(str(i),str(j))

dot.render('mesh.gv', view=True)