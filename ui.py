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

        self.active_word = self.game.list_of_words[0]
        self.determine_word_position(self.active_word)

        self.count_down()

        self.mainloop()

    def config_window(self):
        self.config(padx=20, pady=20)
        self.resizable(False, False)
        self.title("Typing Speed Test")

    def create_widgets(self):
        self.correct_label = Label(text=f'Correct words: {self.game.correct_words}')
        self.incorrect_label = Label(text=f'Incorrect words: {self.game.incorrect_words}')
        self.timer_label = Label(text=f"Timer: {self.game.timer}")

        self.text_display = Text(height=7, width=30)
        self.text_display.insert(INSERT, self.game.game_text)
        self.text_display.config(font=('Helvetica bold', 14), padx=30, wrap=WORD)
        # Center text
        self.text_display.tag_configure("center", justify='center')
        self.text_display.tag_add("center", 1.0, "end")

        self.text_entry = Entry(width=65)

    def setup_widgets_layout(self):
        self.correct_label.grid(row=0, column=0)
        self.incorrect_label.grid(row=0, column=1)
        self.timer_label.grid(row=0, column=2)
        self.text_display.grid(row=1, column=0, columnspan=3)
        self.text_entry.grid(row=2, column=0, pady=20, columnspan=3)

    def bind_functions(self):
        self.bind("<space>", self.compare_words)
        self.bind("<KeyPress>", self.start_timer)

    def compare_words(self, event):
        self.active_word = self.game.list_of_words[0]
        typed_word = self.text_entry.get().strip()
        self.game.answer = typed_word == self.active_word
        self.display_info(self.active_word)
        self.next_word()
        self.text_entry.delete(0, 'end')

    def count_down(self):
        if self.game.started:
            self.game.timer -= 1
            self.timer_label['text'] = f"Timer: {self.game.timer}"

        if self.game.timer == 0:
            self.game.game_over = True
            self.game.started = False
            self.end_game()
            return

        self.after(1000, self.count_down)

    def determine_word_position(self, word):
        word_start = int(self.text_display.search(word, '1.0', END).split('.')[-1])
        word_end = word_start + len(word)
        self.highlight_current_word(word_start, word_end)

        # autoscroll
        self.text_display.see(f'1.{word_end}')

    def display_info(self, word):
        word_start = int(self.text_display.search(word, '1.0', END).split('.')[-1])
        word_end = word_start + len(word)
        if self.game.answer:
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
        messagebox.showinfo("Game over",
                            f"Characters per minute: {self.game.characters_count}\nWords per minute: {self.game.correct_words}\nAccuracy: {round(self.game.correct_words / self.game.current_word * 100)}%")
        self.destroy()

    def highlight_current_word(self, start, stop):
        self.text_display.tag_delete("current_word")
        self.text_display.tag_add("current_word", f"1.{start}", f"1.{stop}")
        self.text_display.tag_config("current_word", background=Color.HIGHLIGHT, foreground=Color.BLACK)

    def next_word(self):
        if self.game.list_of_words:
            del self.game.list_of_words[0]
            self.game.current_word += 1
            active_word = self.game.list_of_words[0]
            self.determine_word_position(active_word)

    def start_timer(self, event):
        if event and not self.game.started:
            self.game.started = True

    def update_score(self):
        if self.game.answer:
            self.correct_label['text'] = f"Correct words: {self.game.correct_words}"
        else:
            self.incorrect_label['text'] = f"Incorrect words: {self.game.incorrect_words}"
