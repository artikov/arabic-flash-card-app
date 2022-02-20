from tkinter import *
import pandas
import random


BG_COLOR = '#008080'


# ------------- Working with data --------------- #

try:
    data = pandas.read_csv('words_to_learn.csv')

except FileNotFoundError:
    data = pandas.read_csv('500_Quranic_verbs.csv')


data_dict = data.to_dict(orient='records')


# ------------- Data File was updated --------------- #

# Root and Form columns are excluded
# modified_data = data.loc[:, ~data.columns.isin(['Root', 'Form'])]
#
# english = data.English.to_list()
# arabic = data.Arabic.to_list()

# ------------- Clearing up the strings --------------- #

# for i in range(len(english)):
#     english[i] = english[i].replace('|', '').replace(' to ', '| to ')
#     english[i] = english[i].strip().replace('  ', ' | ')
#
#
# new_data = {
#     'Arabic': arabic,
#     'English': english
# }
#
# new_df = pandas.DataFrame(new_data)
# new_df.to_csv('500_Quranic_verbs.csv', index=False)

# data_dict = pandas.Series(data.Arabic.values, index=english).to_dict()
# print(data_dict)


# ------------- Functions --------------- #

current_card = {}


def random_word():
    global current_card, flip
    window.after_cancel(flip)

    current_card = random.choice(data_dict)
    arabic_word = current_card["Arabic"].replace(' ', '\n')
    canvas.itemconfig(title_text, text=f'Arabic')
    canvas.itemconfig(word_text, text=f'{arabic_word}')
    canvas.lower(card_back, card_front)

    flip = window.after(3000, flip_card)


def checked():
    data_dict.remove(current_card)
    new_df = pandas.DataFrame(data_dict)
    new_df.to_csv('words_to_learn.csv', index=False)
    random_word()


def flip_card():
    english_word = current_card['English'].replace(' | ', '\n')
    canvas.itemconfig(card_back, image=back_img)
    canvas.lift(card_back, card_front)
    canvas.itemconfig(title_text, text=f'English')
    canvas.itemconfig(word_text, text=f'{english_word}')


# ------------- User interface --------------- #


window = Tk()
window.title('Arabic Flash Card')
window.config(padx=50, pady=50, bg=BG_COLOR)
flip = window.after(3000, flip_card)

card_img = PhotoImage(file='images/card.png')
check_img = PhotoImage(file='images/check.png')
cross_img = PhotoImage(file='images/cross.png')
back_img = PhotoImage(file='images/back.png')

canvas = Canvas(width=312, height=312, highlightthickness=0)
canvas.config(background=BG_COLOR)
card_front = canvas.create_image(156, 156, image=card_img)
card_back = canvas.create_image(155, 155)
title_text = canvas.create_text(156, 80, text='Arabic', font=('Ariel', 30, 'italic'), fill=BG_COLOR)
word_text = canvas.create_text(156, 156, text='', font=('Ariel', 20, 'italic'), fill=BG_COLOR)

canvas.grid(row=0, column=0, columnspan=2)

check_button = Button(image=check_img, command=checked)
check_button.grid(row=1, column=1)

cross_button = Button(image=cross_img, command=random_word)
cross_button.grid(row=1, column=0)

random_word()


window.mainloop()
