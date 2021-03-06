# Visage
# a color game by Conor Eager
# Developed for 91906 Complex Programming Techniques, for Level 3 Computer Science.

# IMPORTS
# Import Tk for graphical user interfaces
import pathlib
import tkinter as tk

# Import random for random generation of colors
import random

# Import pickle for saving and loading of user data & game state
import pickle

# Import one function from os for finding the data file
# From https://stackoverflow.com/a/4028943/7311875
import os.path

# CLASSES


class Application:
    """This class contains the entire application. It calls the main menu, and handles initial loading of data.
    """

    def __init__(self):
        """Initialise game state, including loading data.
        """
        Application.data = Data()
        Application.data.load()

        # Open the main menu.
        self.main_menu = MainMenuWindow(self)


class Data:
    """This class is responsible for all the data stored for the game.
    It contains methods for saving and loading data to/from persistent storage,
    and for modifying and reading data (e.g. settings, highscores).
    """

    def __init__(self):
        # Set the defaults.
        self.button_outlines = False
        self.button_gaps = True
        self.highlight = "dot"
        self.difficulty = 1.0
        self.highscore = 3

    def resolve_save_location(self):
        """Resolve the location of the user's save file.
        This is their home directory plus the name of the save file ("visage_save.data").

        Returns:
            String: The absolute path to the save file.
        """
        return os.path.join(os.path.expanduser("~"), "visage_save.data")

    def save(self):
        """Save the game state to persistent storage.
        """

        # First, get the location to save to. This is the user's home directory.
        # From https://stackoverflow.com/a/4028943/7311875
        location = self.resolve_save_location()

        # Open the file to save to.
        try:
            with open(location, "wb") as file:
                # Now save the entire contents of the Data class to a Pickle file in that location.
                pickle.dump(self, file)
        except Exception as e:
            # If there's an error, alert the user.
            msg = MessageWindow(
                "Error", f"Could not save Visage data at\n'{location}'.\nYour progress and settings have not been saved. Please check that you have permission to write to this directory/file.\nIf you would like to try to save again, press 'Try Again'. To exit without saving your data, press 'Exit Without Saving'.\n\nMore details on the error can be seen below:\n{e}", 1000, 600, "Exit Without Saving", second_button={'text': 'Try Again', 'command': self.save})

    def load(self):
        """Load the game state from persistent storage.
        """

        # First, get the location to load from. This is the user's home directory.
        # From https://stackoverflow.com/a/4028943/7311875
        location = self.resolve_save_location()

        # Open the file to read from.
        try:
            with open(location, "rb") as file:
                # Now load the entire contents of the Pickle file into the Data class.
                Application.data = pickle.load(file)
        except FileNotFoundError:
            # No savefile exists.
            msg = MessageWindow(
                "Information", f"No Visage savefile was found. A new save file will be created at\n'{location}'.\nGame data, including scores & settings, is saved automatically.\nPlease ensure you have access to this location and that your\naccount has the necessary permissions to read/write data there.", 1000, 600, "Continue")
        except Exception as e:
            # If there's an error, alert the user.
            msg = MessageWindow(
                "Error", f"A Visage save file was found at\n'{location}',\nbut it could not be read.\nPlease check you have permission to access this file and that it has not been edited.\nIf you would like to try to load again, press 'Try Again'. To continue without loading your data, press 'Continue Without Loading'.\n\nMore details on the error can be seen below:\n{e}", 1000, 600, "Continue Without Loading", second_button={'text': 'Try Again', 'command': self.load})


class Window:
    """This class contains code for a basic window.
    Any elements or configuration that should be applied across all windows is done here.
    """

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
        """Generate a new tk.Button with some sensible defaults set. This ensures that all buttons are consistent
        across the game UI, and eliminates the need to copy/paste arguments all over the place.

        Args:
            parent (tk.<container>): The container that the new button will be created as a child of.
            fontsize (int, optional): The font size of the text on the button. Defaults to 20.

        Returns:
            tk.Button: The newly generated button.
        """
        return tk.Button(parent, font=("IBM Plex Sans", fontsize), bg="#2b2b2b", fg="#ffffff", relief="flat", **kwargs)


