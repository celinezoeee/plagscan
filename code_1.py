from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def preprocess_text(text):
    # cuts spaces which are more than 1
    text = re.sub(r'\s{2,}', ' ', text)
    # cuts paragraphs which are more than 1
    text = re.sub(r'\n\s*\n', '\n', text)
    # cuts Matlab comments
    text = re.sub(r'%.*', '', text)  # line
    text = re.sub(r'(?s)%\{.*?%\}', '', text)  # block
    return text


def calculate_cosine_similarity(t1, t2):
    # transforms texts into vectors
    vectorizer = CountVectorizer().fit_transform([t1, t2])
    vectors = vectorizer.toarray()
    # calculates cosine similarity between vectors
    cosine_sim = cosine_similarity(vectors)
    return cosine_sim[0][1]


def levenshtein_distance(t1, t2):
    # swaps t1 and t2 if t1 is shorter
    if len(t1) < len(t2):
        return levenshtein_distance(t2, t1)

    # if t2 is empty, return the length of t1
    if len(t2) == 0:
        return len(t1)

    # init of first row of the matrix
    previous_row = range(len(t2) + 1)

    # iterate through each character in t1
    for i, c1 in enumerate(t1):
        # init current row with row number
        current_row = [i + 1]

        # iterate through each character in t2
        for j, c2 in enumerate(t2):
            # calculates cost of insertions, deletions, substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            # choose min cost + append to current row
            current_row.append(min(insertions, deletions, substitutions))

        # update previous row with current row
        previous_row = current_row

    # returns last elem of last row (levenshtein distance)
    return previous_row[-1]


def levenshtein_similarity(t1, t2):
    # calculates max length of the two texts
    max_length = max(len(t1), len(t2))
    # calculates levenshtein distance
    distance = levenshtein_distance(t1, t2)
    # calculates levenshtein similarity
    similarity = 1 - (distance / max_length)
    return similarity


def smith_waterman_similarity(t1, t2):
    # helper function to find max value in matrix
    def max_substring_length(matrix):
        return max(max(row) for row in matrix)

    # init matrix with zeros
    matrix = [[0] * (len(t2) + 1) for _ in range(len(t1) + 1)]

    # fill matrix using smith waterman algorithm
    for i in range(1, len(t1) + 1):
        for j in range(1, len(t2) + 1):
            if t1[i - 1] == t2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1], matrix[i - 1][j - 1])

    # calculate max substring length
    max_len = max_substring_length(matrix)
    # calculate smith-waterman similarity
    similarity = max_len / max(len(t1), len(t2))

    return similarity


def jaccard_similarity(t1, t2):
    #converts text to lowercase + split into sets of words
    set1 = set(t1.lower().split())
    set2 = set(t2.lower().split())

    # calculates intersection and union of the sets
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    # calculate jaccard similarity
    similarity = intersection / union if union > 0 else 0
    return similarity


def plagiarism_checker(t1, t2):
    # preprocess both texts
    pp_t1 = preprocess_text(t1)
    pp_t2 = preprocess_text(t2)

    # calculate similarity scores using the different algorithms
    cosine_sim = calculate_cosine_similarity(pp_t1, pp_t2)
    lev_sim = levenshtein_similarity(pp_t1, pp_t2)
    sm_wa_sim = smith_waterman_similarity(pp_t1, pp_t2)
    jac_sim = jaccard_similarity(pp_t1, pp_t2)

    # round similarity scores to two decimals
    cosine_sim = round(cosine_sim * 100, 2)
    lev_sim = round(lev_sim * 100, 2)
    sm_wa_sim = round(sm_wa_sim * 100, 2)
    jac_sim = round(jac_sim * 100, 2)

    # calculates average similarity score
    result = (cosine_sim + lev_sim + sm_wa_sim + jac_sim) / 4
    result = round(result, 2)
    return cosine_sim, lev_sim, sm_wa_sim, jac_sim, result

def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()

    return text

