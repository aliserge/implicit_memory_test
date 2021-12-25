#!/usr/bin/env python3

import tkinter as tk
import datetime as dt
import random
import time
from pydub import AudioSegment
from pydub.playback import play
import threading
import hashlib
from attempt_post_proc import post_processing

repeats = -1
user_name = ''

sleep_time = 0.3
results = []
previous_time = -1
previous_square_id = -1
seq_a = []
seq_b = []
dict_seq_a = {}
dict_seq_b = {}
our_seq = "A"
position = 0
variants = (1, 3, 7, 9)
variants_to_keys = {"1":1,"3":2,"7":3,"9":4}


n = 0
Is_key_pressed = False
filename = ''
begin_time = 0
circles = 0
circles_to_learn = 2
birth = ''

parameters = {}

with open('config.txt', 'r') as config:
    for line in config:
        parameters[line.split('=')[0]] = int(line.split('=')[1])

percent_change = parameters['change_seq_chance'] / 100
repeats = parameters['repeats']
circles_to_learn = parameters['circles_to_learn']

def table_4x4():     # таблица 4х4
    couples = []
    maximum = 4
    
    for i in range(1, maximum + 1):
        for j in range(1, maximum + 1):
            if i != j:
                new = (i, j)
                couples.append(new)
    return couples

def try_to_calculate_seq():  # 1 попытка сгенерировать последовательность
    
    couples = table_4x4()
    num_tries = 0
    seq = []
    test_list = []
        
    while len(couples) > 0:
        num_tries += 1
        if num_tries > 40:
            break

        selected_couple = random.choice(couples)

        if selected_couple not in test_list:
            if len(seq) > 0:
                previous_couple = seq[-1]
                first, second = previous_couple
                third, forth = selected_couple
                medium_couple = (second, third)

                if (second, third) in test_list or second == third:
                    if len(couples) == 1:
                        first,second = seq[0]
                        pre_last,last = seq[-1]
                        if (last, first) == couples[0]:
                            #print("complete")
                            return seq
                        print('wrong random')
                        print(couples)
                        print(seq)
                        return
                    continue
                test_list.append(medium_couple)
                couples.remove(medium_couple)
            seq.append(selected_couple)
            test_list.append(selected_couple)
            couples.remove(selected_couple)


        else:
            print('wrong list')
            print(couples)
            print(seq)
            return

def calculating_seq():   # генерируем, пока не получим подходящую последовательность
    a = None
    while a == None:
        a = try_to_calculate_seq()
    return a
    print(a)
    
def couples_to_singles(seq):   # формируем список цифр из списка пар
    new_seq = []
    for couple in seq:
        first, second = couple
        new_seq.append(first)
        new_seq.append(second)
    return new_seq

def making_dictionaries(seq):
    dictionary = {}
    for i in range(len(seq)):
        combination = (seq[i - 1], seq[i])
        dictionary[combination] = i
    return dictionary

def print_results(results, results_file_name):   # печатаем результаты в консоль

    with open(results_file_name, 'w') as out_file:
        out_file.write('SeqA:\t'+','.join(str(el) for el in seq_a)+'\n')
        out_file.write('SeqB:\t'+','.join(str(el) for el in seq_b)+'\n')
        out_file.write("Square\tStart time\tDone time\tDelta\tRatio\tCorrectness\tSequence\n")
        for click in results:
            
            key_var = variants_to_keys[click[0]] if click[0] in variants_to_keys else 'ErrKey:' + click[0]
            out_file.write(f"{key_var}\t{click[1]}\t{click[2]}\t{click[3]}\t{click[4]}\t{click[5]}\t{click[6]}\n")

'''
def post_processing(results_file_name):  # ratios
    
    with open(results_file_name, 'r') as outfile:
        results = [line.strip().split('\t') for line in outfile]
    
    results = results[1:] # stripping header
    results = [ [int(line[0]), dt.strptime(line[1]), dt.strptime(line[2]), float(line[3]), float(line[4]),
                 bool(line[5]),line[6] ] for line in results]
    print(results)
'''    
        