class MessageWindow(Window):
    """This class contains code for a single-message window to inform the user of
    an important notice (e.g. save file not found).

    Inherits Window.
    """

    def __init__(self, title, text, width, height, buttontext="OK", second_button={}):
        """Creates a new MessageWindow.

        Args:
            title (str): The title of the window (shown in the window decorations).
            text (str): The main body text of the window.
            width (int): The width, in pixels, of the message window.
            height (int): The height, in pixels, of the message window.
            buttontext (str, optional): The text to show on the button in the window. Defaults to "OK".
            second_button (dict, optional): An optional second button to show, used for cases where a
            second button is required (e.g. "Try Again"). Defaults to {} (no button).
        """
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
    """This class contains the main menu.
    It can call back to the Application class to start the game.

    Inherits Window.
    """

    def __init__(self, application):
        """Open the main menu window.

        Args:
            application (Application): The global application instance, containing references to Data.
        """
        # Perform initialisation using the Window parent class.
        Window.__init__(self, "Main Menu", 500, 600)

        self.application = application

        # Alias the close button to quit()
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Create the frame to keep everything in the centre.
        frame = tk.Frame(self.root, bg="#2b2b2b")
        frame.grid(row=0, column=0)

        # Create the logo image.

        # Resolve the file path of the logo, based on the current working directory.
        # Without this, the game would not run with the wrong working directory (i.e. not the same as the script).
        # This special function is needed to ensure that the directory separators are correct
        # ('/' on Mac and Unix systems, and '\' on Windows)
        #          Join...      the current location of the script...    with the filename.
        img_path = os.path.join(pathlib.Path(
            __file__).parent.resolve(), "logo.png")

        logo = tk.PhotoImage(file=img_path)
        logo_label = tk.Label(frame, image=logo, bg="#2b2b2b")
        # Place it in the grid.
        logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Create the main menu buttons.
        btn_play = Window.Button(
            frame, text="Play", command=self.play, width=25)
        btn_highscores = Window.Button(
            frame, text="Highscores", command=self.highscores, width=25)
        btn_settings = Window.Button(
            frame, text="Options", command=self.settings, width=25)
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
        """Start the game.
        """
        self.root.destroy()
        game = GameWindow(self.application.data)

        # Once the game closes, reopen the main menu.
        self.__init__(self.application)

    def highscores(self):
        """Open the highscores window.
        """
        self.root.destroy()
        scorewindow = ScoreWindow(self.application.data)

        # Once the score window closes, reopen the main menu.
        self.__init__(self.application)

    def settings(self):
        """Open the settings window.
        """
        self.root.destroy()
        settings = SettingsWindow(self.application.data)

        # Once settings closes, reopen the main menu.
        self.__init__(self.application)

    def quit(self):
        """Quit the game, saving data in the process.
        """
        self.root.destroy()
        self.application.data.save()


