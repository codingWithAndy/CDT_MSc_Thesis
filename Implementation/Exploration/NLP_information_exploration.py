import spacy
import pandas as pd
from itertools import combinations as combs
from spacy.matcher import Matcher
from spacy import displacy

import nltk

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Dropout, SpatialDropout1D
from tensorflow.keras.layers import LSTM
from tensorflow.keras.models import load_model

from collections import Counter
import text_normalizer as tn
import model_evaluation_utils as meu

from keras.preprocessing import sequence
from sklearn.preprocessing import LabelEncoder

# %% [markdown]
# ## Data Pipeline

# %%
nlp = spacy.load('en_core_web_sm')

doc1  = nlp(u'An Englishman, a Scotsman and an Irishman walk into a bar. The Englishman wanted to go so they all had to leave. #Brexitjokes')
doc2  = nlp(u'Why do we need any colour passport? We should just be able to shout, “British! Less of your nonsense!” and stroll straight through.')
doc3  = nlp(u'Q: With Britain leaving the EU how much space was created? A: Exactly 1GB')
doc4  = nlp(u'VOTERS: we want to give a boat a ridiculous name UK: no VOTERS: we want to break up the EU and trash the world economy UK: fine')
doc5  = nlp(u'#BrexitJokes How did the Brexit chicken cross the road? \"I never said there was a road. Or a chicken\".')
doc6  = nlp(u'After #brexit, when rapper 50 cent performs in GBR he\'ll appear as 10.00 pounds. #brexitjokes')
doc7  = nlp(u'I long for the simpler days when #Brexit was just a term for leaving brunch early.')
doc8  = nlp(u'Say goodbye to croissants, people. Delicious croissants. We\'re stuck with crumpets FOREVER.')
doc9  = nlp(u'Hello, I am from Britain, you know, the one that got tricked by a bus')
doc10 = nlp(u'How many Brexiteers does it take to change a light bulb? None, they are all walked out because they didn’t like the way the electrician did it.')

docs = [
    doc1,
    doc2,
    doc3,
    doc4,
    doc5,
    doc6,
    doc7,
    doc8,
    doc9,
    doc10]


# %%
#Creating DF for LSTM
tweets = np.array([
    ["An Englishman, a Scotsman and an Irishman walk into a bar. The Englishman wanted to go so they all had to leave. #Brexitjokes"],
    ["Why do we need any colour passport? We should just be able to shout, “British! Less of your nonsense!” and stroll straight through."],
    ["Q: With Britain leaving the EU how much space was created? A: Exactly 1GB"],
    ["VOTERS: we want to give a boat a ridiculous name UK: no VOTERS: we want to break up the EU and trash the world economy UK: fine"],
    ["#BrexitJokes How did the Brexit chicken cross the road? \"I never said there was a road. Or a chicken\"."],
    ["After #brexit, when rapper 50 cent performs in GBR he'll appear as 10.00 pounds. #brexitjokes"],
    ["I long for the simpler days when #Brexit was just a term for leaving brunch early."],
    ["Say goodbye to croissants, people. Delicious croissants. We're stuck with crumpets FOREVER."],
    ["Hello, I am from Britain, you know, the one that got tricked by a bus"],
    ["How many Brexiteers does it take to change a light bulb? None, they are all walked out because they didn’t like the way the electrician did it."]])

tweet_df = pd.DataFrame(tweets, columns=['tweet_content'])
tweet_df.head()

# Removing Stop words
stop_words = nltk.corpus.stopwords.words('english')
stop_words.remove('no')
stop_words.remove('but')
stop_words.remove('not')

# %% [markdown]
# ___
# %% [markdown]
# ## Part of Speach Tagging

# %%
tweet_no = 1
for doc in docs:
    print(f'Tweet: {tweet_no}')
    for token in doc:
        print(f'{token.text:{10}} - {token.pos_:{10}} - {token.tag_:{10}} - {spacy.explain(token.tag_)}')
    tweet_no += 1
    


# %%
# POS Counts
tweet_no = 1
for doc in docs:
    print(f'Tweet: {tweet_no}')
    POS_counts = doc.count_by(spacy.attrs.POS)
    for k,v in sorted(POS_counts.items()):
        print(f'{k}: {doc.vocab[k].text:{5}} {v}')
    
    print('\n')
    tweet_no += 1


# %%
# Visualising POS
options = {
    'distance':95,
    'compact':'True'
}

for doc in docs:
    spans = list(doc.sents)
    displacy.render(spans,style='dep',jupyter=True, options = options)

# %% [markdown]
# ___
# %% [markdown]
# ## Named Entity Recognition

