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
	Energy_orig={}
	for i in Variables:
		Energy_orig[i[:3]]=random.randint(1,100)
		if (i[1]==i[2]):
			Energy_orig[i[:3]]=0
	Energy={}
	for i in Variables:
		if i[3]!='0':
			Energy[i]=Energy_orig[i[:3]]+Energy_orig[i[0]+i[2:]]
		else:
			Energy[i]=Energy_orig[i[:3]]

	return Energy,Energy_orig
	
def LPSolver(m,n,E):
	
	#Initializing Problem
	prob=LpProblem("Scheduling",LpMinimize)
	
	#Initializing Decision Variables(X)
	X,Y=decision_variables(m,n)
	X_vars=LpVariable.dicts("X",X,0,1,LpInteger)
	
	#Getting and Updating Energies(C)
	C,W=energy_val(X)
	for i in X:
		for j in range(1,m+1):
			if i[3]==j:
				C[i]+=E[j-1]
	
	#Objective Function(Minimize C*X)
	prob += lpSum(C[i]*X_vars[i] for i in X),"Objective"
	
	#Constraints
	for j in range (0,n-m):
		prob += lpSum(X_vars[i] for i in Y.T[j]) == 1
		
	for k in range(0,m*(n-m+1)):
		for j in Y[k]:
			if (j[1]==j[2]):
				prob += X_vars[j]==0
				
	for k in range (1,m+1):
		for j in range ((n-m+1)*(k-1)+1,(n-m+1)*k):
			prob += lpSum(X_vars[i] for i in Y[j])-((n-m-1)*X_vars['x'+str(j-((n-m+1)*(k-1))+m)+str(k)+str(0)])<=0
			
	#Solving
	prob.solve()
	
	X_Ans={}
	for v in prob.variables():
		key = str(v.name)[2:]
		val = v.varValue
		X_Ans[key] = val
	
	#Calculating Energies of nodes to transmit data to Access Point
	E_next=[]
	for j in range(0,n-m):
		E_next.append(lpSum(C[i]*X_Ans[i] for i in Y.T[j]))

	
	return LpStatus[prob.status],X_Ans,E_next,W


def multilayer_solver(k,layers):
	
	E=0
	X={}
	Weights={}
	r=0
	
	for i in range(1,k):
		s,var,E_next,W=LPSolver(layers[i-1],layers[i-1]+layers[i],E)
		
		for j in var.keys():
			old_key=j
			
			s = list(j[1:])
			s[0] = str(int(s[0])+r)
			s[1] = str(int(s[1])+r)
			if s[2]!='0':
				s[2] = str(int(s[2])+r)
			s.append('0')
			new_key = j[:1]+"".join(s)
			
			var[new_key]=var.pop(old_key)
			
		for j in var.keys():
			new_key=j[:-1]
			var[new_key]=var.pop(j)
		
		for j in W.keys():
			old_key=j
			
			s = list(j[1:])
			s[0] = str(int(s[0])+r)
			s[1] = str(int(s[1])+r)
			s.append('0')
			
			new_key = j[:1]+"".join(s)
			
			W[new_key]=W[old_key]
			del W[old_key]
		
		for j in W.keys():
			new_key=j[:-1]
			W[new_key]=W.pop(j)
			
		
		r=r+layers[i-1]
		
		E=E_next
		X.update(var)
		Weights.update(W)
	return X,Weights
		
X,Weights=multilayer_solver(3,[1,2,3])
print X,"\n"
print Weights
