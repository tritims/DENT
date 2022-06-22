from crypt import methods
from flask import Flask, request, jsonify
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import cleanpost as cp
from flask_cors import CORS, cross_origin
import numpy as np

app = Flask(__name__)
CORS(app)
MODE = 'DEV'

if MODE != 'DEV':
    with open('centroid.pickle', 'rb') as handle:
        centroids = pickle.load(handle)

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('flax-sentence-embeddings/stackoverflow_mpnet-base')

    from keybert import KeyBERT
    kw_model = KeyBERT(model='flax-sentence-embeddings/stackoverflow_mpnet-base')

def getKeywords(text):
    if MODE != 'DEV':
        kws = kw_model.extract_keywords(text, 
                        keyphrase_ngram_range=(2,3), 
                        stop_words='english', 
                        use_mmr=True, diversity=0.7)
        temp = ''
        for w, j in kws:
            if(j>0.5): # custom threashold
                temp = temp + ' ' + w
        return temp
    else:
        return ''

def getPattern(text):
    if MODE != 'DEV':
        pattern = ''
        max_score = 0
        for centroid in centroids:
            t = cosine_similarity([centroids[centroid]], [model.encode(text)])
            if t> max_score:
                max_score = t
                pattern = centroid
        return pattern, max_score
    else:
        return 'tensor operations', np.array([0.56])

# text -> clean -> title + body -> keywords of title & body -> get pattern
@app.route('/', methods=['POST'])
def index():
    # print("inside post...")
    request_data = request.get_json()
    # print(request_data)
    title = request_data['title']
    body = cp.clean_body(request_data['body']) # body in HTML format
    title_kws = getKeywords(title)
    body_kws = getKeywords(body)
    pattern, score = getPattern(title_kws + ' ' + body_kws)
    return jsonify({
        "score": score.item(),
        "pattern": pattern
    })
    

app.run(host='0.0.0.0', port=3000)

# next steps -> write a frontend -> check tags -> extract title + body -> make JSON and REST call -> log the output

# Scraping JSON.stringify(document.getElementsByClassName('s-prose js-post-body')[0].innerHTML).replace(/\s\s+/g, ' ') 
