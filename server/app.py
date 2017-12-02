#!flask/bin/python
import json
from flask import Flask, request
from models import Definition, Word, SeenWord, Sentence, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import spacy

Session = sessionmaker()
engine = create_engine('postgresql://...')
Session.configure(bind=engine)
session = Session()
# conn = engine.connect()
# session = Session(bind=conn)


nlpen = spacy.load('en')
nlpde = spacy.load('de')

app = Flask(__name__)


@app.route('/words', methods=['POST'])
def get_words():
    pl = json.loads(request.data)
    words = session.query(Word)
    return json.dumps(words, indent=4)


@app.route('/definitions/create', methods=['POST'])
def new_definitions():
    pl = json.loads(request.data)
    word = session.query(Word).filter_by(base_form=pl['base_form'], language=pl['language']).first()
    definitions = pl['definitions']
    for d in definitions:
        definition = session.query(Definition).filter_by(shape=d['shape'], definition=d['definition']).first()
        if not definition:
            definition = Definition(d['shape'], d['definition'], word)
            session.add(definition)
    session.commit()
    output = {'Message': 'Definitions saved in database'}
    return json.dumps(output)


@app.route('/sentences/create', methods=['POST'])
def new():
    text = Text()
    session.add(text)
    payload = json.loads(request.data)
    for pl in payload:
        sentence = Sentence(pl['sentence'], pl['language'], pl['order'], pl['translated'], text)
        words = pl['words']
        for w in words:
            word = session.query(Word).filter_by(base_form=w['base_form'], language=w['language']).first()
            if not word:
                word = Word(w['base_form'], w['language'])
            sentence.words.append(word)
            seen_word = session.query(SeenWord).filter_by(seen_form=w['seen_form'], language=w['language']).first()
            if not seen_word:
                seen_word = SeenWord(w['seen_form'], w['language'], word)
                session.add(seen_word)
        session.add(sentence)
    session.commit()
    output = {'Message': 'Sentences saved in database'}
    return json.dumps(output)


@app.route('/spacy',methods=['POST'])
def index():
    analysis = []
    payload = json.loads(request.data)
    if payload['lan'] == 'en':
        doc = nlpen(payload['sent'])
    elif payload['lan'] == 'de':
        doc = nlpde(payload['sent'])
    # string.decode("UTF8"))
    for word in doc:
        analysis.append([word.text, word.lemma_, word.pos_])
    return json.dumps(analysis, indent=4)
    # request.json
    # request.get_json()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug=True)
    # init_db()
