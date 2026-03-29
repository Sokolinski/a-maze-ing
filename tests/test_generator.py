import os
import sys
import unittest


CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


def build_generator(width: int, height: int, entry: tuple[int, int], exit_: tuple[int, int]):
    from generator import MazeGenerator
    from maze import Maze

    maze = Maze(width=width, height=height, entry=entry, exit_=exit_)
    return maze, MazeGenerator(maze)


def render_ascii_maze(maze) -> str:
    lines = ["+" + "---+" * maze.width]

    for y in range(maze.height):
        middle = "|"
        bottom = "+"

        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            middle += "   "
            middle += "|" if cell.walls["RIGHT"] else " "
            bottom += "---+" if cell.walls["BOT"] else "   +"

        lines.append(middle)
        lines.append(bottom)

    return "\n".join(lines)


class TestMazeGenerator(unittest.TestCase):
    def test_generate_marks_all_cells_visited(self) -> None:
        maze, generator = build_generator(6, 4, (0, 0), (5, 3))

        generator.generate()

        for row in maze.grid:
            for cell in row:
                self.assertTrue(cell.visited)

    def test_generate_opens_exactly_n_minus_1_passages(self) -> None:
        maze, generator = build_generator(5, 3, (2, 1), (4, 2))

        generator.generate()

        opened_wall_count = 0
        for row in maze.grid:
            for cell in row:
                opened_wall_count += sum(
                    not is_closed for is_closed in cell.walls.values())

        # Each passage is represented by two opened walls (one on each side).
        passage_count = opened_wall_count // 2
        cell_count = maze.width * maze.height
        self.assertEqual(passage_count, cell_count - 1)

    def test_open_walls_are_reciprocal_between_neighbors(self) -> None:
        maze, generator = build_generator(4, 4, (1, 1), (3, 3))

        generator.generate()

        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)

                if x + 1 < maze.width:
                    right_neighbor = maze.get_cell(x + 1, y)
                    self.assertEqual(
                        cell.walls["RIGHT"], right_neighbor.walls["LEFT"])

                if y + 1 < maze.height:
                    bottom_neighbor = maze.get_cell(x, y + 1)
                    self.assertEqual(
                        cell.walls["BOT"], bottom_neighbor.walls["TOP"])

    def test_generate_single_cell_maze(self) -> None:
        maze, generator = build_generator(1, 1, (0, 0), (0, 0))

        generator.generate()

        only_cell = maze.get_cell(0, 0)
        self.assertTrue(only_cell.visited)
        self.assertTrue(all(only_cell.walls.values()))

    def test_print_maze_output_for_visual_check(self) -> None:
        maze, generator = build_generator(12, 6, (0, 0), (11, 5))

        generator.generate()

        maze_view = render_ascii_maze(maze)
        print("\nGenerated maze preview:\n")
        print(maze_view)

        self.assertIn("+", maze_view)
        self.assertIn("|", maze_view)


if __name__ == "__main__":
    unittest.main()
