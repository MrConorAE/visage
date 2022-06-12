###  Visage ###
# a color game by Conor Eager
# Developed for 91906 Complex Programming Techniques, for Level 3 Computer Science.

# IMPORTS
# Import Tk for graphical user interfaces
import tkinter as tk

# Import random for random generation of colors
import random

# Import pickle for saving and loading of user data & game state
import pickle

# Import one function from os for finding the data file
# From https://stackoverflow.com/a/4028943/7311875
from os.path import expanduser

# CLASSES


class Application:
    # This class is the main class for the game.
    # It calls other classes for the main menu, game, settings, and highscore screens.
    def __init__(self):
        # Initialise game state, including loading data.
        self.data = Data()
        self.data.load()

        # Open the main menu.
        self.main_menu = MainMenuWindow(self)


class Data:
    # This class is responsible for all the data stored for the game.
    # It contains methods for saving and loading data to/from persistent storage,
    # and for modifying and reading data (e.g. settings, highscores).
    def __init__(self):
        # Set the defaults.
        self.button_outlines = False
        self.button_gaps = True
        self.highlight = "dot"
        self.difficulty = 1.0
        self.highscore = 3

    def save(self):
        # Save the game state to persistent storage.

        # First, get the location to save to. This is the user's home directory.
        # From https://stackoverflow.com/a/4028943/7311875
        location = expanduser("~")

        # Open the file to save to.
        try:
            with open(location + "/visage_save.data", "wb") as file:
                # Now save the entire contents of the Data class to a Pickle file in that location.
                pickle.dump(self, file)
        except Exception as e:
            # If there's an error, alert the user.
            msg = MessageWindow(
                "Error", f"Could not save Visage data at\n{location + '/visage_save.data'}\nYour progress HAS NOT been saved. Please check that you have permission to write to this directory/file.\nIf you would like to try again, press 'Try Again'. To exit without saving, press 'Exit Anyway'.\n\nMore details on the error can be seen below:\n\n{e}", 1000, 600, "Exit Anyway", second_button={'text': 'Try Again', 'command': self.save})

    def load(self):
        # Load the game state from persistent storage.

        # First, get the location to load from. This is the user's home directory.
        # From https://stackoverflow.com/a/4028943/7311875
        location = expanduser("~")

        # Open the file to read from.
        try:
            with open(location + "/visage_save.data", "rb") as file:
                # Now load the entire contents of the Pickle file into the Data class.
                self = pickle.load(file)
        except FileNotFoundError:
            # No savefile exists.
            msg = MessageWindow(
                "Information", f"No Visage savefile was found. A new save file will be created at\n{location + '/visage_save.data'}.\nGame data is saved automatically when the game closes.", 1000, 600, "Continue")
        except Exception as e:
            # If there's an error, alert the user.
            msg = MessageWindow(
                "Error", f"A Visage save file was found at\n{location + '/visage_save.data'}\nbut it could not be loaded.\nPlease check you have permission to access this file and that it has not been edited.\n\nMore details on the error can be seen below:\n\n{e}", 1000, 600, "Continue")


class Window:
    # This class contains code for a basic window.
    # Any elements or configuration that should be applied across all windows is done here.
    def __init__(self, title, width, height):
        # Create the window.
        self.root = tk.Tk()
        # Set the window title.
        self.root.title(f"Visage / {title}")
        # Configure the geometry of the window.
        if (width or height):
            self.root.geometry(f"{width}x{height}")
        # Set the visual aspects of the window:
        self.root.configure(bg="#2b2b2b")
        # Set the window to non-resizable.
        self.root.resizable(False, False)
        # Set up the font.
        self.font = ("IBM Plex Sans", 20)

    def Button(parent, fontsize=20, **kwargs):
        # Create a button with the default options.
        return tk.Button(parent, font=("IBM Plex Sans", fontsize), bg="#2b2b2b", fg="#ffffff", relief="flat", **kwargs)


class MessageWindow(Window):
    # This class contains code for a single-message window to inform the user.
    def __init__(self, title, text, width, height, buttontext="OK", second_button={}):
        Window.__init__(self, title, width, height)

        label = tk.Label(self.root, text=text,
                         bg="#2b2b2b", fg="#ffffff", font=("IBM Plex Sans", ))
        label.grid(row=0, column=0)

        button = Window.Button(
            self.root, text=buttontext, command=lambda: self.run(None))
        button.grid(row=1, column=0, padx=10, pady=10)

        if (second_button):
            button_two = Window.Button(
                self.root, text=second_button['text'], command=lambda: self.run(second_button['command']))
            button_two.grid(row=2, column=0, padx=10, pady=10)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.root.mainloop()

    def run(self, command):
        self.root.destroy()
        if (command):
            command()


