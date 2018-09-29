
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
    svalsei = [2.5276280158302, 3.8288863851536448, 4.399189916724655, 2.707601568439506, 1.2675158708428773]
    svalsid = [2.321058785991497, 2.6825244643090156, 3.3743246268226366, 1.570675270705791, 4.59358865343983, 1.8341824783987517]
    svalsed = [2.5276280158302, 4.372702946036679, 2.862214528485689]

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


if __name__ == '__main__':
    main()