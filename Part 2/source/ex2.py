import random
import numpy as np

ids = ["207364332", "318881471"]

Infnity = float('inf')


class Graph:
    # example of adjacency list (or rather map)

    def __init__(self, adjacency_list, H):
        self.adjacency_list = adjacency_list
        self.H = H

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    # heuristic function with equal values for all nodes
    def h(self, n):
        return self.H[n]

    def a_star_algorithm(self, start_node, stop_node):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = set([start_node])
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start_node] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                if n == None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v

            if n == None:
                return -1

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == stop_node:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)

                reconst_path.reverse()

                return reconst_path

            # for all neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        return -1


def createAdjacencyList(Map):
    adjanciesLists = {}
    mapRowLimit = len(Map)
    mapColumnLimit = len(Map[0])

    for i in range(mapRowLimit):
        for j in range(mapColumnLimit):

            coordinateiIJ = (i, j)
            coordinateAdjancey = []
            if (i + 1 < mapRowLimit):
                if Map[i + 1][j] == 'I':
                    coordinateAdjancey.append(((i + 1, j), Infnity))
                else:
                    coordinateAdjancey.append(((i + 1, j), 1))
            if (j + 1 < mapColumnLimit):
                if Map[i][j + 1] == 'I':
                    coordinateAdjancey.append(((i, j + 1), Infnity))
                else:
                    coordinateAdjancey.append(((i, j + 1), 1))
            if (i > 0):
                if Map[i - 1][j] == 'I':
                    coordinateAdjancey.append(((i - 1, j), Infnity))
                else:
                    coordinateAdjancey.append(((i - 1, j), 1))
            if (j > 0):
                if Map[i][j - 1] == 'I':
                    coordinateAdjancey.append(((i, j - 1), Infnity))
                else:
                    coordinateAdjancey.append(((i, j - 1), 1))

            if (i + 1 < mapRowLimit and j + 1 < mapColumnLimit):
                if Map[i + 1][j + 1] == 'I':
                    coordinateAdjancey.append(((i + 1, j + 1), Infnity))
                else:
                    coordinateAdjancey.append(((i + 1, j + 1), 1))

            if (i + 1 < mapRowLimit and j > 0):
                if Map[i + 1][j - 1] == 'I':
                    coordinateAdjancey.append(((i + 1, j - 1), Infnity))
                else:
                    coordinateAdjancey.append(((i + 1, j - 1), 1))
            if i > 0 and j > 0:
                if Map[i - 1][j - 1] == 'I':
                    coordinateAdjancey.append(((i - 1, j - 1), Infnity))
                else:
                    coordinateAdjancey.append(((i - 1, j - 1), 1))
            if i > 0 and j + 1 < mapColumnLimit:
                if Map[i - 1][j + 1] == 'I':
                    coordinateAdjancey.append(((i - 1, j + 1), Infnity))
                else:
                    coordinateAdjancey.append(((i - 1, j + 1), 1))

            adjanciesLists[coordinateiIJ] = coordinateAdjancey
    return adjanciesLists


def createH(Map):
    H = {}
    mapRowLimit = len(Map)
    mapColumnLimit = len(Map[0])

    for i in range(mapRowLimit):
        for j in range(mapColumnLimit):
            coordinateiIJ = (i, j)
            if Map[i][j] == 'I':
                H[coordinateiIJ] = Infnity
            else:
                H[coordinateiIJ] = 1
    return H