class MainMenuWindow(Window):
    # This class contains the main menu.
    # It can call back to the Application class to start the game.
    def __init__(self, application):
        # Open the main menu window.
        # Perform initialisation using the Window parent class.
        Window.__init__(self, "Main Menu", 500, 600)

        self.application = application

        # Create the frame to keep everything in the centre.
        frame = tk.Frame(self.root, bg="#2b2b2b")
        frame.grid(row=0, column=0)

        # Create the logo image.
        logo = tk.PhotoImage(file="logo.png")
        logo_label = tk.Label(frame, image=logo, bg="#2b2b2b")
        # Place it in the grid.
        logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Create the main menu buttons.
        btn_play = Window.Button(
            frame, text="Play", command=self.play, width=25)
        btn_highscores = Window.Button(
            frame, text="Highscores", command=self.highscores, width=25)
        btn_settings = Window.Button(
            frame, text="Settings", command=self.settings, width=25)
        btn_quit = Window.Button(
            frame, text="Quit", command=self.quit, width=25)
        # Place them in the grid.
        btn_play.grid(row=1, column=0, padx=10, pady=10)
        btn_highscores.grid(row=2, column=0, padx=10, pady=10)
        btn_settings.grid(row=3, column=0, padx=10, pady=10)
        btn_quit.grid(row=4, column=0, padx=10, pady=10)

        # Configure row/column weights to centre content
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        for row in range(0, 5):
            frame.rowconfigure(row, weight=1)
        frame.columnconfigure(0, weight=1)

        # Keep the window open, waiting for something to happen.
        # This is blocking because we don't need to do anything else.
        self.root.mainloop()

    def play(self):
        # Start the game.
        self.root.destroy()
        game = GameWindow(self.application.data)

        # Once the game closes, reopen the main menu.
        self.__init__(self.application)

    def highscores(self):
        # Open the highscores window.
        self.root.destroy()
        scorewindow = ScoreWindow(self.application.data)

        # Once the score window closes, reopen the main menu.
        self.__init__(self.application)

    def settings(self):
        # Open the settings window.
        self.root.destroy()
        settings = SettingsWindow(self.application.data)

        # Once settings closes, reopen the main menu.
        self.__init__(self.application)

    def quit(self):
        # Quit the game.
        self.root.destroy()
        self.application.data.save()


