import random


class Test_Strategy_Random(object):
    def __init__(self, count):
        self.seq = ['1', '2', '3', '4'] * count
        random.shuffle(self.seq)

    def __iter__(self):
        self.iter = self.seq.__iter__()
        return self

    def __next__(self):
        return 'R', -1, self.iter.__next__()


class Test_Strategy_Learn(object):
    def __init__(self, seq, count):
        self.seq = seq
        self.count = count
        self.length = len(self.seq)

    def __iter__(self):
        self.position = 0
        self.numbers_shown = 0
        return self

    def __next__(self):
        if self.numbers_shown >= self.length * self.count:
            raise StopIteration
        el = 'L', self.position, self.seq[self.position]

        self.numbers_shown += 1
        self.position += 1
        self.position %= self.length
        return el


class Test_Strategy_Kaufman(object):
    def __init__(self, seq_a, seq_b, repeats, jump_probability, max_stay_in_control=8):
        self.seq_a = seq_a
        self.seq_b = seq_b
        self.repeats = repeats
        self.jump_probability = jump_probability
        self.max_stay_in_control = max_stay_in_control
        self.dict_seq_a = self.make_dictionaries(self.seq_a)
        self.dict_seq_b = self.make_dictionaries(self.seq_b)

    def __iter__(self):
        self.our_seq = "A"
        self.position = 0
        self.numbers_shown = 0
        self.current_stay_in_control = 0
        return self

    def __next__(self):
        if self.numbers_shown >= self.repeats * len(self.seq_a):
            raise StopIteration
        element = self.our_seq, self.position, self.return_current_el()
        self.choose_next_el()
        return element

    def return_current_el(self):
        if self.our_seq == "A":
            current_element = self.seq_a[self.position]
        else:
            current_element = self.seq_b[self.position]
        return current_element

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

    def random_and_new_position(self):
        change = False
        randomizator = random.random()
        if self.our_seq == "A":
            combination = (self.seq_a[self.position - 1], self.seq_a[self.position])
        else:
            combination = (self.seq_b[self.position - 1], self.seq_b[self.position])

        if randomizator <= self.jump_probability and self.our_seq == "A":
            change = True
            new_position = self.dict_seq_b[combination]
        elif (
                randomizator > self.jump_probability or self.current_stay_in_control >= self.max_stay_in_control) and self.our_seq == "B":
            change = True
            self.current_stay_in_control = 0
            new_position = self.dict_seq_a[combination]
        else:
            new_position = self.position
            if self.our_seq == "B":
                self.current_stay_in_control += 1
        new_position = (new_position + 1) % 12

        return change, new_position

    def choose_next_el(self):
        change, new_position = self.random_and_new_position()
        current_element = self.seq_to_seq_jumping(change, new_position)
        self.numbers_shown += 1
        return current_element
