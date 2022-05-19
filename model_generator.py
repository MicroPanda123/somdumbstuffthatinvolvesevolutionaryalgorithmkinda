import json
from tqdm import tqdm

# This peace creates transition matrix, this is the most important but also the worst piece of this code.
# It takes list of sentences as input.
def create_transition_matrix(read: list):
    transition_matrix = {}
    for inputs in tqdm(read):
        inputs_list = inputs.split(' ')
        for i, word in enumerate(inputs_list):
            try:
                try:
                    transition_matrix[word][inputs_list[i+1]] += 1
                except Exception:
                    try:
                        transition_matrix[word][inputs_list[i+1]] = 1
                    except Exception:
                        transition_matrix[word] = {inputs_list[i+1]: 1}
            except IndexError:
                try:
                    transition_matrix[word][None] += 1
                except Exception:
                    try:
                        transition_matrix[word][None] = 1
                    except Exception:
                        transition_matrix[word] = {None: 1}
    return transition_matrix

# This part turns transition_matrix generated previously into model.
def turn_to_model(transition_matrix):
    new_matrix = {}
    model = {}
    for key, val in tqdm(transition_matrix.items()):
        new_matrix[key] = {}
        summed = sum(val.values())
        for word, times in val.items():
            new_matrix[key][word] = times/summed
        model[key] = [[],[]]
        matrix_sum = 0
        for a, p in new_matrix[key].items():
            matrix_sum += p
            model[key][0].append(a)
            model[key][1].append(matrix_sum)
    return model

# This just saves 'model' into a json file
def save_to_json(model, save_file):
    with open(save_file, 'w', encoding='utf-8') as f:
        json.dump(model, f, allow_nan=True, indent=3)

if __name__ == "__main__":
    text_file = 'sample.txt'
    model_save_file = 'model.json'

    with open(text_file, 'r', encoding='utf-8') as f:
            read = f.readlines()
    transition_matrix = create_transition_matrix(read)
    model = turn_to_model(transition_matrix)
    save_to_json(model, model_save_file)