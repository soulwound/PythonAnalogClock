from tkinter import *
from tkinter import ttk
from math import cos, sin, radians, pi
import time
from time import strftime
import threading

root = Tk()
root.title('SoulsClock')
c = Canvas(root, width=400, height=400, bg='white')
c.pack()
root.geometry('400x550')

numbers = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 12]
arrow_color_menu = Frame()
arrow_color_menu.pack(side=LEFT)

hour_arrow_color = LabelFrame(arrow_color_menu, text='Hour color')
hour_color = ['black', 'pink', 'blue']
hour_color_value = StringVar(value=hour_color[0])
hour_combobox = ttk.Combobox(hour_arrow_color, textvariable=hour_color_value, width=10)
hour_combobox['values'] = hour_color
hour_combobox.pack()
hour_arrow_color.pack()


def hour_selected(event):
    selection = hour_combobox.get()
    print(selection)
    c.itemconfig(hour, fill=selection)


hour_combobox.bind("<<ComboboxSelected>>", hour_selected)

minute_arrow_color = LabelFrame(arrow_color_menu, text='Minute color')
minute_color = ['black', 'purple', 'navy']
minute_color_value = StringVar(value=minute_color[0])
minute_combobox = ttk.Combobox(minute_arrow_color, textvariable=minute_color_value, width=10)
minute_combobox['values'] = minute_color
minute_combobox.pack()
minute_arrow_color.pack()


def minute_selected(event):
    selection = minute_combobox.get()
    print(selection)
    c.itemconfig(minute, fill=selection)


minute_combobox.bind("<<ComboboxSelected>>", minute_selected)

second_arrow_color = LabelFrame(arrow_color_menu, text='Second color')
second_color = ['black', 'blue', 'red']
second_color_value = StringVar(value=second_color[0])
second_combobox = ttk.Combobox(second_arrow_color, textvariable=second_color_value, width=10)
second_combobox['values'] = second_color
second_combobox.pack()
second_arrow_color.pack()


def second_selected(event):
    selection = second_combobox.get()
    print(selection)
    c.itemconfig(second, fill=selection)


second_combobox.bind("<<ComboboxSelected>>", second_selected)


def theme_select():
    match themes_values.get():
        case 'light':
            c['bg'] = 'white'
            c.itemconfig(hour, fill='black')
            c.itemconfig(minute, fill='black')
            c.itemconfig(second, fill='black')
            create_nums('black')
            create_small_dots('black')
            create_big_dots('black')
            c.itemconfig(circle_field, outline='black')
        case 'dark':
            c['bg'] = 'black'
            c.itemconfig(hour, fill='white')
            c.itemconfig(minute, fill='white')
            c.itemconfig(second, fill='white')
            create_nums('white')
            create_small_dots('white')
            create_big_dots('white')
            c.itemconfig(circle_field, outline='white')


theme_selection_menu = LabelFrame(root, text='Theme')
themes = ['light', 'dark']
themes_values = StringVar(value='light')
for theme in themes:
    lang_btn = ttk.Radiobutton(text=theme, value=theme, variable=themes_values, command=theme_select)
    lang_btn.pack()
theme_selection_menu.pack(side=RIGHT)


def create_nums(color):
    for i in range(0, len(numbers)):
        c.create_text(
            200 - 120 * sin(((i + 1) * 2 * pi) / 12),
            200 - 120 * cos(((i + 1) * 2 * pi) / 12),
            text=numbers[i],
            font=('Arial', 12, 'normal'),
            fill=color
        )


def create_small_dots(color):
    for y in range(60):
        c.create_text(
            200 - 140 * sin(((y + 1) * 2 * pi) / 60),
            200 - 140 * cos(((y + 1) * 2 * pi) / 60),
            text='•',
            font=('Arial', 7, 'bold'),
            fill=color)


def create_big_dots(color):
    for x in range(12):
        c.create_text(
            200 - 140 * sin(((x + 1) * 2 * pi) / 12),
            200 - 140 * cos(((x + 1) * 2 * pi) / 12),
            text='•',
            font=('Arial', 18, 'bold'),
            fill=color)


hour = c.create_line(200, 200, 200, 200, width=6)
minute = c.create_line(200, 200, 200, 200, width=4)
second = c.create_line(200, 200, 200, 200, width=2)

circle_field = c.create_oval(50, 50, 350, 350, width=2)


# Отрисовываем стрелки
def create_arrows():
    h = int(strftime('%H'))
    m = int(strftime('%M'))
    s = int(strftime('%S'))
    hr = (h / 12) * 360
    mn = (m / 60) * 360
    se = (s / 60) * 360
    c.coords(hour, 200, 200, 200 + 60*sin(radians(hr)), 200 - 60*cos(radians(hr)))
    c.coords(minute, 200, 200, 200 + 95*sin(radians(mn)), 200 - 95*cos(radians(mn)))
    c.coords(second, 200, 200, 200 + 120 * sin(radians(se)), 200 - 120 * cos(radians(se)))


# Обновляем время каждую секунду в другом потоке
def update_arrows():
    while True:
        time.sleep(1)
        c.coords(second, 200, 200, 200, 200)
        create_arrows()


create_nums('black')
create_big_dots('black')
create_small_dots('black')
create_arrows()
process = threading.Thread(target=update_arrows, daemon=True)
process.start()


root.mainloop()
