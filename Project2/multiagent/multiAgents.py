"""
THIS  CODE  WAS MY OWN WORK , IT WAS  WRITTEN  WITHOUT  CONSULTING  ANY
SOURCES  OUTSIDE  OF  THOSE  APPROVED  BY THE  INSTRUCTOR. Alex Welsh
"""

# multiAgents.py
# --------------
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
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        # print legalMoves

        # Choose one of the best actions
        # for action in legalMoves:
        # print action, self.evaluationFunction(gameState, action)
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """

        import util
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currentFood = currentGameState.getFood()  # food available from current state
        currentPacmanPos = currentGameState.getPacmanPosition()
        successorPacmanPos = successorGameState.getPacmanPosition()
        newGhostStates = successorGameState.getGhostStates()

        ghostScore = 0
        foodScore = 1
        ghostAdjMoves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        if successorPacmanPos == currentPacmanPos:                                # don't stay still
            return -9999

        for ghostState in newGhostStates:                                         # if a move puts pacman close to ghost
            for move in ghostAdjMoves:                                            # avoid it.
                x, y = ghostState.getPosition()[0] + move[0], ghostState.getPosition()[1] + move[1]
                if (x, y) == successorPacmanPos:                                  # Ex. P_G. Pacman won't move right
                    return -9999

        foodList = currentFood.asList()

        foodDist = []
        if successorPacmanPos in foodList:                                        # if a successor has food, go to it
            foodScore = .25
        else:
            for foodPos in foodList:                                              # find closest manhattan dist to food
                foodDist.append(util.manhattanDistance(foodPos, successorPacmanPos))
            foodScore = min(foodDist)

        # reflex agent uses the score and the minimum distance to the food to evaluate a state.
        return successorGameState.getScore() + 1.0 / foodScore + random.choice([.1, -.1])


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.action = None


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          legalMoves = gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        self.value(gameState, self.depth, self.index)
        return self.action

    def maxValue(self, state, depth, agentid):                              # max for pacman
        v = -99999999999
        if not state.getLegalActions(agentid):
            return self.evaluationFunction(state)
        for action in state.getLegalActions(agentid):
            if action != Directions.STOP:
                val = self.value(state.generateSuccessor(agentid, action), depth, agentid + 1)
                if agentid == self.index and depth == self.depth:
                    if val > v:
                        self.action = action
                v = max(v, val)
        return v

    def minValue(self, state, depth, agentid):                              # min for ghosts
        v = 99999999999
        if not state.getLegalActions(agentid):
            return self.evaluationFunction(state)
        if agentid == state.getNumAgents() - 1:
            depth -= 1
        for action in state.getLegalActions(agentid):
            val = self.value(state.generateSuccessor(agentid, action), depth, agentid + 1)
            v = min(v, val)
        return v

    def value(self, state, depth, agentid):                                 # helper value method to calculate terminal
        if depth < 1 and agentid == state.getNumAgents():                   # max, and min values
            return self.evaluationFunction(state)
        else:
            if agentid == self.index or agentid == state.getNumAgents():
                return self.maxValue(state, depth, self.index)
            else:
                return self.minValue(state, depth, agentid)

        return None


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):                                             # main method for alpha-beta
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha = -99999999999
        beta = 99999999999
        self.value(gameState, self.depth, self.index, alpha, beta)
        return self.action

    def maxValue(self, state, depth, agentid, alpha, beta):                     # max value function to maximize pacman
        v = -99999999999                                                        # values.
        if not state.getLegalActions(agentid):
            return self.evaluationFunction(state)
        for action in state.getLegalActions(agentid):
            if action != Directions.STOP:
                val = self.value(state.generateSuccessor(agentid, action), depth, agentid + 1, alpha, beta)
                if agentid == self.index and depth == self.depth:               # keeps track of pacman's actions
                    if val > v:
                        self.action = action
                v = max(v, val)
                if v > beta:
                    return v
                alpha = max(alpha, v)
        return v

    def minValue(self, state, depth, agentid, alpha, beta):                     # min value function to minimize ghost
        v = 99999999999                                                         # values.
        if not state.getLegalActions(agentid):
            return self.evaluationFunction(state)
        if agentid == state.getNumAgents() - 1:
            depth -= 1
        for action in state.getLegalActions(agentid):
            val = self.value(state.generateSuccessor(agentid, action), depth, agentid + 1, alpha, beta)
            v = min(v, val)
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

    def value(self, state, depth, agentid, alpha, beta):                        # helper value method, returns eval
        if depth < 1 and agentid == state.getNumAgents():                       # eval for terminal states, max and min
            return self.evaluationFunction(state)
        else:
            if agentid == self.index or agentid == state.getNumAgents():
                return self.maxValue(state, depth, self.index, alpha, beta)
            else:
                return self.minValue(state, depth, agentid, alpha, beta)

        return None


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        self.value(gameState, self.depth, self.index)
        return self.action

    def maxValue(self, state, depth, agentid):                      # gets the max value for pacman
        v = -99999999999
        if not state.getLegalActions(agentid):
            return self.evaluationFunction(state)

        for action in state.getLegalActions(agentid):
            # print action
            if action != Directions.STOP:
                val = self.value(state.generateSuccessor(agentid, action), depth, agentid + 1)
                if agentid == self.index and depth == self.depth:   # determines pacman's action to take
                    if val > v:
                        self.action = action
                v = max(v, val)
        return v

    def expValue(self, state, depth, agentid):                      # gets the expected value for ghosts
        v = 0.0
        if not state.getLegalActions(agentid):
            return self.evaluationFunction(state)

        probability = 1.0 / len(state.getLegalActions(agentid))

        for action in state.getLegalActions(agentid):
            successor = state.generateSuccessor(agentid, action)
            val = self.value(successor, depth, agentid + 1)
            v += probability * val
        return v

    def value(self, state, depth, agentid):                         # helper value method that resets the agent to
        if agentid >= state.getNumAgents():                         # pacman and increases the depth when needed
            agentid = self.index
            depth -= 1
        if depth < 1 or state.isWin() or state.isLose():            # returns the terminal state, max or min value if
            return self.evaluationFunction(state)                   # current agent is pacman or ghost, respectively
        else:
            if agentid == self.index:
                return self.maxValue(state, depth, self.index)
            else:
                return self.expValue(state, depth, agentid)
        return None


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <This evaluation function gives the highest priority to maximizing the game score. It also takes into
      consideration the distance to the closest food, the total distance from pacman to every food, and the distance to
      the closest capsule. >
    """

    import util
    capsules = currentGameState.getCapsules()
    foodList = currentGameState.getFood().asList()
    totalDist = 0
    minFood = 99999999999999
    minCap = 99999999999999

    for foodPos in foodList:
        dist = util.manhattanDistance(foodPos, currentGameState.getPacmanPosition())
        minFood = min(dist, minFood)
        totalDist += dist

    for capsulePos in capsules:
        dist = util.manhattanDistance(capsulePos, currentGameState.getPacmanPosition())
        minCap = min(dist, minCap)

    return currentGameState.getScore() * 3000.0 + 200.0 / (minFood+1.0) + \
           10.0 / (totalDist + 1.0) + 30.0 / (minCap + 1.0)

# Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
