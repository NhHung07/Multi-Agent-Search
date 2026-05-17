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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # Nếu nước đi này thắng -> buộc phải đi, Nếu nước đi này thua -> tuyết đối tránh
        if successorGameState.isWin():
            return successorGameState.getScore() + 100000
        if successorGameState.isLose():
            return successorGameState.getScore() - 100000

        # Lấy điểm số cơ bản của trạng thái kế tiếp để làm nền tảng cho hàm đánh giá
        score = successorGameState.getScore()

        # Ưu tiên di chuyển về phía thức ăn gần nhất
        foodList = newFood.asList()
        if foodList:
            # Tìm khoảng cách Manhattan ngắn nhất tới 1 viên thức ăn
            minFoodDist = min(manhattanDistance(newPos, foodPos) for foodPos in foodList)   
            score += 1.0 / (minFoodDist + 1)

        # Tránh ma đang hoạt động, đuổi ma đang sợ hãi
        for i, ghostState in enumerate(newGhostStates):
            ghostPos = ghostState.getPosition()
            dist = manhattanDistance(newPos, ghostPos)
            if newScaredTimes[i] > 0:
                score += 2.0 / (dist + 1)
            else:
                if dist <= 1:
                    score -= 10
                score -= 1.5 / (dist + 1)

        # Trừ lượng nhỏ điểm cho thức ăn còn lại để khuyến khích Pacman ăn nhanh
        score -= 0.1 * len(foodList)
        return score

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


            if agentIndex == 0:
                # Nút Max dành cho Pacman
                return max(
                    value(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent)
                    for action in legalActions
                )
            # Nút Min dành cho ma
            return min(
                value(state.generateSuccessor(agentIndex, action), nextDepth, nextAgent)
                for action in legalActions
            )

        # Khỏi tạo biến bestScore và bestAction để theo dõi nước đi tốt nhất
        bestScore = -float('inf')
        bestAction = Directions.STOP
        
        for action in gameState.getLegalActions(0):
            # Gọi đệ quy cho con ma đầu tiên (agentIndex=1) và độ sâu ban đầu là 0
            score = value(gameState.generateSuccessor(0, action), 0, 1 % numAgents)
            # Cập nhật bestScore và bestAction nếu tìm thấy nước đi tốt hơn
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        numAgents = gameState.getNumAgents()

        def value(state, depth, agentIndex, alpha, beta):
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
                # Khởi tạo giá trị v với -inf để tìm max
                v = -float('inf')
                for action in legalActions:
                    # Tính điểm của nước đi hiện tại bằng cách:
                    # 1. Mô phỏng trạng thái bàn cờ tiếp theo (generateSuccessor)
                    # 2. Gọi đệ quy hàm value() để dự đoán điểm số cuối cùng của nhánh tương lai này
                    # 3. So sánh điểm vừa dự đoán với kỷ lục hiện tại (v) và lưu lại giá trị lớn nhất (max)
                    v = max(
                        v,
                        value(
                            state.generateSuccessor(agentIndex, action),
                            nextDepth,
                            nextAgent,
                            alpha,
                            beta,
                        ),
                    )
                    # Điều kiện cắt tỉa alpha-beta: nếu v đã lớn hơn beta, không cần tiếp tục đánh giá các hành động còn lại
                    if v > beta:
                        return v
                    # Cập nhật alpha nếu v tốt hơn alpha hiện tại
                    alpha = max(alpha, v)
                return v

            # Nút Min dành cho ma
            # Khởi tạo giá trị v với +inf để tìm min
            v = float('inf')
            for action in legalActions:
                # Tính điểm của nước đi hiện tại bằng cách:
                # 1. Mô phỏng trạng thái bàn cờ tiếp theo (generateSuccessor)
                # 2. Gọi đệ quy hàm value() để dự đoán điểm số cuối cùng của nhánh tương lai này
                # 3. So sánh điểm vừa dự đoán với kỷ lục hiện tại (v) và lưu lại giá trị nhỏ nhất (min)
                v = min(
                    v,
                    value(
                        state.generateSuccessor(agentIndex, action),
                        nextDepth,
                        nextAgent,
                        alpha,
                        beta,
                    ),
                )
                # Điều kiện cắt tỉa alpha-beta: nếu v đã nhỏ hơn alpha, không cần tiếp tục đánh giá các hành động còn lại
                if v < alpha:
                    return v
                # Cập nhật beta nếu v tốt hơn beta hiện tại
                beta = min(beta, v)
            return v

        # Khởi tạo alpha và beta, cũng như biến bestScore và bestAction để theo dõi nước đi tốt nhất
        alpha = -float('inf')
        beta = float('inf')
        bestScore = -float('inf')
        bestAction = Directions.STOP

        for action in gameState.getLegalActions(0):
            # Gọi đệ quy cho con ma đầu tiên (agentIndex=1) và độ sâu ban đầu là 0, đồng thời truyền alpha và beta
            score = value(gameState.generateSuccessor(0, action), 0, 1 % numAgents, alpha, beta)
            # Cập nhật bestScore và bestAction nếu tìm thấy nước đi tốt hơn
            if score > bestScore:
                bestScore = score
                bestAction = action
            # Cập nhật alpha sau khi đánh giá nước đi của Pacman
            alpha = max(alpha, bestScore)
        return bestAction

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

    DESCRIPTION: Combines current game score with distance-based features.
    Rewards being close to food and scared ghosts, penalizes being near active
    ghosts and leaving many foods/capsules on the board. Returns very large
    values on win/lose terminal states.
    """

    # Nếu nước đi này thắng -> buộc phải đi, Nếu nước đi này thua -> tuyết đối tránh
    if currentGameState.isWin():
        return currentGameState.getScore() + 100000
    if currentGameState.isLose():
        return currentGameState.getScore() - 100000

    # Lấy các thông tin cần thiết từ trạng thái hiện tại để tính toán điểm số
    pacmanPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    # Bắt đầu với điểm số cơ bản của trạng thái hiện tại
    score = currentGameState.getScore()

    # Mục tiêu chính chính là thu thập thức ăn
    if foodList:
        minFoodDist = min(manhattanDistance(pacmanPos, foodPos) for foodPos in foodList)
        # Thưởng lớn cho việc di chuyển gần thức ăn và phạt nặng thức ăn còn thừa để Pacman di chuyển tối ưu hơn
        score += 4.0 / (minFoodDist + 1)
        score -= 8.0 * len(foodList)
    else:
        # Bonus để dọn sạch map
        score += 1000  

    # Ưu tiên cao cho viên năng lượng nếu nó xuất hiện trên bản đồ 
    if capsules:
        minCapsuleDist = min(manhattanDistance(pacmanPos, capPos) for capPos in capsules)
        score += 4.0 / (minCapsuleDist + 1)
        score -= 50.0 * len(capsules)

    # Đánh giá mối đe dạo từ ma
    for ghostState in ghostStates:
        ghostPos = ghostState.getPosition()
        dist = manhattanDistance(pacmanPos, ghostPos)
        
        if ghostState.scaredTimer > 0:
            # Ưu tiên cao nhất cho việc đuổi ma đang sợ hãi
            score += 10.0 / (dist + 1)
        else:
            # Phân vùng tránh ma để thuật toán hiệu quả hơn 
            if dist <= 1:
                score -= 500
            elif dist == 2:
                score -= 100
            elif dist == 3:
                score -= 25
            else:
                score -= 3.0 / (dist + 1)

    return score

def riskAwareEvaluationFunction(currentGameState: GameState):
    
    # Nếu nước đi này thắng -> buộc phải đi, Nếu nước đi này thua -> tuyết đối tránh
    if currentGameState.isWin():
        return currentGameState.getScore() + 100000
    if currentGameState.isLose():
        return currentGameState.getScore() - 100000

    # Lấy các thông tin cần thiết từ trạng thái hiện tại để tính toán điểm số
    pacmanPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    walls = currentGameState.getWalls()

    # Hàm BFS để tính khoảng cách thực tế trong mê cung từ vị trí hiện tại đến tất cả các vị trí khác
    def computeMazeDistances(startPos):
        queue = util.Queue()
        queue.push(startPos)
        distances = {startPos: 0}

        while not queue.isEmpty():
            x, y = queue.pop()
            baseDist = distances[(x, y)]
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                # Nếu là tường thì bỏ qua
                if walls[nx][ny]:
                    continue
                # Nếu đã tính khoảng cách đến vị trí này rồi thì bỏ qua
                if (nx, ny) in distances:
                    continue
                distances[(nx, ny)] = baseDist + 1
                queue.push((nx, ny))
        return distances

    # Tạo ra 1 distMap từ Pacman đến mọi nơi
    distMap = computeMazeDistances(pacmanPos)

    # Hàm con để trả về khoảng cách từ Pacman đến 1 điểm
    def mazeDistance(toPos):
        return distMap.get(toPos)

    # Hàm con để tìm khoảng cách nhỏ nhất từ Pacman đến một tập hợp các vị trí, bỏ qua những vị trí không thể tiếp cận được
    def minMazeDistance(positions):
        if not positions:
            return None
        distances = [mazeDistance(pos) for pos in positions if mazeDistance(pos) is not None]
        return min(distances) if distances else None

    # Bắt đầu với điểm số cơ bản của trạng thái hiện tại
    score = currentGameState.getScore()

    # Tìm khoảng cách thực tế đến thức ăn gần nhất
    minFoodDist = minMazeDistance(foodList)
    # Thưởng lớn cho việc di chuyển gần thức ăn và phạt nặng thức ăn còn thừa để Pacman di chuyển tối ưu hơn
    if minFoodDist is not None:
        score += 3.0 / (minFoodDist + 1)
        score -= 4.0 * len(foodList)

    # Tìm khoảng cách thực tế đến viên năng lượng gần nhất
    minCapsuleDist = minMazeDistance(capsules)
    # Ưu tiên cao cho viên năng lượng nhưng không quá tham lam
    if minCapsuleDist is not None:
        score += 2.0 / (minCapsuleDist + 1)
        score -= 20.0 * len(capsules)

    # Tạo mảng lưu khoảng cách đến các ma 
    activeGhostDists = []
    for ghostState in ghostStates:
        ghostPos = ghostState.getPosition()
        dist = mazeDistance(ghostPos)
        # Nếu ma này không thể tiếp cận được thì bỏ qua nó, tránh việc đánh giá sai do khoảng cách vô hạn hoặc không xác định
        if dist is None:
            continue
        # Ưu tiên đuổi ma đang sợ hãi
        if ghostState.scaredTimer > 0:
            score += 8.0 / (dist + 1)
        else:
            # Trừ điểm trên tất cả ma đang hoạt động để đo lường áp lực
            activeGhostDists.append(dist)
            score -= 3.0 / (dist + 0.5)
            # Nếu dưới 2 bước trừ cực nặng
            if dist <= 2:
                score -= 60.0 * (3 - dist)

    # Trừ điểm mạnh dựa trên con ma gần nhất để ưu tiên sinh tồn là tuyệt đối
    if activeGhostDists:
        minActiveDist = min(activeGhostDists)
        score -= 12.0 / (minActiveDist + 0.1)

    # Lây danh sách các hướng Pacman có thể di chuyển trừ STOP
    legalMoves = currentGameState.getLegalActions(0)
    movable = [action for action in legalMoves if action != Directions.STOP]
    mobility = len(movable)
    # Chui vào ngõ cụt phạt nặng
    if mobility <= 1:
        score -= 25.0
    # Hành lang hẹp không có ngã rẽ phạt nhẹ hơn
    elif mobility == 2:
        score -= 8.0

    # Khi bị truy đuổi thì không được đi vào ngõ cụt
    if activeGhostDists and min(activeGhostDists) <= 4 and mobility <= 2:
        score -= 40.0

    return score

# Abbreviation
better = betterEvaluationFunction
riskAware = riskAwareEvaluationFunction