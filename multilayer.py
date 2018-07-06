from pulp import *
from numpy import *


def decision_variables(m,n):
	X=[]
	for i in range(m+1,n+1):
		for k in range(1,m+1):
			X.append("x"+str(i)+str(k)+str(0))
			for j in range(m+1,n+1):
				X.append("x"+str(i)+str(j)+str(k))
	
	Q=asarray(X)
	Y=Q.reshape((n-m),m*(n-m+1)).T
				
	return X,Y
	
def energy_val(Variables):
	C={}
	for i in Variables:
		C[i]=random.randint(1,100)
	return C

def Lpsolver(m,n,E):

	prob=LpProblem("Scheduling",LpMinimize)
	
	X,Y=decision_variables(m,n)
	X_vars=LpVariable.dicts("X",X,0,1,LpInteger)
	
	C=energy_val(X)
	for i in X:
		for j in range(1,m+1):
			if i[3]==j:
				C[i]+=E[j-1]
	
	prob += lpSum(C[i]*X_vars[i] for i in X),"Objective"
	
	for j in range (0,n-m):
		prob += lpSum(X_vars[i] for i in Y.T[j]) == 1
		
	for k in range(0,m*(n-m+1)):
		for j in Y[k]:
			if (j[1]==j[2]):
				prob += X_vars[j]==0
				
	for k in range (1,m+1):
		for j in range ((n-m+1)*(k-1)+1,(n-m+1)*k):
			prob += lpSum(X_vars[i] for i in Y[j])-((n-m-1)*X_vars['x'+str(j-((n-m+1)*(k-1))+m)+str(k)+str(0)])<=0
			
	prob.solve()
	
	X_Ans={}
	for v in prob.variables():
		key = str(v.name)[2:]
		val = v.varValue
		X_Ans[key] = val
	
	E_next=[]
	for j in range(0,n-m):
		E_next.append(lpSum(C[i]*X_Ans[i] for i in Y.T[j]))

	
	return LpStatus[prob.status],X_Ans,C,E_next
	
# status,var,C,E=Lpsolver(2,5,[10,10])
# print status
# print var
# print E