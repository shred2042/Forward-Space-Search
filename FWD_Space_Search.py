# returns true if the smaller set is included in the bigger set
def included(smaller, bigger):
    for x in smaller:
        if not x in bigger:
            return False
    return True

#taken from the lab
def NOT(P):
    return "NOT_" + P

#main function
def makePlan(problemData):
    problem = processInput(problemData)
    answer = solveProblem(problem, problemData)
    return answer

def solveProblem(problem, problemData):
    graph = computeDistances(problemData["wormholes"], problemData["start"], "Sol")
    answer = Search(problem, problem['initialState'], graph, [], 0, int(problemData["time"]))
    return answer

def processInput(problemData):
    Problem = {}
    Problem['initialState'] = []
    Problem['actions'] = {}

    #initial state data    
    Problem['initialState'].append(("Fuel", 1))
    Problem['initialState'].append(("Money", 0))
    Problem['initialState'].append(("Empty", "StorageA"))
    Problem['initialState'].append(("Empty", "StorageB"))
    Problem['initialState'].append(("In", problemData["start"]))

    #wormholes
    for w in problemData["wormholes"]:
        Problem['initialState'].append(("WormHole", w[0], w[1]))
        Problem['actions'][("Jump", w[0], w[1])] = ([("In", w[0])], [("In", w[1]), (NOT("In"), w[0])])
        Problem['actions'][("Jump", w[1], w[0])] = ([("In", w[1])], [("In", w[0]), (NOT("In"), w[1])])

    #gas stations
    for g in problemData["gas"]:
        Problem['initialState'].append(("GasStation", g))
        Problem['actions'][("BuyGas", g )] = ([("In", g)], [("Money", 0)])

    #packages
    for p in problemData["packages"]:
        Problem['initialState'].append(("From", p[0] ,p[1]))
        Problem['initialState'].append(("To", p[0], p[2]))
        Problem['initialState'].append(("Reward", p[0] , p[3]))
        Problem['actions'][("Pickup", p[0], "StorageA")] = ([("In", p[1]), ("Empty", "StorageA"), ("From", p[0], p[1])], [("Carries", "StorageA", p[0]), (NOT("Empty"), "StorageA"), (NOT("From"), p[0], p[1])])
        Problem['actions'][("Pickup", p[0], "StorageB")] = ([("In", p[1]), ("Empty", "StorageB"), ("From", p[0], p[1])], [("Carries", "StorageB", p[0]), (NOT("Empty"), "StorageB"), (NOT("From"), p[0], p[1])])
        Problem['actions'][("Deliver0", p[0])] = ([("In", p[2]), ("Carries", "StorageA", p[0]), ("To", p[0], p[2])], [(NOT("Carries"), "StorageA", p[0]), ("Empty", "StorageA"), (NOT("To"), p[0], p[2])])
        Problem['actions'][("Deliver1", p[0])] = ([("In", p[2]), ("Carries", "StorageB", p[0]), ("To", p[0], p[2])], [(NOT("Carries"), "StorageB", p[0]), ("Empty", "StorageB"), (NOT("To"), p[0], p[2])])

    #goal
    Problem['goals'] = [("In", "Sol")]

    return Problem

"""
This is basically a graph created by applying BFS starting from the goal system
"""
def computeDistances(edges, root, destination):
    MAX_INT = 9999999

    """
    Here we fill the graph with basic data
    """
    graphNodes = {}
    #Judging by the edges in the wormhole structure, find out the neighbours
    for edge in edges:
        if edge[0] not in graphNodes:
            graphNodes[edge[0]] = {}
            graphNodes[edge[0]]["neigh"] = []
            graphNodes[edge[0]]["distance"] = MAX_INT
        #Put the data for the first vertex in the neighbour list
        graphNodes[edge[0]]["neigh"].append(edge[1])
        if edge[1] not in graphNodes:
            graphNodes[edge[1]] = {}
            graphNodes[edge[1]]["neigh"] = []
            graphNodes[edge[1]]["distance"] = MAX_INT
        #Put the data for the second vertex in the neighbour list
        graphNodes[edge[1]]["neigh"].append(edge[0])

    #the BFS algorithm
    queue = []
    queue.append(destination)
    distance = 0
    graphNodes[destination]["distance"] = 0
    while len(queue) != 0:
        curNode = queue.pop(0)
        distance = distance + 1

        for neigh in graphNodes[curNode]["neigh"]:
            if graphNodes[neigh]["distance"] == MAX_INT:
                graphNodes[neigh]["distance"] = distance
                queue.append(neigh)
    return graphNodes


