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

class WordStatus(Base):
    __tablename__ = 'word_status'
    word_rank = Column(Integer, primary_key=True)
    word = Column(String)
    status = Column(Integer)

def load_words_from_text_to_sql(filename='', sqlConString='',
                                numOfLines=0, printDebugMsg=False):
    """

    :type fileName: str
    """
    fileWithWords = open(filename, 'r', encoding='utf-8')
    listOfWords = fileWithWords.readlines()
    lineIndex = 0
    engine = create_engine('sqlite:///vocabDB_sqlite')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    for line in listOfWords:
        lineIndex += 1
        if lineIndex == 1:
            continue
        splittedLine = line.split('\t')
        wordRank = int(splittedLine[0])
        wordText = splittedLine[1].lower()
        result = session.query(WordsRank).filter(WordsRank.rank == wordRank).all()
        if len(result) == 0:
            new_word = WordsRank(rank=wordRank, word=wordText)
            session.add(new_word)
            if printDebugMsg:
                print('The word {} has rank {} and added into the DB'.format(wordText, wordRank))
        else:
            if printDebugMsg:
                print('The word {} is already in the DB'.format(wordText))

        if lineIndex == numOfLines:
            break
    session.commit()

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
