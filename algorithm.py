from connection_calculations import minimax_structure
import os.path
import json
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

class Agent:
    def __init__(self, code_length=4, color_count=6, max_guesses=10) -> None:
        self.code_length = code_length
        self.color_count = color_count
        self.max_guesses = max_guesses

        source_directory = os.path.dirname(__file__)
        structure_file_name = f"len{code_length}_count{color_count}.json"
        structure_path = os.path.join(source_directory, "SavedStructures", structure_file_name)

        if os.path.exists(structure_path):
            print("Precomputed structure found. Loading data.")
            with open(structure_path, 'r') as input_file:
                self.search_structure = json.load(input_file)["structure"]
                print("Data loaded successfully.")
        else:
            print("No saved data found. Computing data.")
            self.search_structure = minimax_structure(code_length, color_count)
            print("Data computed.")
            with open(structure_path, 'w') as output_file:
                print("Writing data for future use.")
                json.dump({"structure": self.search_structure}, output_file)
                print("File written.")
    
    def optimal_guess(self):
        # Goal: Maximize the information gained with the worst case response
        # -> Each response eliminates all possibilities inconsistent with the guess and response
        # -> Worst case response eliminates the least possibilities
        # -> Worst case response matches the most possibilities for the guess
        # -> Score of a guess is the size of its largest set of possibilities for a single response
        # -> Best guess minimizes score amongst all still valid codes
        best_guess = None
        best_score = float('inf')
        
        for idx, code in enumerate(self.search_structure):
            if code is None:
                continue
            score = max([len(poss_set) for poss_set in code.values()])
            if score < best_score:
                best_score = score
                best_guess = idx

        return best_guess
        
    def update_possibilities(self, guess: int, response: str):
        # Remove each code incompatible with the guess and response
        old_entry = self.search_structure[guess] # Just to avoid any shenanigans with modifying an iterator
        for key in old_entry:
            if key == response:
                continue
            for code in old_entry[key]:
                self.remove_possibility(code)

    def remove_possibility(self, code_num: int):
        # For every key in the code's entry
        #   For every possibility in that key's associated list
        #       Remove the code from the list associated with the key in the possibility's entry
        # Remove the code's entry
        entry = self.search_structure[code_num]
        for key in entry:
            if key == f"{self.code_length}-0":
                continue
            for possibility in entry[key]:
                self.search_structure[possibility][key].remove(code_num)
                if len(self.search_structure[possibility][key]) == 0:
                    self.search_structure[possibility].pop(key)
        self.search_structure[code_num]=None

    def num_to_code(self, num: int):
        # Codes are their number converted to base <color count> and zero padded to meet the code length
        human_readable = [0]*self.code_length
        for i in reversed(range(self.code_length)):
            human_readable[i] = num%self.color_count
            num = num//self.color_count
        return " ".join([str(elem) for elem in human_readable])

    def code_to_num(self, code: str):
        list_format = [int(x) for x in code.split(" ")]
        num = 0
        for x in list_format:
            num *= self.color_count
            num += x
        return num

    def visualize_state(self):
        valid = np.array([(x is not None)*1 for x in self.search_structure])
        vertical_digits = self.code_length//2
        horizontal_digits = self.code_length-vertical_digits
        vertical_length = self.color_count**vertical_digits
        horizontal_length = self.color_count**horizontal_digits
        valid = np.reshape(valid, (vertical_length, -1))

        cmap = colors.ListedColormap(['red', 'green'])
        fig, ax = plt.subplots()
        ax.imshow(valid, cmap=cmap)
        ax.set_xticks(np.arange(-.5,horizontal_length-.5,1))
        ax.set_xticklabels([])
        ax.set_yticks(np.arange(-.5,vertical_length-.5,1))
        ax.set_yticklabels([])
        ax.grid(which="both", linestyle="-", color="k", linewidth=1)
        plt.show()

    def wrapper(self):
        while True:
            self.visualize_state()
            best_guess = self.optimal_guess()
            print(f"Recommended Guess: {self.num_to_code(best_guess)}")
            made_guess = input("Your Guess: ")
            response = input("Response Received: ")
            if response == f"{self.code_length}-0":
                break
            self.update_possibilities(self.code_to_num(made_guess), response)

if __name__=="__main__":
    ai = Agent()
    ai.wrapper()