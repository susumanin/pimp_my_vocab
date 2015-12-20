__author__ = 'mak'

import epub

book = epub.open_epub('TFASbook.epub')

for item in book.opf.manifest.values():
    # read the content
    data = book.read_item(item)
    print(item.media_type)
    #if (item.media_type == 'application/xhtml+xml'):
        #print(data.decode('utf-8'))

