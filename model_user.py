import random
import json
from tqdm import tqdm
from math import inf
import time
from dataclasses import dataclass
import threading
from pprint import pprint

@dataclass
class Student:
    setting: float
    score: float = 0
    iteration: int = 0

# It's what made NumPy obsolete (yes basically slightly modified binary search)
# Model in this place is supposed to be table of probabilities (aka model[choice][1]), num on the other hand is randomly generated number
# Index returned here is required for finding apropriate word choice list
def search(model, num):
    bottom = 0
    top = len(model) - 1
    closest = 0

    while bottom <= top:
        closest = int((bottom + top) / 2)
        if model[closest] < num:
            bottom = closest + 1
        elif model[closest] > num:
            top = closest - 1
        else:
            break
    
    return bottom

def generate(model, start = None):
    sum_of_posibilities = 1
    choice = random.choice(list(model.keys())) if start is None else start
    sentence = [choice]

    while True:
        index = search(model[choice][1], random.random())
        prev_choice = choice
        choice = model[prev_choice][0][index]
        if choice:
            sentence.append(choice)
            sum_of_posibilities *= model[prev_choice][1][index]
        else:
            break
    return ' '.join(sentence), sum_of_posibilities

def getbest(model, student: Student):
    test = [generate(model) for _ in range(10)]
    max_prob = 0
    index = 0
    for enum, (_, prob) in enumerate(test):
        if prob == 1:
            prob = student.setting
        if max_prob < prob:
            index = enum
            max_prob = prob

    return test[index]

# if __name__ == "__main__":
#     with open('model.json', 'r') as f:
#         model = json.load(f)
#     ones = 1
#     iters = 0
#     with tqdm(total=1) as pbar:
#         while True:
#             time.sleep(0.1)
#             iters += 1
#             res = getbest(model)
#             if len(res[0].split(' ')) == 1:
#                 ones += 1
#             pbarset = (ones / iters) - pbar.n
#             pbar.update(pbarset)

def test_student(model, student, testing_steps, expected):
    ones = 0
    for iters, _ in enumerate(range(testing_steps), start=1):
    # for iters, _ in enumerate(range(testing_steps), start=1):
        res = getbest(model, student)
        if len(res[0].split(' ')) == 1:
            ones += 1
        ratio = ones / iters

    try:
        student.score = 100 / (expected - ratio) if expected > ratio else 100 / (ratio - expected)
    except ZeroDivisionError:
        student.score = 100 / (1 / testing_steps)

# def learning(model, testing_steps = 10, step = 0.1, expected = 0.6, iterations = 10, students = 5):
#     student_list = []
#     best_student = student(0)
#     for i in tqdm(range(iterations)):
#         if i == 0:
#             student_list.extend(student(random.random()) for _ in range(students))
#         else:
#             student_list = [student(random.uniform(best_student.setting - step, best_student.setting + step)) for _ in range(students)]

def learning(model, testing_steps = 20, step = 0.1, expected = 0.6, iterations = 5, students = 5):
    best_student = Student(0, 0, 0)
    changes = 0
    for i in tqdm(range(iterations)):
        student_list = []
        if i == 0:
            student_list.extend(Student(random.random(), iteration=i) for _ in range(students))
        else:
            student_list.extend(Student(random.uniform(best_student.setting - step, best_student.setting + step), iteration=i) for _ in range(int(students/2)))
            student_list.extend(Student(random.random(), iteration=i) for _ in range(int(students/2)))
        thread_list = [threading.Thread(target=test_student, args=(model, i, testing_steps, expected,)) for i in student_list]
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
        
        for student in student_list:
            if student.score > best_student.score:
                best_student = student
        if i == best_student.iteration:
            changes = 0
            with open(f'models/student_model_{i}.json', 'w') as f:
                json.dump({'setting': best_student.setting, 'score': best_student.score}, f)
            print('Step best: ', best_student)
        else:
            changes += 1
            if changes == 3:
                print("Breaking due to score not improving.")
                break
            print(f'Iteration {best_student.iteration} still has the best student. {3-changes} left to break.')

    print(best_student)
    with open('models/student_model_final.json', 'w') as f:
            json.dump({'setting': best_student.setting, 'score': best_student.score}, f)

    return best_student


if __name__ == "__main__":
    with open('model.json', 'r') as f:
        model = json.load(f)
    # learning(model, 100, 0.05, 0.6, 10, 5)
    nintyp = learning(model, 20, 0.1, 1, 10, 10)

    tyryry = 100
    nintylist = [getbest(model, nintyp) for _ in tqdm(range(tyryry))]
    nintyratio = sum(len(res[0].split(' ')) == 1 for res in nintylist)
    print(f'Ninty ratio: {nintyratio/tyryry}')