class GameWindow(Window):
    """This class contains the game window itself.

    Inherits Window.
    """

    def __init__(self, data):
        """Open the game window.

        Args:
            data (Data): A reference to the global Data object, to get settings & highscores.
        """
        # Perform initialisation using the Window parent class.
        Window.__init__(self, "Play", 500, 500)

        self.data = data

        # Alias the close button to quit()
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Lives counter.
        self.lives = round(3 / self.data.difficulty)

        if (self.lives > 10):
            self.lives = 10
        elif (self.lives < 1):
            self.lives = 1

        # Generate a difficulty description for use in the UI.
        if (self.data.difficulty <= 0.75):
            self.difficulty_str = "Easy"
        elif (self.data.difficulty <= 1.25):
            self.difficulty_str = "Normal"
        elif (self.data.difficulty <= 3.0):
            self.difficulty_str = "Hard"
        elif (self.data.difficulty <= 4.0):
            self.difficulty_str = "Very Hard"
        else:
            self.difficulty_str = "Insane"

        self.difficulty_str += f" ({int(self.data.difficulty * 10)})"

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
                                   text=f"{'???'*self.lives}\nDifficulty: {self.difficulty_str}", font=("IBM Plex Sans", 10), width=20, padx=10, pady=10)
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
        """Generate a new set of buttons according to the current level,
        difficulty, and settings.

        Args:
            level (int): The current game level.
            data (Data): A reference to the global Data object, containing settings & highscores.
        """
        self.busy = True

        original_color_ok = False
        different_color_ok = False

        # Create a 2D array to store the buttons.
        self.buttons = list()

        while original_color_ok is False:
            # Set loading message.
            self.help_label.configure(
                text=f"Loading...\nColors (1/2)", bg="#ffffff", fg="#2b2b2b")

            # Reset the frame, clearing the existing buttons.
            # First, destroy the old frame (and all the buttons in it):
            self.frame.destroy()
            # Then, create a new frame to replace it:
            self.frame = tk.Frame(self.root, bg="#2b2b2b")
            self.frame.grid(row=0, column=0, columnspan=3)
            self.root.update()

            # Generate the "correct" color.
            original_color = [
                random.randint(0x00, 0xff), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
            # Convert it to a string for use with Tk.
            original_color_str = f"#{original_color[0]:02X}{original_color[1]:02X}{original_color[2]:02X}"

            self.help_label.configure(
                text=f"Loading...\nColors (2/2)")

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

        self.help_label.configure(
            text=f"Loading...(2/4)\nSetting up")

        # Choose which button will be incorrect.
        self.diff_btn_row = random.randint(0, level-1)
        self.diff_btn_col = random.randint(0, level-1)

        # Configure row/column weights for the inner frame:
        for i in range(0, level):
            self.frame.rowconfigure(i, weight=1)
            self.frame.columnconfigure(i, weight=1)

        # Check settings for creating buttons.
        padding = 1 if data.button_gaps is True else 0
        outlines = 1 if data.button_outlines is True else 0

        self.help_label.configure(
            text=f"Loading...\nButtons (000/{level**2:03})")

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
                                   relief="flat", text="???", font=("IBM Plex Sans", round(100/level)), command=lambda x=row, y=col: self.check_color(x, y), width=100, height=100)

                button.grid(row=row, column=col, padx=padding, pady=padding)

                # Save the button to the list.
                self.buttons[row].append(button)

                # Update the progress indicator.
                self.help_label.configure(
                    text=f"Loading...\nButtons ({(row*level)+col:03}/{level**2:03})", bg="#ffffff", fg="#2b2b2b")
                self.help_label.update()

        self.help_label.configure(
            text=f"Loading...\nFinishing")

        self.busy = False

        self.help_label.configure(
            text=f"{'???'*self.lives}\nDifficulty: {self.difficulty_str}", bg="#2b2b2b", fg="#ffffff")

    def quit(self):
        """Quit the game, saving the highscore if necessary.
        """
        # Is this a new highscore?
        if ((self.level * self.data.difficulty) >= self.data.highscore):
            self.data.highscore = self.level * self.data.difficulty
        self.root.destroy()
        self.data.save()

    def game_over(self):
        """Game over!
        Show the game over screen.
        """
        # Game over! Show the user's score, and save it.
        self.frame = tk.Frame(self.root, bg="#2b2b2b")
        self.frame.grid(row=0, column=0, columnspan=3)
        self.root.update()

        game_over_text = tk.Label(
            self.frame, text=f"Game over!", bg="#2b2b2b", fg="#ffffff", font=("IBM Plex Sans", 30))
        game_over_text.grid(row=0, column=0)

        score_text = tk.Label(
            self.frame, text=f"Level {self.level}\n on {self.difficulty_str} difficulty\n= Score: {(self.level * self.data.difficulty)}", bg="#2b2b2b", fg="#ffffff", font=("IBM Plex Sans", 24))
        score_text.grid(row=1, column=0)

        next_steps_text = tk.Label(
            self.frame, text=f"Press Quit to return\nto the main menu.", bg="#2b2b2b", fg="#ffffff", font=("IBM Plex Sans", 18))
        next_steps_text.grid(row=2, column=0)

    def check_color(self, row, col):
        """Check the clicked button, if it's the correct button.

        Args:
            row (int): The row number of the clicked button.
            col (int): The column number of the clicked button.
        """
        if (self.busy is True):
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
            # Set busy to disallow clicks
            self.busy = True
            self.score_label.configure(
                text="Incorrect...",  fg="#e01b24")

            self.lives -= 1

            # Indicate where the incorrect button is by flashing a dot on it.
            self.buttons[self.diff_btn_row][self.diff_btn_col].configure(
                fg="#ffffff", text="???")
            self.root.after(
                500, lambda: self.buttons[self.diff_btn_row][self.diff_btn_col].configure(text=""))
            self.root.after(
                1000, lambda: self.buttons[self.diff_btn_row][self.diff_btn_col].configure(text="???"))
            self.root.after(
                1500, lambda: self.buttons[self.diff_btn_row][self.diff_btn_col].configure(text=""))
            self.root.after(
                2000, lambda: self.buttons[self.diff_btn_row][self.diff_btn_col].configure(text="???"))

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
    """This class contains the Settings window.

    Inherits Window.
    """

    def __init__(self, data):
        """Open the Settings window.

        Args:
            data (Data): A reference to the global Data object, which contains settings & highscores.
        """
        # Perform initialisation using the Window parent class.
        Window.__init__(self, "Options", 700, 500)

        self.data = data

        # Alias the close button to save_and_exit()
        self.root.protocol("WM_DELETE_WINDOW", self.save_and_exit)

        # Create the title.
        self.title = tk.Label(self.root, text="Options",
                              font=("IBM Plex Sans", 30), bg="#2b2b2b", fg="#ffffff", justify="center")
        self.title.grid(row=0, column=0, columnspan=6)

        # Create the save & exit button.
        self.exit = Window.Button(self.root, text="Save & Exit",
                                  command=self.save_and_exit)
        self.exit.grid(row=6, column=0, columnspan=6)

        # Create the setting labels.
        label_text = ["Button outlines:", "Gaps between buttons:",
                      "Hover highlight type:", "Game difficulty preset:", "...or set a custom value (2-50):"]
        for t in range(len(label_text)):
            label = tk.Label(
                self.root, text=label_text[t], font=("IBM Plex Sans", 16), bg="#2b2b2b", fg="#ffffff", justify="left")
            label.grid(row=t+1, column=0, columnspan=3)

        # Create the option buttons.
        # Button outlines:
        self.button_outlines_btn = Window.Button(
            self.root, 16, text="Off", command=self.toggle_outlines, width=5)
        self.button_outlines_btn.grid(row=1, column=4)

        # Button gaps:
        self.button_gaps_btn = Window.Button(
            self.root, 16, text="On", command=self.toggle_gaps, width=5)
        self.button_gaps_btn.grid(row=2, column=4)

        # Highlights:
        self.highlight_color_btn = Window.Button(
            self.root, 16, text="Color", command=lambda x="color": self.change_highlight(x), width=5)
        self.highlight_dot_btn = Window.Button(
            self.root, 16, text="Dot", command=lambda x="dot": self.change_highlight(x), width=5)
        self.highlight_none_btn = Window.Button(
            self.root, 16, text="None", command=lambda x="none": self.change_highlight(x), width=5)
        self.highlight_color_btn.grid(row=3, column=3)
        self.highlight_dot_btn.grid(row=3, column=4)
        self.highlight_none_btn.grid(row=3, column=5)

        # Difficulty presets:
        self.difficulty_easy_btn = tk.Button(
            self.root, font=("IBM Plex Sans", 16), relief="flat", text="Easy",
            command=lambda x=5: self.change_difficulty(x, True), width=5, fg="#33d17a", bg="#2b2b2b", highlightbackground="#33d17a")
        self.difficulty_normal_btn = tk.Button(
            self.root, font=("IBM Plex Sans", 16), relief="flat", text="Normal",
            command=lambda x=10: self.change_difficulty(x, True), width=5, fg="#f6d32d", bg="#2b2b2b", highlightbackground="#f6d32d")
        self.difficulty_hard_btn = tk.Button(
            self.root, font=("IBM Plex Sans", 16), relief="flat", text="Hard",
            command=lambda x=20: self.change_difficulty(x, True), width=5, fg="#e01b24", bg="#2b2b2b", highlightbackground="#e01b24")
        self.difficulty_easy_btn.grid(row=4, column=3)
        self.difficulty_normal_btn.grid(row=4, column=4)
        self.difficulty_hard_btn.grid(row=4, column=5)

        # Difficulty spinbox:
        self.difficulty_spinbox = tk.Spinbox(
            self.root, font=("IBM Plex Sans", 16), relief="flat", from_=2, to=50, increment=1, width=5, fg="#ffffff", bg="#2b2b2b", highlightbackground="#ffffff", buttonbackground="#2b2b2b", validate="key")
        self.difficulty_spinbox["validatecommand"] = (
            self.root.register(self.validate_difficulty), '%P')
        self.difficulty_spinbox.grid(row=5, column=3, columnspan=3)

        # Set weights for the grid.
        for c in range(0, 6):
            self.root.columnconfigure(c, weight=1)
        for r in range(0, 7):
            self.root.rowconfigure(r, weight=1)

        self.root.columnconfigure(0, weight=2, minsize=250)

        # Initialise the buttons with the existing data.
        self.change_difficulty(int(self.data.difficulty * 10), True)
        self.change_highlight(self.data.highlight)
        self.set_gaps(self.data.button_gaps)
        self.set_outlines(self.data.button_outlines)

        self.root.mainloop()

    def save_and_exit(self):
        """Save and exit the settings window.
        """
        # Validate, save, and exit the settings window.
        if (self.exit["state"] == "disabled"):
            # An invalid setting. Don't exit.
            pass
        else:
            # Close the window.
            self.root.destroy()
            # Save data.
            self.data.save()

    def set_outlines(self, value):
        """Set the button outlines setting.

        Args:
            value (bool): The value to set the option to.
        """
        if (value is False):
            self.button_outlines_btn.configure(
                bg="#2b2b2b", fg="#ffffff", text="Off")
        else:
            self.button_outlines_btn.configure(
                bg="#ffffff", fg="#2b2b2b", text="On")
        self.data.button_outlines = value

    def toggle_outlines(self):
        """Toggle the button outlines setting.
        """
        # Toggle the outlines setting.
        if (self.button_outlines_btn["text"] == "On"):
            # Currently on, turn it off.
            self.set_outlines(False)
        else:
            # Currently off, turn it on.
            self.set_outlines(True)

    def set_gaps(self, value):
        """Set the button gaps setting.

        Args:
            value (bool): The value to set the option to.
        """
        if (value is False):
            self.button_gaps_btn.configure(
                bg="#2b2b2b", fg="#ffffff", text="Off")
        else:
            self.button_gaps_btn.configure(
                bg="#ffffff", fg="#2b2b2b", text="On")
        self.data.button_gaps = value

    def toggle_gaps(self):
        """Toggle the button gaps setting.
        """
        # Toggle the gaps setting.
        if (self.button_gaps_btn["text"] == "On"):
            # Currently on, turn it off.
            self.set_gaps(False)
        else:
            # Currently off, turn it on.
            self.set_gaps(True)

    def change_highlight(self, mode):
        """Change the button highlight setting.

        Args:
            mode (str): The mode to set the setting to.
        """
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

    def change_difficulty(self, difficulty, overwrite=False):
        """Change the difficulty setting.

        Args:
            difficulty (int): The difficulty to set the setting to.
            overwrite (bool, optional): Whether to overwrite the spinbox for the new value. Only set to True if triggered by clicking a preset. Defaults to False.
        """
        # Change the difficulty setting.

        # Convert difficulty to an integer.
        difficulty = int(difficulty)

        if (overwrite):
            # If this was triggered by a preset, then overwrite the spinbox contents.
            # Otherwise, don't.
            self.difficulty_spinbox.delete(0, "end")
            self.difficulty_spinbox.insert(0, difficulty)

        # If the current value matches a preset, highlight that button.
        if (difficulty == 5):
            self.difficulty_easy_btn.configure(bg="#33d17a", fg="#2b2b2b")
            self.difficulty_normal_btn.configure(bg="#2b2b2b", fg="#f6d32d")
            self.difficulty_hard_btn.configure(bg="#2b2b2b", fg="#e01b24")
        elif (difficulty == 10):
            self.difficulty_easy_btn.configure(bg="#2b2b2b", fg="#33d17a")
            self.difficulty_normal_btn.configure(bg="#f6d32d", fg="#2b2b2b")
            self.difficulty_hard_btn.configure(bg="#2b2b2b", fg="#e01b24")
        elif (difficulty == 20):
            self.difficulty_easy_btn.configure(bg="#2b2b2b", fg="#33d17a")
            self.difficulty_normal_btn.configure(bg="#2b2b2b", fg="#f6d32d")
            self.difficulty_hard_btn.configure(bg="#e01b24", fg="#2b2b2b")
        else:
            self.difficulty_easy_btn.configure(bg="#2b2b2b", fg="#33d17a")
            self.difficulty_normal_btn.configure(bg="#2b2b2b", fg="#f6d32d")
            self.difficulty_hard_btn.configure(bg="#2b2b2b", fg="#e01b24")

        # Update the setting value.
        self.data.difficulty = float(int(difficulty) / 10)

    def validate_difficulty(self, value):
        """Validate the entered difficulty value.
        Ensure that it is not:
        - less than 2 or greater than 50
        - or a non-number (empty, text, etc.)
        If successful, will update the difficulty and change the buttons accordingly.
        if unsuccessful, will disable the Save & Exit button and change the outline of the spinbox
        to indicate the error.

        Args:
            value (Any): The value to check.

        Returns:
            True: This will be always True, to allow the input to the box. 
            Returning False will cancel the input, which is confusing to the end user.
        """

        # Set our valid state, default to valid.
        valid = True

        # Check for float-ness
        if (not value.isdigit()):
            valid = False

        try:
            # Check for bounds
            if (int(value) < 2 or int(value) > 50):
                valid = False

        except ValueError:
            valid = False

        # Finally, apply the result.
        # It's valid:
        if (valid):
            self.exit.configure(
                state="normal", fg="#ffffff", bg="#2b2b2b", highlightbackground="#ffffff", text="Save & Exit")
            self.difficulty_spinbox.configure(
                fg="#ffffff", bg="#2b2b2b", highlightbackground="#ffffff")
            self.change_difficulty(value)
        # It's not valid:
        elif (not valid):
            self.exit.configure(
                state="disabled", fg="#424242", bg="#2b2b2b", highlightbackground="#424242", text="Invalid Difficulty")
            self.difficulty_spinbox.configure(
                fg="#e01b24", bg="#2b2b2b", highlightbackground="#e01b24")

        return True


class ScoreWindow(Window):
    """This class contains the score window which shows highscores.

    Inherits Window.
    """
    # This class contains the highscore window, viewed when clicking "Highscores" on the main menu.
    # It gathers its' data from the Data class.

    def __init__(self, data):
        """Open the Score window.

        Args:
            data (Data): A reference to the global Data object, containing settings & scores.
        """
        Window.__init__(self, "High Score", 500, 500)

        self.data = data

        # Alias the close button to quit()
        self.root.protocol("WM_DELETE_WINDOW", self.back)

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
        """Close the score window.
        """
        # Close this window.
        self.root.destroy()

    def reset(self):
        """Process a click on the reset button.
        If this is the first click, "arm" the button, but don't reset.
        If this is the second click (the button is already "armed"), reset the highscore.
        """
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
