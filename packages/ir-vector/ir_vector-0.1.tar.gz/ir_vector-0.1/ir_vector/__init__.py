#initiator
#vector space cosine similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import nltk
from nltk.corpus import stopwords
import numpy as np
from numpy.linalg import norm

# Training and testing datasets
train_set = [
    "Document about python programming language and data programming techniques.",
    "Document discussing machine learning algorithms and applications.",
    "Overview of natural language processing and its analysis."
]

# Query for Cosine Similarity
query = "python programming"

# Download stopwords and set them
nltk.download('stopwords')
stopWords = stopwords.words('english')

# Create CountVectorizer and TfidfTransformer
vectorizer = CountVectorizer(stop_words=stopWords)
transformer = TfidfTransformer()

# Fit and transform the training set to get term frequency matrix
doc_term_matrix = vectorizer.fit_transform(train_set)

# TF-IDF Transformation
tfidf_matrix = transformer.fit_transform(doc_term_matrix)

# Transform Query Using the Same Vectorizer (for Consistent Feature Space)
query_vector = vectorizer.transform([query])
query_tfidf = transformer.transform(query_vector)

# Cosine Similarity Function
def cosine_similarity(a, b):
    """Calculate the cosine similarity between two vectors"""
    return np.inner(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Output all the results
print("\n--------------- Fit Vectorizer to Train Set ---------------")
print(doc_term_matrix.toarray())
print("----------------------------------------------------------")

print("\n--------------- Transformer Vectorizer to Test Set ---------------")
print(query_vector.toarray())
print("----------------------------------------------------------")

print("\n--------------- TF-IDF Transformation of Train Set ---------------")
print(tfidf_matrix.toarray())
print("----------------------------------------------------------")

print("\n--------------- TF-IDF Transformation of the Query ---------------")
print(query_tfidf.toarray())
print("----------------------------------------------------------")

# Compute Cosine Similarity between Query and Documents
print("\n--------------- Cosine Similarity Results ---------------")
for i, doc_vector in enumerate(tfidf_matrix.toarray()):
    similarity = cosine_similarity(query_tfidf.toarray(), doc_vector)
    print(f"Cosine similarity between query and Document {i+1}: {similarity}")
    print("------------------------------------")  # separator for clarity
