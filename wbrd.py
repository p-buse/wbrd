from collections import deque
class Node(object):
    def __init__(self, state):
        self.state = state
        self.explored = False

    def __repr__(self):
        return "Node: " + self.state + " | Explored: " + str(self.explored)

class Board(object):
    def __init__(self, width, height):
        self.board = [[Node('x') for x in range(width)] for x in range(height)]
        self.width = width
        self.height = height

    def __init__(self, filename):
        self.board = []
        self.width = 0
        self.height = 0
        with open(filename, 'r') as board_file:
            for row in board_file:
                if len(row) > self.width:
                    self.width = len(row)
                self.board.append([Node(char) for char in row.strip()])
                self.height += 1

    def __str__(self):
        board_str = ''
        for row in self.board:
            for node in row:
               board_str += node.state
            board_str += "\n"
        return board_str

    def __getitem__(self, coords):
        x, y = coords
        return self.board[y][x]

    def __setitem__(self, coords, data):
        x, y = coords
        self.board[y][x] = data

    """ Returns a list of indices of neighbors of a node in our board 
        Keyword arguments:
        filt -- a function that takes a Node as a single parameter and returns True or False
        """
    def get_neighbors(self, x, y, filt=None):
        L = []
        # define a list for North, South, East, West
        for neighbor_x, neighbor_y in [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]:
            if neighbor_x >= 0 and neighbor_x < self.width and neighbor_y >= 0 and neighbor_y < self.height:
                if filt and filt(self[neighbor_x, neighbor_y]):
                        L.append((neighbor_x, neighbor_y))
                elif not filt:
                    L.append((neighbor_x, neighbor_y))
        return L

    def is_edge(self, x, y):
        return x == 0 or y == 0 or x == self.width-1 or y == self.height-1

    def test_closed(self, x, y, filt=None):
        seen_list = []
        work_queue = deque()
        is_open = False
        work_queue.append((x, y))
        seen_list.append((x, y))
        while work_queue:
            curnode_x, curnode_y = work_queue.popleft()
            for neighbor_x, neighbor_y in self.get_neighbors(curnode_x, curnode_y, filt):
                seen_list.append((neighbor_x, neighbor_y))
                if self.is_edge(neighbor_x, neighbor_y):
                    print("Found edge of the board!")
                    self.set_to(seen_list, 'S')
                    return
                work_queue.append((neighbor_x, neighbor_y))
        print("Didn't find edge of the board.")

    """ Sets a list of indices of nodes in the board to be a particular state"""
    def set_to(self, nodes, state):
        for node_x, node_y in nodes:
            self[node_x, node_y].state = state

def main():
    board = Board('board.brd')
    print(board)
    board.test_closed(7, 5, lambda x: x.state != 'A')
    print(board)

main()
