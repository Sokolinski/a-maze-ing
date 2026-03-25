from maze import DIRECTIONS, OFFSETS, OPPOSITE, Maze
from random import Random


class MazeGenerator():
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def generate(self) -> None:
        self._backtrac_genetation(*self.maze.entry)

    def _backtrac_genetation(self, x: int, y: int) -> None:
        cell = self.maze.get_cell(x, y)
        cell.visited = True

        directions = list(DIRECTIONS)
        Random.shuffle(directions)

        for direction in directions:
            dx, dy = OFFSETS[direction]
            nx, ny = x + dx, y + dy

            if not self.maze.in_bounds(nx, ny):
                continue

            neighbor = self.maze.get_cell(nx, ny)
            if neighbor.visited:
                continue

            cell.walls[direction] = False
            neighbor.walls[OPPOSITE[direction]] = False
            self._backtrac_genetation(nx, ny)
