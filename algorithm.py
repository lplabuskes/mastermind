from connection_calculations import minimax_structure
import os.path
import json

class Agent:
    def __init__(self, code_length=4, color_count=6, max_guesses=10) -> None:
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


if __name__=="__main__":
    temp = Agent()