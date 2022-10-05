import random
import json


ids = ["207364332", "318881471"]


class DroneAgent:
    def __init__(self, n, m, epsilon=0.01, alpha=0.25, gamma=0.999):
        self.mode = 'train'
        self.Q = {}
        self.n = n
        self.m = m
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def possible_action(self, state):
        x = state['drone_location'][0]
        y = state['drone_location'][1]
        allActions = []
        if x + 1 <= self.n:
            allActions.append('move_down')
        if (x - 1) >= 0:
            allActions.append('move_up')
        if y + 1 <= self.m:
            allActions.append('move_right')
        if y - 1 >= 0:
            allActions.append('move_left')
        return allActions

    def deliver_action (self, state):
        for a in state["packages"]:
            if a[1] == "drone":
                if state["drone_location"] == state["target_location"]:
                    return 'deliver'

    def pick_action(self, state):
        packeges_counter = 0

        for a in state["packages"]:
            if a[1] == 'drone':
                packeges_counter = packeges_counter + 1

        if packeges_counter < 2:
            for a in state["packages"]:
                if a[1] != "drone":
                    if state["drone_location"] == a[1]:
                        return 'pick'

    def select_action(self, obs0):
        if self.deliver_action(obs0) != None:
            return 'deliver'
        if self.pick_action(obs0) != None:
            return 'pick'
        if len(obs0["packages"]) == 0 :
            return "reset"

        NowActions = self.possible_action(obs0)
        if random.random() < self.epsilon:
            action = random.choice(NowActions)

        else:
            Q = [self.getQreward(obs0, a) for a in NowActions]
            maxQ = max(Q)
            count = Q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(NowActions)) if Q[i] == maxQ]
                i = random.choice(best)
            else:
                i = Q.index(maxQ)
            action = NowActions[i]
        return action

    def train(self):
        self.mode = 'train'  # do not change this!

    def eval(self):
        self.mode = 'eval'  # do not change this!

    def update(self, obs0, action, obs1, reward):
        """
         Q-learning:
            Q(s, a) += alpha * (reward_func(s,a) + max(Q(s')) - Q(s,a))
        """
        NowActions = self.possible_action(obs1)
        q_max = max([self.getQreward(obs1, a) for a in NowActions])
        obs0['packages'] = tuple(obs0['packages'])
        obs0 = json.dumps(obs0)
        old_q = self.Q.get((obs0, action), None)
        if old_q is None:
            # todo : change
            self.Q[(obs0, action)] = reward
        else:
            self.Q[(obs0, action)] = old_q + self.alpha * (reward + self.gamma * q_max - old_q)

    def getQreward(self, obs0, action):
        obs0['packages'] = tuple(obs0['packages'])
        obs0 = json.dumps(obs0)
        return self.Q.get((obs0, action), 0.0)
