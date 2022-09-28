# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Kelvin Ma (kelvinm2@illinois.edu) on 01/24/2021

"""
This is the main entry point for MP3. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)


# Feel free to use the code below as you wish
# Initialize it with a list/tuple of objectives
# Call compute_mst_weight to get the weight of the MST with those objectives
# TODO: hint, you probably want to cache the MST value for sets of objectives you've already computed...
# Note that if you want to test one of your search methods, please make sure to return a blank list
#  for the other search methods otherwise the grader will not crash.
from asyncio import queues
from calendar import c
import heapq


class MST:
    def __init__(self, objectives):
        self.elements = {key: None for key in objectives}

        # TODO: implement some distance between two objectives
        # ... either compute the shortest path between them, or just use the manhattan distance between the objectives
        def DISTANCE(i, j):
            return abs(i[0] - j[0]) + abs(i[1] - j[1])
        self.distances   = {
                (i, j): DISTANCE(i, j)
                for i, j in self.cross(objectives)
            }

    # Prim's algorithm adds edges to the MST in sorted order as long as they don't create a cycle
    def compute_mst_weight(self, dict):
        if tuple(self.elements) in dict.keys():
            return dict.get(tuple(self.elements))
        weight      = 0
        for distance, i, j in sorted((self.distances[(i, j)], i, j) for (i, j) in self.distances):
            if self.unify(i, j):
                weight += distance
        dict[tuple(self.elements)] = weight       
        return weight

    # helper checks the root of a node, in the process flatten the path to the root
    def resolve(self, key):
        path = []
        root = key
        while self.elements[root] is not None:
            path.append(root)
            root = self.elements[root]
        for key in path:
            self.elements[key] = root
        return root

    # helper checks if the two elements have the same root they are part of the same tree
    # otherwise set the root of one to the other, connecting the trees
    def unify(self, a, b):
        ra = self.resolve(a)
        rb = self.resolve(b)
        if ra == rb:
            return False
        else:
            self.elements[rb] = ra
            return True

    # helper that gets all pairs i,j for a list of keys
    def cross(self, keys):
        return (x for y in (((i, j) for j in keys if i < j) for i in keys) for x in y)

def bfs(maze):

    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    queue = [maze.start]
    graph = {}
    explored = []
    path = []
    good = []
    output = 0
    while(queue):
        if queue[0] == maze.waypoints[0]:
            output = queue[0]
            break
        else:
            if queue[0] not in explored:
                for element in maze.neighbors(queue[0][0], queue[0][1]):
                    if maze.navigable(element[0],element[1]):
                        good.append(element)
                        queue.append(element)
                graph.update({queue[0]: good})
                good = []    
                explored.append(queue[0])
            queue.pop(0)
    
    while(output != maze.start):
        path.insert(0, output)
        for key in graph.keys():
            if output in graph.get(key):
                output = key
                break
    path.insert(0, output)            
    return path

                   

def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    queue = [[maze.start,0]]
    graph = {}
    explored = []
    path = []
    good = []
    output = 0
    waypoints = maze.waypoints[0]
    while(queue):
        #print(queue)
        if queue[0][0] == maze.waypoints[0]:
            output = queue[0][0]
            break
        else:
            if queue[0][0] not in explored:
                mark = queue[0]
                queue.pop(0)
                for element in maze.neighbors(mark[0][0], mark[0][1]):
                    if maze.navigable(element[0],element[1]) and element not in explored:
                        good.append(element)
                        for count in range(len(queue) + 1):
                            if count == len(queue):
                                queue.append([element,mark[1]+1])
                                break
                            if((abs(waypoints[0] - element[0]) + abs(waypoints[1] - element[1]))+ mark[1]+1) < (abs(waypoints[0] - queue[count][0][0]) + abs(waypoints[1] - queue[count][0][1])+queue[count][1]):
                                queue.insert(count, [element, mark[1]+1])
                                break    
                graph.update({mark[0]: good})      
                good = []    
                explored.append(mark[0])
            else:
                queue.pop(0)
        #print(queue)
    while(output != maze.start):
        path.insert(0, output)
        for key in graph.keys():
            if output in graph.get(key):
                output = key
                break
    path.insert(0, output)        
    return path

    

def astar_multiple(maze):
    def nearest(cur, waypoints):
        min_dis = 999
        for point in waypoints:
            dis = abs(cur[0] - point[0]) +abs(cur[1] -point[1])
            if dis < min_dis:
                min_dis = dis         
        return min_dis


    if len(maze.waypoints) < 10:
        dict1 = {}
        waypoints =  maze.waypoints
        start_way = waypoints
        queue = [(nearest(maze.start, waypoints)+MST(waypoints).compute_mst_weight(dict1),waypoints,0,maze.start)]
        heapq.heapify(queue)
        # print(mst.elements)
        # print(mst.distances)
        # print(mst.compute_mst_weight())
        explored = []
        output = []
        graph={}
        path = []
        while(queue): #queue is stiil not full
            #print(queue)
            #print()
            mark = heapq.heappop(queue)# choose best one
            waypoints = mark[1]
            if (mark[1],mark[3]) in explored:
                continue
            explored.append((mark[1],mark[3]))
            if mark[3] in waypoints:
                waypoints = list(waypoints)
                waypoints.remove(mark[3])
                waypoints = tuple(waypoints)
                output = mark
                if not waypoints: # if reach all waypoints
                    break
                
            
            good = []
            for element in maze.neighbors(mark[3][0], mark[3][1]):
                    if maze.navigable(element[0],element[1]):
                        
                        dis = nearest(element,waypoints)+MST(waypoints).compute_mst_weight(dict1)
                        new = (dis+mark[2]+1,waypoints,mark[2]+1,element)
                        heapq.heappush(queue, new)
                        good.append(new)
                                                
            graph.update({mark: good})
        
        
        path.append(output)
        real_path = [output[3]]
        req =  (nearest(maze.start,start_way)+MST(start_way).compute_mst_weight(dict1),start_way, 0,maze.start) 
        while(req not in path):
            for key in graph.keys():
                if  output in graph.get(key):
                    path.append(key)
                    real_path.insert(0,key[3])
                    output = key
                    break
        return real_path
    else:
        waypoints =  list(maze.waypoints)
        start_len = len(waypoints)
        queue = [[maze.start,start_len,0,0]]
        # print(mst.elements)
        # print(mst.distances)
        # print(mst.compute_mst_weight())
        explored = []
        output = []
        graph={}
        path = []
        pre_node = [maze.start,start_len]
        print(pre_node)
        while(queue): #queue is stiil not full
            #print(queue)
            #print()
            mark = queue[0] # choose best one
            queue.pop(0)    #del 
            if mark[1] > len(waypoints) : #or (abs(mark[0][0]-pre_node[0][0]) + abs(mark[0][1]-pre_node[0][1]) > 1)
                continue
            if [mark[0],mark[1]] in explored:
                continue
            explored.append([mark[0],mark[1]])

            if mark[0] in waypoints:
                waypoints.remove(mark[0])
                output = tuple([mark[0],mark[1]])
                if not waypoints: # if reach all waypoints
                    break
                
            
            good = []
            for element in maze.neighbors(mark[0][0], mark[0][1]):
                    if maze.navigable(element[0],element[1]) and [element, len(waypoints)] not in explored:
                        good.append([element,len(waypoints)])
                        dis = nearest(element,waypoints)
                        for i in range(len(queue) + 1):   
                            if i == len(queue):
                                queue.append([element,len(waypoints),mark[2]+1,dis])
                                break
                            if dis+mark[2] + 1 <= queue[i][2] + queue[i][3]:
                                queue.insert(i,[element,len(waypoints),mark[2]+1,dis])
                                break
            graph.update({tuple([mark[0],mark[1]]): good})
            pre_node = tuple([mark[0],mark[1]])
        # for i in graph.keys():
        #     print(i, graph.get(i))  
        # print(output)
        path.append(output)
        real_path = [output[0]]
        while((maze.start,start_len) not in path):
            for key in graph.keys():
                if list(output) in graph.get(key):
                    path.append(key)
                    real_path.insert(0,key[0])
                    output = key
                    break
        print(real_path)
        return real_path

   

def fast(maze):
    """
    Runs suboptimal search algorithm for extra credit/part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    return astar_single(maze)