#forward space search algorithm
def Search(Problem, state, Graph, plan, time, LIMIT):
    if time > LIMIT:
        return False
    currentState = state
    currentPlan = plan
    if included(Problem['goals'], currentState):
        return currentPlan
    validActions = getValidActions(currentState, Problem)
    if validActions == {}:
        return False
    heuristicFunction = createHeuristicFunction(Problem, Graph, state, validActions)
    heuristicFunction.sort(key=lambda x: x[1])
    
    while len(validActions) != 0:
        action = getAction(validActions, heuristicFunction)
        nextState = getNextState(action, currentState)
        currentPlan.append(format(action[0]))
        if action[0][0] == 'JUMP':
            answer = Search(Problem, nextState, Graph, currentPlan, time + 1, LIMIT)
        else:            
            answer = Search(Problem, nextState, Graph, currentPlan, time, LIMIT)
        #this path does not lead to a solution, backtrack
        if answer == False:
            del validActions[action[0]]
            currentPlan.pop() 
        else:
            return answer
    return False

def format(action):
    #differentiate the delivers
    if action[0] == "Deliver0" or action[0] == "Deliver1":
        ret = "Deliver("
    else:
        ret = action[0] + "("
    #take all members of the action tuple except for the first one
    for i in action[1:]:
        ret = ret + str(i) + ","
    #add the parantheses and remove the trailing comma
    ret = ret[0:len(ret)-1] + ")"
    return ret
 

def createHeuristicFunction(problem, graph, state, applicables):
    heuristicFunction = []
    for action in applicables:
        if action[0] == 'JUMP':
            setNo = 1
        else:
            setNo = 0
        for preconditions in applicables[action][setNo]:
            if preconditions[0] == "In":
                strLocation = preconditions[1]
                heuristicFunction.append((action, graph[strLocation]["distance"])) 
                break
    return heuristicFunction

def getValidActions(currentState, Problem):
    validActions = {}
    for key, value in Problem['actions'].items():
        preconditionsitions = value[0]
        effects = value[1]
        if key[0] == "Jump":
            (newPreconditions, newEffects) = getJumpEffects(currentState)
        if key[0] == "Deliver0" or key[0] == "Deliver1":
            (newPreconditions, newEffects) = getDeliverEffects(currentState, key)    
        if key[0] == "Pickup":
            (newPreconditions, newEffects) = ([], [])
        if key[0] == "BuyGas":
            (key, newPreconditions, newEffects) = getBuyGasEffects(currentState)

        if newPreconditions == None:
            continue
        else:
            if included(preconditionsitions + newPreconditions, currentState):
                validActions[key] = (preconditionsitions + newPreconditions, effects + newEffects) 
    return validActions


def getJumpEffects(state):
    for strFact in state:
        if strFact[0] == "Fuel":
            intValue = int(strFact[1])
            if intValue != 0:
                return ([strFact], [("Fuel", intValue - 1), (NOT("Fuel"), intValue)])
            else:
                return (None, None)

def getDeliverEffects(state, strKey):
    strId = strKey[1]
    tupReward = [fact for fact in state if fact[0] == "Reward" and fact[1] == strId][0]
    intGain = int(tupReward[2])
    for strFact in state:
        if strFact[0] == "Money":
            intValue = strFact[1]
            preconditions = []
            effects= []
            preconditions.append(strFact)
            effects.append((NOT("Money"), intValue))
            intValue = intValue + intGain
            effects.append(("Money", intValue))
            return (preconditions, effects)

def getBuyGasEffects(state):
    for strFact in state:
        if strFact[0] == "Money":
            intValue = strFact[1]
            if intValue == 0:
                return (None, None, None)
            for strFact2 in state:
                if strFact2[0] == "Fuel":
                    preconditions = []
                    effects= []
                    intValue2 = strFact2[1]
                    preconditions.append(strFact)
                    preconditions.append(strFact2)
                    effects.append((NOT("Money"), intValue))
                    effects.append(("Fuel", intValue + intValue2))
                    effects.append((NOT("Fuel"), intValue2))
                    key = ("BuyGas", intValue)
                    return (key, preconditions, effects)


def getAction(validActions, heuristicFunction):
    for action in heuristicFunction:
        if action[0] in validActions:
            return (action[0], validActions[action[0]])

def getNextState(action, arrCurrState):
    (preconditions, eff) = action[1]
    newState = list(arrCurrState)
    for e in eff:
        if e[0][0:4] == "NOT_":
            f = list(e)
            f[0] = f[0][4:]
            f = tuple(f)
            if f in newState:
                newState.remove(f)
        else:
            newState.append(e)
    return newState

