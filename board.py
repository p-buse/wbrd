import pygame
from pygame.locals import *
from collections import deque
class Node(object):
    def __init__(self, state):
        self.state = state
        self.explored = False

    def __repr__(self):
        return "Node: " + self.state + " | Explored: " + str(self.explored)

class Board(object):
    wall_char = 'A'
    empty_char = 'x'
    wall_color = Color('Green')
    empty_color = Color('White')
    def __init__(self, filename, player_list):
        self.board = []
        self.width = 0
        self.height = 0
        self.player_list = player_list
        with open(filename, 'r') as board_file:
            for row in board_file:
                if len(row) > self.width:
                    self.width = len(row)
                self.board.append([Node(char) for char in row.strip()])
                self.height += 1


        # Quick n dirty way to make sure players aren't on top of one another
        for i in range(len(self.player_list)):
            player_list[i].pos[0] += i

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
    def get_neighbors(self, coords, filt=None):
        L = []
        x, y = coords
        # define a list for North, South, East, West
        for neighbor_x, neighbor_y in [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]:
            if neighbor_x >= 0 and neighbor_x < self.width and neighbor_y >= 0 and neighbor_y < self.height:
                if filt and filt(self[neighbor_x, neighbor_y]):
                    L.append((neighbor_x, neighbor_y))
                elif filt is None:
                    L.append((neighbor_x, neighbor_y))
        return L

    """ Returns True or False depending on whether the coordinates are on the edge of the board"""
    def is_edge(self, coords):
        x, y = coords
        return x == 0 or y == 0 or x == self.width-1 or y == self.height-1

    """ Returns a flat list of nodes in the board
        Syntax from: http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    """
    def __iter__(self):
        return iter([item for sublist in self.board for item in sublist])

    """ Sets all nodes on the board as Unexplored """
    def set_all_unexplored(self):
        for node in self:
            node.explored = False

    """ Does a BFS at a point in the board.
        If it finds the edge, sets all nodes in the area to open_char.
        Otherwise, sets all nodes in the area to closed_char
        @param coords - the coordinates of the starting position of the BFS
        @param filt - a boolean function that takes a Node as its single parameter to be used for traversing the graph
        @return void"""
    def test_closed(self, coords, filt, open_char, closed_char):
        # If we filter the starting coordinates, do nothing
        if not filt(self[coords]):
            return
        seen_list = []
        work_queue = deque()
        is_open = False
        work_queue.append(coords)
        while work_queue:
            curnode_coords = work_queue.popleft()  # pop current node off our queue
            self[curnode_coords].explored = True  # set node as explored
            seen_list.append(curnode_coords)   # add it to our seen list
            if self.is_edge(curnode_coords):   #if it's an edge, we know the entire area is open
                is_open = True
            for neighbor_coords in self.get_neighbors(curnode_coords, filt):  # add our (filtered) neighbors to the queue
                work_queue.append(neighbor_coords)
        if is_open:
            self.set_to(seen_list, open_char)
            print("Found edge of the board!")
        else:
            self.set_to(seen_list, closed_char)
            print("Didn't find edge of the board.")

    """ Sets a list of coords of nodes in the board to be a particular state"""
    def set_to(self, coords_list, state):
        for node_x, node_y in coords_list:
            self[node_x, node_y].state = state

    def move_players(self):
        # set intended position, colliding against walls.
        for player in self.player_list:
            player.intended_pos = [item1 + item2 for item1, item2 in zip(player.pos, player.velocity)]
            # clamp intended position to be on our board
            player.intended_pos[0] = max(0, min(player.intended_pos[0], self.width - 1))
            player.intended_pos[1] = max(0, min(player.intended_pos[1], self.height - 1))
            # collide against walls
            if self[tuple(player.intended_pos)] == Board.wall_char:
                player.intended_pos = player.pos

        # make players bump against each other
        collision_list = []
        for player_index, player in enumerate(self.player_list):
            for other_index, other_player in enumerate(self.player_list):
                if other_player.intended_pos == player.intended_pos and player_index != other_index:
                    collision_list.append(other_index)

        # bump the ones who would collide
        for i in collision_list:
            self.player_list[i].intended_position = self.player_list[i].pos

        # actually move the players
        for player in self.player_list:
            self[tuple(player.pos)].state = Board.wall_char # write wall where player was
            player.pos = player.intended_pos
            self[tuple(player.pos)].state = player.char

    def process_input(self, pressed_keys):
        for player in self.player_list:
            player.process_input(pressed_keys)

    def update(self):
        self.move_players()

    def render(self, screen, pixel_size):
        # draw our walls and empty spaces
        for row in range(self.height - 1):
            for col in range(self.width - 1):
                if self[col, row].state == Board.wall_char:
                    draw_color = Board.wall_color
                elif self[col, row].state == Board.empty_char:
                    draw_color = Board.empty_color
                else:
                    draw_color = Color('Black')
                pygame.draw.rect(screen, draw_color, Rect(col * pixel_size, row * pixel_size, pixel_size, pixel_size))
        # draw our players
        for player in self.player_list:
            pygame.draw.rect(screen, player.color, Rect(player.pos[0] * pixel_size, player.pos[1] * pixel_size, pixel_size, pixel_size))
        print(self)

if __name__ == "__main__":
    board = Board('test_board.brd')
    print(board)
    board.test_closed((3, 9), lambda x: x.state != Board.wall_char and not x.explored, 'O', 'C')
    print(board)