class DroneAgent:

    def __init__(self, initial):
        self.Map = initial["map"]
        self.map_Rlimit = len(self.Map) - 1
        self.map_Climit = len(self.Map[0]) - 1


    def act(self, state):

        allActions = self.Possible_Actions(state)
        if len(state["packages"]) == 0:
            return "reset"


        alltuples = ()

        for drone in state['drones']:
            alltuples = alltuples + tuple(allActions[drone])

        # print(alltuples)
        # print(self.score)
        return alltuples

    # def checkMoves(self,actions):

    def Possible_Actions(self, state):
        # the limits of the board

        global clientNext

        drones = state['drones']
        clients = state["clients"]
        packages = state["packages"]
        if len(packages) == 0:
            return "reset"

        dect_drones = {}

        # packages Counter
        # packCounter = 0
        graph = Graph(createAdjacencyList(state["map"]), createH(state["map"]))

        for drone in drones:
            packCounter = 0

            # coordinates (i,j)
            dronegetAction = False
            i = drones[drone][0]
            j = drones[drone][1]

            dect_drones[drone] = []

            # deliver :
            for pack in packages:
                if drone == packages[pack]:
                    for client in clients:
                        if pack in clients[client]['packages'] and \
                                clients[client]['location'] == drones[drone]:
                            dect_drones[drone].append(('deliver', drone, client, pack))

                            dronegetAction = True
                            break
                if dronegetAction:
                    break
            if dronegetAction:
                continue

            # check how packages the drone have
            for pack in packages:
                if drone == packages[pack]:
                    packCounter = packCounter + 1

            # pick up just of the drone have less than 2 packages:
            if packCounter < 2:

                for package in packages:
                    if drones[drone] == packages[package]:
                        twosamepack = False
                        for x in dect_drones:
                            if drone != x and dect_drones[x][0][0] == "pick up" and dect_drones[x][0][2] == package:
                                twosamepack = True
                                break

                        if not twosamepack:
                            dect_drones[drone].append(("pick up", drone, package))
                            dronegetAction = True
                            break

                    if dronegetAction:
                        break

            if dronegetAction:
                continue

            # move :
            # this is for drone that have a packege of the client

            for client in clients:
                packagesDrone = self.dronepackages(drone, packages)
                # if the drone have the package of the client
                if any(x in packagesDrone for x in clients[client]['packages']):
                    # what is the next possible place of the client
                    clientNext = self.nextPosition(clients[client]['probabilities'], clients[client]['location'])

                    # get the path from the drone to the client
                    path = graph.a_star_algorithm(drones[drone], clientNext)

                    # if the path doesn't exist
                    if path == -1:
                        return "reset"
                    # if the drone on the client place
                    if len(path) == 1 and self.Map[clients[client]['location'][0]][
                        clients[client]['location'][1]] != 'I':
                        dect_drones[drone].append(("move", drone, clients[client]['location']), )
                        break
                    # if the drone want to move to illegal place

                    if len(path) == 1 or self.Map[path[1][0]][path[1][1]] == 'I':
                        dect_drones[drone].append(("wait", drone), )
                        # dect_drones[drone].append(("move", drone, self.moveOptionsRandom(drones[drone])), )
                        break

                    dect_drones[drone].append(("move", drone, path[1]), )
                    break

                else:
                    lenpack = {}
                    for pack in packages:
                        path = graph.a_star_algorithm(drones[drone], packages[pack])
                        if path != -1:
                            lenpack[len(path)] = path
                    if len(lenpack) == 0:
                        itsgo = False
                        for client in clients:

                            packagesDrone = self.dronepackages(drone, packages)
                            if any(x in packagesDrone for x in clients[client]['packages']):
                                clientNext = self.nextPosition(clients[client]['probabilities'],
                                                               clients[client]['location'])
                                path = graph.a_star_algorithm(drones[drone], clientNext)
                                if path == -1:
                                    return "reset"
                                if len(path) == 1 and self.Map[clients[client]['location'][0]][
                                    clients[client]['location'][1]] != 'I':
                                    dect_drones[drone].append(("move", drone, self.moveOptionsRandom(drones[drone])), )
                                    break
                                # if the drone want to move to illegal place
                                if len(path) == 1 or self.Map[path[1][0]][path[1][1]] == 'I':
                                    # dect_drones[drone].append(("wait", drone), )
                                    dect_drones[drone].append(("move", drone, self.moveOptionsRandom(drones[drone])), )
                                    break
                                dect_drones[drone].append(("move", drone, path[1]), )
                                break

                        alltaken = False
                        packagesDrone = self.dronepackages(drone, packages)
                        for pack in packages:
                            if len(packages[pack]) == 2:
                                alltaken = True

                        if not alltaken and len(packagesDrone) == 0:
                            dect_drones[drone].append(("wait", drone), )
                            break



                    else:
                        min_value = min(lenpack.values())

                        # if the drone have 2 packages and he in the same plase of package 3 :
                        # todo: check if its do here sometime
                        if len(min_value) == 1:
                            dect_drones[drone].append(("move", drone, self.moveOptionsRandom(drones[drone])), )
                            break

                        dect_drones[drone].append(("move", drone, min_value[1]))
                    break

        return dect_drones

    def nextPosition(self, probabilities, position):
        i = position[0]
        j = position[1]
        canmoveto = []

        # up
        if i - 1 >= 0:
            canmoveto.append(probabilities[0])
        else:
            canmoveto.append(0)
        # down
        if i + 1 <= self.map_Rlimit:
            canmoveto.append(probabilities[1])
        else:
            canmoveto.append(0)

        # left
        if j - 1 >= 0:
            canmoveto.append(probabilities[2])
        else:
            canmoveto.append(0)

        # drone moves to the upper tile
        if j + 1 <= self.map_Climit:
            canmoveto.append(probabilities[3])
        # drone moves to the left tile
        else:
            canmoveto.append(0)
        # stay
        canmoveto.append(0)

        nextprob = canmoveto.index(max(canmoveto))

        if nextprob == 0:
            return position[0] - 1, position[1]
        if nextprob == 1:
            return position[0] + 1, position[1]
        if nextprob == 2:
            return position[0], position[1] - 1
        if nextprob == 3:
            return position[0], position[1] + 1
        if nextprob == 4:
            return position[0], position[1]

    def moveOptionsRandom(self, drone):
        # add the move statement thar wesal did to return the possible actions of the drone
        actions = []
        i = drone[0]
        j = drone[1]

        if j + 1 <= self.map_Climit and self.Map[i][j + 1] == 'P':
            actions.append((i, j + 1))
            # drone moves to the left tile
        if j - 1 >= 0 and self.Map[i][j - 1] == 'P':
            actions.append((i, j - 1))
            # drone moves to the upper tile
        if i - 1 >= 0 and self.Map[i - 1][j] == 'P':
            actions.append((i - 1, j))
            # drone moves to the downer tile
        if i + 1 <= self.map_Rlimit and self.Map[i + 1][j] == 'P':
            actions.append((i + 1, j))
            # go left and up
        if 0 <= i - 1 <= self.map_Rlimit and 0 <= j - 1 <= self.map_Climit and self.Map[i - 1][j - 1] == 'P':
            actions.append((i - 1, j - 1))
            # go right and up
        if 0 <= i - 1 <= self.map_Rlimit and 0 <= j + 1 <= self.map_Climit and self.Map[i - 1][j + 1] == 'P':
            actions.append((i - 1, j + 1))
            # go ritht and down
        if 0 <= i + 1 <= self.map_Rlimit and 0 <= j + 1 <= self.map_Climit and self.Map[i + 1][j + 1] == 'P':
            actions.append((i + 1, j + 1))
            # go left and down
        if 0 <= i + 1 <= self.map_Rlimit and 0 <= j - 1 <= self.map_Climit and self.Map[i + 1][j - 1] == 'P':
            actions.append((i + 1, j - 1))

        y = np.random.choice(len(actions), 1, p=None)

        return actions[y[0]]

    def dronepackages(self, drone, packages):
        dronepack = []
        for pack in packages:
            if packages[pack] == drone:
                dronepack.append(pack)
        return dronepack
