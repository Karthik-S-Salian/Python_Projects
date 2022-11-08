from json import load
from random import randint, shuffle
from time import gmtime, time
import pathlib


class ExamHandler:
    def __init__(self):
        self.reset()
        self.load_available_question_sets()

    def reset(self):
        self.start_time=None
        self.current = 0
        self.no_attempted_q = 0
        self.remaining_q = 40
        self.no_marked = 0
        self.mark = 0
        self.stop_time = 0
        self.has_started = False
        self.question_set_index = None
        self.topic=""
        self.subject = None
        self.stop_time=None


    def load_questions(self):
        path=self.data_dict[self.subject]["question_sets"][self.question_set_index]
        with open(path) as fp:
            self.question_set = load(fp)

    def load_available_question_sets(self) -> dict:
        data_dir = pathlib.Path("data")
        self.data_dict = dict()
        for dir in data_dir.iterdir():
            d = dict()
            if dir.is_dir():
                d["question_sets"] = list(dir.glob("./question_sets/*.json"))
                d["bg_image"] = list(dir.glob("./bg_image/*.jpg"))[0]
                self.data_dict[dir.name] = d
        return self.data_dict

    def start_session(self, current_set):
        self.start_time = time()
        self.has_started = True
        self.load_questions()
        self.init_exam()

    def end_session(self):
        self.stop_time = gmtime(time() - self.start_time)
        self.evaluate_marks()
        self.has_started = False

    def select_questions(self):
        l = len(self.question_set) - 1
        question_list = [randint(0, l) for _ in range(40)]
        var = len(set(question_list))
        while var < 40:
            question_list.extend([randint(0, l) for _ in range(40 - var)])
            var = len(set(question_list))
        return list(set(question_list))

    def init_exam(self):
        current_questions = self.select_questions()
        self.question_list = []
        for ele in current_questions:
            d: dict = self.question_set[ele].copy()
            c = d["options"][0]
            shuffle(d["options"])
            d["answer"] = d["options"].index(c)
            d["selected"] = None
            d["marked"] = False
            self.question_list.append(d)

    def get_time(self):
        c = gmtime(45 * 60 - (time() - self.start_time))
        return c.tm_min, c.tm_sec

    def evaluate_marks(self):
        self.mark = 0
        for ele in self.question_list:
            if ele["selected"]:
                if ele["selected"] == ele["answer"]:
                    self.mark += 1

    def get_current_question(self, index):
        self.current = index
        l = self.question_list[index]
        return l["question"], l["options"], l["selected"], l["marked"]

    def change_selection(self, value):
        if self.question_list[self.current]["selected"] is None:
            self.no_attempted_q += 1
            self.remaining_q = 40 - self.no_attempted_q
        self.question_list[self.current]["selected"] = value

    def clear_selection(self):
        self.no_attempted_q -= 1
        self.remaining_q = 40 - self.no_attempted_q
        self.question_list[self.current]["selected"] = None

    def change_review_state(self):
        if self.question_list[self.current]["marked"]:
            self.question_list[self.current]["marked"] = False
            self.no_marked -= 1
            return False, (self.question_list[self.current]["selected"] is None)
        self.question_list[self.current]["marked"] = True
        self.no_marked += 1
        return True, False


