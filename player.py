import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import random

class Strategy:
    def __init__(self, n_players, low, high):
        self.n_players = n_players
        self.low = low
        self.high = high

        # Strategies
        self.s0 = np.random.randint(low, high)
        self.s1 = np.zeros(self.n_players)
        self.s2 = np.zeros(self.list_to_number([7,7], 8))
        self.s3 = np.zeros(self.list_to_number([7,7,7], 8))

        # Allowed actions
        self.allowed_s0_actions = range(self.low, self.high)
        self.allowed_s1_actions = [[] for i in range(len(self.s1))]
        self.allowed_s2_actions = [[] for i in range(len(self.s2))]
        self.allowed_s3_actions = [[] for i in range(len(self.s3))]

    def generate_s1(self):
        for i in range(len(self.s1)):
            choices = list(range(self.low, self.high))
            allowed_actions = [x for x in choices if x != i]
            self.allowed_s1_actions[i] = allowed_actions
            self.s1[i] = random.choice(allowed_actions)

    def generate_s2(self):
        for i in range(len(self.s2)):
            choices = list(range(self.low, self.high))
            eliminated_players = self.number_to_list(i, 8, 2)
            allowed_actions = [x for x in choices if x not in eliminated_players]
            self.allowed_s2_actions[i] = allowed_actions
            self.s2[i] = random.choice(allowed_actions)

    def generate_s3(self):
        for i in range(len(self.s3)):
            choices = list(range(self.low, self.high))
            eliminated_players = self.number_to_list(i, 8, 3)
            allowed_actions = [x for x in choices if x not in eliminated_players]
            self.allowed_s3_actions[i] = allowed_actions
            self.s3[i] = random.choice(allowed_actions)
    
    def list_to_number(self, elements, base):
        unique_number = 0
        for i, element in enumerate(reversed(elements)):
            unique_number += element * (base ** i)
        return unique_number

    def number_to_list(self, unique_number, base, list_length):
        numbers = []
        for _ in range(list_length):
            numbers.append(unique_number % base)
            unique_number //= base
        return numbers[::-1]

class Player:
    def __init__(self, name, score, strategy, n_players):
        self.name = name
        self.score = score
        self.strategy = strategy
        self.reward = 0
        self.current_strategy = strategy
        self.current_reward = 0

        self.strategy.generate_s1()
        self.strategy.generate_s2()
        self.strategy.generate_s3()
        self.remove_self_voting()
    def update_strategy(self, strategy):
            self.strategy.s0 = strategy
            
    def vote(self, eliminated_players):
        if not eliminated_players:
            return self.strategy.s0
        elif len(eliminated_players) == 1:
            index = eliminated_players[0].name - 1
            return self.strategy.s1[index]
        elif len(eliminated_players) == 2:
            elim_list = [x.name-1 for x in eliminated_players]
            index = self.strategy.list_to_number(elim_list, 8)
            return self.strategy.s2[index]
        elif len(eliminated_players) == 3:
            elim_list = [x.name-1 for x in eliminated_players]
            index = self.strategy.list_to_number(elim_list, 8)
            return self.strategy.s3[index]
    
    def remove_self_voting(self):
        self.strategy.allowed_s0_actions = [x for x in self.strategy.allowed_s0_actions if x != self.name-1]
        for inner_list in self.strategy.allowed_s1_actions:
            if self.name-1 in inner_list:
                inner_list.remove(self.name-1)
        for inner_list in self.strategy.allowed_s2_actions:
            if self.name-1 in inner_list:
                inner_list.remove(self.name-1)
        for inner_list in self.strategy.allowed_s3_actions:
            if self.name-1 in inner_list and len(inner_list)>1:
                inner_list.remove(self.name-1)