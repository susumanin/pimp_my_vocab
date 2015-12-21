__author__ = 'mak'

import epub
from bs4 import BeautifulSoup

book = epub.open_epub('TFASbook.epub')
epubNavPointsList = book.toc.nav_map.nav_point
for point in epubNavPointsList:
    print('%s. %s'%(point.play_order, point.labels[0][0]))
chosenChapter = int(input("Give me the chapter: "))
curPoint = epubNavPointsList[chosenChapter - 1]
srcOfFile = curPoint.src
# this srcOfFile can contain #filepos attr at the end of string
# and we should remove it
position = srcOfFile.find('#')
srcOfFile = srcOfFile[:position]
curItem = book.get_item_by_href(srcOfFile)
readedItemB = book.read_item(curItem)
readedItem = readedItemB.decode('utf-8', 'ignore')
soup = BeautifulSoup(readedItem)
for script in soup(["script", "style"]):
    script.extract()
text = soup.get_text()
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
textWithoutDots = text.translate({ord(i):None for i in '1234567“890:"!,.?/'})
listOfAllwords = textWithoutDots.split(' ')
print('There are %s words in text.'% len(listOfAllwords))
dictOfUniqeWords = {}
for curWord in listOfAllwords:
    curWord = curWord.strip()
    curWord = curWord.lower()
    if curWord in dictOfUniqeWords:
        dictOfUniqeWords[curWord] = dictOfUniqeWords[curWord] + 1
    else:
        dictOfUniqeWords[curWord] = 1
print('There are %s distinct words in text.'% len(dictOfUniqeWords))
mostFreqWords = {}
for x, y in dictOfUniqeWords.items():
    #print("%s occur %s times" % (x, y))
    if y > 9:
        mostFreqWords[x] = y
print('Most frequent words: ')
for x, y in mostFreqWords.items():
    print("%s occur %s times" % (x, y))




'''for item in book.opf.manifest.values():
    # read the content
    data = book.read_item(item)
    print(item.media_type)
    if (item.media_type == 'application/x-dtbncx+xml'):
        print(data.decode('utf-8'))
        justStr = book.read_item(item)
        xmlData = data.decode('utf-8')
'''