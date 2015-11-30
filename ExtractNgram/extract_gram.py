__author__ = 'v-tedl'

import os
import csv
import string
from nltk.util import ngrams
#from nltk.stem import SnowballStemmer
#stemmer = SnowballStemmer('english')
fp = open('stopwords.txt', 'r')
_stop_words = []
for line in fp:
    _stop_words.append(line.strip('\n').strip(' '))
fp.close()
print _stop_words
print 'the' in _stop_words
print _stop_words
path = 'Wunderlist/'
delset = string.punctuation

for filename in os.listdir(path):
    assert filename.endswith('.csv')
    print filename, '--------'
    csvfile = file(path + filename, 'rb')
    reader = csv.reader(csvfile)
    lines = []
    ng = [dict(), dict(), dict()]
    _processed_texts = []
    count = 0
    for line in reader:
        if line[0] == 'list_title':
            continue
        content = '%s %s' % (line[1], line[2].strip(' ').replace('\n', '').replace('\t', '').replace('http://www/', ''))
        if 'http' in content:
            content = content.replace('/', ' ').replace('http', '')
        sentence = content.translate(None, delset).decode('utf8')
        _word_list = [word.encode('utf8') for word in sentence.split(' ') if word != '']

        _stemmed_word_list = filter(lambda x: x.lower() not in _stop_words, _word_list)
        if count == 0:
            print _stemmed_word_list
            count += 1
        _processed_texts.append(_stemmed_word_list)
        for i in xrange(1, 4):
            igram = ngrams(_stemmed_word_list, i)
            for item in igram:
                key = ' '.join(item)
                ng[i-1][key] = ng[i-1].get(key, 0) + 1
    csvfile.close()
    for i in xrange(1, 4):
        fp = open('%s_gram/%s_%sgram.txt' % (i, filename, i), 'w+')
        _sorted_dict_items = sorted(ng[i-1].iteritems(), key=lambda t:t[1], reverse=True)
        for item in _sorted_dict_items:
            fp.write('%s\t%s\n' % (item[0], item[1]))

    """
    lines = [[], [], []]
    for sequence in _processed_texts:
        for i in xrange(1, 4):
            igram = ngrams(sequence, i)
            line = []
            for item in igram:
                key = ' '.join(item)
                line.append('%s:%s' % (key, ng[i-1][key]))
            sorted_line = sorted(line, key=lambda x: int(x.split(':')[1]), reverse=True)
            lines[i-1].append('%s\n' % '\t'.join(list(set(sorted_line))))
    for i in xrange(1, 4):
        fp = open('%s_gram/%s_%sgram.txt' % (i, filename, i), 'w+')
        fp.writelines(lines[i-1])
        fp.close()
    """
