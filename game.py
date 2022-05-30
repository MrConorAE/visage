###  Visage ###
# a color game by Conor Eager
# Developed for 91906 Complex Programming Techniques, for Level 3 Computer Science.

# IMPORTS
# Import Tk for graphical user interfaces
import tkinter as tk

# Import random for random generation of colors
import random

# Import time for accurate timers
import time


# CLASSES

class Application:
    # This class is the main class for the game.
    # It calls other classes for the main menu, game, settings, and highscore screens.
    def __init__(self):
        # Initialise game state, including loading data.
        # self.data = Data()
        # self.data.load()

        # Open the main menu.
        self.main_menu = MainMenuWindow()


class Data:
    # This class is responsible for all the data stored for the game.
    # It contains methods for saving and loading data to/from persistent storage,
    # and for modifying and reading data (e.g. settings, highscores).
    pass


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


class MainMenuWindow(Window):
    # This class contains the main menu.
    # It can call back to the Application class to start the game.
    def __init__(self):
        # Open the main menu window.
        # Perform initialisation using the Window parent class.
        Window.__init__(self, "Main Menu", 500, 600)

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
        self.game = GameWindow()

    def highscores(self):
        # Open the highscores window.
        pass

    def settings(self):
        # Open the settings window.
        pass

    def quit(self):
        # Quit the game.
        pass


class GameWindow(Window):
    # This class is the game itself.
    # It contains the game loop, and can call back to Application or Data for the game state.
    def __init__(self):
        # Open the main menu window.
        # Perform initialisation using the Window parent class.
        Window.__init__(self, "Play", 500, 500)

        # Initialise difficulty counter.
        self.difficulty = 3

        # Create the frame for the buttons.
        self.frame = tk.Frame(self.root, bg="#2b2b2b", width=400, height=400)
        self.frame.grid(row=0, column=0, columnspan=3, sticky="NESW")

        # Score label
        self.score_label = tk.Label(self.root, bg="#2b2b2b", fg="#ffffff",
                                    text=f"Level {self.difficulty}", font=("IBM Plex Sans", 20))
        self.score_label.grid(row=2, column=1, padx=20, pady=20)

        # Help label
        self.help_label = tk.Label(self.root, bg="#2b2b2b", fg="#ffffff",
                                   text="Click the odd one out!", font=("IBM Plex Sans", 10), padx=10, pady=10)
        self.help_label.grid(row=2, column=2, padx=20, pady=20)

        # Create the main menu buttons.
        btn_quit = Window.Button(
            self.root, 10, text="Quit", command=self.quit)
        # Place them in the grid.
        btn_quit.grid(row=2, column=0, padx=20, pady=20)

        # Configure row/column weights to centre content
        self.root.rowconfigure(0, weight=1, minsize=100)
        self.root.rowconfigure(0, weight=1)
        for col in range(0, 3):
            self.root.columnconfigure(col, weight=1)

        # Generate colors.
        self.generate_buttons(self.difficulty)

        # Keep the window open, waiting for something to happen.
        # This is blocking because we don't need to do anything else.
        # TODO: implement main loop.
        self.root.mainloop()

    def generate_buttons(self, difficulty):
        # Generate a new set of color buttons according to difficulty.
        # Set loading message.
        self.help_label.configure(
            text=f"Loading (000/{difficulty**2:03})", bg="#ffffff", fg="#2b2b2b")

        # Reset the frame, clearing the existing buttons:
        self.frame = tk.Frame(self.root, bg="#2b2b2b")
        self.frame.grid(row=0, column=0, columnspan=3)
        self.root.update()

        # Calculate the size the buttons should be:
        size = round(100 / difficulty)

        # Generate the "correct" color.
        original_color = [
            random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
        # Convert it to a string for use with Tk.
        original_color_str = f"#{original_color[0]:02X}{original_color[1]:02X}{original_color[2]:02X}"

        # Generate a color.
        while True:
            # Generate the "incorrect" color.
            # Choose which part to change:
            component_to_change = random.randint(0, 2)
            # How much to change it by:
            change_it_by = round(0xFF / difficulty)
            # Change by pos or neg?
            add_or_subtract = random.choice([-1, 1])

            different_color = original_color
            # Generate the new color, using the correct color as a base.
            different_color[component_to_change] = round(
                original_color[component_to_change] + (change_it_by * add_or_subtract))

            # If the result is over 255 or under 0, over/underflow it by wrapping around.
            if (different_color[component_to_change] > 0xFF) or (different_color[component_to_change] < 0x00):
                different_color[component_to_change] = round(
                    different_color[component_to_change] % 0xFF)

            # Convert it to a string for use with Tk.
            different_color_str = f"#{different_color[0]:02X}{different_color[1]:02X}{different_color[2]:02X}"

            if (different_color_str == original_color_str):
                # Identical color, start again.
                continue

            if len(different_color_str) != 7:
                # Invalid color, start again.
                continue

            # Valid color! Break.
            break

        # Choose which button will be incorrect.
        self.diff_btn_row = random.randint(0, difficulty-1)
        self.diff_btn_col = random.randint(0, difficulty-1)

        print("Colors done")

        # Configure row/column weights for the inner frame:
        for i in range(0, difficulty):
            self.frame.rowconfigure(i, weight=1)
            self.frame.columnconfigure(i, weight=1)

        # Generate the buttons:
        for row in range(0, difficulty):
            for col in range(0, difficulty):
                # Choose the color for this button.
                # Is this the wrong button?
                if (row == self.diff_btn_row and col == self.diff_btn_col):
                    color = different_color_str
                else:
                    color = original_color_str
                button = tk.Button(self.frame, bg=color, fg=color, highlightthickness=0, activebackground=color, activeforeground="#ffffff",
                                   relief="flat", text="●", font=("IBM Plex Sans", round(100/difficulty)), command=lambda x=row, y=col: self.check_color(x, y), width=size, height=size)
                button.grid(row=row, column=col, padx=1, pady=1)
                self.help_label.configure(
                    text=f"Loading ({(row*difficulty)+col:03}/{difficulty**2:03})", bg="#ffffff", fg="#2b2b2b")
                self.help_label.update()

        print("Buttons done")

        self.help_label.configure(
            text="Click the odd one out!", bg="#2b2b2b", fg="#ffffff")

    def quit(self):
        # Quit the game.
        # TODO: Save score and reopen main menu.
        self.root.destroy()

    def check_color(self, row, col):
        print("Click!")
        if (row == self.diff_btn_row and col == self.diff_btn_col):
            # Different color: correct choice!
            # TODO: Start the next level
            self.difficulty += 1
            self.score_label["text"] = f"Level {self.difficulty}"
            self.generate_buttons(self.difficulty)
        else:
            # Original color: incorrect.
            # TODO: Alert the user and exit.
            pass


class SettingsWindow(Window):
    # This class contains the settings window.
    # It can call back to Application or Data to change the game settings.
    pass


class ScoreWindow(Window):
    # This class contains the score window, shown at the end of the game.
    # It can call back to Application when done, and Data to save the score.
    pass


# RUNNING
if __name__ == "__main__":
    # Run the game.
    application = Application()
