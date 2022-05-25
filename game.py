###  Visage ###
# a color game by Conor Eager
# Developed for 91906 Complex Programming Techniques, for Level 3 Computer Science.

class Application:
    # This class is the main class for the game.
    # It calls other classes for the main menu, game, settings, and highscore screens.
    pass


class Data:
    # This class is responsible for all the data stored for the game.
    # It contains methods for saving and loading data to/from persistent storage,
    # and for modifying and reading data (e.g. settings, highscores).
    pass


class Window:
    # This class contains code for a basic window.
    # Any elements or configuration that should be applied across all windows is done here.
    pass


class MainMenuWindow(Window):
    # This class contains the main menu.
    # It can call back to the Application class to start the game.
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
