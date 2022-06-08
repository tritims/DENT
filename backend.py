from crypt import methods
from flask import Flask, request
import pickle
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
with open('centroid.pickle', 'rb') as handle:
    centroids = pickle.load(handle)

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('flax-sentence-embeddings/stackoverflow_mpnet-base')

from keybert import KeyBERT
kw_model = KeyBERT(model='flax-sentence-embeddings/stackoverflow_mpnet-base')

def getKeywords(text):
    kws = kw_model.extract_keywords(text, 
                      keyphrase_ngram_range=(2,3), 
                      stop_words='english', 
                      use_mmr=True, diversity=0.7)
    temp = ''
    for w, j in kws:
        if(j>0.5): # custom threashold
            temp = temp + ' ' + w
    return temp

def getPattern(text):
    pattern = ''
    max_score = 0
    for centroid in centroids:
        t = cosine_similarity([centroids[centroid]], [model.encode(text)])
        if t> max_score:
            max_score = t
            pattern = centroid
    return pattern

@app.route('/', methods=['POST'])
def index():
    return '200'

app.run(host='0.0.0.0', port=80)