# %%
def show_ents(doc):
    no_ents = 0
    if doc.ents:
        for ent in doc.ents:
            print(f'{ent.text} - {ent.label_} - {spacy.explain(ent.label_)}')
            no_ents += 1
        print(f'Total number of entities: {no_ents}')
    else:
        print('No entites found')


# %%
tweet_no = 1
for doc in docs:
    print(f'Tweet: {tweet_no}')
    show_ents(doc)
    print('\n')
    tweet_no += 1


# %%
tweet_no = 1
for doc in docs:
    print(f'Tweet: {tweet_no}')
    displacy.render(doc, style="ent")
    tweet_no += 1

# %% [markdown]
# ___
# %% [markdown]
# ## Feature Extraction

# %%
tweet_df.isnull().sum() #delete at a later date


# %%
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer


# %%
tfidf = TfidfVectorizer(min_df=2, max_df=0.5, ngram_range=(1,2))


# %%
doc1  = ('An Englishman, a Scotsman and an Irishman walk into a bar. The Englishman wanted to go so they all had to leave. #Brexitjokes')
doc2  = ('Why do we need any colour passport? We should just be able to shout, “British! Less of your nonsense!” and stroll straight through.')
doc3  = ('Q: With Britain leaving the EU how much space was created? A: Exactly 1GB')
doc4  = ('VOTERS: we want to give a boat a ridiculous name UK: no VOTERS: we want to break up the EU and trash the world economy UK: fine')
doc5  = ('#BrexitJokes How did the Brexit chicken cross the road? \"I never said there was a road. Or a chicken\".')
doc6  = ('After #brexit, when rapper 50 cent performs in GBR he\'ll appear as 10.00 pounds. #brexitjokes')
doc7  = ('I long for the simpler days when #Brexit was just a term for leaving brunch early.')
doc8  = ('Say goodbye to croissants, people. Delicious croissants. We\'re stuck with crumpets FOREVER.')
doc9  = ('Hello, I am from Britain, you know, the one that got tricked by a bus')
doc10 = ('How many Brexiteers does it take to change a light bulb? None, they are all walked out because they didn’t like the way the electrician did it.')

fe_docs = [
    doc1,
    doc2,
    doc3,
    doc4,
    doc5,
    doc6,
    doc7,
    doc8,
    doc9,
    doc10]


# %%
features = tfidf.fit_transform(fe_docs)


# %%
fe_df = pd.DataFrame(features.todense(),columns=tfidf.get_feature_names())


# %%
fe_df

# %% [markdown]
# ___
# %% [markdown]
# ## Sentiment Analysis

# %%
# Load pre-trained model
model = load_model('LSTM_model.h5')


# %%
norm_tweets = tn.normalize_corpus(tweet_df['tweet_content'], stopwords=stop_words)
tokenized_tweets  = [tn.tokenizer.tokenize(text) for text in norm_tweets]

# build word to index vocabulary
token_counter = Counter([token for review in tokenized_tweets for token in review])
vocab_map     = {item[0]: index+1 for index, item in enumerate(dict(token_counter).items())}
max_index     = np.max(list(vocab_map.values()))

vocab_map['PAD_INDEX']       = 0
vocab_map['NOT_FOUND_INDEX'] = max_index+1

vocab_size    = len(vocab_map)

# view vocabulary size and part of the vocabulary map
print('Vocabulary Size:', vocab_size)
print('Sample slice of vocabulary map:', dict(list(vocab_map.items())))

#get max length of train corpus and initialize label encoder
le          = LabelEncoder()
num_classes = 2 # positive -> 1, negative -> 0
max_len     = np.max([len(review) for review in tokenized_tweets])


## Test reviews data corpus
# Convert tokenized text reviews to numeric vectors
tweet_ready = [[vocab_map[token] for token in tokenized_review] for tokenized_review in tokenized_tweets]
tweet_ready = sequence.pad_sequences(tweet_ready, maxlen=max_len) # pad 


# view vector shapes
print('Max length of tweet review vectors:', max_len)
print('Tweet vectors shape:', tweet_ready.shape)


# %%
my_pred_test = model.predict(tweet_ready)


# %%
pred_score = [1 if p > 0.5 else 0 for p in my_pred_test]
pred_sent = ['Positive' if p > 0.5 else 'Negative' for p in my_pred_test]


# %%
for i in range(len(pred_score)):
    print(f'Tweet {i+1}:\nActual Score: {my_pred_test[i]} - Score: {pred_score[i]} - Sentiment: {pred_sent[i]}')

# %% [markdown]
# ___
# %% [markdown]
# ## Tweet Similarity Scoring
# %% [markdown]
# ### Document Similarity

# %%
tweet_id = [i for i in range(1,11)]
id_combs = list(combs(tweet_id, 2))


