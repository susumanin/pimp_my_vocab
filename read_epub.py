__author__ = 'mak'

import epub

book = epub.open_epub('TFASbook.epub')
epubNavPointsList = book.toc.nav_map.nav_point
for point in epubNavPointsList:
    print('%s. %s'%(point.play_order, point.labels[0][0]))
chosenChapter = int(input("Give me the chapter: "))
curPoint = epubNavPointsList[chosenChapter - 1]
print(curPoint)
curItem = book.get_item_by_href(curPoint.src)
readedItemB = book.read_item(curItem)
readedItem = readedItemB.decode('utf-8', 'ignore')
print(readedItem)


'''for item in book.opf.manifest.values():
    # read the content
    data = book.read_item(item)
    print(item.media_type)
    if (item.media_type == 'application/x-dtbncx+xml'):
        print(data.decode('utf-8'))
        justStr = book.read_item(item)
        xmlData = data.decode('utf-8')
'''