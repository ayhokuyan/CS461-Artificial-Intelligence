from queue import Queue

PEOPLE_COEFF = 4 #put 3 to see the valid solution and put 4 to see the no solution

#1 for this side, -1 for across side
#This class is used to hold the states that are configured through
#tree traversal
class State(object):
    def __init__(self,  miss, cann, boat, parent_node):
        self.miss = miss
        self.cann = cann
        self.boat = boat

        self.parent_node = parent_node


    def children(self):
        if self.boat == 1:
            for m in range(PEOPLE_COEFF):
                for c in range(PEOPLE_COEFF):
                    newState = State(self.miss - m, self.cann - c, -1, self);
                    if m + c >= 1 and m + c <= 2 and newState.isValid() and newState.isUnique():
                        yield newState

        else:
            for m in range(PEOPLE_COEFF):
                for c in range(PEOPLE_COEFF):
                    newState = State(self.miss + m, self.cann + c, 1, self);
                    if m + c >= 1 and m + c <= 2 and newState.isValid() and newState.isUnique():
                        yield newState

    def getStateVector(self):
        return [self.miss,self.cann,self.boat]

    def getDepth(self):
        node = self
        depth = 0
        while node.parent_node is not None:
            depth += 1
            node = node.parent_node
        return depth

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
    print("solution: " + str(len(pathList)-1) + " steps")
    for i in range(len(pathList)-1):
        state1 = pathList[i]
        state2 = pathList[i+1]
        if(state1[2] == 1):
            #karşıya
            stateStr = '%d missionaries and %d cannibals go to the east side.' % (state1[0] - state2[0], state1[1] - state2[1])
        else:
            #karşıdan
            stateStr = '%d missionaries and %d cannibals come back to the west side.' % (state2[0] - state1[0], state2[1] - state1[1])
        print(stateStr +  ' State: ' + str(state2))

def bfs(root):
    queue = Queue()
    queue.put(root)
    cur_depth = -1
    while True:
        #not solvable
        if(queue.empty()):
           return None

        curNode = queue.get()

        if(curNode.getDepth() > cur_depth):
            cur_depth = curNode.getDepth()
            print('Depth:', cur_depth)

        print(curNode)
        if(curNode.isGoal()):
            printPath(curNode)
            return curNode.path()

        children = []
        for child in curNode.children():
            queue.put(child)


initial_state = State(PEOPLE_COEFF, PEOPLE_COEFF, 1, None)
solution = bfs(initial_state)
if solution is None:
    print("No solution for this start node is present in the graph.")
