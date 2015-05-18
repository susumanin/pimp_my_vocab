f = open('/Users/mak/Documents/python_scripts/vocab/rank_word_count', 'r',
            encoding='utf-8')
list_of_words = f.readlines()
k = 0

for line in list_of_words:
    splitted_line = line.split('	')
    print(splitted_line[1])
    k = k + 1
    if k == 3:
        break
