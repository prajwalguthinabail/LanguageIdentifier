import csv
from math import log

"""
file: AdaTrainer.py
language: python3
authors: Prajwal Guthinabail
description: This file generates a ensemble classifier program as another py file based on the training data.
"""
__author__ = "Prajwal Guthinabail"


def main():
    training_file = 'trainfile.csv'
    records = read_csv(training_file)

    lcountei = 5  # Learners for classifying English and Italian
    svalsei = adatrain(records, lcountei, 'EI')

    lcountid = 6  # Learners for classifying Dutch and Italian
    svalsid = adatrain(records, lcountid, 'ID')

    lcounted = 3  # Learners for classifying English and Dutch
    svalsed = adatrain(records, lcounted, 'ED')

    # Program file with decision tree
    dst_file = open('AdaPredictor.py', 'w', encoding='UTF-8')
    emit_prologue(dst_file, str(svalsei), str(svalsid), str(svalsed))
    emit_epilogue(dst_file)
    # Close second program file once write is complete
    dst_file.close()

    check_accuracy()


def check_accuracy():
    """
    Compute the accuracy of classifier
    :return: none
    """
    from AdaPredictor import predict

    files = ['new_e.txt', 'new_i.txt', 'new_d.txt']
    print('\nAccuracy for English, Italian, and Dutch')
    for fi in range(len(files)):
        count_e = 0
        count_i = 0
        count_d = 0
        with open(files[fi]) as cfile:
            lines = cfile.readlines()
            for line in lines:
                res = predict(line.strip())
                if res == "English":
                    count_e += 1
                elif res == "Italian":
                    count_i += 1
                else:
                    count_d += 1
            count = [count_e, count_i, count_d]
            print(round(count[fi] / (count_e + count_i + count_d) * 100, 4), '%')


def adatrain(allrecords, learnercount, langs):
    """
    Adaboost algorithm to compute stage values for the learners.  Based on the pseudo code from textbook
    :param allrecords: input
    :param learnercount: number of leraners for these pair of languages
    :param langs: 2 languages key
    :return: stage values
    """
    if langs == 'EI':  # English vs Italian
        records = [rec for rec in allrecords if rec[len(rec) - 1] == 'E' or rec[len(rec) - 1] == 'I']
    elif langs == 'ID':  # italian vs Dutch
        records = [rec for rec in allrecords if rec[len(rec) - 1] == 'I' or rec[len(rec) - 1] == 'D']
    else:  # English vs Dutch
        records = [rec for rec in allrecords if rec[len(rec) - 1] == 'E' or rec[len(rec) - 1] == 'D']
    weights = [1 / len(records)] * len(records)
    svals = []

    for learn in range(learnercount):
        error = 0
        for idx in range(len(records)):
            if oneR(records[idx], learn, langs) != records[idx][len(records[idx]) - 1]:
                error += weights[idx]
        for idx in range(len(records)):
            if oneR(records[idx], learn, langs) == records[idx][len(records[idx]) - 1]:
                weights[idx] *= error / (1 - error)
        for idx in range(len(records)):
            weights[idx] /= sum(weights)
        svals.append(log((1 - error) / error))
    return svals


def oneR(recline, learn, langs):
    """
    Collection of decision stumps for various pairs of languages
    :param recline: records
    :param learn: stump id
    :param langs: 2 languages
    :return: target class
    """
    if langs == 'EI':
        if learn == 0:
            if recline[0] == 'True':
                return 'E'
            else:
                return 'I'

        elif learn == 1:
            if recline[4] == 'False':
                return 'E'
            else:
                return 'I'

        elif learn == 2:
            if recline[5] == 'False':
                return 'E'
            else:
                return 'I'

        elif learn == 3:
            if recline[7] == 'False':
                return 'E'
            else:
                return 'I'

        else:
            if recline[9] == 'False':
                return 'E'
            else:
                return 'I'

    elif langs == 'ID':
        if learn == 0:
            if recline[2] == 'True':
                return 'D'
            else:
                return 'I'

        elif learn == 1:
            if recline[4] == 'False':
                return 'D'
            else:
                return 'I'

        elif learn == 2:
            if recline[5] == 'False':
                return 'D'
            else:
                return 'I'

        elif learn == 3:
            if recline[7] == 'False':
                return 'D'
            else:
                return 'I'

        elif learn == 4:
            if recline[6] == 'True':
                return 'D'
            else:
                return 'I'

        else:
            if recline[9] == 'False':
                return 'D'
            else:
                return 'I'
    else:
        if learn == 0:
            if recline[0] == 'True':
                return 'E'
            else:
                return 'D'

        elif learn == 1:
            if recline[2] == 'False':
                return 'E'
            else:
                return 'D'

        else:
            if recline[6] == 'False':
                return 'E'
            else:
                return 'D'


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
    return records


