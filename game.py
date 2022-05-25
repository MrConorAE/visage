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
        self.root.geometry(f"{width}x{height}")
        # Set the visual aspects of the window:
        self.root.configure(bg="#2b2b2b")
        # Set the window to non-resizable.
        self.root.resizable(False, False)
        # Set up the font.
        self.font = ("IBM Plex Sans", 20)

    def Button(parent, **kwargs):
        # Create a button with the default options.
        return tk.Button(parent, font=("IBM Plex Sans", 20), bg="#2b2b2b", fg="#ffffff", relief="flat", **kwargs)


class MainMenuWindow(Window):
    # This class contains the main menu.
    # It can call back to the Application class to start the game.
    def __init__(self):
        # Open the main menu window.
        # Perform initialisation using the Window parent class.
        Window.__init__(self, "Main Menu", 500, 500)

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
        pass

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
application = Application()