def show_square(square_id):  # рисуем квадрат
    if square_id == 7:
        square7.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "nsew")
    elif square_id == 9:
        square9.grid(row = 0, column = 4, padx = 5, pady = 5, sticky = "nsew")
    elif square_id == 1:
        square1.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "nsew")
    else:
        square3.grid(row = 3, column = 4, padx = 5, pady = 5, sticky = "nsew")
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

def search_square_id(current_element):
    if current_element == 1:
        square_id = 1
    elif current_element == 2:
        square_id = 3
    elif current_element == 3:
        square_id = 7
    else:
        square_id = 9
    return square_id

def seq_to_seq_jumping(change, our_seq, new_position):
    if change == True:
        if our_seq == "A":
            our_seq = "B"
        else:
            our_seq = "A"

    if our_seq == "A":
        current_element = seq_a[new_position]
    else:
        current_element = seq_b[new_position]
        
    return current_element, our_seq

def random_and_new_position(seq_a, seq_b, dict_seq_a, dict_seq_b, position, our_seq):
    global circles
    change = False
    if circles > circles_to_learn:
        randomizator = random.random()
        if our_seq == "A":
            combination = (seq_a[position - 1], seq_a[position])
        else:
            combination = (seq_b[position - 1], seq_b[position])
        
        if randomizator <= percent_change and our_seq == "A":
            change = True
            new_position = dict_seq_b[combination]
        elif randomizator > percent_change and our_seq == "B":
            change = True
            new_position = dict_seq_a[combination]
        else:
            new_position = position
    else:
        new_position = position
    new_position = (new_position + 1) % 12
    if new_position == 0:
        circles += 1
    return (change, new_position)

def decisioners():
    global our_seq
    global position
    change, new_position = random_and_new_position(seq_a, seq_b, dict_seq_a, dict_seq_b, position, our_seq)
    current_element, our_seq = seq_to_seq_jumping(change, our_seq, new_position)
    square_id = search_square_id(current_element)
    position = new_position
    return square_id

def save():
    global user_name
    global begin_time
    user_name = info.get()
    begin_time = dt.datetime.now()
    window.bind("<Key>", keypressed)    # привязать нажатие любой клавиши к функции keypressed
    btn_ready["state"] = tk.DISABLED
    info["state"] = tk.DISABLED
    #entry_repeats["state"] = tk.DISABLED
    time.sleep(sleep_time)
    fr_info_ready.grid_forget()
    label_name.grid_forget()
    info.grid_forget()
    #label_repeats.grid_forget()
    #entry_repeats.grid_forget()
    
    ready_button_and_rules()
    
def ready_button_and_rules():
    fr_rules_button.grid(row = 1, column = 2, padx = 5, pady = 5)
    lbl_rules.grid(row = 0, column = 1)
    btn_start.grid(row = 1, column = 1, sticky = "s")
    
    
def initialization():
    global seq_a
    global seq_b
    global dict_seq_a
    global dict_seq_b
    global entry_birth
    global birth
    
    birth = entry_birth.get()

    # генерация последовательностей
    seq_a = calculating_seq() 
    #print(seq_a)
    seq_b = calculating_seq()
    #print(seq_b)

    # формирование последовательностей цифр из пар
    seq_a = couples_to_singles(seq_a)
    #print(seq_a)
    seq_b = couples_to_singles(seq_b)
    #print(seq_b)
    dict_seq_a = making_dictionaries(seq_a)
    dict_seq_b = making_dictionaries(seq_b)

def starting():
    global our_seq
    global position
    global previous_time
    global previous_square_id
    print("Starting")
    btn_start["state"] = tk.DISABLED
    
    for i in (1,3,7,9):
        forget_square(i)
    time.sleep(sleep_time)
    previous_square_id = search_square_id(seq_a[0])
    show_square(previous_square_id)
    previous_time = dt.datetime.now()
    
    
