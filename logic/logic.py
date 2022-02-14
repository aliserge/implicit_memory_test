import datetime as dt
import hashlib
from configparser import ConfigParser
from collections import namedtuple
import pickle

from PyQt5.QtCore import QObject, pyqtSignal

from logic.post_proc import post_processing

config_file_name = 'config.ini'

User_Record = namedtuple('User_record',
                             'Sequence Position Right_answer User_answer Correctness Start_time Stop_time RT')

class Test_Logic(QObject):
    number_to_show_event = pyqtSignal(str)
    test_ended = pyqtSignal()
    play_sound_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.user_name = "user_name_default"
        self.date_birth = "date_birth_default"

        config = ConfigParser()

        config.read(config_file_name)
        self.key_info = []
        try:
            self.seq_a = config['Sequences']['seq_a']
            self.seq_b = config['Sequences']['seq_b']

            self.random_repeats = int(config['Settings']['random_repeats'])
            self.learn_repeats = int(config['Settings']['learn_repeats'])
            self.test_repeats = int(config['Settings']['test_repeats'])
            data_file_name = config['Datafile']['data_file_name']
        except KeyError:
            print("No config file provided for the application.")
            exit()


        with open(data_file_name, 'rb') as data_file:
            self.seq_random = pickle.load(data_file)
            self.seq_learn = pickle.load(data_file)
            self.seq_test = pickle.load(data_file)
        l_random = min(self.random_repeats, len(self.seq_random))
        l_learn = min(self.learn_repeats, len(self.seq_learn))
        l_test = min(self.test_repeats, len(self.seq_test))
        self.seq = self.seq_random[:l_random] + self.seq_learn[:l_learn] + self.seq_test[:l_test]

    def start_testing(self, user_name, date_birth):
        self.user_name = user_name
        self.date_birth = date_birth
        print(f"User information recorded: {user_name}, {date_birth}")
        self.current_number = 0

    def emit_number(self):
        if self.current_number >= len(self.seq):
            self.test_ended.emit()
            return

        self.start_time = self.timer()
        self.our_seq, self.position, self.current_element = self.seq[self.current_number]
        self.number_to_show_event.emit(self.current_element)

    def timer(self):
        return dt.datetime.now()

    def match_check(self, key):
        # тайминг
        self.stop_time = self.timer()
        ping = self.stop_time - self.start_time
        correctness = (key == self.current_element)
        key_record = User_Record(Sequence=self.our_seq, Position=self.position, Right_answer=self.current_element,
                                 User_answer=key, Correctness=correctness, Start_time=self.start_time,
                                 Stop_time=self.stop_time, RT=ping.total_seconds())
        self.key_info.append(key_record)
        self.current_number += 1
        self.play_sound_signal.emit(str(correctness))

    def print_results(self):
        if len(self.key_info) == 0:
            print("No user answers were recorded - nothing to output")
            return
        user_name_birth = self.user_name + ' ' + self.date_birth
        hash_user = hashlib.md5(user_name_birth.encode()).hexdigest()[:15]
        current_date = dt.datetime.now().strftime("%Y-%m-%d_%H-%M")
        with open('user_to_hash.txt', 'a') as user_to_hash:
            user_to_hash.write(f"{user_name_birth}\t{hash_user}\t{current_date}\n")
        results_file_name = f'res_{hash_user}_{current_date}.tsv'
        with open(results_file_name, 'w') as out_file:
            out_file.write('Sequence A:\t' + self.seq_a + '\n')
            out_file.write('Sequence B:\t' + self.seq_b + '\n')
            out_file.write('\t'.join(User_Record._fields) + '\n')
            for key_record in self.key_info:
                out_file.write("\t".join([str(el) for el in key_record]) + "\n")

        post_processing(results_file_name)
