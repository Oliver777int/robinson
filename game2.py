from player import *
import sys

class Game:
    def __init__(self, initial_players, deterministic):
        self.deterministic = deterministic
        self.n_players = len(initial_players)
        self.current_players = initial_players
        self.current_eliminations = []
        self.winning_team = []
        self.s0_history = [[] for _ in range(self.n_players)]
        self.s1_history = [[] for _ in range(self.n_players)]
        self.s2_history = [[] for _ in range(self.n_players)]
        self.s3_history = [[] for _ in range(self.n_players)]
    def run_game(self, A, B, debugging):
        size_of_smallest_team = len(A)
        eliminated_players = []
        winning_team = []
        self.debugging = debugging
        while size_of_smallest_team > 1:
            score_A = sum(player.score for player in A[:size_of_smallest_team])
            score_B = sum(player.score for player in B[:size_of_smallest_team])
            if score_A > score_B:
                B, eliminated_player = self.run_elimination(B, eliminated_players)
                winning_team.append("A")
            else:
                A, eliminated_player = self.run_elimination(A, eliminated_players)
                winning_team.append("B")
            if debugging:
                print(eliminated_player.name)
            eliminated_players.append(eliminated_player)
            size_of_smallest_team = min(len(A), len(B))
        
        player_placement = self.merge_teams(A, B, eliminated_players)
        self.compute_rewards(player_placement)
        self.current_players = player_placement
        self.current_eliminations = [x.name for x in eliminated_players]
        self.winning_team = winning_team
        return eliminated_players

    # This method runs the elimination of one round. The most frequently voted player is removed from the players list, then the updated list
    # is returned along with the most voted player as second return argument.
    def run_elimination(self, players, eliminated_players):
        if len(players) <= 2: # If only 2 players the lowest score player loses.
            removed_player = min(players, key=lambda player: player.score)
            players.remove(removed_player)
        else:
            casted_votes = [player.vote(eliminated_players) for player in players]
            if self.debugging:
                print([x.name for x in eliminated_players])
                print(casted_votes)
            vote_frequency = Counter(casted_votes)
            max_frequency = max(vote_frequency.values())
            most_voted_players_indicies = [int(element+1) for element, frequency in vote_frequency.items() if frequency == max_frequency]
            most_voted_players = []
            for player in players:
                if player.name in most_voted_players_indicies:
                    most_voted_players.append(player)

            if len(most_voted_players) > 1: # Stochastic elimination of worst player 80% and 2nd worst with 20% 
                sorted_most_voted_players = sorted(most_voted_players, key=lambda player: player.score, reverse=True)
                if self.deterministic:
                    r = 0
                else:
                    r = random.random()
                if r < 0.95:
                    removed_player = sorted_most_voted_players[-1]
                else:
                    removed_player = sorted_most_voted_players[-2]
            else:
                removed_player = most_voted_players[0]
            players.remove(removed_player)
        return players, removed_player

    def merge_teams(self, A, B, eliminated_players):
        merged_team = A + B
        sorted_merged_list = sorted(merged_team, key=lambda player: player.score, reverse=True)
        return sorted_merged_list + eliminated_players[::-1]

    def compute_rewards(self, players):
        score_punishment = 0
        for i, player in enumerate(players):
            player.reward = len(players) - i - score_punishment
            score_punishment += player.score * 0.01

    def print_leaderboard(self, players):
        print("---- Leaderboard of the game ----")
        players_sorted = sorted(players, key=lambda player: player.reward, reverse=True)
        for i, player in enumerate(players_sorted):
            print(f"{i+1}: Player {player.name} with reward {round(player.reward,2)}")
        print(f"--- The game consisted of {len(self.current_eliminations)} rounds. ---")
        print(f"--> Eliminated players: {self.current_eliminations}")
        print(f"--> Winning team per round: {self.winning_team}")

    def find_first_eliminated_players(self, A, B, n):
        size_of_smallest_team = len(A)
        eliminated_players = []

        while size_of_smallest_team > 1:
            score_A = sum(player.score for player in A[:size_of_smallest_team])
            score_B = sum(player.score for player in B[:size_of_smallest_team])
            if score_A > score_B:
                B, eliminated_player = self.run_elimination(B, eliminated_players)
            else:
                A, eliminated_player = self.run_elimination(A, eliminated_players)
            eliminated_players.insert(0, eliminated_player)

            size_of_smallest_team = min(len(A), len(B))
            if len(eliminated_players) == n:
                break
        eliminated_players = [x.name-1 for x in eliminated_players]
        return eliminated_players[::-1]
    
    def list_to_number(self, elements, base):
        unique_number = 0
        for i, element in enumerate(reversed(elements)):
            unique_number += element * (base ** i)
        return unique_number
    
    def save_history(self, players):
        elims = [x-1 for x in self.current_eliminations]
        for i, player in enumerate(players):
            self.s0_history[i].append(int(player.strategy.s0+1))
            self.s1_history[i].append(int(player.strategy.s1[elims[0]]+1))
            self.s2_history[i].append(int(player.strategy.s2[self.list_to_number(elims[0:2], 8)]+1))
            self.s3_history[i].append(int(player.strategy.s3[self.list_to_number(elims[0:3], 8)]+1))
    
    def print_history(self, players):
        for player in players:
            print(f"Player {player.name} voted")
            print(f"s0: {self.s0_history[player.name-1]}")
            print(f"s1: {self.s1_history[player.name-1]}")
            print(f"s2: {self.s2_history[player.name-1]}")
            print(f"s3: {self.s3_history[player.name-1]}")