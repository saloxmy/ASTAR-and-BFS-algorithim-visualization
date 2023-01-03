import pygame 
from queue import PriorityQueue
from collections import deque
import random


pygame.init()
WINDOW_WIDTH = 1000
WIDTH = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
pygame.display.set_caption("Finding Algorithms")

blackboard = pygame.rect.Rect(0, 570, 1000, 330)
font = pygame.font.Font('freesansbold.ttf', 36)
smallfont = pygame.font.Font('freesansbold.ttf', 20)
subfont = pygame.font.Font('freesansbold.ttf', 20)
text1 = font.render("A for A*", True, (255, 255, 255))
text2 = font.render("S for BFS", True, (255, 255, 255))
text3 = font.render("C to clear", True, (255, 255, 255))
text4 = font.render("R for random barrier", True, (255, 255, 255))
text5 = smallfont.render("Left click to place start, end", True, (255, 255, 255))
text6 = smallfont.render("and barrier tiles", True, (255, 255, 255))
text7 = smallfont.render("Right click to delete tiles", True, (255, 255, 255))



red = (255,0,0)
blue = (0,255,0)
yellow = (255,255,0)
white = (255,255,255)
orange =(205, 133, 0)
purple = (160, 50, 220)
black = (0,0,0)
green = (0,255,0)
aqua = (60,225,210)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width +200
        self.y = col * width
        self.color = white
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == red

    def is_open(self):
        return self.color == green

    def is_barrier(self):
        return self.color == black

    def is_start(self):
        return self.color == orange
        
    def is_end(self):
        return self.color == aqua
        
    def reset(self):
        self.color = white

    def make_closed(self):
        self.color = red

    def make_open(self):
        self.color = green

    def make_barrier(self):
        self.color = black

    def make_start(self):
        self.color = orange
        
    def make_end(self):
        self.color = aqua

    def make_path(self):
        self.color = purple

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows -1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col < self.total_rows -1 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def update_all_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1:
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0:
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows -1:
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col < self.total_rows -1:
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self,other):
        return False

def h(p1,p2):
    x1,y1 = p1
    x2, y2 = p2
    return abs(x1-x2) +abs(y1-y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current] 
        current.make_path()
        draw()

def clear_algo(grid, draw):
    for row in grid:
        for node in row:
            if node.is_open() or node.is_closed():
                node.reset()
        draw()
def remove_path(grid):
    for row in grid:
        for node in row:
            if node.color == purple:
                node.reset()
def generate_maze(draw, start, grid, visited):
    if start.color != orange and start.color != aqua:
        start.reset()
    visited.add(start)
    non_visited = []
    for neighbor in start.neighbors:
        if neighbor not in visited: 
            non_visited.append(neighbor)
    random.shuffle(non_visited)
    draw()
    if not(non_visited):
        return False
    generate_maze(draw,non_visited[0], grid, visited)

    

def BFS(draw, grid, start, end):
    remove_path(grid)
    queue = deque([start])
    visited = set()
    came_from = {}
    while len(queue) > 0:
        curr = queue.popleft()
        if curr == end:
            reconstruct_path(came_from, end, draw)
            clear_algo(grid, draw)
            curr.make_end()
            return True
        visited.add(curr)
        curr.make_open()
        for neighbor in curr.neighbors:
            neighbor.make_closed()
            if neighbor not in visited:
                queue.append(neighbor)
                came_from[neighbor] = curr 
        draw()
    return False

def a_star(draw, grid, start, end):
    remove_path(grid)
    cnt = 0
    open_set = PriorityQueue()
    open_set.put((0, cnt, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(),end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            clear_algo(grid, draw)
            end.make_end()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    cnt+=1
                    open_set.put((f_score[neighbor], cnt, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()
    return False
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows +1):
        pygame.draw.line(win, black, (200, i*gap), (width+200,i*gap))
        for j in range(rows +1):
            pygame.draw.line(win, black, (j*gap+200,0), (j*gap+200, width))

def draw(win,grid,rows,width):
    win.fill(white)
    
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win,rows,width)
    pygame.draw.rect(win, (0, 0, 0), blackboard)
    win.blit(text1, (100, 650))
    win.blit(text2, (100, 700))
    win.blit(text3, (100, 750))
    win.blit(text4, (100, 800))
    win.blit(text5, (600, 650))
    win.blit(text6, (600, 670))
    win.blit(text7, (600, 710))
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = (y-200) // gap
    col = x // gap
    return row,col 


def main(win, width):
    ROWS = 20
    grid = make_grid(ROWS, width)

    start = None
    end = None
    started = False
    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if 200 < pos[0] < 800 and 0 < pos[1] < 600:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col] 
                    if not start:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if 200 < pos[0] < 800 and 0 < pos[1] < 600:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None 

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r and not(started):
                    for row in grid:
                        for node in row:
                            if node != start and node != end:
                                node.make_barrier()
                        draw(win, grid, ROWS, width)
                    for row in grid:
                        for node in row:
                            node.update_all_neighbors(grid)
                    if start and end:
                        generate_maze(lambda: draw(win, grid, ROWS, width),start, grid, set())
                        generate_maze(lambda: draw(win, grid, ROWS, width), end, grid, set())
                        generate_maze(lambda: draw(win, grid, ROWS, width), grid[(start.row + end.row)//2][(start.col + end.col)//2], grid, set())
                    elif start:
                        generate_maze(lambda: draw(win, grid, ROWS, width),start, grid, set())
                        generate_maze(lambda: draw(win, grid, ROWS, width), grid[5][15], grid, set())
                        generate_maze(lambda: draw(win, grid, ROWS, width), grid[5][5], grid, set())
                    else:      
                        generate_maze(lambda: draw(win, grid, ROWS, width), grid[5][5], grid, set())
                        generate_maze(lambda: draw(win, grid, ROWS, width), grid[5][15], grid, set())
                        generate_maze(lambda: draw(win, grid, ROWS, width), grid[15][5], grid, set())
                if event.key == pygame.K_a and start and end:
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    started = False
                if event.key == pygame.K_s and start and end:
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    BFS(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    started = False
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(window, WIDTH)

