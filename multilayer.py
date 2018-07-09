from pulp import *
from numpy import *


def decision_variables(m,n):
	X=[]
	for i in range(m+1,n+1):
		for k in range(1,m+1):
			X.append("x_"+str(i)+'_'+str(k)+'_'+str(0))
			for j in range(m+1,n+1):
				X.append("x_"+str(i)+'_'+str(j)+'_'+str(k))
	
	Q=asarray(X)
	Y=Q.reshape((n-m),m*(n-m+1)).T
				
	return X,Y
	
def energy_val(Variables):
	Energy_edges={}
	for i in Variables:
		j=i.split('_')
		j=j[0]+'_'+j[1]+'_'+j[2]
		Energy_edges[j]=random.randint(1,100)
		if (i.split('_')[1]==i.split('_')[2]):
			Energy_edges[j]=0
			
	Energy={}
	for i in Variables:
		j=i.split('_')
		l=j[0]+'_'+j[1]+'_'+j[2]
		k=j[0]+'_'+j[2]+'_'+j[3]
		
		if i.split('_')[3]!='0':
			Energy[i]=Energy_edges[l]+Energy_edges[k]
		else:
			Energy[i]=Energy_edges[l]

	return Energy,Energy_edges
	
def LPSolver(m,n,E):
	
	#Initializing Problem
	prob=LpProblem("Scheduling",LpMinimize)
	
	#Initializing Decision Variables(X)
	X,Y=decision_variables(m,n)
	X_vars=LpVariable.dicts("X",X,0,1,LpInteger)
	
	#Getting and Updating Energies(C)
	C,W=energy_val(X)
	
	for i in C.keys():
		l=i.split('_')
		for j in range(1,m+1):
			if l[3]==str(j) or (l[3]=='0' and l[2] == str(j)):
				C[i]= C[i]+E[j-1]
	
	#Objective Function(Minimize C*X)
	prob += lpSum(C[i]*X_vars[i] for i in X),"Objective"
	
	#Constraints
	for j in range (0,n-m):
		prob += lpSum(X_vars[i] for i in Y.T[j]) == 1
		
	for k in range(0,m*(n-m+1)):
		for j in Y[k]:
			if (j.split('_')[1]==j.split('_')[2]):
				prob += X_vars[j]==0
				
	for k in range (1,m+1):
		for j in range ((n-m+1)*(k-1)+1,(n-m+1)*k):
			prob += lpSum(X_vars[i] for i in Y[j])-((n-m-1)*X_vars['x'+'_'+str(j-((n-m+1)*(k-1))+m)+'_'+str(k)+'_0'])<=0
			
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
	
	E=[0]; Ener=[]
	X={}
	Weights={}
	r=0
	
	for i in range(1,k):
		s,var,E_next,W=LPSolver(layers[i-1],layers[i-1]+layers[i],E)
		
		for j in var.keys():
			old_key=j
			
			s = j.split('_')
			s[1] = str(int(s[1])+r)
			s[2] = str(int(s[2])+r)
			if s[3]!='0':
				s[3] = str(int(s[3])+r)
			s.append('0')
			new_key = "_".join(s)
			
			var[new_key]=var.pop(old_key)
			
		for j in var.keys():
			new_key="_".join(j.split('_')[:-1])
			var[new_key]=var.pop(j)
		
		for j in W.keys():
			old_key=j
		
			s = j.split('_')
			s[1] = str(int(s[1])+r)
			s[2] = str(int(s[2])+r)
			s.append('0')
			
			new_key = "_".join(s)
			
			W[new_key]=W.pop(old_key)
		
		for j in W.keys():
			new_key="_".join(j.split('_')[:-1])
			W[new_key]=W.pop(j)
			
		
		r=r+layers[i-1]
		
		E=E_next
		Ener.extend(E)
		X.update(var)
		Weights.update(W)
	return X,Weights,Ener
		
#X,Weights,E=multilayer_solver(6,[1,10,10,10,10,10])
#print "\n",X,"\n"
#print Weights,"\n"
#print E,"\n"

