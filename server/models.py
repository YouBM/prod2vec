from sqlalchemy import Table, Column, DateTime, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, UUID
from database import Base


# >>> sentence.words.append(Word('wendy'))

sentence_word_association = Table('sentence_word_association', Base.metadata,
    Column('word_id', Integer, ForeignKey('word.id')),
    Column('sentence_id', Integer, ForeignKey('sentence.id'))
)

class Sentence(Base):
    __tablename__ = 'sentences'
    id = Column(Integer, primary_key=True)
    sentence = Column(TEXT, nullable=False) #solved directly
    language = Column(String, nullable=False)#solved directly
    order = Column(Integer, nullable=False)#solved directly
    translated = Column(Boolean, nullable=False)#solved directly
    text_id = Column(Integer, ForeignKey('text.id'), nullable=False)
    text = relationship("Text", back_populates="sentences")#solved via reference
    words = relationship( #solved via append
        "Word",
        secondary=sentence_word_association,
        back_populates="sentences")

    def __init__(self, sentence, language, order, translated, text):
        self.sentence = sentence
        self.language = language
        self.order = order
        self.translated = translated
        self.text = text

    def __repr__(self):
        return 'Sentence(%r, %r, %r, %r, %r)' % (
            self.sentence, self.language, self.order, self.translated, self.text
        )

class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    base_form = Column(String, nullable=False)#solved directly
    seen_forms = relationship("SeenWord", back_populates="word")#solved via SeenWord
    language = Column(String, nullable=False)#solved directly
    definitions = relationship("Definition", back_populates="word")#solved via Definition
    sentences = relationship( #solved via append
        "Sentence",
        secondary=sentence_word_association,
        back_populates="words")

    def __init__(self, base_form, language):
        self.base_form = base_form
        self.language = language

    def __repr__(self):
        return 'Word(%r, %r, %r, %r)' % (
            self.base_form, self.language, self.seen_forms, self.definitions
        )

class SeenWord(Base):
    __tablename__ = 'seen_words'
    id = Column(Integer, primary_key=True)
    seen_form = Column(String, nullable=False) #solved directly
    language = Column(String, nullable=False)  # solved directly
    word_id = Column(Integer, ForeignKey('word.id'),  nullable=False)
    word = relationship("Word", back_populates="seen_forms")#solved via reference

    def __init__(self, seen_form, language, word):
        self.seen_form = seen_form
        self.language = language
        self.word = word

    def __repr__(self):
        return 'SeenWord(%r, %r)' % (
            self.seen_form, self.word
        )

class Text(Base):
    __tablename__ = 'texts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    sentences = relationship("Sentence", back_populates="text") #solved via Sentence

    def __init__(self):
        self.title = ""

    def __repr__(self):
        return 'Text(text_id=%r)' % (
            self.id
        )

class Definition(Base):
    __tablename__ = 'definitions'
    id = Column(Integer, primary_key=True)
    shape = Column(String, nullable=False)#solved directly
    definition = Column(TEXT, nullable=False)#solved directly
    word_id = Column(Integer, ForeignKey('word.id'), nullable=False)
    word = relationship("Word", back_populates="definitions")#solved via reference

    def __init__(self, shape, definition, word):
        self.shape = shape
        self.definition = definition
        self.word = word

    def __repr__(self):
        return 'Definition(%r, %r, %r)' % (
            self.shape, self.definition, self.word
        )

