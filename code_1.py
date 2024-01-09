from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text):
    return text


def calculate_cosine_similarity(t1, t2):
    vectorizer = CountVectorizer().fit_transform([t1, t2])
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)
    return cosine_sim[0][1]


def levenshtein_distance(t1, t2):
    if len(t1) < len(t2):
        return levenshtein_distance(t2, t1)

    if len(t2) == 0:
        return len(t1)

    previous_row = range(len(t2) + 1)

    for i, c1 in enumerate(t1):
        current_row = [i + 1]

        for j, c2 in enumerate(t2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]


def levenshtein_similarity(t1, t2):
    max_length = max(len(t1), len(t2))
    distance = levenshtein_distance(t1, t2)
    similarity = 1 - (distance / max_length)
    return similarity


def smith_waterman_similarity(t1, t2):
    def max_substring_length(matrix):
        return max(max(row) for row in matrix)

    def backtrack(matrix, t1, t2, i, j):
        alignment1, alignment2 = '', ''

        while i > 0 and j > 0:
            if matrix[i][j] == matrix[i - 1][j - 1] + 1:
                alignment1 = t1[i - 1] + alignment1
                alignment2 = t2[j - 1] + alignment2
                i -= 1
                j -= 1
            elif matrix[i][j] == matrix[i - 1][j]:
                i -= 1
            else:
                j -= 1

        return alignment1, alignment2

    matrix = [[0] * (len(t2) + 1) for _ in range(len(t1) + 1)]

    for i in range(1, len(t1) + 1):
        for j in range(1, len(t2) + 1):
            if t1[i - 1] == t2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1], matrix[i - 1][j - 1])

    max_len = max_substring_length(matrix)
    similarity = max_len / max(len(t1), len(t2))

    return similarity


def jaccard_similarity(t1, t2):
    set1 = set(t1.lower().split())
    set2 = set(t2.lower().split())

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    similarity = intersection / union if union > 0 else 0
    return similarity


def plagiarism_checker(t1, t2):
    pp_t1 = preprocess_text(t1)
    pp_t2 = preprocess_text(t2)

    cosine_sim = calculate_cosine_similarity(pp_t1, pp_t2)
    lev_sim = levenshtein_similarity(pp_t1, pp_t2)
    sm_wa_sim = smith_waterman_similarity(pp_t1, pp_t2)
    jac_sim = jaccard_similarity(pp_t1, pp_t2)

    cosine_sim = round(cosine_sim * 100, 2)
    lev_sim = round(lev_sim * 100, 2)
    sm_wa_sim = round(sm_wa_sim * 100, 2)
    jac_sim = round(jac_sim * 100, 2)

    result = (cosine_sim + lev_sim + sm_wa_sim + jac_sim) / 4
    result = round(result * 100, 2)
    return cosine_sim, lev_sim, sm_wa_sim, jac_sim, result

def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()

    return text


# path1 = 'C:\Python\Plagiatscanner\plagscan\matlabtest1.m'
# path2 = 'C:\Python\Plagiatscanner\plagscan\matlabtest2.m'

# text1 = read_file(path1)
# text2 = read_file(path2)

# result = plagiarism_checker(text1, text2)
# print(f"Ähnlichkeit: {result}%")
#kommentar





