import argparse


def load_words_from_text_to_sql(filename='', sqlConString='',
                                numOfLines=0, printDebugMsg=False):
    """

    :type fileName: str
    """
    fileWithWords = open(filename, 'r', encoding='utf-8')
    listOfWords = fileWithWords.readlines()
    lineIndex = 0
    for line in listOfWords:
        lineIndex += 1
        splittedLine = line.split('\t')
        wordRank = splittedLine[0]
        wordText = splittedLine[1].lower()
        if printDebugMsg:
            print('The word {} has rank {}'.format(wordText, wordRank))
        if lineIndex == numOfLines:
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='''Need an action command: load -
        loads file from text to sql''')
    parser.add_argument('--numOfLines', type=int, help='''Number of lines to
                            read from file''')
    args = parser.parse_args()
    fileName = '/Users/mak/Documents/python_scripts/vocab/rank_word_count'
    sqlConString = ''
    if args.numOfLines is None:
        numOfLines = 0
    else:
        numOfLines = args.numOfLines
    if args.action == 'load':
        load_words_from_text_to_sql(fileName, sqlConString,
                                    numOfLines, printDebugMsg=True)


if __name__ == "__main__":
    main()
