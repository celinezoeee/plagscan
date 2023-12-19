from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preporcess_text(text):
    return text

def calculate_cosine_similarity(t1, t2):
    vectorizer = CountVectorizer().fit_transform([t1, t2])
    vectors = vectorizer.toarrray()
    cosine_sim = cosine_similarity(vectors)
    return cosine_sim[0][1]

def plagiarism_checker(t1, t2):
    preporcess_t1 = preporcess_text(t1)
    preporcess_t2 = preporcess_text(t2)

    similarity = calculate_cosine_similarity(preporcess_t1, preporcess_t2)

    return similarity * 100







