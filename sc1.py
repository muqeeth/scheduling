from pulp import *
from numpy import *
n=4
X=[]
for i in range(2,n+1):
	for j in range(1,n+1):
		X.append("x"+str(i)+str(j))
print X
Q=asarray(X)
Y=Q.reshape(n-1,n).T

C={'x21':100,'x22':0,'x23':15,'x24':15,
	'x31':100,'x32':15,'x33':0,'x34':15,
	'x41':100,'x42':15,'x43':15,'x44':0}

prob=LpProblem("Scheduling",LpMinimize)

X_vars=LpVariable.dicts("X",X,0,1,LpInteger)

prob += lpSum(C[i]*X_vars[i] for i in X),"Objective"

for j in range (0,n-1):
	prob += lpSum(X_vars[i] for i in Y.T[j]) == 1
	
for j in range (1,n):
	prob += lpSum(X_vars[i] for i in Y[j])-((n-2)*X_vars['x'+str(j+1)+str(1)])<=0
	
for k in range(0,n):
	for j in Y[k]:
		if (j[1]==j[2]):
			prob += X_vars[j]==0
	
prob.solve()

print LpStatus[prob.status]

for v in prob.variables():
    print(v.name, "=", v.varValue)
	
print value(prob.objective)
