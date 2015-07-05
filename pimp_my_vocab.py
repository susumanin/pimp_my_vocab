import argparse
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class WordsRank(Base):
    __tablename__ = 'word_with_ranks'
    rank = Column(Integer, primary_key=True)
    word = Column(String)
    know_status = Column(Integer)


def load_words_from_text_to_sql(filename='', sqlConString='',
                                numOfLines=0, printDebugMsg=False, startFrom=1):
    """

    :type fileName: str
    """
    fileWithWords = open(filename, 'r', encoding='utf-8')
    listOfWords = fileWithWords.readlines()
    lineIndex = 0
    readLine = 0
    engine = create_engine('sqlite:///vocabDB_sqlite')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    for line in listOfWords:
        lineIndex += 1
        if lineIndex < startFrom:
            continue
        else:
            readLine += 1
        splittedLine = line.split('\t')
        wordRank = int(splittedLine[0])
        wordText = splittedLine[1].lower()
        result = session.query(WordsRank).filter(WordsRank.rank == wordRank).all()
        if len(result) == 0:
            new_word = WordsRank(rank=wordRank, word=wordText, know_status=0)
            session.add(new_word)
            if printDebugMsg:
                print('The word {} has rank {} and added into the DB'.format(wordText, wordRank))
        else:
            if printDebugMsg:
                print('The word {} is already in the DB'.format(wordText))

        if numOfLines == readLine:
            break
    session.commit()


def show_stat(print_all=False):
    engine = create_engine('sqlite:///vocabDB_sqlite')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    result = session.query(WordsRank).count()
    count_of_know = session.query(WordsRank).filter(WordsRank.know_status == 1).count()
    count_of_unknow = session.query(WordsRank).filter(WordsRank.know_status == 2).count()
    print('There are {} words in vocab'.format(result))
    print('{} words you know'.format(count_of_know))
    print('{} words you don\'t know'.format(count_of_unknow))
    print('{} words without any status'.format(result - count_of_know - count_of_unknow))
    if print_all:
        result = session.query(WordsRank).all()
        for word in result:
            print('{} == rank == {}'.format(word.word, word.rank))


def set_status_for_words(numOfWords, fast_status):
    engine = create_engine('sqlite:///vocabDB_sqlite')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    result = session.query(WordsRank).filter(WordsRank.know_status == 0)
    if numOfWords != 0:
        result = result.limit(numOfWords)
    if not fast_status:
        for word in result:
            user_input = input('Do you know the word:   {}  ?'.format(word.word))
            while True:
                if user_input == 'y':
                    word.know_status = 1
                    break
                elif user_input == 'n':
                    word.know_status = 2
                    break
                else:
                    user_input = input('Enter y or n, please')
        if result is None:
            print('There is no words with unsetted status')
        else:
            session.commit()
    elif fast_status:
        ## need to take 10 words from query result, show them to user
        ## and ask which of them he knows. Then repeat this action
        numOfWordsInResult = result.count()
        firstPos = 0
        while numOfWordsInResult >= firstPos + 10:
            cur_list = result[firstPos:firstPos + 10]
            print("Which of these words do you know? ")
            k = 0
            for word in cur_list:
                print("{}. {}".format(k, word.word))
                k = k + 1
            user_input = input("y if you know all words, or indexses of words you don't know")
            while True:
                if user_input == 'y':
                    for word in cur_list:
                        word.know_status = 1
                    break
                elif user_input == 'break':
                    break
                else:
                    parsed_indexes = user_input.split(' ')
                    for cur_index in parsed_indexes:
                        if cur_index == '':
                            break
                        cur_i = int(cur_index)
                        cur_word = cur_list[cur_i]
                        cur_word.know_status = 2
                    # now we need to left words set status 1
                    for word in cur_list:
                        if word.know_status == 0:
                            word.know_status = 1
                    break
            firstPos += 10
        session.commit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='''Need an action command: load -
        loads file from text to sql''')
    parser.add_argument('--numOfLines', type=int, help='''Number of lines to
                            read from file''')
    parser.add_argument('--startFrom', type=int, help='''Number of lines to
                            read from file''')
    parser.add_argument('--printAll', type=int, help='''1 - print all words''')
    parser.add_argument('--fast', type=int, help='''1 - fast words status editing ''')

    args = parser.parse_args()
    fileName = '/Users/mak/Documents/python_scripts/vocab/rank_word_count'
    sqlConString = ''
    if args.numOfLines is None:
        numOfLines = 0
    else:
        numOfLines = args.numOfLines
    if args.startFrom is None:
        startFrom = 1
    else:
        startFrom = args.startFrom
    if args.printAll is None:
        printAll = False
    elif args.printAll == 1:
        printAll = True
    if args.fast is None:
        fast_status = False
    else:
        fast_status = True

    if args.action == 'load':
        load_words_from_text_to_sql(fileName, sqlConString, numOfLines, True, startFrom)
    elif args.action == 'show_stat':
        show_stat(printAll)
    elif args.action == 'set_status':
        set_status_for_words(numOfLines, fast_status)


if __name__ == "__main__":
    main()
