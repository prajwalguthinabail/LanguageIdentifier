import csv

"""
file: TreeTrainer.py
language: python3
authors: Prajwal Guthinabail
description: This file generates a decision tree program as another py file based on the training data.
"""
__author__ = "Prajwal Guthinabail"

# Parameters to tune the decision tree generation
DEPTH = 5  # Recursion depth
MIN_INSTANCES = 60  # Remaining instances to classifiy
MAJORITY = 1.0  # portion of majority belonging to same class


def main():
    """
    Reads csv file to get training data, calls functions to write content to the other program
    :return: none
    """
    training_file = 'trainfile.csv'
    attributes, records = read_csv(training_file)

    attr_feat = {attributes[0]: "sen.__contains__('the') or sen.__contains__('but') or sen.__contains__('and') or "
                         "sen.__contains__('for') or sen.__contains__('that')",
                 attributes[1]: "sen.__contains__('is') or sen.__contains__('was') or sen.__contains__('of')",
                 attributes[2]: "sen.__contains__('het') or sen.__contains__('de') or sen.__contains__('en') or "
                         "sen.__contains__('een') or sen.__contains__('voor')",
                 attributes[3]: "sen.__contains__('come') or sen.__contains__('a')",
                 attributes[4]: "sen.__contains__('e') or sen.__contains__('il') or sen.__contains__('un') or "
                         "sen.__contains__('che')",
                 attributes[5]: "not sentence.__contains__('j') and not sentence.__contains__('k') and not "
                         "sentence.__contains__('w') and not sentence.__contains__('x') and not "
                         "sentence.__contains__('y')",
                 attributes[6]: "sentence.__contains__('sch') or sentence.__contains__('ijk')",
                 attributes[7]: "sentence.__contains__(\"l'\")",
                 attributes[8]: "sentence.__contains__('aa') or sentence.__contains__('ii') or sentence.__contains__('uu')",
                 attributes[9]: "sentence.__contains__('è')"
                 }

    # Program file with decision tree
    dst_file = open('TreePredictor.py', 'w', encoding='UTF-8')
    emit_prologue(dst_file)
    build_tree(records, attributes, attr_feat, 1, dst_file)
    emit_epilogue(dst_file)
    # Close second program file once write is complete
    dst_file.close()

    check_accuracy()


def build_tree(records, attributes, attr_feat, depth, dst_file):
    """
    The core part of the program which builds a decision tree based on the training data.
    :param dst_file: file to create
    :param attr_feat: key-value set for features
    :param records: training data
    :param attributes: data attribute names
    :param depth: used to indent code based on recursion level
    :return: target class
    """
    tab = '\t'

    total_records = len(records)
    majority_attr, majority_count = zero_rule(records)

    # Stop if X% of records belong to one group or if number of records are less than equal to n or depth equals to m
    if majority_count >= MAJORITY * total_records or total_records <= MIN_INSTANCES or depth == DEPTH:
        dst_file.write(tab * depth)
        if majority_attr == 'E':
            result = 'English'
        elif majority_attr == 'I':
            result = 'Italian'
        else:
            result = 'Dutch'
        dst_file.write('return \'' + result + '\'\n')
        return majority_attr
    else:
        # Initialize with worst value possible
        best_impurity = 1.0
        # Check all possible attributes and their values
        for attr_idx in range(len(attributes) - 1):
            impurity = compute_impurity(attr_idx, records)
            # Keep track of best possible values
            if impurity <= best_impurity:
                best_impurity = impurity
                best_attr = attr_idx

        # Split data
        left_records, right_records = split(best_attr, records)
        # Use selected attributes and threshold as decision nodes
        dst_file.write(tab * depth + 'if ' + attr_feat[attributes[best_attr]] + ':\n')
        build_tree(left_records, attributes, attr_feat, depth + 1, dst_file)
        dst_file.write(tab * depth)
        dst_file.write('else:\n')
        build_tree(right_records, attributes, attr_feat, depth + 1, dst_file)


