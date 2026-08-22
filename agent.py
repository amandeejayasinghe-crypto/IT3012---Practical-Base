# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

from collections import deque
import heapq


class SearchAgent:

    def __init__(self):
        self.plan = []
        self.active_algo = "BFS"

    def get_neighbors(self, state, width, height, walls):

        x, y = state

        moves = [
            ((x, y + 1), "Up"),
            ((x, y - 1), "Down"),
            ((x - 1, y), "Left"),
            ((x + 1, y), "Right")
        ]

        neighbors = []

        for pos, action in moves:
            nx, ny = pos

            if (
                0 <= nx < width and
                0 <= ny < height and
                pos not in walls
            ):
                neighbors.append((pos, action))

        return neighbors


    # ---------------- BFS ---------------- #
    def bfs_search(self, start, goal, width, height, walls):

        frontier = deque()
        frontier.append((start, []))

        reached = {start}

        while frontier:

            state, path = frontier.popleft()

            if state == goal:
                return path

            for next_state, action in self.get_neighbors(
                    state, width, height, walls):

                if next_state not in reached:
                    reached.add(next_state)
                    frontier.append(
                        (next_state, path + [action])
                    )

        return []


    # ---------------- DFS ---------------- #
    def dfs_search(self, start, goal, width, height, walls):

        frontier = [(start, [])]
        reached = {start}

        while frontier:

            state, path = frontier.pop()

            if state == goal:
                return path

            for next_state, action in self.get_neighbors(
                    state, width, height, walls):

                if next_state not in reached:
                    reached.add(next_state)
                    frontier.append(
                        (next_state, path + [action])
                    )

        return []


    # ---------------- UCS ---------------- #
    def ucs_search(self, start, goal, width, height, walls):

        frontier = []
        heapq.heappush(frontier, (0, start, []))

        reached = {}

        while frontier:

            cost, state, path = heapq.heappop(frontier)

            if state == goal:
                return path

            if state in reached and reached[state] <= cost:
                continue

            reached[state] = cost

            for next_state, action in self.get_neighbors(
                    state, width, height, walls):

                new_cost = cost + 1

                heapq.heappush(
                    frontier,
                    (
                        new_cost,
                        next_state,
                        path + [action]
                    )
                )

        return []


    def find_closest_food(self, start, food_list):

        if not food_list:
            return None

        closest = min(
            food_list,
            key=lambda food:
            abs(food[0] - start[0]) +
            abs(food[1] - start[1])
        )

        return closest


    def sense_and_act(self, percept):

        if not self.plan:

            start = tuple(percept["agent_pos"])

            food_list = percept["all_food"]

            if not food_list:
                return "Up"

            goal = self.find_closest_food(start, food_list)

            width, height = percept["grid_size"]
            walls = set(percept["walls"])

            if self.active_algo == "BFS":
                self.plan = self.bfs_search(
                    start, goal,
                    width, height,
                    walls
                )

            elif self.active_algo == "DFS":
                self.plan = self.dfs_search(
                    start, goal,
                    width, height,
                    walls
                )

            elif self.active_algo == "UCS":
                self.plan = self.ucs_search(
                    start, goal,
                    width, height,
                    walls
                )

        if self.plan:
            return self.plan.pop(0)

        return "Up"
    