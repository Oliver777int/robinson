from player import *
from game2 import *
import sys
from tqdm import tqdm
import time

def list_to_number(elements, base):
    unique_number = 0
    for i, element in enumerate(reversed(elements)):
        unique_number += element * (base ** i)
    return unique_number

def number_to_list(unique_number, base, list_length):
        numbers = []
        for _ in range(list_length):
            numbers.append(unique_number % base)
            unique_number //= base
        return numbers[::-1]

# Initialize players
NUMBER_OF_PLAYERS = 8
players_list = [
    Player(name=1, score=8, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=2, score=7, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=3, score=6, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=4, score=5, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=5, score=4, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS),
    Player(name=6, score=3, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS),
    Player(name=7, score=2, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS),
    Player(name=8, score=1, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS)
]
players_list2 = [
    Player(name=1, score=14, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=2, score=13, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=3, score=12, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=4, score=11, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=5, score=17, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS),
    Player(name=6, score=16, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS),
    Player(name=7, score=15, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS),
    Player(name=8, score=1, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS)
]
players_list3 = [
    Player(name=1, score=15, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=2, score=12, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=3, score=7, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=4, score=6, strategy=Strategy(NUMBER_OF_PLAYERS,0,4), n_players=NUMBER_OF_PLAYERS),
    Player(name=5, score=16, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS),
    Player(name=6, score=10, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS),
    Player(name=7, score=9, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS),
    Player(name=8, score=4, strategy=Strategy(NUMBER_OF_PLAYERS,4,8), n_players=NUMBER_OF_PLAYERS)
]

midpoint = len(players_list) // 2

# Run the game with random initialization to get rewards
A = players_list[:midpoint]
B = players_list[midpoint:]
game = Game(players_list, deterministic=True)
game.run_game(A,B,False)

RUNS = 4
count = 0
start = time.time()
for run in tqdm(range(RUNS)):
    for player in range(len(players_list)): # Loop over all 8 players
        print(f"Finding best response of player {player+1}")
        max_s0_reward = 0
        max_s0 = players_list[player].strategy.allowed_s0_actions[0]
        for i in players_list[player].strategy.allowed_s0_actions: # Loop over all allowed s0 strategies
            players_list[player].strategy.s0 = i
            for eliminated_player in range(len(players_list)): # Loop over all single eliminations
                if players_list[player].name-1 == eliminated_player:
                    continue
                max__s1_reward = 0
                max_s1 = players_list[player].strategy.allowed_s1_actions[eliminated_player][0]
                for j in players_list[player].strategy.allowed_s1_actions[eliminated_player]: # Loop over all allowed s1 strategies
                    players_list[player].strategy.s1[eliminated_player] = j
                    for eliminated_pair in range(len(players_list[0].strategy.s2)): # Loop over all pair eliminations
                        if players_list[player].name-1 in players_list[0].strategy.number_to_list(eliminated_pair,8,2):
                            continue
                        max_s2_reward = 0
                        max_s2 = players_list[player].strategy.allowed_s2_actions[eliminated_pair][0]
                        for k in players_list[player].strategy.allowed_s2_actions[eliminated_pair]: # Loop over all allowed s2 strategies
                            players_list[player].strategy.s2[eliminated_pair] = k
                            A = players_list[:midpoint]
                            B = players_list[midpoint:]
                            eliminated_trio = game.find_first_eliminated_players(A,B, 3)
                            eliminated_trio_number = list_to_number(eliminated_trio, 8)
                            if players_list[player].name-1 in eliminated_trio:
                                continue
                            max_s3_reward = 0
                            max_s3 = players_list[player].strategy.allowed_s3_actions[eliminated_trio_number][0]
                            for l in players_list[player].strategy.allowed_s3_actions[eliminated_trio_number]: # Loop over all allowed s3 strategies
                                players_list[player].strategy.s3[eliminated_trio_number] = l

                                # Run game with assigned strategies
                                A = players_list[:midpoint]
                                B = players_list[midpoint:]
                                elims = game.run_game(A,B,False)
                                #if players_list[player].name <= 2 and eliminated_pair==59:
                                #    print(k)
                                # Checks if current strategy yielded highest reward
                                current_reward = players_list[player].reward

                                if current_reward > max__s1_reward:
                                    max_s1 = j
                                    max__s1_reward = current_reward
                                elif (current_reward == max__s1_reward) and (players_list[j].score > players_list[max_s1].score):
                                    max_s1 = j
                                    max__s1_reward = current_reward
                                if current_reward > max_s0_reward:
                                    max_s0 = i
                                    max_s0_reward = current_reward
                                elif (current_reward == max_s0_reward) and (players_list[i].score > players_list[max_s0].score):
                                    max_s0 = i
                                    max_s0_reward = current_reward
                                if current_reward > max_s2_reward:
                                    max_s2 = k
                                    max_s2_reward = current_reward
                                elif (current_reward == max_s2_reward) and (players_list[k].score > players_list[max_s2].score):
                                    max_s2 = k
                                    max_s2_reward = current_reward
                                if current_reward > max_s3_reward:
                                    max_s3 = l
                                    max_s3_reward = current_reward
                                elif (current_reward == max_s3_reward) and (players_list[l].score > players_list[max_s3].score):
                                    max_s3 = l
                                    max_s3_reward = current_reward
                                count +=1
                            players_list[player].strategy.s3[eliminated_trio_number] = max_s3
                        players_list[player].strategy.s2[eliminated_pair] = max_s2
                players_list[player].strategy.s1[eliminated_player] = max_s1
        players_list[player].strategy.s0 = max_s0
    game.save_history(players_list)
end = time.time()
print(f"Done after running {count} Simulations. Time: {end-start}")
A = players_list[:midpoint]
B = players_list[midpoint:]
elims = game.run_game(A,B,True)
game.print_history(players_list)
game.print_leaderboard(players_list)
