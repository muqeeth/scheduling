from graphviz import Digraph
from graphviz import Graph
from multilayer import Lpsolver

dot = Digraph(comment='Mesh network',format='png')

n = None
m = None
try:
	m = raw_input("enter m value(receiving nodes): ")
except:
	m = 5

m = int(m)

try:
	n = raw_input("enter n value(n-m transmitting nodes): ")
except:
	n = 5

n = int(n)

status,d,C,E = Lpsolver(m,n,[10]*m)

print status
print C
print d

for i in range(n-m,n+1):
    for j in range(1,n+1):
        for k in range(0,m+1):
            r = d.get("x"+str(i)+str(j)+str(k))
            if(r!=None):
                if(i!=j):
                    if(k==0):
                        if(d["x"+str(i)+str(j)+str(k)]==1.0):
                            dot.attr('edge',color='green',label = str(C["x"+str(i)+str(j)+str(k)]))
                            dot.edge(str(i),str(j))
                        else:
                            dot.attr('edge',color='red',label = str(C["x"+str(i)+str(j)+str(k)]))
                            dot.edge(str(i),str(j))
                    else:
                        if(d["x"+str(i)+str(j)+str(k)]==1.0):
                            dot.attr('edge',color='green',label = str(C["x"+str(i)+str(j)+str(k)]))
                            dot.edge(str(i),str(j))
                            dot.edge(str(j),str(k))
                        else:
                            dot.attr('edge',color='blue',label = str(C["x"+str(i)+str(j)+str(k)]))
                            dot.edge(str(i),str(j))
                            dot.edge(str(j),str(k))
dot.render('mesh2.gv', view=True)