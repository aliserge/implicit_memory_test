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

songs = ()
filename1 = "sounds/one.wav"
filename2 = "sounds/two.wav"
filename3 = "sounds/three.wav"
filename4 = "sounds/four.wav"
songs = (AudioSegment.from_wav(filename1), AudioSegment.from_wav(filename2), AudioSegment.from_wav(filename3), AudioSegment.from_wav(filename4))
repeats = -1
user_name = ''

sleep_time = 0.5
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
n = 0
Is_key_pressed = False
filename = ''
begin_time = 0
circles = 0
circles_to_learn = 0
birth = ''
change_seq_chance = 0

def parameters_input():
    global repeats
    global circles_to_learn
    global change_seq_chance
    parameters = {}
    with open("config.txt", "r") as config_file:
        for line in config_file:
            parameter = line.strip().split("=")
            parameters[parameter[0]] = parameter[1]
    repeats = int(parameters['repeats'])
    circles_to_learn = int(parameters['circles_to_learn'])
    change_seq_chance = int(parameters['change_seq_chance']) / 100


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
    #for row in results:
    #    print(row)
    
    with open(results_file_name, 'w') as out_file:
        out_file.write('SeqA:\t'+','.join(str(el) for el in seq_a)+'\n')
        out_file.write('SeqB:\t'+','.join(str(el) for el in seq_b)+'\n')
        out_file.write("Square\tStart time\tDone time\tDelta\tRatio\tCorrectness\tSequence\n")
        for click in results:
            out_file.write(f"{click[0]}\t{click[1]}\t{click[2]}\t{click[3]}\t{click[4]}\t{click[5]}\t{click[6]}\n")


    
def save():
    global user_name
    global begin_time
    user_name = info.get()
    begin_time = dt.datetime.now()
    #window.bind("<Key>", keypressed)    # привязать нажатие любой клавиши к функции keypressed
    btn_ready["state"] = tk.DISABLED
    info["state"] = tk.DISABLED
    #entry_repeats["state"] = tk.DISABLED
    time.sleep(sleep_time)
    fr_info_ready.grid_forget()
    label_name.grid_forget()
    info.grid_forget()
    
    
    ready_button_and_rules()
    
def ready_button_and_rules():
    fr_rules_button.grid(row = 1, column = 2, padx = 5, pady = 5)
    lbl_rules.grid(row = 0, column = 1)
    btn_start.grid(row = 1, column = 1, sticky = "s")
    
def search_square_id(current_element):
    return current_element

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
    print('=== New position look ===')
    print(circles, circles_to_learn)
    if circles > circles_to_learn:
        randomizator = random.random()
        if our_seq == "A":
            combination = (seq_a[position - 1], seq_a[position])
        else:
            combination = (seq_b[position - 1], seq_b[position])
        
        print(randomizator, change_seq_chance)
        
        if randomizator <= change_seq_chance and our_seq == "A":
            change = True
            new_position = dict_seq_b[combination]
        elif randomizator > change_seq_chance and our_seq == "B":
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
    seq_b = couples_to_singles(seq_b)
    dict_seq_a = making_dictionaries(seq_a)
    dict_seq_b = making_dictionaries(seq_b)
    
    
def starting():
    global our_seq
    global position
    global previous_time
    global previous_square_id

    print("Starting")
    btn_start.grid_forget()
    lbl_rules.grid_forget()
    
    btn_1.grid(row = 1, column = 0, sticky = "nsew")
    btn_2.grid(row = 1, column = 1, sticky = "nsew")
    btn_3.grid(row = 1, column = 2, sticky = "nsew")
    btn_4.grid(row = 1, column = 3, sticky = "nsew")
    
    
    
    

    time.sleep(sleep_time)
    previous_square_id = search_square_id(seq_a[0])
    play_number(previous_square_id)
    previous_time = dt.datetime.now()

def btn_one():
    btn_pressed(1)

def btn_two():
    btn_pressed(2)
    
def btn_three():
    btn_pressed(3)
    
def btn_four():
    btn_pressed(4)

