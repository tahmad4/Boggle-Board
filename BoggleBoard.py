import tkinter as tk
import winsound
import random
import time

# Controls whether or not timer will run
global timer_count
timer_count = 0


class GameCount:
    """Keeps count of game number"""

    def __init__(self):
        self.game_count = 0

    def reset(self):
        self.game_count = 0

    def increment(self):
        self.game_count += 1

    def get(self):
        return self.game_count


class Counter:
    def __init__(self):
        self.count = 0

    def reset(self):
        self.count = 0

    def increment(self):
        self.count += 1
        if self.count >= 26:
            self.count = 0

    def decrement(self):
        self.count -= 1
        if self.count >= 25:
            self.count = 0

    def get(self):
        return self.count


class IndexCounter:
    def __init__(self):
        self.index_count = 0

    def reset(self):
        self.index_count = 0

    def increment(self):
        # 25 is the board size so it resets after that
        self.index_count += 1
        if self.index_count >= 25:
            self.index_count = 0

    def get(self):
        return self.index_count


# Initializing above classes
count = Counter()

game_count = GameCount()

index_count = IndexCounter()


class Boggle:

    def __init__(self):
        self.x = 200
        self.y = 50
        self.WIDTH = 140
        self.HEIGHT = 140
        self.game_number = 1
        self.time_label = 1
        self.timer_sound = "TimerSound.wav"
        self.dies = []
        self.die = []
        self.one_letter = ""
        self.final_letter = ""
        self.letters = []

        # Initializes Window
        self.root = tk.Tk()

        # Initialize time
        self.initial_time = tk.StringVar()
        self.initial_time.set("00:00")

        # Creates the main canvas
        self.canvas = tk.Canvas(self.root, bg="#7395AE", width=1570, height=1000)
        self.canvas.pack()

        # Creates the side bar
        self.game_frame = tk.Frame(self.root, bg="#557A95")
        self.game_frame.place(relx=.9, y=0, relwidth=.3, relheight=1, anchor="n")

        # # Automatic fullscreen
        self.root.state("zoomed")

        # Initial board setup
        self.letterdisplayer()

        # Start button
        self.scramble_button = tk.Button(self.game_frame, bg="#7395AE", fg="#3d3c42", text="Start",
                                         font="ComicSans 32", command=lambda: self.start())
        self.scramble_button.place(relx=0.3, rely=0.3)

        # Scramble Button
        self.scramble_button = tk.Button(self.game_frame, bg="#7395AE", fg="#3d3c42", text="Scramble",
                                         font="ComicSans 32", command=lambda: self.letterdisplayer())
        self.scramble_button.place(relx=0.22, rely=0.1)

        # Starts the window loop
        self.root.mainloop()

    def gamecount(self):
        """Updates game count and displays the current game number in the side frame"""
        game_count.increment()
        self.game_number = tk.Label(self.game_frame, bg="#557A95", fg="#3d3c42",
                                    text="Game Number: " + str(game_count.get()), font="ComicSans 24", width=16)
        self.game_number.place(relx=0.19, rely=0.95)

    def letterdisplayer(self):
        """Draws the 5x5 Boggle board calling on letterchooser to get each letter"""
        for j in range(5):
            for i in range(5):
                self.letter_button = tk.Button(self.root, bg="#B1A296", text=self.letterchooser(), font="Times 42")
                self.letter_button.place(x=self.x, y=self.y, width=self.WIDTH, height=self.HEIGHT)
                self.x += self.WIDTH
            self.x = 200
            self.y += self.HEIGHT
        self.x = 200
        self.y = 50
        self.resettime()

    def letterList(self):
        """Creates a list of 25 randomized letters drawing one from each die"""

        global count, index_count

        # Dies produced by diePopulate.py and drawn from actual Boggle dies
        self.dies = [['A', 'A', 'A', 'F', 'R', 'S'], ['A', 'A', 'E', 'E', 'E', 'E'],
                     ['A', 'A', 'F', 'I', 'R', 'S'], ['A', 'D', 'E', 'N', 'N', 'N'],
                     ['A', 'E', 'E', 'E', 'E', 'M'], ['A', 'E', 'E', 'G', 'M', 'U'],
                     ['A', 'E', 'G', 'M', 'N', 'N'], ['A', 'F', 'I', 'R', 'S', 'Y'],
                     ['B', 'B', 'J', 'K', 'X', 'Z'], ['C', 'C', 'E', 'N', 'S', 'T'],
                     ['E', 'I', 'I', 'L', 'S', 'T'], ['C', 'E', 'I', 'P', 'S', 'T'],
                     ['D', 'D', 'H', 'N', 'O', 'T'], ['D', 'H', 'H', 'L', 'O', 'R'],
                     ['D', 'H', 'H', 'N', 'O', 'W'], ['D', 'H', 'L', 'N', 'O', 'R'],
                     ['E', 'I', 'I', 'I', 'T', 'T'], ['E', 'I', 'L', 'P', 'S', 'T'],
                     ['E', 'M', 'O', 'T', 'T', 'T'], ['E', 'N', 'S', 'S', 'S', 'U'],
                     ['G', 'O', 'R', 'R', 'V', 'W'], ['I', 'P', 'R', 'S', 'Y', 'Y'],
                     ['N', 'O', 'O', 'T', 'U', 'W'], ['O', 'O', 'O', 'T', 'T', 'U'],
                     ['Qu', 'In', 'Th', 'Er', 'He', 'An']]

        # Resets if previous list exists
        if len(self.letters) == 25:
            self.letters = []

        # For each die takes a random letter and adds it to a list
        for i in range(25):
            self.die = self.dies[count.get()]
            self.one_letter = random.choice(self.die)
            self.letters.append(self.one_letter)
            count.increment()

        # Shuffles the final list of letters
        random.shuffle(self.letters)

        return self.letters

    def letterchooser(self):
        """Picks the final letter to be displayed"""
        global count, index_count
        # Calls for a new list to be generated if it is a new game or next scramble
        if count.get() == 0:
            self.letterList()

        self.final_letter = self.letters[index_count.get()]

        count.decrement()
        index_count.increment()

        return self.final_letter

    def start(self):
        """Resets timer_count to 0 so timer will run and starts timer"""
        global timer_count
        timer_count = 0

        # Updates the game number
        self.gamecount()
        self.calculatetime()

    def displaytime(self, time):

        self.time_label = tk.Label(self.game_frame, bg="#557A95", fg="#3d3c42",
                                   text=time, width=6, font="ComicSans 52")
        self.time_label.place(relx=.2, rely=0.75)

    def resettime(self):
        """Resets timer to 00:00 and prevents it from ticking"""
        global timer_count
        timer_count = 1
        self.initial_time.set("00:00")

    def calculatetime(self):
        # Converts string initial time to usable int
        if timer_count == 0:
            self.time_string = str(self.initial_time.get())
            self.minutes, self.seconds = map(int, self.time_string.split(":"))

            # To prevent a type error later on. A little unsure why it is needed given the above line but it is

            self.minutes = int(self.minutes)
            self.seconds = int(self.seconds)
            # Ticks up the second and minute values
            if self.seconds < 59:
                self.seconds += 1
            elif self.seconds == 59:
                self.seconds = 0
                if self.minutes < 59:
                    self.minutes += 1
                else:
                    self.minutes = 0

        # Converts minutes into proper string
        if int(self.minutes) < 10:
            self.minutes = str(0) + str(self.minutes)
        else:
            self.minutes = str(self.minutes)

        # Converts second into proper string
        if self.seconds < 10:
            self.seconds = str(0) + str(self.seconds)
        else:
            self.seconds = str(self.seconds)

        # Final constructed time as string
        self.time_string = self.minutes + ":" + self.seconds

        # Updates the initial time to new time
        self.initial_time.set(self.time_string)

        # For testing purposes
        print(self.time_string)

        # Timer sound for last ten seconds
        if self.time_string == "02:50":
            winsound.PlaySound(self.timer_sound, winsound.SND_ASYNC)

        # Controls length of game
        if self.time_string == "03:00":
            self.resettime()

        # Updates timer in window
        self.displaytime(self.time_string)

        # Waits approximately one second before running a refresh on the time, 1000 millisecond wait
        if timer_count == 0:
            self.root.after(1000, lambda: self.calculatetime())


def main():
    Boggle()


if __name__ == "__main__":
    main()

