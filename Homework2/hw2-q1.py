'''
In order to build an admissible heuristic, we have thought of the easiest way possible to cross the river if there were
no cannibal/missionary rule since the heuristic should always underestimate.
We thought that the we should start with the number of people that needs to cross the river which is the number of cannibals
+ the number of missionaries.
Then we thought that the most efficient way to cross the river is to always send people equal to the boat capacity however,
for the boat to move, one should always be back. Hence, the net people send would became (boat capacity -1)
Then the number of steps to take would become (#missionaries + #cannibals)/(boat capacity -1)
As we know that the heuristic should always give integer results, we decided either to ceil or floor this result.
After consideration we have chose floor since if we ceil, the underestimation assumption would fail one step from the goal.
Hence, H(m,c,boatCapacity) = floor((m+c)/(boatCapacity-1))
It may not be the best one, but it is definitely an admissible one.
For single stepping, we have printed the queue after each sorting in order to be able see that the queue is in line with
the heuristics.
Then there is the formatted output.
1. Ayhan Okuyan
2. Barış Akçin
3. Berkan Özdamar
4. Deniz Doğanay
5. Mustafa Bay
'''
from queue import Queue
import numpy as np

PEOPLE_COEFF = 6 #put 3 to see the valid solution and put 4 to see the no solution
MAX_ON_BOAT = 5

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
            if(node.getStateVector() == prNode.getStateVector()):
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

    def getHeur(self):
        return int(np.floor(((self.miss + self.cann)/(MAX_ON_BOAT-1))))

    def getTotalCost(self):
        return self.getHeur() + self.getDepth()


    def path(self):
        solution = []
        node = self
        while node.parent_node is not None:
            node = node.parent_node
            solution.append(node.getStateVector)
        solution.reverse()
        return solution

    #Here we modify the repr function of object class to recursively print the path from the beginning to the end
    def __repr__(self):
        return "(%d, %d, %d) , %r" % (self.miss, self.cann, self.boat, self.parent_node)


def printPath(finalNode):
    pathList = []
    node = finalNode
    while node.parent_node != None:
        pathList.append(node.getStateVector())
        node = node.parent_node
    pathList.append(node.getStateVector())
    pathList.reverse()

    begStr = '\n\n'
    for i in range(PEOPLE_COEFF):
        begStr += 'M'
    begStr += '\n'
    for i in range(PEOPLE_COEFF):
        begStr += 'C'
    print(begStr + '\n')

    for i in range(len(pathList)-1):
        state1 = pathList[i]
        state2 = pathList[i+1]
        if(state1[2] == 1):
            #karşıya
            stateStr = 'SEND   %d MISSIONARIES %d CANNIBALS' % (state1[0] - state2[0], state1[1] - state2[1])
        else:
            #karşıdan
            stateStr = 'RETURN %d MISSIONARIES %d CANNIBALS' % (state2[0] - state1[0], state2[1] - state1[1])
        stateStr += visualState(state2)
        print(stateStr)


def visualState(state):
    retStr = '\n'
    missHere = state[0]
    cannHere = state[1]
    missThere = PEOPLE_COEFF - missHere
    cannThere = PEOPLE_COEFF - cannHere
    for i in range(missHere):
        retStr += 'M'
    retStr += '                '
    for i in range(missThere):
        retStr += 'M'
    retStr += '\n'
    for i in range(cannHere):
        retStr += 'C'
    retStr += '                '
    for i in range(cannThere):
        retStr += 'C'
    return retStr + '\n'



def sortQueue(queue):
    objList = list(queue.queue)
    removeList = set()

    for i in range(len(objList)):
        cur = objList[i]
        for j in range(i+1,len(objList)-1,1):
            checked = objList[j]
            if cur.getStateVector() == checked.getStateVector():
                if cur.getTotalCost() <= checked.getTotalCost():
                    removeList.add(checked)
                elif cur.getTotalCost() > checked.getTotalCost():
                    removeList.add(cur)

    objList = [x for x in objList if x not in list(removeList)]

    objList.sort(key=lambda c: c.getTotalCost())
    queue.queue.clear()
    for i in range(len(objList)):
        queue.put(objList[i])
    return queue

#for single stepping
def printQueue(queue):
    for el in queue.queue:
        print(el)

def astars(root):
    queue = Queue()
    queue.put(root)
    while True:
        #not solvable
        if(queue.empty()):
           return None

        curNode = queue.get()

        if(curNode.isGoal()):
            printPath(curNode)
            return curNode.path()

        for child in curNode.children():
            queue.put(child)

        queue = sortQueue(queue)

        #for single stepping
        print("\nSorted queue")
        printQueue(queue)



initial_state = State(PEOPLE_COEFF, PEOPLE_COEFF, 1, None)
solution = astars(initial_state)
if solution is None:
    print("No solution for this start node is present in the graph.")