def btn_disabled():
    btn_1["state"] = tk.DISABLED
    btn_2["state"] = tk.DISABLED
    btn_3["state"] = tk.DISABLED
    btn_4["state"] = tk.DISABLED
    
def btn_enabled():
    btn_1["state"] = tk.NORMAL
    btn_2["state"] = tk.NORMAL
    btn_3["state"] = tk.NORMAL
    btn_4["state"] = tk.NORMAL

def btn_pressed(btn_number):
    global n
    global previous_time
    global previous_square_id
    global Is_key_pressed
    
    if Is_key_pressed == False:
        n += 1
        key_info = []
        Is_key_pressed = True
    # тайминг
        current_time = dt.datetime.now()
        ping = current_time - previous_time
        ratio = (current_time - begin_time).total_seconds() / (previous_time - begin_time).total_seconds()
        key_info.append(btn_number)
        key_info.append(previous_time)
        key_info.append(current_time)
        key_info.append(ping.total_seconds())
        key_info.append(ratio)
        previous_time = current_time
        
        btn_disabled()
        window.update()

    # сопоставление кнопки и звука

        if btn_number == previous_square_id:
            key_info.append(True)
        else:
            key_info.append(False)
        
        # указатель случайных квадратов
        key_info.append(our_seq)
        results.append(key_info)    
    
    # прощание
        if n == repeats * 12:
            fr_info_ready.grid_forget()
            window.update()
            time.sleep(sleep_time)
            congrats = tk.Label(text = "The end. Thank you!", bg = "yellow", fg = "blue", font = ('Helvetica', '20'))
            congrats.grid(row = 1, column = 1, padx = 5, pady = 5)
            return
        
        square_id = decisioners()
        time.sleep(sleep_time)
        play_number(square_id)
        previous_square_id = square_id

        btn_enabled()
        previous_time = dt.datetime.now()
        Is_key_pressed = False 
    
        
def play_number(square_id):
    t = threading.Thread(target=play, args=(songs[square_id - 1],))
    t.start()



parameters_input()

# оформление окна
window = tk.Tk()


window.title("Statistical learning test № 2")
window.rowconfigure([0,1,2,3], minsize = 200, weight = 1)
window.columnconfigure([0,1,2,3,4], minsize = 200, weight = 1)


fr_info_ready = tk.Frame(window)

# Label и Entry для ввода имени
label_name = tk.Label(fr_info_ready, text = "Name, please:", font = ('Helvetica', '20'))
info = tk.Entry(fr_info_ready, font = ('20'))

# Label и Entry для ввода даты рождения
label_birth = tk.Label(fr_info_ready, text = "Date of birth:", font = ('Helvetica', '20'))
entry_birth = tk.Entry(fr_info_ready, font = ('20'))

# Button с функциями для начала тестирования
btn_ready = tk.Button(fr_info_ready, text = "Start", font = ('Helvetica', '20'), command = lambda:[save(), initialization()])

# Создание текста правил и кнопки Ready
fr_rules_button = tk.Frame(window)
lbl_rules = tk.Label(fr_rules_button, text = """Press 1, 2, 3, 4 
buttons on the screen
according to numbers you hear 
as accurate and rapid as possible""", font = ('Helvetica', '12'))
btn_start = tk.Button(fr_rules_button, text = "Ready", font = ('15'), command = starting)

# Buttons 1, 2, 3, 4 on the screen
btn_1 = tk.Button(text = "1", font = "30", command = btn_one)
btn_2 = tk.Button(text = "2", font = "30", command = btn_two)
btn_3 = tk.Button(text = "3", font = "30", command = btn_three)
btn_4 = tk.Button(text = "4", font = "30", command = btn_four)

# размещение элементов в сетке
fr_info_ready.grid(row = 1, column = 2, padx = 5, pady = 5)
label_name.grid(row = 0, column = 1, sticky = "n")
info.grid(row = 1, column = 1)
label_birth.grid(row = 4, column = 1)
entry_birth.grid(row = 5, column = 1)
btn_ready.grid(row = 6, column = 1, sticky = "s")


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
