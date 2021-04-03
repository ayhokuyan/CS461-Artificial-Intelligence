'''
Here, we have again used the A* star search since we have implemented that algorithm in the previous question with a
little twist. Instead of stopping the algorithm after a goal node is reached, we have saved the depth of this goal node
and the node itself. After that we kept saving all of the goal states that have the same depth, for which we are sure that
that depth value is the minimum cost that can be achieved. Then we have displayed the length of that vector that contains
all of the shortest solutions.
As the queue continues to progress, after the shortest paths are found, the algoirthm stops at the first min+1 depth
node. We haven't checked the validity of the states after the shortest paths are found since the algorithm wouldn't continue
even they are valid or not.
1. Ayhan Okuyan
2. Barış Akçin
3. Berkan Özdamar
4. Deniz Doğanay
5. Mustafa Bay
'''
from queue import Queue
import numpy as np

PEOPLE_COEFF = 4 #put 3 to see the valid solution and put 4 to see the no solution
MAX_ON_BOAT = 3

#1 for this side, -1 for across side
#This class is used to hold the states that are configured through
#tree traversal
class State(object):
    def __init__(self,  miss, cann, boat, parent_node, cost=0):
        self.miss = miss
        self.cann = cann
        self.boat = boat

        self.cost = cost

        self.parent_node = parent_node


    def children(self):
        if self.boat == 1:
            for m in range(PEOPLE_COEFF):
                for c in range(PEOPLE_COEFF):
                    newState = State(self.miss - m, self.cann - c, -1, self, self.cost+1)
                    if self.isBoatValid(m,c) and newState.isValid() and newState.isUnique():
                        yield newState

        else:
            for m in range(PEOPLE_COEFF):
                for c in range(PEOPLE_COEFF):
                    newState = State(self.miss + m, self.cann + c, 1, self, self.cost+1)
                    if self.isBoatValid(m,c) and newState.isValid() and newState.isUnique():
                        yield newState

    def isBoatValid(self, m, c):
        if ((c > m) and (m > 0)) or (m + c < 1) or (m + c > MAX_ON_BOAT):
            return False
        return True

    def getStateVector(self):
        return [self.miss,self.cann,self.boat]

    def getDepth(self):
        return self.cost

    def isGoal(self):
        if(self.miss == 0 and self.cann == 0 and self.boat == -1):
            return True
        return False


    def isUnique(self):
        node = self
        prNode = node.parent_node
        while(prNode is not None):
            if node.getStateVector() == prNode.getStateVector():
                return False
            prNode = prNode.parent_node
        return True

    def isValid(self):
        if self.miss < 0 or self.cann < 0 or self.miss > PEOPLE_COEFF or self.cann > PEOPLE_COEFF  or (self.boat != -1 and self.boat != 1):
            return False
        if (self.cann > self.miss) and (self.miss > 0):
            return False
        if (self.cann < self.miss) and (self.miss < PEOPLE_COEFF):
            return False
        return True

    def heur(self):
        return int(np.floor((self.miss + self.cann)/(MAX_ON_BOAT-1)))

    def getTotalCost(self):
        return self.heur() + self.getDepth()

    #Here we modify the repr function of object class to recursively print the path from the beginning to the end
    def __repr__(self):
        return "(%d, %d, %d) , %r" % (self.miss, self.cann, self.boat, self.parent_node)


#for single stepping
def printQueue(queue):
    print(queue.queue[0])

def sortQueue(queue):
    objList = list(queue.queue)
    removeList = set()

    for i in range(len(objList)):
        cur = objList[i]
        for j in range(i+1,len(objList)-1,1):
            checked = objList[j]
            if cur.getStateVector() == checked.getStateVector():
                if cur.getTotalCost() < checked.getTotalCost():
                    removeList.add(checked)
                elif cur.getTotalCost() > checked.getTotalCost():
                    removeList.add(cur)

    objList = [x for x in objList if x not in list(removeList)]
    objList.sort(key=lambda c: c.getTotalCost())

    queue.queue.clear()
    for i in range(len(objList)):
        queue.put(objList[i])
    return queue


def astars(root):
    finalPaths = list()
    minDepth = -1
    queue = Queue()
    queue.put(root)
    cur_depth = -1
    while True:
        #not solvable
        if(queue.empty()):
           return None

        curNode = queue.get()

        if(curNode.isGoal()):
            minDepth = curNode.getDepth()
            finalPaths.append(curNode)

        if(minDepth > 0 and curNode.getDepth() > minDepth):
            return finalPaths

        for child in curNode.children():
            queue.put(child)

        queue = sortQueue(queue)

        # for single stepping
        # here we only showed to fronts of the queues and the minimum paths to be able to
        #search for them with ctri+f and see the multiples
        print("\nSorted queue front")
        printQueue(queue)



initial_state = State(PEOPLE_COEFF, PEOPLE_COEFF, 1, None)
solutions = astars(initial_state)
if solutions is None:
    print("No solution for this start node is present in the graph.")
else:
    print("\n\nhe number of possible solutions are ", len(solutions))
    print("These solutions are, ")
    for sol in solutions:
        print(sol)


