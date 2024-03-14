import pygame
import numpy as np
from scipy.spatial import KDTree
import heapq


# PRM Planner
class PRMPlanner:
    def __init__(self, num_samples, num_neighbors, step_size):
        self.num_samples = num_samples
        self.num_neighbors = num_neighbors
        self.step_size = step_size
        self.samples = []
        self.edges = []
        self.start = None
        self.goal = None
        self.obstacles = []
        self.kd_tree = None
        self.graph = []
        

    def sample_configuration(self):
        return np.random.rand(2) * np.array([WIDTH, HEIGHT])
    
    def build_kd_tree(self):
        self.kd_tree = KDTree(self.samples)

    def find_neighbors(self, q):
        distances, indices = self.kd_tree.query(q, self.num_neighbors)
        return [self.samples[i] for i in indices]

    def local_planner(self, q1, q2):
        delta = q2 - q1
        distance = np.linalg.norm(delta)
        steps = int(distance / self.step_size)
        self.graph.extend([[q1, q2, steps]])
        if steps == 0:
            return [q1, q2]
        else:
            return [q1 + i * delta / steps for i in range(1, steps + 1)]
    
    
    def dijkstra_search(self, graph, start, goal):
        queue = [(0, start, [])]
        visited = set()
        while queue:
            cost, current, path = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)
            path = path + [current]           
            if current == goal:
                return path
            for neighbor, edge_cost in graph.get(current, {}).items():
                heapq.heappush(queue, (cost + edge_cost, neighbor, path))
        return None
                
            
    def plan_sample(self):
        self.samples = [self.sample_configuration() for _ in range(self.num_samples)]
        self.build_kd_tree()
        return self.samples
    

    def plan_edges(self, start, goal, samples):       
        self.edges = []
        self.build_kd_tree()

        for s in samples:
            neighbors = self.find_neighbors(s)

            for neighbor in neighbors:
                path = self.local_planner(s, neighbor)
                self.edges.extend([(path[i], path[i + 1]) for i in range(len(path) - 1)])
        
        self.edges.extend([(start, neighbor) for neighbor in self.find_neighbors(start)])
        self.edges.extend([(goal, neighbor) for neighbor in self.find_neighbors(goal)])
        
        return self.edges



pygame.init()

initial = False
final = False
I = None
F = None
sample = [] 
edges = []
graph = []
optimal_path = []

WIDTH, HEIGHT = 1280, 720
green = (0, 255, 0)
blue = (0, 0, 128)
dark_gray = (50, 50, 50)
blue_gray = [115, 147, 179]
light_gray = [127, 127, 127]
font = pygame.font.Font('freesansbold.ttf', 10)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

#flags
i_flag = False
f_flag = False
s_flag = False


def disp_cord(x,y):
    text = font.render("X="+str(int(x))+"  "+"Y="+str(int(y)), True, green, blue)
    textRect = text.get_rect()
    textRect.center = (1200, 30)
    screen.blit(text, textRect)


# Set the initial parameters for PRM
prm = PRMPlanner(num_samples=2000, num_neighbors=8, step_size=2)
sample = prm.plan_sample()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                print("Select initial coordinates")
                initial = True
                selected_coordinates = None   
            if event.key == pygame.K_f:
                print("Select final coordinates")
                final = True
                selected_coordinates = None
            if event.key == pygame.K_RETURN:
                print("start")
                s_flag=True

        if event.type == pygame.MOUSEBUTTONDOWN:
                if initial:
                    I = pygame.mouse.get_pos()
                    initial = False
                    i_flag = True
                    print("Initial coordinates",I)
                if final:
                    F = pygame.mouse.get_pos()
                    final = False
                    f_flag = True
                    print("Final coordinates",F)
                            
    
    screen.fill(dark_gray) 

    #display mouse pointer coordinates
    mx,my=pygame.mouse.get_pos()
    disp_cord(mx,my)
    
    if i_flag:
        pygame.draw.rect(screen, blue ,pygame.Rect(I[0]-10,I[1]-10, 20, 20))
    if f_flag:
        pygame.draw.rect(screen, "red",pygame.Rect(F[0]-10,F[1]-10, 20, 20))
    if s_flag:
        start_config = np.array([I[0], I[1]])
        goal_config = np.array([F[0], F[1]])
        edges = prm.plan_edges(start_config, goal_config, sample)
        graph = {}
        for edge in edges:
            if tuple(edge[0]) not in graph:
                graph[tuple(edge[0])] = {}
            if tuple(edge[1]) not in graph:
                graph[tuple(edge[1])] = {}
            graph[tuple(edge[0])][tuple(edge[1])] = np.linalg.norm(np.array(edge[0]) - np.array(edge[1]))
            graph[tuple(edge[1])][tuple(edge[0])] = np.linalg.norm(np.array(edge[0]) - np.array(edge[1]))

        optimal_path = prm.dijkstra_search(graph, tuple(start_config.astype(int)), tuple(goal_config.astype(int)))
        s_flag= False
        

    if optimal_path:
        pygame.draw.lines(screen, "green", False, optimal_path, 5)
    elif optimal_path == None:
        print("No path found")
      
    #Draw nodes
    for s in sample:
        pygame.draw.circle(screen, light_gray, s.astype(int), 2, 1)

    # Draw edges
    for edge in edges:
        pygame.draw.line(screen, blue_gray, edge[0], edge[1], 1)
    

    pygame.display.flip()
    dt = clock.tick(60)/1000

pygame.quit()