# %%
doc_df = pd.DataFrame()

for each_pair in id_combs:
    doc_similarity = docs[each_pair[0]-1].similarity(docs[each_pair[1]-1])
    doc_results = {
        'tweet1': int(each_pair[0]),
        'tweet2': int(each_pair[1]),
        'similarity': doc_similarity,
        'text 1': docs[each_pair[0]-1],
        'text 2': docs[each_pair[1]-1]
    }
    
    doc_df = doc_df.append(doc_results, ignore_index=True)


# %%
doc_df['tweet1'] = doc_df['tweet1'].astype(int)
doc_df['tweet2'] = doc_df['tweet2'].astype(int)
doc_df.head()


# %%
doc_df_ordered = doc_df.sort_values(by=['similarity'], ascending=False)
doc_df_ordered.head(10)


# %%
doc_df_ordered.tail(10)

# %% [markdown]
# ### Term Similarity

# %%
spans = {}


# %%
for j,doc in enumerate(docs):
    named_entity_span = [doc[i].text for i in range(len(doc)) if doc[i].ent_type != 0]
    print(named_entity_span)
    named_entity_span = ' '.join(named_entity_span)
    named_entity_span = nlp(named_entity_span)
    spans.update({j:named_entity_span})


# %%
df = pd.DataFrame()

for each_pair in id_combs:
    similarity = spans[each_pair[0]-1].similarity(spans[each_pair[1]-1])
    #print(f'doc{each_pair[0]} is similar to doc{each_pair[1]} by: {similarity}') #Un-comment if you want to see individual scores printed.
    results = {
        'tweet1': int(each_pair[0]),
        'tweet2': int(each_pair[1]),
        'similarity': similarity,
        'tweet1 NE Span': spans[each_pair[0]-1],
        'tweet2 NE Span': spans[each_pair[1]-1]
    }
    
    df = df.append(results, ignore_index=True)


# %%
# Chaning Data Types
df['tweet1'] = df['tweet1'].astype(int)
df['tweet2'] = df['tweet2'].astype(int)


# %%
# Saving to/loading from CSV
#df = pd.read_csv('similarity_scores_v2.csv') #Uncomment to load.
#df.to_csv('similarity_scores_v2.csv') #Uncomment to resave.


# %%
df_ordered = df.sort_values(by=['similarity'], ascending=False)


# %%
# Display the Top 10 Simialr Combinations 
df_ordered.head(10)


# %%
# Display the Bottom 10 Simialr Combinations 
df_ordered.tail(10)

# %% [markdown]
# ___
# %% [markdown]
# ## Utterence Pattern Matching

# %%
def dep_pattern(doc):
    for i in range(len(doc)-1):
        if doc[i].dep_ == 'nsubj' and doc[i+1].dep_ == 'aux' and doc[i+2].dep_ == 'ROOT':
            for tok in doc[i+2].children:
                if tok.dep_ == 'dobj':
                    return True
    else:
        return False


# %%
for i in docs:
    if dep_pattern(i):
        print(f'Found in: {i}')
    else:
        print('Not Found')

# %% [markdown]
# ___
# %% [markdown]
# ## Finding Word Sequence Patterns

# %%
matcher = Matcher(nlp.vocab)
pattern = [{
    'DEP':"nsubj"}, 
    {"DEP":"aux"}, 
    {"DEP":"ROOT"}
    ]

matcher.add("NsubjAuxRoot", [pattern])

tweet_no = 1

for doc in docs:
    matches = matcher(doc)
    print(f'Tweet: {tweet_no}')
    for match_id, start, end in matches:
        span = doc[start:end]
        print(f"Span: {span.text}")
        print(f"The position in the doc are: {start} - {end}\n")
    else:
        print("None found.\n")
    tweet_no += 1

# %% [markdown]
# ___
# %% [markdown]
# ## Key Phrases

# %%
def keyphrase(doc):
    for t in doc:
        if t.dep_ == 'probj' and (t.pos_ == 'NOUN' or t.pos_ == "PROPN"):
            return (' '.join([child.text for child in t.lefts]) + ' ' + t.text).lstrip()
    for t in reversed(doc):
        if t.dep_ == 'nsubj' and (t.pos_ == 'NOUN' or t.pos_ == 'PROPN'):
            return t.text + ' ' + t.head.text
    for t in reversed(doc):
        if t.dep_ == 'dobj' and (t.pos_ == 'NOUN' or t.pos_ == 'PROPN'):
            return t.head.text + ' ' + 'ing' + ' ' + t.text
    return False


# %%
tweet_no = 1
for doc in docs:
    print(keyphrase(doc))
    tweet_no += 1

# %% [markdown]
# ___

