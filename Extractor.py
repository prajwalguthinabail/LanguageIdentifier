import re

"""
file: Extractor.py
language: python3
authors: Prajwal Guthinabail
description: This file reads in text documents in 3 languages and processes them to prepare txt files with each line 
containing 15 words.
"""
__author__ = "Prajwal Guthinabail"


def prepro(fn):
    """
    Remove unwanted characters, create new collection with 15 words per line
    :param fn: filename
    :return: processed text collection
    """
    file = open(fn)
    words = file.read().split()
    count = 0
    sentrecs = []
    line = []
    for w_idx in range(len(words)):
        word = words[w_idx]
        if re.match('[0-9]*', word):
            word = re.sub('[0-9]*', '', word)
        if re.match('[!?~`@#$%&*)(_=+/.,"»;«-]*', word):
            word = re.sub('[!?~`@#$%&*)(_=+/.,"»;«-]*', '', word)
        if word != '':
            line.append(word.lower())
            if len(line) == 15:
                sentrecs.append(line)
                line = []
    return sentrecs


def writefile(sentrecs, fname, sep, header):
    with open(fname, 'w') as cfile:
        cfile.writelines(header)
        cfile.write('\n')
        for line in sentrecs:
            row = ''
            for word in line:
                row += str(word) + sep
            cfile.writelines(row[:len(row) - 1])
            cfile.write('\n')


def classify(sentence, lang):
    """
    Find language specific features and create boolean records
    :param sentence: text
    :param lang: language
    :return: boolean record
    """
    sen = sentence.split()
    fline = []

    # English   0
    if (sen.__contains__('the') or sen.__contains__(
            'but') or sen.__contains__('and') or sen.__contains__('for') or sen.__contains__('that')):
        fline.append(True)
    else:
        fline.append(False)

    # English and Dutch 1
    if (sen.__contains__('is') or sen.__contains__('was') or sen.__contains__('of')):
        fline.append(True)
    else:
        fline.append(False)

    # Dutch 2
    if (sen.__contains__('het') or sen.__contains__('de') or sen.__contains__('en') or sen.__contains__(
            'een') or sen.__contains__('voor')):
        fline.append(True)
    else:
        fline.append(False)

    # English and Italian    3
    if (sen.__contains__('come') or sen.__contains__('a')):
        fline.append(True)
    else:
        fline.append(False)

    # Italian   4
    if (sen.__contains__('e') or sen.__contains__('il') or sen.__contains__('un') or sen.__contains__('che')):
        fline.append(True)
    else:
        fline.append(False)

    # Contains in substring 5   italian
    if (not sentence.__contains__('j') and not sentence.__contains__('k') and not sentence.__contains__(
            'w') and not sentence.__contains__('x') and not sentence.__contains__('y')):
        # print( 'has jkwyx', lang)
        fline.append(True)
    else:
        fline.append(False)

    # 6 dutch
    if (sentence.__contains__('sch') or sentence.__contains__('ijk')):
        # print(sentence, 'has ijk or sch')
        fline.append(True)
    else:
        fline.append(False)

    # 7 italian
    if (sentence.__contains__("l'")):
        # print(sentence, 'has l"')
        fline.append(True)
    else:
        fline.append(False)

    # 8 italian and dutch
    if (sentence.__contains__('aa') or sentence.__contains__('ii') or sentence.__contains__('uu')):
        # print(sentence, 'had double vowel')
        fline.append(True)
    else:
        fline.append(False)

    # 9 italian
    if (sentence.__contains__('è')):
        # print('had è, lang)
        fline.append(True)
    else:
        fline.append(False)

    return fline


def process(pfn, lang):
    """
    Get training file from the text documents based on select features
    :param pfn: filename to read txt
    :param lang: txt language
    :return: records
    """
    train_rec = []
    with open(pfn) as cfile:
        lines = cfile.readlines()
        for line in lines:
            flag = classify(line.strip(), lang)
            # Ignoreinstances if all attribute values are same
            if flag.count(False) != len(flag) and flag.count(True) != len(flag):
                flag.append(lang)
                train_rec.append(flag)

    return train_rec


def main():
    # fn = input('Enter document name')
    # lang= input('Enter any one: E, D, I')
    fne = 'e.txt'
    lange = 'E'

    fni = 'i.txt'
    langi = 'I'

    fnd = 'd.txt'
    langd = 'D'

    # Create processed document with each line containing 15 words
    recse = prepro(fne)
    writefile(recse, 'new_'+fne, ' ','')

    recsi = prepro(fni)
    writefile(recsi, 'new_'+fni, ' ','')

    recsd = prepro(fnd)
    writefile(recsd, 'new_'+fnd, ' ','')

    # Create a trainer csv which has True or False for various features
    traine = process('new_' + fne, lange)  # 20223
    le = len(traine)
    traini = process('new_' + fni, langi)  # 14488
    li = len(traini)
    traind = process('new_' + fnd, langd)  # 17263
    ld = len(traind)

    # Select equal number of records from all languages and use this to control number of records
    l = min(le, li, ld) // 3

    header = 'A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,LANG'
    writefile(traine[:l] + traini[:l] + traind[:l], 'trainfile.csv', ',', header)


if __name__ == '__main__':
    main()
