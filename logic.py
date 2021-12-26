from PyQt5.QtCore import QObject, pyqtSignal
import datetime as dt
import random
import time
import hashlib
from configparser import ConfigParser
from collections import namedtuple
from post_proc_pandas import post_processing

class test_logic(QObject):
    number_to_show_event = pyqtSignal(str)
    test_ended = pyqtSignal()
    play_sound_signal = pyqtSignal(str)
    
    User_record = namedtuple('User_record','Sequence Position Right_answer User_answer Correctness Start_time Stop_time RT')
    
    def __init__(self, parent=None, reverse_seq=False):
        super().__init__(parent)
        parameters = {}
        config = ConfigParser()
        config.read('config.ini')
        self.percent_change = int(config['Default']['change_seq_chance']) / 100
        self.repeats = int(config['Default']['repeats'])
        self.numbers_to_learn = int(config['Default']['numbers_to_learn'])
        self.seq_a = config['Default']['seq_a'].split(',')
        self.seq_b = config['Default']['seq_b'].split(',')
        if reverse_seq:
            self.seq_a = self.seq_a[::-1]
            self.seq_b = self.seq_b[::-1]
        
        print(self.seq_a)
        self.dict_seq_a = self.make_dictionaries(self.seq_a)
        self.dict_seq_b = self.make_dictionaries(self.seq_b)
        self.our_seq = "A"
        self.position = 0
        self.numbers_shown = 0
        self.key_info = []

    
    def make_dictionaries(self, seq):
        dictionary = {}
        for i in range(len(seq)):
            combination = (seq[i - 1], seq[i])
            dictionary[combination] = i
        return dictionary
        
    def seq_to_seq_jumping(self, change, new_position):
        if change == True:
            if self.our_seq == "A":
                self.our_seq = "B"
            else:
                self.our_seq = "A"
        self.position = new_position
        return self.return_current_el()

    def return_current_el(self):
        if self.our_seq == "A":
            current_element = self.seq_a[self.position]
        else:
            current_element = self.seq_b[self.position]
            
        return current_element
    
    def random_and_new_position(self):
        change = False
        if self.numbers_shown > self.numbers_to_learn:
            randomizator = random.random()
            if self.our_seq == "A":
                combination = (self.seq_a[self.position - 1], self.seq_a[self.position])
            else:
                combination = (self.seq_b[self.position - 1], self.seq_b[self.position])
            
            if randomizator <= self.percent_change and self.our_seq == "A":
                change = True
                new_position = self.dict_seq_b[combination]
            elif randomizator > self.percent_change and self.our_seq == "B":
                change = True
                new_position = self.dict_seq_a[combination]
            else:
                new_position = self.position
        else:
            new_position = self.position
        new_position = (new_position + 1) % 12
        
        return (change, new_position)

    def choose_next_el(self):
        change, new_position = self.random_and_new_position()
        current_element = self.seq_to_seq_jumping(change, new_position)
        self.numbers_shown += 1
        return current_element
    
    def start_testing(self, user_name, date_birth):
        self.user_name = user_name
        self.date_birth = date_birth
        
    def emit_number(self):
        if self.numbers_shown > self.repeats:
            self.test_ended.emit()
            return
        
        self.start_time = self.timer()
        print("Sending square element", str(self.return_current_el()))
        self.number_to_show_event.emit(self.return_current_el())
        
    def timer(self):
        return dt.datetime.now()
        
    def match_check(self, key):
        print("recieved key to record:", key)
        # тайминг
        self.stop_time = self.timer()
        ping = self.stop_time - self.start_time
        right_answer = str(self.return_current_el())
        
        correctness = key == right_answer
        key_record = self.User_record(Sequence=self.our_seq, Position=self.position, Right_answer=right_answer,
            User_answer=key, Correctness=correctness, Start_time = self.start_time, Stop_time = self.stop_time, RT = ping.total_seconds())
        self.key_info.append(key_record)
        self.play_sound_signal.emit(str(correctness))
        
        self.choose_next_el()
        
    def print_results(self):

        user_name_birth = self.user_name + ' ' + self.date_birth
        hash_user = hashlib.md5(user_name_birth.encode()).hexdigest()[:15]
        with open('user_to_hash.txt', 'a') as user_to_hash:
            user_to_hash.write(f"{user_name_birth}\t{hash_user}\n")
        results_file_name = f'res_{hash_user}.txt'
        with open(results_file_name, 'w') as out_file:
            out_file.write('SeqA:\t'+','.join(str(el) for el in self.seq_a)+'\n')
            out_file.write('SeqB:\t'+','.join(str(el) for el in self.seq_b)+'\n')
            out_file.write('\t'.join(self.User_record._fields)+'\n')
            for key_record in self.key_info:
                out_file.write("\t".join([str(el) for el in key_record])+"\n")
        
        post_processing(results_file_name)
