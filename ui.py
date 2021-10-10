from tkinter import *
from tkinter import messagebox

from settings import Color


class Window(Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.config_window()
        self.create_widgets()
        self.setup_widgets_layout()
        self.bind_functions()
        # Initialize game : Pick a word, highlight it and enter the countdown event
        self.active_word = self.game.list_of_words[0]
        word_starting_position, word_ending_position = self.determine_word_position(self.active_word)
        # Now we send theses two indexes values to our highlight function
        self.highlight_current_word(word_starting_position, word_ending_position)
        # Enter the countdown event
        self.count_down()

        self.mainloop()

    def config_window(self):
        self.config(padx=20, pady=20)
        self.resizable(False, False)
        self.title("Typing Speed Test")

    def create_widgets(self):
        # ---------------------------- LABELS ------------------------------- #
        self.correct_label = Label(text=f'Correct words: {self.game.correct_words}')
        self.incorrect_label = Label(text=f'Incorrect words: {self.game.incorrect_words}')
        self.timer_label = Label(text=f"Timer: {self.game.timer}")
        # ---------------------------- TEXT ------------------------------- #
        self.text_display = Text(height=7, width=30)
        self.text_display.insert(INSERT, self.game.game_text)
        self.text_display.config(font=('Helvetica bold', 14), padx=30, wrap=WORD)
        # Center text in the Text widget
        self.text_display.tag_configure("center", justify='center')
        # Specify which part needs to be centered: in our case from beginning to end
        self.text_display.tag_add("center", 1.0, "end")
        # ---------------------------- ENTRY ------------------------------- #
        self.text_entry = Entry(width=65)
        # Set the text entry as the active widget so the user doesnt have to click on it to start the game
        self.text_entry.focus_set()

    def setup_widgets_layout(self):
        self.correct_label.grid(row=0, column=0)
        self.incorrect_label.grid(row=0, column=1)
        self.timer_label.grid(row=0, column=2)
        self.text_display.grid(row=1, column=0, columnspan=3)
        self.text_entry.grid(row=2, column=0, pady=20, columnspan=3)

    def bind_functions(self):
        # Catch space bar press to submit typed word for comparison
        self.bind("<space>", self.compare_words)
        # Catch any keypress to start the game
        self.bind("<KeyPress>", self.start_game)

    def calc_accuracy(self):
        """
        :returns accuracy: The percentage (integer) of correctly typed words.
        """
        if self.game.current_word_id > 0:
            return round(self.game.correct_words / self.game.current_word_id * 100)
        return self.game.accuracy

    def compare_words(self, event):
        """
        Compare the word typed by the user with the word to type.
        """
        # Get the first word from the list of words
        self.active_word = self.game.list_of_words[0]
        # Get the string typed by the user in typed_word variable and remove the end 'space character'
        typed_word = self.text_entry.get().strip()
        # Compare theses 2 values. If they match it means the user typed correctly and self.game.correct_answer will
        # be True
        self.game.correct_answer = typed_word == self.active_word
        self.display_user_feedback(self.active_word)
        self.next_word()
        # Clear the text entry
        self.text_entry.delete(0, 'end')

    def count_down(self):
        """
        This function is being called when creating the Window object and will be calling itself every 1 second.
        Does nothing until the user starts the game by pressing any key.
        It will allow our program to run for 60 seconds.
        """
        # Decrement timer value
        if self.game.started:
            self.game.timer -= 1
            self.timer_label['text'] = f"Timer: {self.game.timer}"

        # If timer goes down to zero, game is over
        if self.game.timer == 0:
            self.game.game_over = True
            self.game.started = False
            self.end_game()
            # We exit the function since it is no longer needed to count down
            return

        # Calls itself until the 'return' statement is reached when timer value becomes 0.
        self.after(1000, self.count_down)

    def determine_word_position(self, word):
        """
        Determine the current word indexes (his position) in the Text widget to highlight it.
            :param word: The current word (string) the user has to type correctly
        """
        # We use search to look for our word in the Text widget
        # The returned value is the index value (position) of the first letter of the word we are looking for
        # It is a string looking like this: e.g. : '1.4' if the word we are looking for is 'cat' in the following Text
        # widget : "dog cat"
        # We split the value around '.' character and take the last index of the resulting list to get the '4'.
        # Then we get it as integer
        word_start_index = int(self.text_display.search(word, '1.0', END).split('.')[-1])
        # Since we found the beginning positon of our word, we just add the length to get the ending position
        word_end_index = word_start_index + len(word)
        return word_start_index, word_end_index

    def display_user_feedback(self, word):
        """
        Give a feedback to the user regarding the word he just typed.
        Highlight the word in blue if it was typed correctly and in red otherwise.
            :param word: The word (string) the user just typed.
        """
        word_start = int(self.text_display.search(word, '1.0', END).split('.')[-1])
        word_end = word_start + len(word)
        if self.game.correct_answer:
            self.text_display.tag_add("correct", f"1.{word_start}", f"1.{word_end}")
            self.text_display.tag_config("correct", foreground=Color.CORRECT)
            self.game.correct_words += 1
            self.game.characters_count += len(word)
        else:
            self.text_display.tag_add("incorrect", f"1.{word_start}", f"1.{word_end}")
            self.text_display.tag_config("incorrect", foreground=Color.INCORRECT)
            self.game.incorrect_words += 1
        self.update_score()

    def end_game(self):
        """
        Show the end game statistics to the user : Characters per minute, words per minute and accuracy.
        """
        messagebox.showinfo("Game over",
                            f"Characters per minute: {self.game.characters_count}\nWords per minute: {self.game.correct_words}\nAccuracy: {self.calc_accuracy()}%")
        self.destroy()

    def highlight_current_word(self, start, stop):
        """
        Highlight in green the current word the user has to type in the Text widget.
            :param start: An index (integer) representing the beginning of the region of the word to highlight
            :param stop: An index (integer) representing the end of the region of the word to highlight
        """
        # Before highlighting a word, we need to remove the previous one
        self.text_display.tag_delete("current_word")
        # Define the region where the word is located
        self.text_display.tag_add("current_word", f"1.{start}", f"1.{stop}")
        # Define the style to apply to this specific region
        self.text_display.tag_config("current_word", background=Color.HIGHLIGHT, foreground=Color.BLACK)

    def next_word(self):
        """
        Pick the next word the user will have to type from the list of words
        """

        # Remove the first word from the list since we already dealt with it
        del self.game.list_of_words[0]
        # Increment current_word value to get global progression and calc the user accuracy later on
        self.game.current_word_id += 1

        # If there still are words in our list
        if self.game.list_of_words:
            # Update the active word to guess with the first word value from the list
            self.active_word = self.game.list_of_words[0]
            # Getting word location (starting and ending indexes) in Text widget
            word_starting_position, word_ending_position = self.determine_word_position(self.active_word)
            # Now we send theses two indexes values to our highlight function
            self.highlight_current_word(word_starting_position, word_ending_position)
            # Autoscroll down the Text widget by giving the current word ending position
            self.text_display.see(f'1.{word_ending_position}')
        # If there are no words left
        else:
            self.end_game()

    def start_game(self, event):
        """
        Set the started attribute to True to allow the countdown to run.
        """
        if event and not self.game.started:
            self.game.started = True

    def update_score(self):
        """
        Increment correctly and incorrectly typed words counters to give some real time feedback to the user
        """
        # Check if the user typed the word correctly
        if self.game.correct_answer:
            # Update label text
            self.correct_label['text'] = f"Correct words: {self.game.correct_words}"
        else:
            # Update label text
            self.incorrect_label['text'] = f"Incorrect words: {self.game.incorrect_words}"
