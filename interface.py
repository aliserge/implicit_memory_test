import tkinter as tk
import datetime as dt
import random
import time

repeats = -1
user_name = ''
mutaion_rate = 0.15
sleep_time = 1
results = []
previous_time = -1
previous_square_id = -1
#quantity = 0
seq_a = []
seq_b = []
dict_seq_a = {}
dict_seq_b = {}
our_seq = "A"
position = 0
variants = (1, 3, 7, 9)
n = 0

def show_square(square_id):  # рисуем квадрат
    if square_id == 7:
        square7.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "nsew")
    elif square_id == 9:
        square9.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = "nsew")
    elif square_id == 1:
        square1.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "nsew")
    else:
        square3.grid(row = 2, column = 2, padx = 5, pady = 5, sticky = "nsew")
    window.update()

def forget_square(k):  # забываем квадрат
    if k == 7:
        square7.grid_forget()
    elif k == 9:
        square9.grid_forget()
    elif k == 1:
        square1.grid_forget()
    else:
        square3.grid_forget()
    window.update()

# оформление окна
window = tk.Tk()
window.title("Mollon memory test")
window.rowconfigure([0,1,2], minsize = 80, weight = 1)
window.columnconfigure([0,1,2], minsize = 80, weight = 1)


fr_info_ready = tk.Frame(window)

# Label и Entry для ввода имени
label_name = tk.Label(fr_info_ready, text = "Name, please:")
info = tk.Entry(fr_info_ready)

# Label и Entry для ввода длины последовательности
#label_quantity = tk.Label(fr_info_ready, text = "Quantity of elements, please:")
#entry_quantity = tk.Entry(fr_info_ready)

# Label и Entry для ввода повторов последовательности
label_repeats = tk.Label(fr_info_ready, text = "Number of repeats:")
entry_repeats = tk.Entry(fr_info_ready)

# Button с функциями для начала тестирования
btn_ready = tk.Button(fr_info_ready, text = "Start", command = lambda:[save(), initialization(), starting()])

# размещение элементов в сетке
fr_info_ready.grid(row = 1, column = 1, padx = 5, pady = 5)
label_name.grid(row = 0, column = 1, sticky = "n")
info.grid(row = 1, column = 1)
#label_quantity.grid(row = 2, column = 1)
#entry_quantity.grid(row = 3, column = 1)
label_repeats.grid(row = 4, column = 1)
entry_repeats.grid(row = 5, column = 1)
btn_ready.grid(row = 6, column = 1, sticky = "s")

# Создание квадратов
square7 = tk.Label(bg = "red")
square9 = tk.Label(bg = "red")
square1 = tk.Label(bg = "red")
square3 = tk.Label(bg = "red")

# Прорисовка квадратов
for i in (1,3,7,9):
    show_square(i)

window.mainloop()