def emit_prologue(dst_file, svalsei, svalsid, svalsed):
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
    print(predict(sentence))
    

def predict(sentence):
    svalsei = '''
               + svalsei +
               '''
    svalsid = '''
               + svalsid +
               '''
    svalsed = '''
               + svalsed +
               '''

    resei = classify(sentence, 'EI', svalsei)  # + is I, - is E
    resid = classify(sentence, 'ID', svalsid)  # + is I, - is D
    resed = classify(sentence, 'ED', svalsed)  # + is D, - is E

    result = []
    if resei > 0:
        result.append('Italian')
    else:
        result.append('English')

    if resid > 0:
        result.append('Italian')
    else:
        result.append('Dutch')

    if resed > 0:
        result.append('Dutch')
    else:
        result.append('English')

    if result.count('English') == 2:
        return 'English'
    elif result.count('Italian') == 2:
        return 'Italian'
    else:
        return 'Dutch'
    

def classify(sentence, langs, svals):
    sen = sentence.split()
    result = []
    sum = 0
    if langs == 'EI':
        if sen.__contains__('the') or sen.__contains__('but') or sen.__contains__('and') or sen.__contains__('for') or sen.__contains__('that'):
            result.append(-1)#E
        else:
            result.append(1)#I

        if sen.__contains__('e') or sen.__contains__('il') or sen.__contains__('un') or sen.__contains__('che'):
            result.append(1)#I
        else:
            result.append(-1)#E

        if not sentence.__contains__('j') and not sentence.__contains__('k') and not sentence.__contains__('w') and not sentence.__contains__('x') and not sentence.__contains__('y'):
            result.append(1)#I
        else:
            result.append(-1)#E

        if sentence.__contains__("l'"):
            result.append(1)#I
        else:
            result.append(-1)#E

        if sentence.__contains__('è'):
            result.append(1)#I
        else:
            result.append(-1)#E

        for idx in result:
            sum += svals[idx]*result[idx]

        return sum

    elif langs == 'ID':
        if sen.__contains__('het') or sen.__contains__('de') or sen.__contains__('en') or sen.__contains__('een') or sen.__contains__('voor'):
            result.append(-1)#D
        else:
            result.append(1)#I

        if sen.__contains__('e') or sen.__contains__('il') or sen.__contains__('un') or sen.__contains__('che'):
            result.append(1)#I
        else:
            result.append(-1)#D

        if not sentence.__contains__('j') and not sentence.__contains__('k') and not sentence.__contains__('w') and not sentence.__contains__('x') and not sentence.__contains__('y'):
            result.append(1)#I
        else:
            result.append(-1)#D

        if sentence.__contains__("l'"):
            result.append(1)#I
        else:
            result.append(-1)#D

        if sentence.__contains__('sch') or sentence.__contains__('ijk'):
            result.append(-1)#D
        else:
            result.append(1)#I

        if sentence.__contains__('è'):
            result.append(1)#I
        else:
            result.append(-1)#D

        for idx in result:
            sum += svals[idx]*result[idx]

        return sum

    else:
        if sen.__contains__('the') or sen.__contains__('but')or sen.__contains__('and') or sen.__contains__('for') or sen.__contains__('that'):
            result.append(-1)#E
        else:
            result.append(1)#D

        if sen.__contains__('het') or sen.__contains__('de') or sen.__contains__('en') or sen.__contains__('een') or sen.__contains__('voor'):
            result.append(1)#D
        else:
            result.append(-1)#E

        if sentence.__contains__('sch') or sentence.__contains__('ijk'):
            result.append(1)#D
        else:
            result.append(-1)#E

        for idx in result:
            sum += svals[idx]*result[idx]

        return sum

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