class GameWindow(Window):
    # This class is the game itself.
    # It contains the game loop, and can call back to Application or Data for the game state.
    def __init__(self, data):
        # Open the main window.
        # Perform initialisation using the Window parent class.
        Window.__init__(self, "Play", 500, 500)

        self.data = data

        # Lives counter.
        if self.data.difficulty == 0.5:
            self.lives = 5
        elif self.data.difficulty == 1.0:
            self.lives = 3
        elif self.data.difficulty == 2.0:
            self.lives = 1

        # Generate a difficulty description for use in the UI.
        if (self.data.difficulty == 0.5):
            self.difficulty_str = "Easy"
        elif (self.data.difficulty == 1.0):
            self.difficulty_str = "Normal"
        elif (self.data.difficulty == 2.0):
            self.difficulty_str = "Hard"

        # Initialise level counter.
        self.level = 3

        # Create the frame for the buttons.
        self.frame = tk.Frame(self.root, bg="#2b2b2b",
                              width=400, height=400)
        self.frame.grid(row=0, column=0, columnspan=3, sticky="NESW")

        # Score label
        self.score_label = tk.Label(self.root, bg="#2b2b2b", fg="#ffffff",
                                    text=f"Level {self.level}", font=("IBM Plex Sans", 20), padx=10, pady=10, width=10)
        self.score_label.grid(row=2, column=1, padx=20, pady=20)

        # Help label
        self.help_label = tk.Label(self.root, bg="#2b2b2b", fg="#ffffff",
                                   text=f"{'❤'*self.lives}\nDifficulty: {self.difficulty_str}", font=("IBM Plex Sans", 10), width=15, padx=10, pady=10)
        self.help_label.grid(row=2, column=2, padx=20, pady=20)

        # Create the main menu buttons.
        btn_quit = Window.Button(
            self.root, 16, text="Quit", command=self.quit)
        # Place them in the grid.
        btn_quit.grid(row=2, column=0, padx=20, pady=20)

        # Configure row/column weights to centre content
        self.root.rowconfigure(0, weight=1, minsize=100)
        self.root.rowconfigure(0, weight=1)
        for col in range(0, 3):
            self.root.columnconfigure(col, weight=1)

        # Initialise the "busy" variable, which will disable click processing
        # while false - preventing the user from clicking while buttons are being generated.
        self.busy = False

        # Generate colors.
        self.generate_buttons(self.level, self.data)

        # Keep the window open, waiting for something to happen.
        # This is blocking because we don't need to do anything else.
        self.root.mainloop()

    def generate_buttons(self, level, data):
        # Generate a new set of color buttons according to difficulty.
        self.busy = True

        original_color_ok = False
        different_color_ok = False

        # Create a 2D array to store the buttons.
        self.buttons = list()

        while original_color_ok is False:
            # Set loading message.
            self.help_label.configure(
                text=f"Loading (000/{level**2:03})", bg="#ffffff", fg="#2b2b2b")

            # Reset the frame, clearing the existing buttons:
            self.frame = tk.Frame(self.root, bg="#2b2b2b")
            self.frame.grid(row=0, column=0, columnspan=3)
            self.root.update()

            # Calculate the size the buttons should be:
            size = round(100 / level)

            # Generate the "correct" color.
            original_color = [
                random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
            # Convert it to a string for use with Tk.
            original_color_str = f"#{original_color[0]:02X}{original_color[1]:02X}{original_color[2]:02X}"

            # Generate a color.
            while different_color_ok is False:
                # Generate the "incorrect" color.
                # Choose which part to change:
                component_to_change = random.randint(0, 2)
                # How much to change it by:
                change_it_by = round(0xFF / round(level * data.difficulty))
                # Change by pos or neg?
                add_or_subtract = random.choice([-1, 1])

                different_color = original_color
                # Generate the new color, using the correct color as a base.
                different_color[component_to_change] = round(
                    original_color[component_to_change] + (change_it_by * add_or_subtract))

                # If the result is over 255 or under 0, generate a new base color.
                if (different_color[component_to_change] > 0xFF) or (different_color[component_to_change] < 0x00):
                    original_color_ok = False
                    different_color_ok = False
                    break

                # Convert it to a string for use with Tk.
                different_color_str = f"#{different_color[0]:02X}{different_color[1]:02X}{different_color[2]:02X}"

                if (different_color_str == original_color_str):
                    # Identical color, start again.
                    original_color_ok = True
                    different_color_ok = False
                    continue

                if len(different_color_str) != 7:
                    # Invalid color, start again.
                    original_color_ok = True
                    different_color_ok = False
                    continue

                # Valid color! Break.
                original_color_ok = True
                different_color_ok = True
                break

        # Choose which button will be incorrect.
        self.diff_btn_row = random.randint(0, level-1)
        self.diff_btn_col = random.randint(0, level-1)

        print("Colors done")

        # Configure row/column weights for the inner frame:
        for i in range(0, level):
            self.frame.rowconfigure(i, weight=1)
            self.frame.columnconfigure(i, weight=1)

        # Check settings for creating buttons.
        padding = 1 if data.button_gaps == True else 0
        outlines = 1 if data.button_outlines == True else 0

        # Generate the buttons:
        for row in range(0, level):
            # Add a new array row.
            self.buttons.append([])

            for col in range(0, level):
                # Choose the color for this button.
                # Is this the wrong button?
                if (row == self.diff_btn_row and col == self.diff_btn_col):
                    color = different_color_str
                else:
                    color = original_color_str

                # Check what the highlight settings are.
                if (data.highlight == "color"):
                    highlight_bg = "#ffffff"
                    highlight_fg = "#ffffff"
                elif (data.highlight == "dot"):
                    highlight_bg = color
                    highlight_fg = "#ffffff"
                elif (data.highlight == "none"):
                    highlight_bg = color
                    highlight_fg = color

                # Create the button.
                button = tk.Button(self.frame, bg=color, fg=color, highlightthickness=outlines, activebackground=highlight_bg, activeforeground=highlight_fg,
                                   relief="flat", text="●", font=("IBM Plex Sans", round(100/level)), command=lambda x=row, y=col: self.check_color(x, y), width=size, height=size)

                button.grid(row=row, column=col, padx=padding, pady=padding)

                # Save the button to the list.
                self.buttons[row].append(button)

                # Update the progress indicator.
                self.help_label.configure(
                    text=f"Loading ({(row*level)+col:03}/{level**2:03})", bg="#ffffff", fg="#2b2b2b")
                self.help_label.update()

        print("Buttons done")

        self.busy = False

        self.help_label.configure(
            text=f"{'❤'*self.lives}\nDifficulty: {self.difficulty_str}", bg="#2b2b2b", fg="#ffffff")

    def quit(self):
        # Quit the game.
        # Is this a new highscore?
        if (round(self.level * self.data.difficulty) > self.data.highscore):
            self.data.highscore = round(self.level * self.data.difficulty)
        self.data.save()
        self.root.destroy()

    def game_over(self):
        # Game over! Show the user's score, and save it.
        self.frame = tk.Frame(self.root, bg="#2b2b2b")
        self.frame.grid(row=0, column=0, columnspan=3)
        self.root.update()

        game_over_text = tk.Label(
            self.frame, text=f"Game over!", bg="#2b2b2b", fg="#ffffff", font=("IBM Plex Sans", 30))
        game_over_text.grid(row=0, column=0)

        score_text = tk.Label(
            self.frame, text=f"Level {self.level}\n on {self.difficulty_str} difficulty", bg="#2b2b2b", fg="#ffffff", font=("IBM Plex Sans", 24))
        score_text.grid(row=1, column=0)

        next_steps_text = tk.Label(
            self.frame, text=f"Press Quit to return\nto the main menu.", bg="#2b2b2b", fg="#ffffff", font=("IBM Plex Sans", 18))
        next_steps_text.grid(row=2, column=0)

    def check_color(self, row, col):
        if (self.busy == True):
            # We're currently busy generating buttons.
            # Don't process click.
            return

        if (row == self.diff_btn_row and col == self.diff_btn_col):
            # Different color: correct choice!
            self.level += 1
            self.score_label.configure(
                text="Correct!", fg="#33d17a")
            self.generate_buttons(self.level, self.data)
            self.score_label.configure(
                text=f"Level {self.level}", fg="#ffffff", bg="#2b2b2b")
        else:
            # Original color: incorrect.
            # TODO: Alert the user and exit.

            # Set busy to disallow clicks
            self.busy = True
            self.score_label.configure(
                text="Incorrect...",  fg="#e01b24")

            self.lives -= 1

            # Indicate where the incorrect button is by flashing a dot on it.
            self.buttons[self.diff_btn_row][self.diff_btn_col].configure(
                fg="#ffffff", text="●")
            self.root.after(
                500, lambda: self.buttons[self.diff_btn_row][self.diff_btn_col].configure(text=""))
            self.root.after(
                1000, lambda: self.buttons[self.diff_btn_row][self.diff_btn_col].configure(text="●"))
            self.root.after(
                1500, lambda: self.buttons[self.diff_btn_row][self.diff_btn_col].configure(text=""))
            self.root.after(
                2000, lambda: self.buttons[self.diff_btn_row][self.diff_btn_col].configure(text="●"))

            # Was that the last life?
            # If so, exit and show the user's score (the level).
            if (self.lives == 0):
                self.root.after(2500, lambda: self.game_over())
            else:
                # Generate a new set of buttons at the SAME difficulty.
                self.root.after(2500, lambda: self.generate_buttons(
                    self.level, self.data))
                self.root.after(2500, lambda: self.score_label.configure(
                    text=f"Level {self.level}", fg="#ffffff", bg="#2b2b2b"))


class SettingsWindow(Window):
    # This class contains the settings window.
    # It can call back to Application or Data to change the game settings.
    def __init__(self, data):
        # Open the settings window.
        # Perform initialisation using the Window parent class.
        Window.__init__(self, "Settings", 700, 500)

        self.data = data

        # Create the title.
        title = tk.Label(self.root, text="Settings",
                         font=("IBM Plex Sans", 30), bg="#2b2b2b", fg="#ffffff", justify="center")
        title.grid(row=0, column=0, columnspan=6)

        # Create the save & exit button.
        exit = Window.Button(self.root, text="Save & Exit",
                             command=self.save_and_exit)
        exit.grid(row=5, column=0, columnspan=6)

        # Create the setting labels.
        label_text = ["Button outlines", "Gaps between buttons",
                      "Highlight type", "Game difficulty"]
        for t in range(len(label_text)):
            label = tk.Label(
                self.root, text=label_text[t], font=("IBM Plex Sans", 16), bg="#2b2b2b", fg="#ffffff", justify="left")
            label.grid(row=t+1, column=0, columnspan=3)

        # Create the option buttons.
        # Button outlines:
        self.button_outlines_btn = Window.Button(
            self.root, 16, text="OFF", command=self.toggle_outlines, width=5)
        self.button_outlines_btn.grid(row=1, column=4)

        # Button gaps:
        self.button_gaps_btn = Window.Button(
            self.root, 16, text="ON", command=self.toggle_gaps, width=5)
        self.button_gaps_btn.grid(row=2, column=4)

        # Highlights:
        self.highlight_color_btn = Window.Button(
            self.root, 16, text="COLOR", command=lambda x="color": self.change_highlight(x), width=5)
        self.highlight_dot_btn = Window.Button(
            self.root, 16, text="DOT", command=lambda x="dot": self.change_highlight(x), width=5)
        self.highlight_none_btn = Window.Button(
            self.root, 16, text="NONE", command=lambda x="none": self.change_highlight(x), width=5)
        self.highlight_color_btn.grid(row=3, column=3)
        self.highlight_dot_btn.grid(row=3, column=4)
        self.highlight_none_btn.grid(row=3, column=5)

        self.difficulty_easy_btn = tk.Button(
            self.root, font=("IBM Plex Sans", 16), relief="flat", text="EASY",
            command=lambda x=0.5: self.change_difficulty(x), width=5, fg="#33d17a", bg="#2b2b2b", highlightbackground="#33d17a")
        self.difficulty_normal_btn = tk.Button(
            self.root, font=("IBM Plex Sans", 16), relief="flat", text="NORMAL",
            command=lambda x=1.0: self.change_difficulty(x), width=5, fg="#f6d32d", bg="#2b2b2b", highlightbackground="#f6d32d")
        self.difficulty_hard_btn = tk.Button(
            self.root, font=("IBM Plex Sans", 16), relief="flat", text="HARD",
            command=lambda x=2.0: self.change_difficulty(x), width=5, fg="#e01b24", bg="#2b2b2b", highlightbackground="#e01b24")
        self.difficulty_easy_btn.grid(row=4, column=3)
        self.difficulty_normal_btn.grid(row=4, column=4)
        self.difficulty_hard_btn.grid(row=4, column=5)

        # Set weights for the grid.
        for c in range(0, 6):
            self.root.columnconfigure(c, weight=1)
        for r in range(0, 6):
            self.root.rowconfigure(r, weight=1)

        self.root.columnconfigure(0, weight=2, minsize=250)

        # Initialise the buttons with the existing data.
        self.change_difficulty(self.data.difficulty)
        self.change_highlight(self.data.highlight)
        self.set_gaps(self.data.button_gaps)
        self.set_outlines(self.data.button_outlines)

        self.root.mainloop()

    def save_and_exit(self):
        # Validate, save, and exit the settings window.
        self.root.destroy()

    def set_outlines(self, value):
        if (value == False):
            self.button_outlines_btn.configure(
                bg="#2b2b2b", fg="#ffffff", text="OFF")
        else:
            self.button_outlines_btn.configure(
                bg="#ffffff", fg="#2b2b2b", text="ON")
        self.data.button_outlines = value

    def toggle_outlines(self):
        # Toggle the outlines setting.
        if (self.button_outlines_btn["text"] == "ON"):
            # Currently on, turn it off.
            self.set_outlines(False)
        else:
            # Currently off, turn it on.
            self.set_outlines(True)

    def set_gaps(self, value):
        if (value == False):
            self.button_gaps_btn.configure(
                bg="#2b2b2b", fg="#ffffff", text="OFF")
        else:
            self.button_gaps_btn.configure(
                bg="#ffffff", fg="#2b2b2b", text="ON")
        self.data.button_gaps = value

    def toggle_gaps(self):
        # Toggle the gaps setting.
        if (self.button_gaps_btn["text"] == "ON"):
            # Currently on, turn it off.
            self.set_gaps(False)
        else:
            # Currently off, turn it on.
            self.set_gaps(True)

    def change_highlight(self, mode):
        # Change the highlights setting.
        if (mode == "color"):
            self.highlight_color_btn.configure(bg="#ffffff", fg="#2b2b2b")
            self.highlight_dot_btn.configure(bg="#2b2b2b", fg="#ffffff")
            self.highlight_none_btn.configure(bg="#2b2b2b", fg="#ffffff")
        elif (mode == "dot"):
            self.highlight_color_btn.configure(bg="#2b2b2b", fg="#ffffff")
            self.highlight_dot_btn.configure(bg="#ffffff", fg="#2b2b2b")
            self.highlight_none_btn.configure(bg="#2b2b2b", fg="#ffffff")
        elif (mode == "none"):
            self.highlight_color_btn.configure(bg="#2b2b2b", fg="#ffffff")
            self.highlight_dot_btn.configure(bg="#2b2b2b", fg="#ffffff")
            self.highlight_none_btn.configure(bg="#ffffff", fg="#2b2b2b")

        self.data.highlight = mode

    def change_difficulty(self, difficulty):
        # Change the difficulty setting.
        if (difficulty == 0.5):
            self.difficulty_easy_btn.configure(bg="#33d17a", fg="#2b2b2b")
            self.difficulty_normal_btn.configure(bg="#2b2b2b", fg="#f6d32d")
            self.difficulty_hard_btn.configure(bg="#2b2b2b", fg="#e01b24")
        elif (difficulty == 1.0):
            self.difficulty_easy_btn.configure(bg="#2b2b2b", fg="#33d17a")
            self.difficulty_normal_btn.configure(bg="#f6d32d", fg="#2b2b2b")
            self.difficulty_hard_btn.configure(bg="#2b2b2b", fg="#e01b24")
        elif (difficulty == 2.0):
            self.difficulty_easy_btn.configure(bg="#2b2b2b", fg="#33d17a")
            self.difficulty_normal_btn.configure(bg="#2b2b2b", fg="#f6d32d")
            self.difficulty_hard_btn.configure(bg="#e01b24", fg="#2b2b2b")

        self.data.difficulty = difficulty


class ScoreWindow(Window):
    # This class contains the highscore window, viewed when clicking "Highscores" on the main menu.
    # It gathers its' data from the Data class.
    def __init__(self, data):
        Window.__init__(self, "High Score", 500, 500)

        self.data = data

        # Create the title.
        title = tk.Label(self.root, text="High Score",
                         font=("IBM Plex Sans", 30), bg="#2b2b2b", fg="#ffffff", justify="center")
        title.grid(row=0, column=0)

        # Show the highscore.
        self.score = tk.Label(self.root, text=f"Your highscore:\n{self.data.highscore}",
                              font=("IBM Plex Sans", 24), bg="#2b2b2b", fg="#ffffff", justify="center")
        self.score.grid(row=1, column=0)

        # Create the reset button.
        self.reset_clicks = 0
        self.reset = tk.Button(
            self.root, font=("IBM Plex Sans", 20), relief="flat", text="Reset Highscore",
            command=self.reset, fg="#e01b24", bg="#2b2b2b", highlightbackground="#e01b24")
        self.reset.grid(row=2, column=0)

        # Create the back button.
        exit = Window.Button(self.root, text="Back to Menu",
                             command=self.back)
        exit.grid(row=3, column=0)

        # Set weights for the grid.
        for r in range(0, 4):
            self.root.rowconfigure(r, weight=1)

        self.root.columnconfigure(0, weight=1, minsize=250)

        self.root.mainloop()

    def back(self):
        # Close this window.
        self.root.destroy()

    def reset(self):
        if (self.reset_clicks == 0):
            # First click. Change button to "armed" state.
            self.reset.configure(
                text="Are you sure?", bg="#e01b24", fg="#2b2b2b", highlightbackground="#e01b24")
            self.reset_clicks = 1
        elif (self.reset_clicks == 1):
            # Second click. Actually reset!
            self.data.highscore = 3
            # Show the updated score.
            self.score.configure(
                text=f"Your highscore:\n{self.data.highscore}")
            self.reset.configure(
                text="Highscore Reset", bg="#2b2b2b", fg="#424242", highlightbackground="#424242", state="disabled")


    # RUNNING
if __name__ == "__main__":
    # Run the game.
    application = Application()
