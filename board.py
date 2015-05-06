import pygame
from vector2 import Vector2
from pygame.locals import *
from collections import deque
class Node(object):
    def __init__(self, char):
        self.char = char
        self.explored = False
        self.captured = False

    def __repr__(self):
        return "Node: " + self.char + " | Explored: " + str(self.explored)

class Board(object):
    wall_char = 'A'
    empty_char = 'x'
    trail_char = 't'
    captured_char = 'C'
    colors = { wall_char: Color('black'), empty_char: Color('White'), trail_char: Color('green'), captured_char: Color('pink')}
    def __init__(self, filename, player_list):
        self.board = []
        self.width = 0
        self.height = 0
        self.player_list = player_list
        with open(filename, 'r') as board_file:
            for row in board_file:
                row = row.strip()
                if len(row) > self.width:
                    self.width = len(row)
                if len(row) > 0:
                    self.board.append([Node(char) for char in row.strip()])
                    self.height += 1


        # Quick n dirty way to make sure players aren't on top of one another
        for i in range(len(self.player_list)):
            player_list[i].pos = Vector2(player_list[i].pos.x + i, player_list[i].pos.y)

    def __str__(self):
        board_str = ''
        for row in self.board:
            for node in row:
               board_str += node.char
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
        coords -- a coordinate to get neighbors of
        filt -- a function that takes a Node as a single parameter and returns True or False
        """
    def _get_neighbors(self, coords, filt, eightway=False):
        L = []
        x, y = coords
        # define a list for North, South, East, West
        if not eightway:
            neighbor_list = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
        else:
            neighbor_list = [(x, y+1), (x, y-1), (x+1, y), (x+1, y+1), (x+1, y-1), (x-1, y), (x-1, y+1), (x-1, y-1)]
        for neighbor_x, neighbor_y in neighbor_list:
            if neighbor_x >= 0 and neighbor_x < self.width and neighbor_y >= 0 and neighbor_y < self.height:
                if filt(self[neighbor_x, neighbor_y]):
                    L.append((neighbor_x, neighbor_y))
        return L

    """ Returns True or False depending on whether the coordinates are on the edge of the board"""
    def _is_edge(self, coords):
        x, y = coords
        return x == 0 or y == 0 or x == self.width-1 or y == self.height-1

    """ Sets all nodes on the board as Unexplored """
    def _set_all_unexplored(self):
        for y in range(self.height):
            for x in range(self.width):
                self[x, y].explored = False

    """ Does a BFS at a point in the board.
        @param coords - the coordinates of the starting position of the BFS
        @param filt - a boolean function that takes a Node as its single parameter for filtering finding neighbors
        @return a tuple (is_open, seen_list) of whether the point is open, and coordinates of points that are accessible from the starting coordinate"""
    def _check_open(self, coords, filt):
        self._set_all_unexplored()
        seen_set = set()
        work_queue = deque()
        is_open = False
        work_queue.append(coords)
        while work_queue:
            curnode_coords = work_queue.popleft()  # pop current node off our queue
            self[curnode_coords].explored = True  # set node as explored
            seen_set.add(curnode_coords)   # add it to our seen list
            if self._is_edge(curnode_coords):   #if it's an edge, we know the entire area is open
                return True, set()
            for neighbor_coords in self._get_neighbors(curnode_coords, filt):  # add our (filtered) neighbors to the queue
                if neighbor_coords not in work_queue:
                    work_queue.append(neighbor_coords)
        return is_open, seen_set

    """ Sets a list of coords of nodes in the board to be a particular state"""
    def _set_to(self, coords_list, char, captured=True):
        for node_x, node_y in coords_list:
            self[node_x, node_y].char = char
            self[node_x, node_y].captured = captured

    def _move_players(self):
        # set intended position, colliding against walls.
        for player_index in range(len(self.player_list)):
            intended_x, intended_y = self.player_list[player_index].intended_pos
            # clamp intended position to be on our board
            intended_x = max(0, min(intended_x, self.width - 1))
            intended_y = max(0, min(intended_y, self.height - 1))
            self.player_list[player_index].intended_pos = Vector2(intended_x, intended_y)
            # collide against walls
            if self[intended_x, intended_y].char == Board.wall_char:
                self.player_list[player_index].intended_pos = self.player_list[player_index].pos

        # make players bump against each other
        collision_set = set()
        for player_index, player in enumerate(self.player_list):
            for other_index, other_player in enumerate(self.player_list):
                if other_player.intended_pos == player.intended_pos and player_index != other_index:
                    collision_set.add(player_index)
                    collision_set.add(other_index)
        # bump the ones who would collide
        for i in collision_set:
            self.player_list[i].intended_pos = self.player_list[i].pos

        # actually move the players
        for player in self.player_list:
            if not self[player.pos].captured:
                self[player.pos].char = Board.trail_char  # write trail where player was
            player.pos = player.intended_pos

    def _search_filt(self, node):
        return node.char == Board.empty_char and not node.explored and not node.captured

    def process_input(self, pressed_keys):
        for player in self.player_list:
            player.process_input(pressed_keys)

    def update(self):
        self._move_players()
        for player in self.player_list:
            self._set_all_unexplored()
            for neighbor_pos in self._get_neighbors(player.pos, self._search_filt, True):
                is_open, seen_coords = self._check_open(neighbor_pos, self._search_filt)
                if not is_open:
                    self._set_to(seen_coords, player.char)

    def render(self, screen, pixel_size):
        # draw our walls and empty spaces
        for y in range(self.height):
            for x in range(self.width):
                char = self[x, y].char
                draw_color = Color('Black') # default color
                if char in Board.colors:
                    draw_color = Board.colors[char]
                else:
                    for player in self.player_list:
                        if char == player.char:
                            draw_color = player.color.correct_gamma(0.5)
                            break
                screen.fill(draw_color, Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size))
        for player in self.player_list:
            screen.fill(player.color, Rect(player.pos.x * pixel_size, player.pos.y * pixel_size, pixel_size, pixel_size))
