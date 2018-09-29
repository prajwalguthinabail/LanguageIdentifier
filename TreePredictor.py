
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

	if not sentence.__contains__('j') and not sentence.__contains__('k') and not sentence.__contains__('w') and not sentence.__contains__('x') and not sentence.__contains__('y'):
		if sen.__contains__('the') or sen.__contains__('but') or sen.__contains__('and') or sen.__contains__('for') or sen.__contains__('that'):
			return 'English'
		else:
			if sen.__contains__('is') or sen.__contains__('was') or sen.__contains__('of'):
				return 'Dutch'
			else:
				if sentence.__contains__('aa') or sentence.__contains__('ii') or sentence.__contains__('uu'):
					return 'Italian'
				else:
					return 'Italian'
	else:
		if sen.__contains__('het') or sen.__contains__('de') or sen.__contains__('en') or sen.__contains__('een') or sen.__contains__('voor'):
			if sen.__contains__('e') or sen.__contains__('il') or sen.__contains__('un') or sen.__contains__('che'):
				if sentence.__contains__('sch') or sentence.__contains__('ijk'):
					return 'Dutch'
				else:
					return 'Italian'
			else:
				if sentence.__contains__("l'"):
					return 'Italian'
				else:
					return 'Dutch'
		else:
			if sentence.__contains__('aa') or sentence.__contains__('ii') or sentence.__contains__('uu'):
				if sen.__contains__('e') or sen.__contains__('il') or sen.__contains__('un') or sen.__contains__('che'):
					return 'Italian'
				else:
					return 'Dutch'
			else:
				if sen.__contains__('e') or sen.__contains__('il') or sen.__contains__('un') or sen.__contains__('che'):
					return 'Italian'
				else:
					return 'English'


if __name__ == '__main__':
    main()