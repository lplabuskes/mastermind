import random

class Game:
    def __init__(self, code_length=4, color_count=6, max_guesses=10) -> None:
        self.code_length = code_length
        self.color_count = color_count
        self.max_guesses = max_guesses
        self.secret_code = [random.randint(0, color_count-1) for i in range(code_length)]
        print(f"Code Length: {code_length}, Number of Colors: {color_count}")
        print("Secret Code Generated")

        self.secret_counts = [0] * color_count
        for entry in self.secret_code:
            self.secret_counts[entry] += 1

    def check_guess(self, guess):
        if len(guess) is not self.code_length:
            print("Incorrect Length Guess")
            return
        guess_counts = [0] * self.color_count
        black_count = 0

        for idx, entry in enumerate(guess):
            if not isinstance(entry, int) or entry >= self.color_count or entry < 0:
                print("Invalid Code Element")
                return
            guess_counts[entry] += 1
            if entry is self.secret_code[idx]:
                black_count += 1
        
        white_count = sum([ min(self.secret_counts[i], guess_counts[i]) for i in range(self.color_count) ]) - black_count

        return (black_count, white_count)

    def run(self):
        num_guesses = 0
        correct = False

        print("Enter your guesses in the format:\n"+
              "# # # #")
        
        while not correct and num_guesses < self.max_guesses:
            user_input = input(f"You Have {self.max_guesses-num_guesses} Guesses Remaining:")
            guess = [int(element) for element in user_input.split(" ")]
            response = self.check_guess(guess)
            if response is None:
                continue
            else:
                num_guesses += 1
                print(f"Black: {response[0]}, White: {response[1]}")
            
            if response[0] is self.code_length:
                print("You Correctly Guessed the Secret Code!")
                print(f"You Used {num_guesses}/{self.max_guesses} Available Guesses")
                break

        if num_guesses >= self.max_guesses:
            print("You Lost")
            print(f"The Secret Code Was: {self.secret_code}")

if __name__ == "__main__":
    test_game = Game()
    test_game.run()
