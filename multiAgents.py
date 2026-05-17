# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition() # tọa độ dự kiến của Pacman sau khi thực hiện hành động
        newFood = successorGameState.getFood() # lưới thức ăn sau khi thực hiện hành động
        newGhostStates = successorGameState.getGhostStates() # trạng thái của các ma sau khi thực hiện hành động
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # thời gian còn lại mà mỗi ma sẽ bị sợ sau khi thực hiện hành động

        "*** YOUR CODE HERE ***"
        # 1. Chuyển lưới thức ăn thành danh sách các tọa độ
        foodList = newFood.asList()

        # 2. Xử lý Ma (Ghosts) - Đảm bảo sinh tồn
        for ghostState in newGhostStates:
            ghostPos = ghostState.getPosition()
            # Tính khoảng cách từ vị trí mới của Pacman đến ma
            distance_to_ghost = util.manhattanDistance(newPos, ghostPos)
            
            # Nếu ma ở quá gần (cách 1 ô hoặc ngay tại đó) và ma không bị sợ
            if distance_to_ghost <= 1 and ghostState.scaredTimer == 0:
                # Hành động này vô cùng nguy hiểm, trả về điểm thấp tuyệt đối
                return float('-inf') 

        # 3. Xử lý Thức ăn (Food) - Khuyến khích ăn điểm
        if not foodList:
            # Nếu không còn thức ăn nào, nghĩa là hành động này giúp qua màn
            return float('inf')

        # Tìm khoảng cách đến viên thức ăn gần nhất
        closest_food_dist = min([util.manhattanDistance(newPos, food) for food in foodList])

        # 4. Tính toán và trả về điểm tổng hợp
        # Kết hợp điểm số cơ bản của game với điểm thưởng từ thức ăn (nghịch đảo khoảng cách)
        return successorGameState.getScore() + 1.0 / closest_food_dist

def scoreEvaluationFunction(currentGameState: GameState):
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        numAgents = gameState.getNumAgents()

        def value(state, depth, agentIndex):
            # Điều kiện dừng: đạt độ sâu tối đa hoặc trạng thái thắng/thua
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            legalActions = state.getLegalActions(agentIndex)
            # Xử lý nếu không có hành động hợp lệ để tránh lỗi bước tính max/min trên danh sách rỗng
            if not legalActions:
                return self.evaluationFunction(state)

            # Xác định chỉ số tác nhân tiếp theo và độ sâu tiếp theo
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth

            # Nút Max dành cho Pacman
            if agentIndex == 0:
                return max(
                    value(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent)
                    for action in legalActions
                )

            # Tính xác suất cho mỗi hành động của ma (giả sử chọn ngẫu nhiên đồng đều)
            probability = 1.0 / len(legalActions)
            # Nút Expectimax dành cho ma: tính giá trị kỳ vọng bằng cách lấy trung bình có trọng số của các điểm số dự đoán từ các hành động hợp lệ
            return sum(
                probability * value(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent)
                for action in legalActions
            )

        # Khởi tạo biến bestScore và bestAction để theo dõi nước đi tốt nhất
        bestScore = -float('inf')
        bestAction = Directions.STOP

        for action in gameState.getLegalActions(0):
            # Gọi đệ quy cho con ma đầu tiên (agentIndex=1) và độ sâu ban đầu là 0
            score = value(gameState.generateSuccessor(0, action), 0, 1 % numAgents)
            # print(f"Action: {action}, Score: {score}")
            # Cập nhật bestScore và bestAction nếu tìm thấy nước đi tốt hơn
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction
def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction