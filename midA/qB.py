import re

text = input()
 
word = input()
 
match = re.search(word, text)

if match:
    print('First time {} occured in position:'.format(word))
    # text_pos = match.span()
    print(match.start())
    #возвращает индекс найденного слова
else:
    print('Not found')