# scheduling
## Requirements

1.python2 should be installed in the system.

2.Install pip.

3.Install python packages pulp,graphviz,numpy,networkx,pygraphviz.

4.Install graphviz package for linux here(https://packages.ubuntu.com/search?keywords=graphviz&searchon=names).

5.Install packages for graphviz `sudo apt-get install graphviz libgraphviz-dev pkg-config`.

Follow below terminal commands to install above mentioned python packages.

1.`pip install graphviz` to install graphviz python package.

2.`pip install pulp` to install pulp.

3.`pip install numpy` to install numpy.

4.`pip install pygraphviz` to install pygraphviz.

### Documentation
1. We approach the problem solving two layers,one layer of m receiving nodes and other layer of n transmitting nodes. 
2. Each node in a layer is allowed to communicate directly to anyone of receiving nodes or relay its data to receiving nodes    through only one node in its layer.
3. We consider each node transmitting and receiving only a unit data.
4. After solving transmitting layer we assign energy weights required by each node in the layer to transmit unit data to        layer below it.
5. We solve layer by layer until we reach the top most layer.
#### Decision variables
1. We use `x_i_j_k` as notation for node communication from i to k via node j.If node directly communicates with manager        layer the value of k is 0. Decision variables with same i and j are maintained for uniformity in matrix.
2. decision_variables function takes m(number of receiving nodes) and n(number of transmitting nodes) as input.
3. We generate decision variables using for loop.
```
def decision_variables(m,n):
	X=[]
	for i in range(m+1,n+1):
		for k in range(1,m+1):
			X.append("x_"+str(i)+'_'+str(k)+'_'+str(0))
			for j in range(m+1,n+1):
				X.append("x_"+str(i)+'_'+str(j)+'_'+str(k))
```
4. Reshape `X` to write constraints for lpsolver in easy way and return X and reshaped X ie Y
```
	Q=asarray(X)
	Y=Q.reshape((n-m),m*(n-m+1)).T
	print X,"\n",Y			
	return X,Y
```
#### Random Energy values
1. We use `random` method in numpy to assign energy values for communication from node i to node j.
2. If node i and node j are equal we assign zero energy value.
```
def energy_val(Variables):
	Energy_edges={}
	for i in Variables:
		j=i.split('_')
		j=j[0]+'_'+j[1]+'_'+j[2]
		Energy_edges[j]=random.randint(1,100)
		if (i.split('_')[1]==i.split('_')[2]):
			Energy_edges[j]=0
 ```
3. If node j is in receiving nodes then cost for that path is the value assigned using random method. If node j acts as relay    then we add energy node j takes to transmit to node k to previous value.
```
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
  ```
4. To make cost function for a particular path we should also add energy weights(energy the receiving node takes to transmit    data to manager) of receiving node for each path to that received node.
```
	C,W=energy_val(X)
	
	for i in C.keys():
		l=i.split('_')
		for j in range(1,m+1):
			if l[3]==str(j) or (l[3]=='0' and l[2] == str(j)):
				C[i]= C[i]+E[j-1]
```
#### Lpsolver
1. Use LpProblem to initialize problem.prob is an instance object of LpProblem.
```
def LPSolver(m,n,E):
	
	#Initializing Problem
	prob=LpProblem("Scheduling",LpMinimize) 
```
2. Use LpVariable to create with decision variables as keys and values as either 0 or 1. 0 means not active and 1 mean          active path.
```
	X,Y=decision_variables(m,n)
	X_vars=LpVariable.dicts("X",X,0,1,LpInteger)
```
3. Use LpSum to create objective function with each path multiplying its cost value.
```
	prob += lpSum(C[i]*X_vars[i] for i in X),"Objective"
```
4. Define constraints for Lpsolver.
5. The sum of elements of each column should be less than 1, signifying each node sends its data only to one node.
```
	for j in range (0,n-m):
		prob += lpSum(X_vars[i] for i in Y.T[j]) == 1
```
6. If a node receives data from a node in the same layer, than it must send its data to the below layer.
```
	for k in range (1,m+1):
		for j in range ((n-m+1)*(k-1)+1,(n-m+1)*k):
			prob += lpSum(X_vars[i] for i in Y[j])-((n-m-1)*X_vars['x'+'_'+str(j-((n-m+1)*(k-1))+m)+'_'+str(k)+'_0'])<=0
```
7. We also ensure the path starting and ending at same node is not active.
   x_i_j_k = 0, if i = j.
```
	for k in range(0,m*(n-m+1)):
		for j in Y[k]:
			if (j.split('_')[1]==j.split('_')[2]):
				prob += X_vars[j]==0
 ```
8. Use solve method in LpProblem to solve.`prob.variables()` has keys representing each path and value 1 or 0 after solving
   the problem. LpSolver returns `X_Ans`. 
9. The energy weight of each node in transmitting nodes is calculated by adding cost value where the path is active.These      weights will be used to solve the layer above it.
```
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
 ```
#### Multilayer_solver
1.This function calls LpSolver for each two layers one transmitting with n-m nodes and other receiving with m nodes.
```
status,var,E_next,W=LPSolver(layers[i-1],layers[i-1]+layers[i],E)
```
2. All E_next values are appended to Ener list.
3. In weights and decision variables when the Lpsolver is called it returns keys which are present before so we need to add    number of nodes in previous layer for correct indexing.
```
def multilayer_solver(k,layers):
	
	E=[0,0]; Ener=[]
	X={}
	Weights={}
	r=0
	
	for i in range(1,k):
		status,var,E_next,W=LPSolver(layers[i-1],layers[i-1]+layers[i],E)
		
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
  ```
#### Plot input and output 

### Run
once the packages are successfully installed run scheduling.py file in the directory.

### Generated files
1. input.dot,output.dot,input.dot.png,ouput.dot.png.
<<<<<<< HEAD
2. Above dot files can be ran seperately to generate required formatted files. For example use `dot -Tpng input.dot -o outfile.png` to generate png files.
=======
2. Above dot files can be ran seperately to generate required formatted files. For example use `dot -Tpng input.dot -o outfile.png` to generate png files.
>>>>>>> 65e51ebb6a542c2450b48da96879096efdd4c271
