
import random
import math
import utils
import json
#from check import DroneStochasticProblem

ids = ["209459288", "315044446"]

MAX_PACKAGES_ON_DRONE = 2
class ActionFound(ValueError):
    pass


class DroneAgent:
    def __init__(self, initial):
        self.state=initial



    def assert_is_solvable(self, required_packages):
        the_map = self.configuration['map']
        for package_position in required_packages.values():
            if the_map[package_position[0]][package_position[1]] == 'I':
                raise ValueError('whatever')  # todo change

    def actions(self, raw_state):
        # state = json.loads(raw_state)
        state= raw_state
        drones_list = list(state["drones"].keys())
        actions = {k: [] for k in drones_list}
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""
        #actions = []
        print(state)
        for drone_id, drone_info in state['drones'].items():
            #if DroneStochasticProblem.is_action_legal(self, action):
            try:
                # pickups

                #if len(drone_info['packages']) < MAX_PACKAGES_ON_DRONE:
                    # look for packages we can pick up
                for package_id, package_location in state['packages'].items():
                    counter=0
                    if package_location == drone_id:
                        counter=counter+1
                    if counter < MAX_PACKAGES_ON_DRONE:

                        if drone_info == package_location:
                            actions[drone_id].append(('pick up', drone_id, package_id))
                           # raise ActionFound()

                # deliver
                location = drone_info
                # find clients in current location
                clients_in_location = []
                for client_id, client_data in state['clients'].items():
                    if client_data['location'] == location:
                        clients_in_location.append(client_id)

                for client in clients_in_location:
                    for package_id,package_location in state['packages'].items():
                        if package_location == drone_id:

                    #for drone_package in drone_info['packages']:
                            if self.get_client_desired_packages(client).count(package_id) > 0:
                                actions[drone_id].append(
                                    ('deliver', drone_id, client, package_id))
                            #    raise ActionFound()


                # wait
                # for package in drone_info['packages']:
                #     requiring_client = self.get_requiring_client(package, state)
                #     required_client_path = self.configuration['clients'][requiring_client]['path']
                #     if tuple(location) in required_client_path:
                #         actions[drone_id].append(("wait", drone_id))
                #         raise ActionFound()

                # move
                options = [
                    (location[0], location[1] + 1),
                    (location[0], location[1] - 1),
                    (location[0] + 1, location[1]),
                    (location[0] - 1, location[1]),
                    (location[0] +1 , location[1] + 1),
                    (location[0] -1 , location[1] - 1),
                    (location[0] + 1, location[1] -1),
                    (location[0] - 1, location[1] +1),
                ]
                random.shuffle(options)
                options = list(filter(lambda opt: self.is_in_map(opt) and self.is_passable(opt), options))

                # for package in drone_info['packages']:
                    # attempt 1: prioritize next-to locations
                    # requiring_client = self.get_requiring_client(package, state)
                    # required_client_path = self.configuration['clients'][requiring_client]['path']
                    # nice_options = filter(lambda opt: opt in required_client_path, options)
                    # for opt in nice_options:
                    #     options.insert(0, opt)

                    # attempt 2: prioritize by distance
                #     requiring_client = self.get_requiring_client(package, state)
                #     required_client_path = self.configuration['clients'][requiring_client]['path']
                #     first_path_item = required_client_path[0] # our arbitrary destination
                #     distances = [utils.distance(option, first_path_item) for option in options]
                #     best_option_index = distances.index(min(distances))
                #     options.insert(0, options[best_option_index])
                #     break  # quit after prioritizing a single package
                #
                # should_random = (state['step'] // 10) % 2 == 0  # do random things every other 100 steps
                # if len(drone_info['packages']) < MAX_PACKAGES_ON_DRONE and len(state['packages']) > 0: #and not should_random:
                #     # go in direction of packages on the floor
                #     package_locations = [list(state['packages'].values())[0]]
                #     for package_location in package_locations:
                #         distances = [utils.distance(option, package_location) for option in options]
                #         best_option_index = distances.index(min(distances))
                #         # print(distances, options)
                #         options.insert(0, options[best_option_index])

                for option in options:
                    actions[drone_id].append(('move', drone_id, option))
                    # raise ActionFound()

                # wait as fallback because everything didn't work, shouldn't happen
                actions[drone_id].append(("wait", drone_id))
                raise ActionFound()
            except ActionFound:
                pass
        print("actions",actions.values())

        return tuple(actions.values())

    def get_map_size(self):
        return (
            len(self.state['map']), len(self.state['map'][0]))

    def is_in_map(self, location):
        map_size = self.get_map_size()
        return not (location[0] < 0 or location[0] > map_size[0] - 1 \
            or location[1] < 0 or location[1] > map_size[1] - 1)



    def is_passable(self, location: tuple) -> bool:
        return self.state['map'][location[0]][location[1]] == 'P'

    def get_client_desired_packages(self, client_name) -> tuple:
        return self.state['clients'][client_name]['packages']

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""
        counter = 0
        state = json.loads(node.state)

        # make a dict of packages and their destination
        for package in self.packages:
            requiring_client = self.get_requiring_client(package, state)
            package_destination = state['clients'][requiring_client][
                'location']

            # calculate distance between current location and destination
            package_current_location = self.get_package_location(package,
                                                                 state)

            if package_current_location is None:
                # package has already delivered
                continue
            distance = \
                abs(package_current_location[0] - package_destination[0]) \
                + abs(package_current_location[1] - package_destination[1])

            counter += distance

        return counter




    def act(self, state):
        possible_actions= self.actions(state)
        # print("origianl",possible_actions)
        # print(len(possible_actions))
        really_best_option=[]
        best_option=[]
        for num_drone in range(len(possible_actions)):
            best_option.append(possible_actions[num_drone][0])
            #really_best_option.append(h2(self, state))

        return tuple(best_option)

