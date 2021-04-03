#!/usr/bin/env python
# coding: utf-8

# In[21]:


# CS 461 - Artificial Intelligence - HW 4


# In this code we take topological sorting code from https://www.geeksforgeeks.org/python-program-for-topological-sorting/
# In topological sorting code, it uses recursive method in order to sort the graphs.
# Topological sorting code given in the link above sorts the whole graph, but in our case we need to sort it according to the
# expected element in the graph, so Graph class is modified according to this approach.
# We represented the graphs given in the homework task by using defaultdict library and then implemented the graphs in python.
# Then, we modified the topological sorting code in order to obtain a list for specific elements.
# Finally, we printed each expected elements' list according to the results we obtained from modified topological sorting code.
# 
# 1. Ayhan Okuyan
# 2. Barış Akçin
# 3. Berkan Özdamar
# 4. Deniz Doğanay
# 5. Mustafa Bay


#Python program to print topological sorting of a DAG 
from collections import defaultdict 
  
#Class to represent a graph 
class Graph: 
    def __init__(self,vertices): 
        self.graph = defaultdict(list) #dictionary containing adjacency List 
        self.V = vertices #No. of vertices 
  
    # function to add an edge to graph 
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
  
    # A recursive function used by topologicalSort 
    def topologicalSortUtil(self, v, visited, stack): 
  
        # Mark the current node as visited. 
        visited[v] = True
  
        # Recur for all the vertices adjacent to this vertex 
        for i in self.graph[v]: 
            if visited[i] == False: 
                self.topologicalSortUtil(i, visited, stack) 
  
        # Push current vertex to stack which stores result 
        stack.insert(0,v) 
  
    # The function to do Topological Sort. It uses recursive  
    # topologicalSortUtil() 
    def topologicalSort(self, num): 
        # Mark all the vertices as not visited 
        visited = [False]*self.V 
        stack =[] 
  
        # Call the recursive helper function to store Topological 
        # Sort starting from all vertices one by one 
        for i in range(self.V): 
            if i in self.graph[num]:
                if visited[i] == False: 
                    self.topologicalSortUtil(i, visited, stack) 
        
        # Push current vertex to stack which stores result 
        stack.insert(0,num) 
        # Print contents of stack 
        return stack

# Converting integers into string for first graph
def first(first):
    for i in range(first.__len__()):
        if first[i] == 0:
            first[i] = 'CAIVehicle'
        elif first[i] == 1:
            first[i] = 'CPuppet'
        elif first[i] == 2:
            first[i] = 'CAIPlayer'
        elif first[i] == 3:
            first[i] = 'CPipeUser'
        elif first[i] == 4:
            first[i] = 'CAIActor'
        elif first[i] == 5:
            first[i] = 'CAIObject'
        else:
            first[i] = 'Everything'
    return first

# Converting integers into string for second graph
def second(first):
    for i in range(first.__len__()):
        if first[i] == 0:
            first[i] = 'fstream'
        elif first[i] == 1:
            first[i] = 'ofstream'
        elif first[i] == 2:
            first[i] = 'iostream'
        elif first[i] == 3:
            first[i] = 'ifstream'
        elif first[i] == 4:
            first[i] = 'ostream'
        elif first[i] == 5:
            first[i] = 'istream'
        elif first[i] == 6:
            first[i] = 'ios'
        else:
            first[i] = 'Everything'
    return first

# Converting integers into string for third graph
def third(first):
    for i in range(first.__len__()):
        if first[i] == 0:
            first[i] = 'Permanent Manager'
        elif first[i] == 1:
            first[i] = 'Director'
        elif first[i] == 2:
            first[i] = 'Consultant Manager'
        elif first[i] == 3:
            first[i] = 'Permanent Employee'
        elif first[i] == 4:
            first[i] = 'Manager'
        elif first[i] == 5:
            first[i] = 'Consulant'
        elif first[i] == 6:
            first[i] = 'Temporary Employee'
        elif first[i] == 7:
            first[i] = 'Employee'
        else:
            first[i] = 'Everything'
    return first

# Implementing first graph by using defaultdict
g = Graph(7)
g.addEdge(0, 1)
g.addEdge(1, 3)
g.addEdge(2, 4)
g.addEdge(3, 4)
g.addEdge(4, 5) 
g.addEdge(5, 6) 

# Printing the results we obtained from topological sorting for specific elements
print('Graph 1:    ')
print('*******')
print(' ')
print("Following is a Topological Sort of the first graph for CAIVehicle from lowest precedence to highest")
vehicle = g.topologicalSort(0)
vehicle = first(vehicle)
print(vehicle)
print(' ')
print("Following is a Topological Sort of the first graph for CAIPlayer from lowest precedence to highest")
player = g.topologicalSort(2)
player = first(player)
print(player)
print(' ')
print(' ')

# Implementing second graph by using defaultdict
g = Graph(8)
g.addEdge(0, 2)
g.addEdge(1, 4)
g.addEdge(2, 4)
g.addEdge(2, 5)
g.addEdge(3, 5)
g.addEdge(4, 6)
g.addEdge(5, 6)
g.addEdge(6, 7)

# Printing the results we obtained from topological sorting for specific elements
print('Graph 2:    ')
print('*******')
print(' ')
print("Following is a Topological Sort of the second graph for ifstream from lowest precedence to highest")
ifstream = g.topologicalSort(3)
ifstream = second(ifstream)
print(ifstream)
print(' ')
print("Following is a Topological Sort of the second graph for fstream from lowest precedence to highest")
fstream = g.topologicalSort(0)
fstream = second(fstream)
print(fstream)
print(' ')
print("Following is a Topological Sort of the second graph for ofstream from lowest precedence to highest")
ofstream = g.topologicalSort(1)
ofstream = second(ofstream)
print(ofstream)
print(' ')
print(' ')

# Implementing third graph by using defaultdict
g = Graph(9)
g.addEdge(0, 3)
g.addEdge(0, 4)
g.addEdge(1, 4)
g.addEdge(2, 4)
g.addEdge(2, 5)
g.addEdge(3, 7)
g.addEdge(4, 7)
g.addEdge(5, 6)
g.addEdge(6, 7)
g.addEdge(7, 8)

# Printing the results we obtained from topological sorting for specific elements
print('Graph 3:    ')
print('*******')
print(' ')
print("Following is a Topological Sort of the third graph for Consultant Manager from lowest precedence to highest")
cm = g.topologicalSort(2)
cm = third(cm)
print(cm)
print(' ')
print("Following is a Topological Sort of the third graph for Director from lowest precedence to highest")
director = g.topologicalSort(1)
director = third(director)
print(director)
print(' ')
print("Following is a Topological Sort of the third graph for Permanent Manager from lowest precedence to highest")
pm = g.topologicalSort(0)
pm = third(pm)
print(pm)
print(' ')
print(' ')


# In[ ]:




