"""
THIS  CODE  WAS MY OWN WORK , IT WAS  WRITTEN  WITHOUT  CONSULTING  ANY
SOURCES  OUTSIDE  OF  THOSE  APPROVED  BY THE  INSTRUCTOR. Alex Welsh
"""

# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class Node:                                 # custom node that hold a position (x,y)
    def __init__(self, pos, path, cost):          # and a list of directions to that position
        self.path = path
        self.position = pos
        self.cost = cost

    def getPosition(self):                  # returns position
        return self.position

    def getPath(self):                      # returns list of paths
        return self.path

    def getCost(self):                      # returns cost of path, doesn't include heuristic value
        return self.cost


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    stackStates = util.Stack()                                          # create stack, add start node to stack
    stackStates.push(Node(problem.getStartState(), [], 0))              # create explored dict and add start position
    exploredSet = {}

    while not stackStates.isEmpty():                                    # go until stack is empty, pop the node on top
        currNode = stackStates.pop()

        if problem.isGoalState(currNode.getPosition()):                 # if the position of the popped node is the goal
            return currNode.getPath()                                   # return the list of paths taken to that goal

        if exploredSet.get(currNode.getPosition(), None) is None:       # if the current node isn't explored
            exploredSet[currNode.getPosition()] = currNode              # add it to explored

            for child in problem.getSuccessors(currNode.getPosition()):      # for each successor, create nodes if not
                if exploredSet.get(child[0], None) is None:                  # in explored, add to the stack
                    newNode = Node(child[0], currNode.getPath() + [child[1]], 0)
                    stackStates.push(newNode)
    return False
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """

    queueStates = util.Queue()                                          # create queue, add start node to stack
    queueStates.push(Node(problem.getStartState(), [], 0))              # create explored dict and add start position
    exploredSet = {}

    while not queueStates.isEmpty():                                    # go until queue is empty, pop the node on top
        currNode = queueStates.pop()

        if problem.isGoalState(currNode.getPosition()):                 # if the position of the popped node is the goal
            return currNode.getPath()                                   # return the list of paths taken to that goal

        if exploredSet.get(currNode.getPosition(), None) is None:       # if the current node isn't explored
            exploredSet[currNode.getPosition()] = currNode              # add it to explored

            for child in problem.getSuccessors(currNode.getPosition()):      # for each successor, create nodes if not
                if exploredSet.get(child[0], None) is None:                  # in explored, add to the queue
                    newNode = Node(child[0], currNode.getPath() + [child[1]], 0)
                    queueStates.push(newNode)
    return False
    util.raiseNotDefined()


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    pqStates = util.PriorityQueue()                                     # create priority queue, add start node to queue
    pqStates.push(Node(problem.getStartState(), [], 0), 0)              # create explored map and add start position
    exploredSet = {}

    while not pqStates.isEmpty():                                       # go until pqueue is empty, pop the node on top
        currNode = pqStates.pop()

        if problem.isGoalState(currNode.getPosition()):                 # if the position of the popped node is the goal
            return currNode.getPath()                                   # return the list of paths taken to that goal

        if exploredSet.get(currNode.getPosition(), None) is None:       # if the current node isn't explored
            exploredSet[currNode.getPosition()] = currNode              # add it to explored

            for child in problem.getSuccessors(currNode.getPosition()):      # for each successor, create nodes if not
                if exploredSet.get(child[0], None) is None:                  # in explored, add to the pqueue with
                    newNode = Node(child[0], currNode.getPath() + [child[1]], currNode.getCost() + child[2])
                    pqStates.push(newNode, newNode.getCost())                # priority of the cost to get to node
    return False
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    pqStates = util.PriorityQueue()                    # make pqueue, add start node with priority of heuristic
                                                       # FYI, where you see position, think state
    startNode = Node(problem.getStartState(), [], 0)
    pqStates.push(startNode, heuristic(problem.getStartState(), problem))
    exploredSet = {}

    while not pqStates.isEmpty():                                            # while the queue isn't empty
        currNode = pqStates.pop()                                            # pop the lowest priority node

        if problem.isGoalState(currNode.getPosition()):                      # if that node is the goal. return it's
            return currNode.getPath()                                        # path

        if exploredSet.get(currNode.getPosition(), None) is None:            # if the state of the current node is not
            exploredSet[currNode.getPosition()] = currNode                   # explored, set it to explored.
                                                                             # for each successor of current state,
            for child in problem.getSuccessors(currNode.getPosition()):      # if hasn't been explored, set to explored
                                                                             # create a new node and push it to queue
                if exploredSet.get(child[0], None) is None:                  # with priority of cost + heuristic
                    newNode = Node(child[0], currNode.getPath() + [child[1]], currNode.getCost() + child[2])
                    pqStates.push(newNode, newNode.getCost() + heuristic(newNode.getPosition(), problem))
    return False
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
