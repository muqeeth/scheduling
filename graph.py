from graphviz import Digraph
from graphviz import Graph

dot = Digraph(comment='Mesh network',format='png')
n = 5
for i in range(2,n+1):
    for j in range(1,n+1):
        dot.node(str(j))
        if(i!=j):
            dot.edge(str(i),str(j))

dot.render('mesh.gv', view=True)