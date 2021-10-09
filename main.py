import random
from tkinter import *
from tkinter import messagebox

from game import Game
from words import WORDS

HIGHLIGHT_COLOR = '#b8e069'
INCORRECT_COLOR = '#c00'
CORRECT_COLOR = 'blue'
BLACK = 'black'

list_of_words = WORDS
random.shuffle(list_of_words)
sample_text = ' '.join(list_of_words)


def highlight_current_word(start, stop):
    text.tag_delete("current_word")
    text.tag_add("current_word", f"1.{start}", f"1.{stop}")
    text.tag_config("current_word", background=HIGHLIGHT_COLOR, foreground=BLACK)


def display_info(word):
    word_start = int(text.search(word, '1.0', END).split('.')[-1])
    word_end = word_start + len(word)
    if game.answer:
        text.tag_add("correct", f"1.{word_start}", f"1.{word_end}")
        text.tag_config("correct", foreground=CORRECT_COLOR)
        game.correct_words += 1
        game.characters_count += len(word)
    else:
        text.tag_add("incorrect", f"1.{word_start}", f"1.{word_end}")
        text.tag_config("incorrect", foreground=INCORRECT_COLOR)
        game.incorrect_words += 1
    update_score()


def update_score():
    if game.answer:
        correct_score['text'] = f"Correct words: {game.correct_words}"
    else:
        incorrect_score['text'] = f"Incorrect words: {game.incorrect_words}"


def determine_word_position(word):
    word_start = int(text.search(word, '1.0', END).split('.')[-1])
    word_end = word_start + len(word)
    highlight_current_word(word_start, word_end)

    # autoscroll
    text.see(f'1.{word_end}')


def next_word():
    if list_of_words:
        del list_of_words[0]

        active_word = list_of_words[0]
        determine_word_position(active_word)
        # window.after(500, next_word)


def compare_words(event):
    active_word = list_of_words[0]
    typed_word = text_area.get().strip()
    game.answer = typed_word == active_word
    display_info(active_word)
    next_word()
    text_area.delete(0, 'end')


def count_down():
    if game.started:
        game.timer -= 1
        timer_text['text'] = f"Timer: {game.timer}"

    if game.timer == 0:
        game.game_over = True
        game.started = False
        end_game()
        return

    window.after(1000, count_down)


def end_game():
    messagebox.showinfo("Game over",
                        f"Characters per minute: {game.characters_count}\nWords per minute: {game.correct_words}")


def start_timer(event):
    if event and not game.started:
        game.started = True


window = Tk()
window.config(padx=20, pady=20)

game = Game()

correct_score = Label(text='Correct words: 0')
incorrect_score = Label(text='Incorrect words: 0')
correct_score.grid(row=0, column=0)
incorrect_score.grid(row=0, column=1)

timer_text = Label(text=f"Timer: {game.timer}")
timer_text.grid(row=0, column=2)

text = Text(height=7, width=30)
text.insert(INSERT, sample_text)
text.config(font=('Helvetica bold', 14), padx=30, wrap=WORD)
text.grid(row=1, column=0, columnspan=3)

# Center text
text.tag_configure("center", justify='center')
text.tag_add("center", 1.0, "end")

text_area = Entry(width=65)

text_area.grid(row=2, column=0, pady=20, columnspan=3)

active_word = list_of_words[0]
determine_word_position(active_word)

window.bind("<space>", compare_words)

window.bind("<KeyPress>", start_timer)

count_down()

window.mainloop()
