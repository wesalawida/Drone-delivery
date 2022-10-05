# import self as self
import search
import random
import math
import itertools

ids = ["207364332", "111111111"]


class DroneProblem(search.Problem):
    """This class implements a medical problem according to problem description file"""

    def __init__(self, initial):

        """Don't forget to implement the goal test
        You should change the initial to your own representation.
        search.Problem.__init__(self, initial) creates the root node"""
        self.Map = initial["map"]
        self.drones = self.makeTupleDrones(initial["drones"])
        self.clients = self.makeTupleClients(initial["clients"])
        self.packages = self.makeTuplePackages(initial["packages"])

        initialState = (self.drones,) + (self.clients,) + (self.packages,)
        search.Problem.__init__(self, initialState)

    def makeTupleDrones(self, drone):
        for d in drone:
            drone[d] = (drone[d],) + ((),)

        drones = tuple([(k, v) for k, v in drone.items()])
        return drones

    def makeTupleClients(self, clients):
        allClients = ()

        for C in clients:
            path = tuple(clients[C]['path'])
            pathlen = len(path)
            pack = clients[C]['packages']
            clientTuple = (C,) + (pack,) + (path,) + (0,) + (pathlen,)
            allClients = allClients + (clientTuple,)
        allClients = tuple([(a) for a in allClients])
        return allClients

    def makeTuplePackages(self, packages):
        for p in packages:
            packages[p] = (packages[p],) + ((),)
        packages = tuple([(k, v) for k, v in packages.items()])
        return packages

    def actions(self, state):
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""

        drones, clients, packages = state

        map_Rlimit = len(self.Map) - 1
        map_Climit = len(self.Map[0]) - 1

        actionsMap = {}

        for drone in drones:
            actions = []
            i = drone[1][0][0]
            j = drone[1][0][1]
            # drone moves to the right tile
            if j + 1 <= map_Climit and self.Map[i][j + 1] == 'P':
                actions.append(("move", drone[0], (i, j + 1)))
            # drone moves to the left tile
            if j - 1 >= 0 and self.Map[i][j - 1] == 'P':
                actions.append(("move", drone[0], (i, j - 1)))
            # drone moves to the upper tile
            if i - 1 >= 0 and self.Map[i - 1][j] == 'P':
                actions.append(("move", drone[0], (i - 1, j)))
            # drone moves to the downer tile
            if i + 1 <= map_Rlimit and self.Map[i + 1][j] == 'P':
                actions.append(("move", drone[0], (i + 1, j)), )
            if len(drone[1][1]) == 2:
                continue
            for package in packages:
                # check if drone and package at the same locations
                if package[1][0] == drone[1][0]:
                    if not package[1][1]:
                        actions.append(("pick up", drone[0], package[0]))
            for client in clients:
                client_loc_index = client[3]
                if client[2][client_loc_index] == drone[1][0]:
                    for package in drone[1][1]:
                        if package in client[1]:
                            actions.append(('deliver', drone[0], client[0], package))

            if drone[1][1] == ():
                actionsMap[drone[0]] = actions
                continue
            actions.append(("wait", drone[0]))
            actionsMap[drone[0]] = actions

        dronesNames = list(actionsMap)

        tempDronesActions = ()
        for droneName in dronesNames:
            tempDronesActions = tuple(tempDronesActions) + (tuple(actionsMap[droneName]),)
        TheActions = ()
        for element in itertools.product(*tempDronesActions):
            TheActions = tuple(TheActions) + (element,)

        return TheActions

    # turn the tuple of the stats to tree lists
    def ToList(self, state):
        drones, clients, packages = state
        drones = list(drones)
        clients = list(clients)
        packages = list(packages)
        drones = [list(x) for x in drones]
        clients = [list(x) for x in clients]
        packages = [list(x) for x in packages]
        return drones, clients, packages

    # turn the lists to one tuple state
    def ToTuples(self, drones, clients, packages):
        drones = tuple(tuple(a) for a in drones)
        clients = tuple(tuple(b) for b in clients)
        packages = tuple(tuple(c) for c in packages)
        State = (drones,) + (clients,) + (packages,)
        return State

    def moveclient(self, clients):
        NewClients = []
        for client in clients:
            if client[3] != (client[4] - 1):
                newClint = (client[0],) + (client[1],) + (client[2],) + (client[3] + 1,) + (client[4],)
            else:
                newClint = (client[0],) + (client[1],) + (client[2],) + (0,) + (client[4],)
            NewClients.append(newClint)
        return NewClients

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        drones, clients, packages = self.ToList(state)
        for act in action:
            if act[0] == "move":
                for drone in drones:
                    if drone[0] == act[1]:
                        newlocation = (act[2],) + (drone[1][1],)
                        newlocation = (drone[0],) + (newlocation,)
                        newlocation = list(newlocation)
                        drones.append(newlocation)
                        drones.remove(list(drone))
                        break

            if act[0] == "pick up":
                for drone in drones:
                    if drone[0] == act[1]:
                        Pack = list(drone[1][1])
                        if act[2] in Pack:
                            break
                        Pack.append(act[2])
                        thePack = (tuple(i for i in Pack),)
                        NewPack = (drone[1][0],) + tuple(thePack, )
                        NewPack = (drone[0],) + (tuple(NewPack),)
                        NewPack = list(NewPack)
                        drones.remove(list(drone))
                        drones.append(NewPack)

                for pack in packages:
                    if act[2] == pack[0]:
                        if pack[1][1] == ('picked',):
                            break
                        picked = ("picked",)
                        picked = [picked]
                        picked = (pack[1][0],) + tuple(picked, )
                        pickup = (pack[0],) + (picked,)
                        pickup = list(pickup)
                        packages.remove(list(pack))
                        packages.append(pickup)

            if act[0] == "deliver":
                for client in clients:
                    if client[0] == act[2]:
                        for package in client[1]:
                            if package == act[3]:
                                clientPack = list(client[1])
                                clientPack.remove(package)
                                clientPack = tuple(clientPack)
                                updateClient = list(
                                    (client[0],) + (clientPack,) + (client[2],) + (client[3],) + (client[4],))
                                clients.append(updateClient)
                                clients.remove(client)
                                break

                for pack in packages:
                    if act[3] == pack[0]:
                        packages.remove(pack)
                        break

                for drone in drones:
                    if act[3] in drone[1][1]:
                        packs = list(drone[1][1])
                        packs.remove(act[3])
                        newDrone = (drone[1][0],) + (tuple(packs),)
                        newDrone = list((drone[0],) + (newDrone,))
                        drones.remove(drone)
                        drones.append(newDrone)
                        break

            if act[0] == "wait":
                continue

        clients = self.moveclient(clients)
        newstate = self.ToTuples(drones, clients, packages)
        return newstate

    # ***********************************************************************************************************************
    def finished(self, state):
        drones, clients, packages = self.ToList(state)
        for client in clients:
            for package in client[1]:
                if package:
                    return False
        return True

    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""
        return self.finished(state)

    def ManhattanDistance(self, a, b):
        return sum(abs(e1 - e2) for e1, e2 in zip(a, b))

    # ***********************************************************************************************************************
    def h(self, node):
        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""
        if self.goal_test(node.state):
            return 0

        drones = node.state[0]
        clients = node.state[1]
        packages = node.state[2]
        dis = 0

        if node.parent is not None:
            if node.parent.parent is not None:
                for drone in drones:
                    for dronep in node.parent.parent.state[0]:
                        if drone[0] == dronep[0]:
                            if drone[1][0] == dronep[1][0]:
                                dis = dis + 400

                            else:

                                dis = dis - 10
        for drone in drones:
            for pack in packages:
                dis = dis + (10 * (self.ManhattanDistance(drone[1][0], pack[1][0])))

        for client in clients:
            for pack in packages:
                dis = dis + (10 * (self.ManhattanDistance(client[2][client[3]], pack[1][0])))

        if node.action is not None:
            for atomic in node.action:
                if atomic is not None:
                    if atomic[0] == 'deliver':
                        dis -= 200
                    if atomic[0] == 'pick up':
                        dis -= 100
                    if atomic[0] == 'move':
                        dis -= 50
        dis = dis + (len(packages) * 90)

        return max(dis, 1)

    """Feel free to add your own functions
    (-2, -2, None) means there was a timeout"""


def create_drone_problem(game):
    return DroneProblem(game)
