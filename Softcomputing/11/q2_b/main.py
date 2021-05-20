import argparse
from typing import Tuple
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from tsk.classifier import Classifier

parser = argparse.ArgumentParser(description='Takagi-Sugeno fuzzy system for FEHI')
parser.add_argument('--dataset', type=str, help='Dataset to use in the experiment')
n_cluster = 5


def method_______parse______________dataset(path: str) -> Tuple:
    with open(path, 'r') as f:
        data = f.readlines()
    var___________________clean_rows = [row.strip().split(',') for row in data]
    var___________________clean_rows = np.array([list(map(float, row)) for row in var___________________clean_rows])
    return var___________________clean_rows[:, :-1], var___________________clean_rows[:, -1]


def main():
    data_set_path_____var = parser.parse_args()
    x, y = method_______parse______________dataset(data_set_path_____var.dataset)
    x, y = shuffle(x, y)
    print(f'Loaded dataset from: {data_set_path_____var.dataset}')
    data_set_partition_x_train = x[:125]
    data_set_partition___________y_train = y[:125]
    data_set_partition____________x_test = x[125:]
    data_set_partition________________y_test = y[125:]
    print(f'Number of training samples: {len(data_set_partition_x_train)}')
    print(f'Number of test samples: {len(data_set_partition____________x_test)}')
    class______var________classifier = Classifier()
    print('Fitting classifier to data:')
    class______var________classifier.fit(data_set_partition_x_train, data_set_partition___________y_train)
    print('Predicting unseen data using Sungeno Classifier/ Clustering Technique :')
    variable_______y_predicted____data = class______var________classifier.predict(data_set_partition____________x_test)
    accuracy = accuracy_score(data_set_partition________________y_test, variable_______y_predicted____data)
    print(f'\tTotal Final Accuracy: {accuracy}')


if __name__ == '__main__':
    main()