def keypressed(event):
    global n
    global previous_time
    global previous_square_id
    global Is_key_pressed
    global filename
    
    print(Is_key_pressed)
    if Is_key_pressed == False:
        n += 1
        key_info = []
        Is_key_pressed = True
    # тайминг
        current_time = dt.datetime.now()
        ping = current_time - previous_time
        ratio = (current_time - begin_time).total_seconds() / (previous_time - begin_time).total_seconds()
        key_info.append(event.char)
        key_info.append(previous_time)
        key_info.append(current_time)
        key_info.append(ping.total_seconds())
        key_info.append(ratio)
        previous_time = current_time

    # сопоставление клавиши и квадрата
        print(event.char)
        print(type(event.char),event.char)
        if int(event.char) == previous_square_id:
            key_info.append(True)
            filename = 'sounds/positive-notification.wav'
        else:
            key_info.append(False)
            filename = 'sounds/wrong-answer.wav'
        play_sound(filename)

    # указатель случайных квадратов
        key_info.append(our_seq)
        
        results.append(key_info)
        
        forget_square(previous_square_id)    
     

    # прощание
        if n == repeats * 12:
            fr_info_ready.grid_forget()
            window.update()
            time.sleep(sleep_time)
            congrats = tk.Label(text = "The end. Thank you!", bg = "yellow", fg = "blue", font = ('Helvetica', '20'))
            congrats.grid(row = 1, column = 1, padx = 5, pady = 5)
            return

        time.sleep(sleep_time)
        
        square_id = decisioners()
        show_square(square_id)
        previous_square_id = square_id
        previous_time = dt.datetime.now()
        Is_key_pressed = False
 
def play_sound(filename):
    sound = AudioSegment.from_wav(filename)
    t = threading.Thread(target=play, args=(sound,))
    t.start()

# оформление окна
window = tk.Tk()


window.title("Statistical learning test")
window.rowconfigure([0,1,2,3], minsize = 200, weight = 1)
window.columnconfigure([0,1,2,3,4], minsize = 200, weight = 1)


fr_info_ready = tk.Frame(window)

# Label и Entry для ввода имени
label_name = tk.Label(fr_info_ready, text = "Name, please:", font = ('Helvetica', '20'))
info = tk.Entry(fr_info_ready, font = ('20'))

# Label и Entry для ввода повторов последовательности
label_birth = tk.Label(fr_info_ready, text = "Date of birth:", font = ('Helvetica', '20'))
entry_birth = tk.Entry(fr_info_ready, font = ('20'))

# Button с функциями для начала тестирования
btn_ready = tk.Button(fr_info_ready, text = "Start", font = ('Helvetica', '20'), command = lambda:[save(), initialization()])

# размещение элементов в сетке
fr_info_ready.grid(row = 1, column = 2, padx = 5, pady = 5)
label_name.grid(row = 0, column = 1, sticky = "n")
info.grid(row = 1, column = 1)
label_birth.grid(row = 4, column = 1)
entry_birth.grid(row = 5, column = 1)
btn_ready.grid(row = 6, column = 1, sticky = "s")

# Создание квадратов
square7 = tk.Label(bg = "red")
square9 = tk.Label(bg = "red")
square1 = tk.Label(bg = "red")
square3 = tk.Label(bg = "red")

# Создание текста правил и кнопки Ready
fr_rules_button = tk.Frame(window)
lbl_rules = tk.Label(fr_rules_button, text = """Press 1, 3, 7, 9 
using the number part of the keyboard 
according to appearing red squares 
in the corners of the screen 
as accurate and rapid as possible""", font = ('Helvetica', '12'))
btn_start = tk.Button(fr_rules_button, text = "Ready", font = ('15'), command = starting)

# Прорисовка квадратов
for i in (1,3,7,9):
    show_square(i)

window.mainloop()

print(seq_a, seq_b)
print(user_name)

user_name_birth = user_name + ' ' + birth
hash_user = hashlib.md5(user_name_birth.encode()).hexdigest()[:15]
with open('user_to_hash.txt', 'a') as user_to_hash:
    user_to_hash.write(f"{user_name_birth}\t{hash_user}\n")

results_file_name = f'res_{hash_user}.txt'
print_results(results, results_file_name)
post_processing(results_file_name)
