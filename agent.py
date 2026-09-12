from logic_engine import KnowledgeBase
from collections import deque
import heapq
import math
import random


# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

        self.kb = KnowledgeBase()

        self.kb.tell_rule(
         ['TargetVisible', 'HasDust'],
          'SafeToEngage'
        )

        self.kb.tell_rule(
         ['SafeToEngage', 'BloodseekerMissing'],
         'Retreat'
        )

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)


class SearchAgent:

    def __init__(self):
        self.plan = []
        self.active_algo = "AStar"

        self.kb = KnowledgeBase()

        self.kb.tell_rule(
            ['TargetVisible', 'HasDust'],
            'SafeToEngage'
        )

        self.kb.tell_rule(
            ['SafeToEngage', 'BloodseekerMissing'],
             'Retreat'
        )

    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        return math.sqrt(
            (pos[0] - goal[0]) ** 2 +
            (pos[1] - goal[1]) ** 2
        )

    def find_closest_food(self, start, food_list):

        if not food_list:
            return None

        return min(
            food_list,
            key=lambda food:
            abs(food[0] - start[0]) +
            abs(food[1] - start[1])
        )

    def sense_and_act(self, percept):

        if not self.plan:

            start = tuple(percept["agent_pos"])

            foods = percept["all_food"]

            if not foods:
                return "Up"

            goal = self.find_closest_food(
                start,
                foods
            )

            width, height = percept["grid_size"]

            walls = set(
                percept["walls"]
            )
            walls.update(percept.get("toxic_traps", []))

            if self.active_algo == "AStar":

                self.plan = self.astar_search(
                    start,
                    goal,
                    walls,
                    (width, height)
                )

        if self.plan:
            return self.plan.pop(0)

        return "Up"

    def astar_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size,
        heuristic_type="manhattan"
    ):

        width, height = grid_size

        frontier = []

        g_cost = 0

        h_cost = self.manhattan_distance(
            start_pos,
            goal_pos
         )

        f_cost = g_cost + h_cost

        heapq.heappush(
            frontier,
            (f_cost, g_cost, start_pos, [])
        )

        reached_states = set()

        while frontier:

            f_cost, g_cost, current_pos, path = heapq.heappop(frontier)

            if current_pos == goal_pos:
                return path

            if current_pos in reached_states:
                continue

            reached_states.add(current_pos)

            x, y = current_pos

            neighbors = [
                ((x, y + 1), "Up"),
                ((x, y - 1), "Down"),
                ((x - 1, y), "Left"),
                ((x + 1, y), "Right")
            ]

            for next_pos, action in neighbors:

                nx, ny = next_pos

                if (
                    0 <= nx < width and
                    0 <= ny < height and
                    next_pos not in walls and
                    next_pos not in reached_states
                ):

                    # Clear previous facts
                    self.kb.clear_facts()

                    # Example percepts
                    # Add real percepts later if the game provides them

                    self.kb.forward_chain()

                    # Skip infeasible nodes
                    if 'Retreat' in self.kb.facts:
                        continue

                    new_g = g_cost + 1

                    new_h = self.manhattan_distance(
                        next_pos,
                        goal_pos
                    )

                    new_f = new_g + new_h

                    heapq.heappush(
                        frontier,
                        (
                            new_f,
                            new_g,
                            next_pos,
                            path + [action]
                        )
                    )

        return []


if __name__ == '__main__':
    search_agent = SearchAgent()
    print("Manhattan:", search_agent.manhattan_distance((0, 0), (3, 4)))
    print("Euclidean:", search_agent.euclidean_distance((0, 0), (3, 4)))