def check_accuracy():
    """
    Compute the accuracy of decision tree by testing on training records and verifying the results with given labels
    :return: none
    """
    from TreePredictor import classify

    files = ['new_e.txt', 'new_i.txt', 'new_d.txt']
    print('\nAccuracy for English, Italian, and Dutch')
    for fi in range(len(files)):
        count_e = 0
        count_i = 0
        count_d = 0
        with open(files[fi]) as cfile:
            lines = cfile.readlines()
            for line in lines:
                res = classify(line.strip(), line.strip().split())
                if res == "English":
                    count_e += 1
                elif res == "Italian":
                    count_i += 1
                else:
                    count_d += 1
            count = [count_e, count_i, count_d]
            # print('\n\nEnglish:',count_e,'\nItalian:',count_i,'\nDutch:',count_d, )
            print(round(count[fi] / (count_e + count_i + count_d) * 100, 4), '%')


def compute_impurity(attr_idx, records):
    """
    Compute impurity for the records
    :param records: input
    :param attr_idx: Attribute used to split
    :return: impurity score
    """
    group1_1 = 0
    group1_2 = 0
    group1_3 = 0
    group2_1 = 0
    group2_2 = 0
    group2_3 = 0
    # Split data based on the threshold to get values in frequency table
    for values in records:
        if values[attr_idx] == 'True':
            if values[len(values) - 1] == 'E':
                group1_1 += 1
            elif values[len(values) - 1] == 'I':
                group1_2 += 1
            else:
                group1_3 += 1
        else:
            if values[len(values) - 1] == 'E':
                group2_1 += 1
            elif values[len(values) - 1] == 'I':
                group2_2 += 1
            else:
                group2_3 += 1

    group_1 = group1_1 + group1_2 + group1_3
    group_2 = group2_1 + group2_2 + group2_3
    if group_1 != 0:
        grp1 = 1 - (((group1_1 / group_1) ** 2) + ((group1_2 / group_1) ** 2) + ((group1_3 / group_1) ** 2))
    else:
        grp1 = 1

    if group_2 != 0:
        grp2 = 1 - (((group2_1 / group_2) ** 2) + ((group2_2 / group_2) ** 2) + ((group2_3 / group_2) ** 2))
    else:
        grp2 = 1
    # Return impurity
    return (group_1 / (group_1 + group_2) * grp1) + (group_2 / (group_1 + group_2) * grp2)


def split(best_attr, records):
    """
    Split the input records based on the threshold value of a selected attribute
    :param best_attr: attribute used to split
    :param records: input data
    :return: none
    """
    left_records = []
    right_records = []
    for values in records:
        if values[best_attr] == 'True':
            left_records.append(values)
        else:
            right_records.append(values)
    return left_records, right_records


def zero_rule(records):
    """
    Get majority class for target attribute by using the 0-rule
    :param records: input data
    :return: majority value and its count
    """
    class0 = 0
    class1 = 0
    class2 = 0
    for row in records:
        if row[len(row) - 1] == 'E':
            class0 += 1
        elif row[len(row) - 1] == 'I':
            class1 += 1
        else:
            class2 += 1

    if class0 > class1 and class0 > class2:
        return 'E', class0
    elif class1 > class0 and class1 > class2:
        return 'I', class1
    else:
        return 'D', class2


def read_csv(filename):
    """
    Read rows from csv file and store as a collection
    :param filename: csv file
    :return: attributes name list and their rows
    """
    records = []
    with open(filename) as csv_data:
        lines = csv.reader(csv_data, delimiter=',')
        attributes = next(lines)

        if attributes is not None:
            for row in lines:
                line = []
                for idx in range(len(row)):
                    line.append((row[idx]))
                records.append(line)
    return attributes, records


def emit_prologue(dst_file):
    """
    Writes the boiler plate code of second program. It contains snippet and functions to read test data, write the
    classification results to a new csv file.
    :return: none
    """
    code = str('''
import re


def process():
    words = input('Enter the sentence to predict its language').strip().split()
    line = ''
    for w_idx in range(len(words)):
        word = words[w_idx]
        if re.match('[0-9]*', word):
            word = re.sub('[0-9]*', '', word)
        if re.match('[!?~`@#$%&*)(_=+/.,"»;«-]*', word):
            word = re.sub('[!?~`@#$%&*)(_=+/.,"»;«-]*', '', word)
        if word != '':
            line += (word.lower())+' '

    return line.strip()
    
    
def main():
    sentence = process()
    print(classify(sentence, sentence.split()))


def classify(sentence, sen):

''')

    dst_file.write(code)


def emit_epilogue(dst_file):
    """
    Print the end part of code snippet of second program
    :return: none
    """
    code = str('''

if __name__ == '__main__':
    main()''')
    dst_file.write(code)


if __name__ == '__main__':
    main()
